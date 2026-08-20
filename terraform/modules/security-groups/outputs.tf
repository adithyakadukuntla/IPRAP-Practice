output "alb_sg_id"      { value = aws_security_group.alb.id }
output "frontend_sg_id" { value = aws_security_group.frontend.id }
output "api_sg_id"      { value = aws_security_group.api.id }
