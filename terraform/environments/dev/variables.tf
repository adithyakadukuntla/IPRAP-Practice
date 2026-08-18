variable "aws_region" {
  type    = string
  default = "us-east-1"
}
variable "project_name" {
  type    = string
  default = "ipra"
}
variable "environment" {
  type    = string
  default = "dev"
}
variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}
variable "azs" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b"]
}
variable "public_subnet_cidrs" {
  type    = list(string)
  default = ["10.20.0.0/24", "10.20.1.0/24"]
}
variable "private_subnet_cidrs" {
  type    = list(string)
  default = ["10.20.10.0/24", "10.20.11.0/24"]
}
variable "enable_nat_gateway" {
  type    = bool
  default = true
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

variable "frontend_image_placeholder" {
  type    = string
  default = "public.ecr.aws/nginx/nginx:latest"
}
variable "api_image_placeholder" {
  type    = string
  default = "public.ecr.aws/docker/library/hello-world:latest"
}

variable "certificate_arn" {
  type    = string
  default = ""
}

# ---------------------------------------------------------------------------
# IAM ROLES ARE NOT CREATED BY TERRAFORM IN THIS LAB.
# The lab account blocks iam:CreateRole / iam:PutRolePolicy even for the
# provided root/admin credentials. Paste the ARNs of the roles the lab has
# already pre-created for you (ask your lab provider if you don't have them
# yet -- see docs/iam-lab-constraints.md for exactly what each role needs).
# ---------------------------------------------------------------------------
variable "ecs_execution_role_arn" {
  type        = string
  description = "Optional ECS task EXECUTION role ARN. Leave blank for this lab setup because IAM role creation is blocked."
  default     = ""
}

variable "ecs_task_role_arn" {
  type        = string
  description = "Optional ECS TASK role ARN. Leave blank for this lab setup because IAM role creation is blocked."
  default     = ""
}

variable "alarm_sns_topic_arn" {
  type    = string
  default = ""
}
