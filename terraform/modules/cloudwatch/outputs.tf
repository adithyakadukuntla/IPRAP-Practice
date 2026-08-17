output "frontend_log_group_name" { value = aws_cloudwatch_log_group.frontend.name }
output "api_log_group_name"      { value = aws_cloudwatch_log_group.api.name }
output "dashboard_name"          { value = aws_cloudwatch_dashboard.this.dashboard_name }
