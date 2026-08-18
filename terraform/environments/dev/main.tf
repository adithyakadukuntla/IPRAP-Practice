locals {
  common_tags = {
    Project     = "IPRA"
    Environment = var.environment
    Owner       = "participant-06"
    ManagedBy   = "Terraform"
    CostCenter  = "Training"
  }
  name_prefix = "${var.project_name}-${var.environment}"
}

module "vpc" {
  source = "../../modules/vpc"

  project_name          = var.project_name
  environment            = var.environment
  vpc_cidr               = var.vpc_cidr
  azs                     = var.azs
  public_subnet_cidrs    = var.public_subnet_cidrs
  private_subnet_cidrs   = var.private_subnet_cidrs
  enable_nat_gateway     = var.enable_nat_gateway
  tags                    = local.common_tags
}

module "security_groups" {
  source = "../../modules/security-groups"

  project_name             = var.project_name
  environment              = var.environment
  vpc_id                   = module.vpc.vpc_id
  container_port_frontend  = 80
  container_port_api       = 8000
  tags                     = local.common_tags
}

# Creates only the secret CONTAINERS (metadata). Values are set out-of-band
# via `aws secretsmanager put-secret-value` -- never via Terraform source.
module "secrets" {
  source = "../../modules/secrets"

  project_name = var.project_name
  environment  = var.environment
  secret_names = ["snowflake-credentials", "api-auth-secret"]
  tags         = local.common_tags
}

# NOTE: No `module "iam"` here. IAM role creation is not permitted in this
# lab account (blocked even under root). We reference the lab's pre-created
# roles directly via var.ecs_execution_role_arn / var.ecs_task_role_arn.
# Those roles must already allow: ecr:GetDownloadUrlForLayer/BatchGetImage,
# logs:CreateLogStream/PutLogEvents, and (for the task role, if the API needs
# to read secrets at runtime) secretsmanager:GetSecretValue on the ARNs in
# module.secrets.secret_arns. If they don't, ask the lab provider to attach
# those permissions -- Terraform cannot attach policies to a role it did not
# create, since that also requires an IAM write permission we don't have.

module "ecr" {
  source = "../../modules/ecr"

  project_name = var.project_name
  environment  = var.environment
  repo_names   = ["frontend", "api"]
  tags         = local.common_tags
}

module "alb" {
  source = "../../modules/alb"

  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  public_subnet_ids  = module.vpc.public_subnet_ids
  alb_sg_id          = module.security_groups.alb_sg_id
  frontend_port      = 80
  api_port           = 8000
  certificate_arn    = var.certificate_arn
  tags               = local.common_tags
}

module "cloudwatch" {
  source = "../../modules/cloudwatch"

  project_name            = var.project_name
  environment             = var.environment
  log_retention_days      = 14
  alb_arn_suffix          = module.alb.alb_arn_suffix
  frontend_tg_arn_suffix  = module.alb.frontend_tg_arn_suffix
  api_tg_arn_suffix       = module.alb.api_tg_arn_suffix
  ecs_cluster_name        = "${local.name_prefix}-cluster"
  ecs_frontend_service    = "${local.name_prefix}-frontend"
  ecs_api_service         = "${local.name_prefix}-api"
  alarm_sns_topic_arn     = var.alarm_sns_topic_arn
  tags                     = local.common_tags
}

module "ecs" {
  source = "../../modules/ecs"

  project_name             = var.project_name
  environment              = var.environment
  aws_region               = var.aws_region
  private_subnet_ids       = module.vpc.private_subnet_ids
  frontend_sg_id           = module.security_groups.frontend_sg_id
  api_sg_id                = module.security_groups.api_sg_id

  frontend_image = var.frontend_image_placeholder
  api_image      = var.api_image_placeholder

  frontend_cpu    = var.frontend_cpu
  frontend_memory = var.frontend_memory
  api_cpu         = var.api_cpu
  api_memory      = var.api_memory

  # Pre-created lab roles -- referenced, not created.
  execution_role_arn = var.ecs_execution_role_arn
  task_role_arn       = var.ecs_task_role_arn

  frontend_log_group = module.cloudwatch.frontend_log_group_name
  api_log_group        = module.cloudwatch.api_log_group_name

  frontend_target_group_arn = module.alb.frontend_tg_arn
  api_target_group_arn        = module.alb.api_tg_arn

  api_env_vars = {
    ENVIRONMENT       = var.environment
    SNOWFLAKE_ACCOUNT = "REPLACE_ME"
    SNOWFLAKE_DB      = "IPRA_DB"
  }

  api_secrets = {
    SNOWFLAKE_USER     = module.secrets.secret_arns["snowflake-credentials"]
    SNOWFLAKE_PASSWORD = module.secrets.secret_arns["snowflake-credentials"]
    API_AUTH_SECRET    = module.secrets.secret_arns["api-auth-secret"]
  }

  tags = local.common_tags
}
