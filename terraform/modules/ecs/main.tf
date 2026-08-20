locals {
  name_prefix = "${var.project_name}-${var.environment}"
}

resource "aws_ecs_cluster" "this" {
  name = "${local.name_prefix}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = merge(var.tags, { Name = "${local.name_prefix}-cluster" })
}

# ---------------- Frontend task/service ----------------
resource "aws_ecs_task_definition" "frontend" {
  family                   = "${local.name_prefix}-frontend"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.frontend_cpu
  memory                   = var.frontend_memory
  execution_role_arn       = var.execution_role_arn != "" ? var.execution_role_arn : null
  task_role_arn            = var.task_role_arn != "" ? var.task_role_arn : null

  container_definitions = jsonencode([
    {
      name      = "frontend"
      image     = var.frontend_image
      essential = true
      portMappings = [
        { containerPort = var.frontend_container_port, protocol = "tcp" }
      ]
    }
  ])

  tags = var.tags
}

resource "aws_ecs_service" "frontend" {
  name            = "${local.name_prefix}-frontend"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.frontend.arn
  desired_count   = var.frontend_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [var.frontend_sg_id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.frontend_target_group_arn
    container_name    = "frontend"
    container_port    = var.frontend_container_port
  }

  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  tags = var.tags

  lifecycle {
    ignore_changes = [task_definition] # allow CI/CD to update independently of terraform apply
  }
}

# ---------------- API task/service ----------------
locals {
  api_secrets_list = [
    for name, arn in var.api_secrets : { name = name, valueFrom = arn }
  ]
  api_env_list = [
    for name, value in var.api_env_vars : { name = name, value = value }
  ]
}

resource "aws_ecs_task_definition" "api" {
  family                   = "${local.name_prefix}-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.api_cpu
  memory                   = var.api_memory
  execution_role_arn       = var.execution_role_arn != "" ? var.execution_role_arn : null
  task_role_arn            = var.task_role_arn != "" ? var.task_role_arn : null

  container_definitions = jsonencode([
    {
      name      = "api"
      image     = var.api_image
      essential = true
      portMappings = [
        { containerPort = var.api_container_port, protocol = "tcp" }
      ]
      environment = local.api_env_list
    }
  ])

  tags = var.tags
}

resource "aws_ecs_service" "api" {
  name            = "${local.name_prefix}-api"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = var.api_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [var.api_sg_id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.api_target_group_arn
    container_name    = "api"
    container_port    = var.api_container_port
  }

  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  tags = var.tags

  lifecycle {
    ignore_changes = [task_definition]
  }
}
