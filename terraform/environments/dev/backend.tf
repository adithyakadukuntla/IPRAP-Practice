# Uncomment and fill in once an approved S3 backend + DynamoDB lock table exist.
#
# terraform {
#   backend "s3" {
#     bucket         = "ipra-terraform-state-<account-id>"
#     key            = "dev/terraform.tfstate"
#     region         = "us-east-1"
#     dynamodb_table = "ipra-terraform-locks"
#     encrypt        = true
#   }
# }
