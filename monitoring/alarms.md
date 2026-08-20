# CloudWatch Alarms (project/training thresholds — not production SLAs)

| Alarm | Metric | Threshold | Meaning |
|---|---|---|---|
| `ipra-dev-alb-5xx-high` | ALB 5XX count | > 5 in 1 min, 2 periods | Backend errors trending up |
| `ipra-dev-alb-high-latency` | ALB TargetResponseTime | > 2s avg, 3 periods | Slow responses |
| `ipra-dev-api-unhealthy-targets` | UnHealthyHostCount (API TG) | > 0, 2 periods | API failing health checks |
| `ipra-dev-frontend-unhealthy-targets` | UnHealthyHostCount (Frontend TG) | > 0, 2 periods | Frontend failing health checks |
| `ipra-dev-api-cpu-high` | ECS CPUUtilization (API) | > 80%, 3 periods | API may need more CPU/scaling |
| `ipra-dev-frontend-cpu-high` | ECS CPUUtilization (Frontend) | > 80%, 3 periods | Frontend may need more CPU/scaling |

Wire `alarm_sns_topic_arn` in `terraform.tfvars` to an SNS topic to receive notifications; left empty by default in training.
