# Remaining Tasks for IPRA Deployment

This checklist is based on the Participant 6 deployment flow and the current state of this repository. It tracks the work that still needs to be completed after the Terraform infrastructure was already created successfully.

## Current Status

Completed:
- Terraform VPC, security groups, ECR repositories, ALB, ECS cluster, CloudWatch, and related infrastructure were created successfully.
- The AWS lab resources are available in the dev environment.
- The repository already contains the required Dockerfiles and deployment documentation.

Pending:
- Push actual application images to AWS ECR.
- Update ECS task definitions to use the ECR image URIs.
- Set secret values in AWS Secrets Manager.
- Validate the services become healthy.
- Confirm app runs correctly behind the ALB.
- Optional: set up CI/CD automation.

---

## Task 1: Confirm the ECR repositories exist

Check the output from Terraform:

```bash
terraform output
```

You should see repo URLs similar to:
- `ipra-dev-frontend`
- `ipra-dev-api`

If needed, verify with AWS CLI:

```bash
aws ecr describe-repositories --region us-east-1 --output table
```

---

## Task 2: Authenticate Docker to AWS ECR

Important: Docker Hub credentials and AWS credentials are different. AWS ECR login must be done using AWS credentials.

Run:

```powershell
$REGION = "us-east-1"
$ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"
```

If Docker still shows DNS/network issues, fix Docker Desktop networking first and retry the command.

---

## Task 3: Tag and push your Docker images to ECR

### Frontend

```powershell
cd "C:\Users\Administrator\Desktop\IPRAP-Practice"

$REGION = "us-east-1"
$ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)

docker build `
  -t "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ipra-dev-frontend:v1" `
  -f ".\frontend\Dockerfile" `
  ".\frontend"

docker push "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ipra-dev-frontend:v1"
```

### API

```powershell
cd "C:\Users\Administrator\Desktop\IPRAP-Practice"

$REGION = "us-east-1"
$ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)

docker build `
  -t "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ipra-dev-api:v1" `
  -f ".\docker\api\Dockerfile" `
  ".\api"

docker push "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ipra-dev-api:v1"
```

---

## Task 4: Set secret values in AWS Secrets Manager

This must be done before the API service works correctly if the app uses secret-backed variables.

```bash
aws secretsmanager put-secret-value \
  --secret-id ipra-dev/snowflake-credentials \
  --secret-string '{"user":"<snowflake_user>","password":"<snowflake_password>"}'

aws secretsmanager put-secret-value \
  --secret-id ipra-dev/api-auth-secret \
  --secret-string '{"value":"<random-strong-secret>"}'
```

The actual secret names are defined by the Terraform modules and the outputs from the previous apply.

---

## Task 5: Point ECS to the real ECR images

The current Terraform configuration uses placeholder images. Update the dev config so ECS uses the newly pushed ECR image tags.

Update these values in the dev Terraform variables or pass them with `-var`:

```hcl
frontend_image_placeholder = "659775407375.dkr.ecr.us-east-1.amazonaws.com/ipra-dev-frontend:v1"
api_image_placeholder      = "659775407375.dkr.ecr.us-east-1.amazonaws.com/ipra-dev-api:v1"
```

Then run:

```bash
terraform apply
```

This tells ECS to use the real Docker image versions in ECR.

---

## Task 6: Wait for ECS services to become healthy

Check the ECS services:

```bash
aws ecs describe-services --cluster ipra-dev-cluster --services ipra-dev-frontend ipra-dev-api --region us-east-1
```

Wait until the services are active and healthy.

---

## Task 7: Validate the application over the ALB

Get the ALB DNS name:

```bash
terraform output alb_dns_name
```

Then test the app from the browser or command line:

```bash
curl -f http://<alb_dns_name>/
curl -f http://<alb_dns_name>/api/v1/health
```

Expected results:
- Frontend loads successfully
- API health check returns successful status
- Target groups show healthy targets

---

## Task 8: Check logs and monitoring

Tail the ECS logs:

```bash
aws logs tail /ecs/ipra-dev-api --follow
aws logs tail /ecs/ipra-dev-frontend --follow
```

Open the CloudWatch dashboard for the environment and confirm the alarms and service metrics are active.

---

## Task 9: Optional CI/CD setup

This is not required for the first deployment, but it is the next improvement after the app is running successfully.

Set up GitHub OIDC and deploy automation:
- enable GitHub OIDC in Terraform
- configure GitHub repo secrets
- connect the deploy workflow to AWS
- let GitHub Actions push new images and update ECS automatically

---

## Task 10: Final validation and handoff

Before finishing the assignment, confirm all of the following:
- ECR repositories contain tagged images
- ECS tasks use those ECR image URIs
- ALB routes are healthy
- API health endpoint works
- frontend page loads over the ALB
- logs are available in CloudWatch
- any required secrets are set correctly

---

## Recommended Next Action

The immediate next step is:
1. authenticate Docker to ECR
2. push the frontend and API images
3. update the AWS Terraform values to use the ECR image URIs
4. run `terraform apply`
5. verify ECS and ALB health

This is the exact continuation path to finish the deployment successfully.
