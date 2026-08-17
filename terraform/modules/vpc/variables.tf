variable "project_name" {
  type = string
}
variable "environment"  {
  type = string
}
variable "vpc_cidr"     {
  type = string
  default = "10.20.0.0/16"
}
variable "azs"          {
  type = list(string)
}
variable "public_subnet_cidrs"  {
  type = list(string)
}
variable "private_subnet_cidrs" {
  type = list(string)
}
variable "enable_nat_gateway" {
  type        = bool
  default     = false
  description = "Only enable if private ECS tasks need outbound internet (e.g. to reach Snowflake). Costs money."
}
variable "tags" {
  type = map(string)
  default = {}
}
