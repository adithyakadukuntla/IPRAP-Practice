# IAM in This Lab Account

This account blocks `iam:CreateRole` / `iam:PutRolePolicy` — even under the
root/admin credentials the lab provided. Because of that, **Terraform in this
repo does not create or modify any IAM role.** Every other service (VPC, ECR,
ECS, ALB, CloudWatch, Secrets Manager) is still created normally by
`terraform apply`.

## What you must supply

Two pre-created role ARNs, in `terraform.tfvars`:

```hcl
ecs_execution_role_arn = "arn:aws:iam::<account-id>:role/<execution-role>"
ecs_task_role_arn      = "arn:aws:iam::<account-id>:role/<task-role>"
```

Ask your lab provider for these, or list what's available yourself:
```bash
aws iam list-roles --query "Roles[].{Name:RoleName,Arn:Arn}" --output table
```

## What each role needs (ask the lab admin to confirm/attach if missing)

### `ecs_execution_role_arn` — used by ECS/Fargate itself to start the task
- `ecr:GetAuthorizationToken`
- `ecr:BatchCheckLayerAvailability`, `ecr:GetDownloadUrlForLayer`, `ecr:BatchGetImage`
- `logs:CreateLogStream`, `logs:PutLogEvents`
- `secretsmanager:GetSecretValue` — **only if** the API container uses the
  `secrets` block (it does, in `modules/ecs/main.tf`) to inject
  `SNOWFLAKE_USER` / `SNOWFLAKE_PASSWORD` / `API_AUTH_SECRET` at container
  startup

This is normally satisfied by the AWS-managed policy
`AmazonECSTaskExecutionRolePolicy`, plus an inline statement for Secrets
Manager. If the lab's role already has `AmazonECSTaskExecutionRolePolicy`
attached but *not* Secrets Manager access, the API task will fail to start
with a `ResourceInitializationError` pulling secrets — see the workaround
below.

### `ecs_task_role_arn` — used by your running application code
- `logs:CreateLogStream`, `logs:PutLogEvents` (only if the app writes its own
  custom log streams beyond the container's stdout/stderr, which the
  execution role already handles)
- Anything else your API code itself calls at runtime (e.g. reading a secret
  directly via the AWS SDK instead of via the ECS `secrets` injection)

## If the pre-created execution role can't read Secrets Manager

You have two options, since Terraform can't attach the policy for you:

1. **Ask the lab admin** to attach an inline/managed policy granting
   `secretsmanager:GetSecretValue` on the ARNs Terraform creates (see
   `terraform output secret_arns` after `apply`).
2. **Skip the `secrets` ECS injection entirely** and pass Snowflake
   credentials as plain (non-secret) `api_env_vars` instead, purely for this
   training lab. This is **not** something to do outside a disposable
   training account — do not do this in any environment with real
   credentials. To do it: move `SNOWFLAKE_USER`/`SNOWFLAKE_PASSWORD` from
   `api_secrets` to `api_env_vars` in `environments/dev/main.tf`.

## GitHub Actions CI/CD

The original design used a Terraform-created OIDC IAM role for GitHub
Actions to assume. That's also IAM creation, so it's **not included** in
this version. If you still want automated deploys from GitHub Actions in
this lab, ask the lab provider for a role ARN with `ecr:*Push*` /
`ecs:UpdateService` permissions and reference it directly in your GitHub
Actions secrets — Terraform doesn't need to be involved in creating it.
