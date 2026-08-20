variable "project_name" {
  type = string
}
variable "environment"  {
  type = string
}
variable "log_retention_days" {
  type    = number
  default = 14
}
variable "alb_arn_suffix"      {
  type = string
}
variable "frontend_tg_arn_suffix" {
  type = string
}
variable "api_tg_arn_suffix"      {
  type = string
}
variable "ecs_cluster_name"    {
  type = string
}
variable "ecs_frontend_service" {
  type = string
}
variable "ecs_api_service"      {
  type = string
}
variable "alarm_sns_topic_arn" {
  type        = string
  default     = ""
  description = "Optional SNS topic to notify on alarm. Leave empty to skip notifications (training default)."
}
variable "tags" {
  type    = map(string)
  default = {}
}
