locals {
  name_prefix = "${var.project_name}-${var.environment}"
}

# Creates EMPTY secret containers only. Actual secret VALUES must be set
# out-of-band (AWS Console, CLI, or a secure pipeline step) -- never via
# a value committed to Terraform source or Git.
resource "aws_secretsmanager_secret" "this" {
  for_each                = toset(var.secret_names)
  name                    = "${local.name_prefix}/${each.value}"
  description             = "IPRA ${var.environment} secret: ${each.value}"
  recovery_window_in_days = 0 # training only; use 7-30 for real environments

  tags = merge(var.tags, { Name = "${local.name_prefix}-${each.value}" })
}
