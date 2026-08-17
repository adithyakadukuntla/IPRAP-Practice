terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote state recommended (see backend.tf). If unavailable in the training
  # account, local state is used as a documented exception -- never commit
  # terraform.tfstate to Git (see .gitignore).
  # backend "s3" {}
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.common_tags
  }
}
