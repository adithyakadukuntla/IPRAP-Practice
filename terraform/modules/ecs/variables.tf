variable "project_name" {
  type = string
}
variable "environment" {
  type = string
}
variable "aws_region" {
  type = string
}
variable "private_subnet_ids" {
  type = list(string)
}
variable "frontend_sg_id" {
  type = string
}
variable "api_sg_id" {
  type = string
}
variable "frontend_image" {
  type        = string
  description = "Full ECR image URI incl. tag, e.g. <account>.dkr.ecr.<region>.amazonaws.com/ipra-dev-frontend:<git-sha>"
}
variable "api_image" {
  type = string
}
variable "frontend_container_port" {
  type    = number
  default = 80
}
variable "api_container_port" {
  type    = number
  default = 8000
}
variable "frontend_cpu" {
  type    = number
  default = 256
}
variable "frontend_memory" {
  type    = number
  default = 512
}
variable "api_cpu" {
  type    = number
  default = 256
}
variable "api_memory" {
  type    = number
  default = 512
}
variable "frontend_desired_count" {
  type    = number
  default = 1
}
variable "api_desired_count" {
  type    = number
  default = 1
}
variable "execution_role_arn" {
  type    = string
  default = ""
}
variable "task_role_arn" {
  type    = string
  default = ""
}
variable "frontend_log_group" {
  type = string
}
variable "api_log_group" {
  type = string
}
variable "frontend_target_group_arn" {
  type = string
}
variable "api_target_group_arn" {
  type = string
}
variable "api_env_vars" {
  type        = map(string)
  description = "Non-secret environment variables for the API container"
  default     = {}
}
variable "api_secrets" {
  type        = map(string)
  description = "Map of ENV_VAR_NAME => Secrets Manager ARN, injected securely into the API task"
  default     = {}
}
variable "tags" {
  type    = map(string)
  default = {}
}
