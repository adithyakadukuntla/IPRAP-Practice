# Operations Runbook

**Is the API healthy?**
`curl http://<alb-dns>/api/v1/health` should return `200`. Also check the `ipra-dev-api-unhealthy-targets` CloudWatch alarm.

**Where are application logs?**
CloudWatch Logs → `/ecs/ipra-dev-frontend` and `/ecs/ipra-dev-api`.

**Where are ECS task failures visible?**
ECS console → cluster `ipra-dev-cluster` → service → "Tasks" tab → stopped tasks show a stopped reason. Also check the CloudWatch dashboard `ipra-dev-dashboard`.

**How do I identify an unhealthy ALB target?**
EC2 console → Target Groups → `ipra-dev-api-tg` / `ipra-dev-frontend-tg` → Targets tab → health status/reason.

**How do I roll back?**
See `docs/rollback.md`.

**How do I deploy a new version?**
Push to `main` → GitHub Actions `deploy.yml` builds, pushes to ECR, updates the ECS service, waits for stability, and runs smoke tests automatically. Manual trigger via `workflow_dispatch` is also available.

**How do I verify the ECR image?**
`aws ecr describe-images --repository-name ipra-dev-api --image-ids imageTag=<sha>`

**How do I destroy training resources safely?**
```
cd terraform/environments/dev
terraform destroy
```
Confirm no shared resources (e.g. a shared ECR used by other participants) are in scope before destroying.
