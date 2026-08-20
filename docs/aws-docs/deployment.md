# Deployment Documentation

## How to deploy
1. Provision infrastructure (`terraform apply`, see README "Step-by-step").
2. Merge to `main` — GitHub Actions `deploy.yml` builds Docker images, pushes to ECR, updates ECS task definitions/services, waits for stability, and runs smoke tests.

## How to validate
- `aws ecs wait services-stable ...` (build into the pipeline) confirms ECS reached steady state.
- ALB target health must show `healthy` for both target groups.
- Smoke test: `GET /` (frontend) and `GET /api/v1/health` (API) both return 200.

## How to rollback
See `docs/rollback.md`.
