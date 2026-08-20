# Security

- No hardcoded credentials anywhere in this repository (verified via `git grep` and CI checks).
- Snowflake credentials and API auth secret live in AWS Secrets Manager (`terraform/modules/secrets`), injected into the ECS task via the `secrets` block — never as plain `environment` values.
- IAM: separate **execution role** (pull image, write logs, read secrets) and **task role** (least-privilege app runtime permissions). No `AdministratorAccess` is used for application tasks.
- GitHub Actions authenticates to AWS via **OIDC** (`enable_github_oidc = true`), not long-lived access keys, when available in the training account.
- ECS tasks run in private subnets with no public IP; only the ALB is internet-facing.
- CloudTrail provides an audit trail of IAM/security-group/ECS API changes (see `operations.md`).
- Frontend container never receives Snowflake credentials — client-side values are visible in the browser bundle.
