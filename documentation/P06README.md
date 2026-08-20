# Participant 6 — AWS Cloud Infrastructure, Containerization & DevOps Deployment

Investment Portfolio Risk & Analytics Platform (IPRA)

Owns: Terraform infrastructure, Docker images, ECS/ALB deployment, CI/CD, monitoring, rollback.
Does **not** own: React app code, API business logic, Snowflake data model (those come from
Participants 3/4/5 — see "Handoff" below).

## Repository Structure

```
participant-06-devops/
├── terraform/
│   ├── environments/dev/     # root module: wires all modules together for dev
│   └── modules/
│       ├── vpc/               # VPC, subnets, routing, NAT
│       ├── security-groups/   # ALB / frontend / API security groups
│       ├── iam/                # ECS execution+task roles, GitHub OIDC role
│       ├── ecr/                 # container image repositories
│       ├── ecs/                 # cluster, task definitions, services
│       ├── alb/                 # load balancer, target groups, listeners
│       ├── cloudwatch/         # log groups, alarms, dashboard
│       └── secrets/             # Secrets Manager containers (values set out-of-band)
├── docker/
│   ├── frontend/Dockerfile     # multi-stage React build → nginx
│   └── api/Dockerfile           # FastAPI + uvicorn
├── .github/workflows/
│   ├── ci.yml                    # PR checks: lint/test/build, terraform validate
│   └── deploy.yml                # build, push to ECR, deploy to ECS, smoke test
├── monitoring/                   # dashboard + alarm documentation
├── docs/                          # architecture, networking, security, rollback, operations
└── README.md
```

## Prerequisites

- AWS account with permissions to create VPC/IAM/ECS/ALB/ECR/CloudWatch/Secrets Manager resources
- Terraform >= 1.5
- AWS CLI v2, configured (`aws configure` or SSO)
- Docker
- The Participant 5 React app source (`frontend/react-app`) and Participant 4 API source (`api`)
  checked out as sibling folders to this one, per the doc's monorepo layout:

```
investment-portfolio-risk-analytics/
├── frontend/react-app/        # Participant 5
├── api/                        # Participant 4
└── participant-06-devops/     # this repo section
```

---

## Step-by-Step Guide

### 1. Clone and set up variables

```bash
git clone <your-repo-url>
cd investment-portfolio-risk-analytics/participant-06-devops/terraform/environments/dev

cp terraform.tfvars.example terraform.tfvars
# edit terraform.tfvars: region, github_org/github_repo, certificate_arn if you have one
```

### 2. Initialize and provision the AWS infrastructure

```bash
terraform init
terraform fmt -check -recursive ..
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
```

This creates the VPC, subnets, security groups, IAM roles, ECR repositories, ALB, ECS
cluster/services (running on harmless placeholder images), Secrets Manager containers, and
CloudWatch log groups/alarms/dashboard.

Capture the outputs you'll need next:

```bash
terraform output
# alb_dns_name, frontend_ecr_repository_url, api_ecr_repository_url, ecs_cluster_name, ...
```

### 3. Set real secret values (never in Terraform/Git)

```bash
aws secretsmanager put-secret-value \
  --secret-id ipra-dev/snowflake-credentials \
  --secret-string '{"user":"<snowflake_user>","password":"<snowflake_password>"}'

aws secretsmanager put-secret-value \
  --secret-id ipra-dev/api-auth-secret \
  --secret-string '{"value":"<random-strong-secret>"}'
```

### 4. Build and push the container images (first deploy, manual)

```bash
cd ../../../..   # back to investment-portfolio-risk-analytics/

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1
aws ecr get-login-password --region $REGION | \
  docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# Frontend
docker build -t $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ipra-dev-frontend:v1 \
  -f participant-06-devops/docker/frontend/Dockerfile frontend/react-app
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ipra-dev-frontend:v1

# API
docker build -t $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ipra-dev-api:v1 \
  -f participant-06-devops/docker/api/Dockerfile api
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ipra-dev-api:v1
```

### 5. Point ECS at the real images

```bash
aws ecs describe-task-definition --task-definition ipra-dev-frontend --query taskDefinition > fe.json
jq --arg IMAGE "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ipra-dev-frontend:v1" \
  '.containerDefinitions[0].image=$IMAGE | del(.taskDefinitionArn,.revision,.status,.requiresAttributes,.compatibilities,.registeredAt,.registeredBy)' \
  fe.json > fe-new.json
aws ecs register-task-definition --cli-input-json file://fe-new.json
aws ecs update-service --cluster ipra-dev-cluster --service ipra-dev-frontend \
  --task-definition ipra-dev-frontend --force-new-deployment

# repeat for ipra-dev-api with the api image
```

### 6. Wait for the services and verify

```bash
aws ecs wait services-stable --cluster ipra-dev-cluster --services ipra-dev-frontend
aws ecs wait services-stable --cluster ipra-dev-cluster --services ipra-dev-api

ALB_DNS=$(terraform -chdir=participant-06-devops/terraform/environments/dev output -raw alb_dns_name)
curl -f http://$ALB_DNS/
curl -f http://$ALB_DNS/api/v1/health
```

### 7. Set up CI/CD (GitHub Actions) for subsequent deploys

1. In `terraform.tfvars`, set `enable_github_oidc = true`, `github_org`, `github_repo`, then
   `terraform apply` again to create the OIDC provider + deploy role.
2. `terraform output` → note the deploy role ARN (add an output if not already present, or read
   it from the IAM console: `ipra-dev-github-actions-deploy`).
3. In the GitHub repo → Settings → Secrets and variables → Actions, add:
   - `AWS_DEPLOY_ROLE_ARN` = the role ARN from step 2
4. From then on, every push to `main` runs `.github/workflows/deploy.yml`: it tests, builds
   images tagged with the Git SHA, pushes to ECR, updates both ECS services, waits for
   stability, and runs a smoke test automatically.

### 8. Monitoring

```bash
# View the dashboard
open "https://console.aws.amazon.com/cloudwatch/home?region=$REGION#dashboards:name=ipra-dev-dashboard"

# Tail API logs
aws logs tail /ecs/ipra-dev-api --follow

# Tail frontend logs
aws logs tail /ecs/ipra-dev-frontend --follow
```

### 9. Rollback (if a deploy goes bad)

See `docs/rollback.md` — redeploy the previous Git-SHA-tagged image without rebuilding.

### 10. Tear down (training account cost control)

```bash
cd participant-06-devops/terraform/environments/dev
terraform destroy
```

---

## Handoff Received

- **Participant 5 (React)**: source repo, build command (`npm run build`), required
  `VITE_API_BASE_URL`, container port `80`.
- **Participant 4 (API)**: API base path `/api/v1`, container port `8000`, health endpoint
  `/api/v1/health`, readiness `/api/v1/health/ready`, required Snowflake env vars.

## Evidence Produced (see `docs/` and `monitoring/`)

AWS architecture diagram (`docs/architecture.md`), Terraform plan/apply output, VPC/SG evidence,
ECR repositories, ECS cluster/services, ALB + healthy targets, CloudWatch logs/dashboard/alarms,
GitHub Actions CI/CD runs, smoke test results, rollback test, deployment/operations runbooks.
