locals {
  name_prefix = "${var.project_name}-${var.environment}"
}

resource "aws_ecr_repository" "this" {
  for_each             = toset(var.repo_names)
  name                 = "${local.name_prefix}-${each.value}"
  image_tag_mutability = var.image_tag_mutability

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = merge(var.tags, { Name = "${local.name_prefix}-${each.value}" })
}

resource "aws_ecr_lifecycle_policy" "this" {
  for_each   = aws_ecr_repository.this
  repository = each.value.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep only the last ${var.max_images} images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = var.max_images
        }
        action = { type = "expire" }
      }
    ]
  })
}
