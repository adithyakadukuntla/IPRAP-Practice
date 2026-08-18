# CloudWatch Dashboard — `ipra-dev-dashboard`

Widgets:
1. ALB Request Count / 4xx / 5xx
2. ALB Target Response Time
3. ECS CPU / Memory Utilization (frontend + API)
4. Unhealthy Target Count (frontend + API)

Defined in `terraform/modules/cloudwatch/main.tf` (`aws_cloudwatch_dashboard.this`). View in the AWS Console under CloudWatch → Dashboards.
