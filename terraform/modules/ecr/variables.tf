variable "project_name" {
  type = string
}
variable "environment" {
  type = string
}
variable "repo_names" {
  type        = list(string)
  description = "Short names, e.g. [\"frontend\", \"api\"]"
  default     = ["frontend", "api"]
}
variable "image_tag_mutability" {
  type    = string
  default = "IMMUTABLE"
}
variable "max_images" {
  type    = number
  default = 15
}
variable "tags" {
  type    = map(string)
  default = {}
}
