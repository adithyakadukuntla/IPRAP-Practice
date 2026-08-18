variable "project_name" {
  type = string
}
variable "environment" {
  type = string
}
variable "secret_names" {
  type        = list(string)
  description = "Logical secret names, e.g. [\"snowflake-credentials\", \"api-auth-secret\"]"
  default     = ["snowflake-credentials", "api-auth-secret"]
}
variable "tags" {
  type    = map(string)
  default = {}
}
