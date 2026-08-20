variable "project_name" { type = string }
variable "environment"  { type = string }
variable "vpc_id"       { type = string }
variable "public_subnet_ids" { type = list(string) }
variable "alb_sg_id"    { type = string }
variable "frontend_port" {
  type    = number
  default = 80
}
variable "api_port" {
  type    = number
  default = 8000
}
variable "certificate_arn" {
  type        = string
  default     = ""
  description = "ACM certificate ARN for HTTPS. Leave empty to use HTTP only (training limitation)."
}
variable "tags" {
  type    = map(string)
  default = {}
}
