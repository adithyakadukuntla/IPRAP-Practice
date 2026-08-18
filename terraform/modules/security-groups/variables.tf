variable "project_name" {
  type = string
}
variable "environment"  {
  type = string
}
variable "vpc_id"       {
  type = string
}
variable "container_port_frontend" {
  type = number
  default = 80
}
variable "container_port_api"      {
  type = number
  default = 8000
}
variable "tags" {
  type = map(string)
  default = {}
}
