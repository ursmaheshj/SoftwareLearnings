# ECS Cluster
resource "aws_ecs_cluster" "fastapi_cluster" {
  name = "${var.app_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "${var.app_name}-cluster"
  }
}

# ECS Cluster Capacity Providers
resource "aws_ecs_cluster_capacity_providers" "fastapi_capacity_providers" {
  cluster_name = aws_ecs_cluster.fastapi_cluster.name

  capacity_providers = ["FARGATE", "FARGATE_SPOT"]

  default_capacity_provider_strategy {
    base              = 1
    weight            = 100
    capacity_provider = "FARGATE"
  }
}

# CloudWatch Log Group for ECS
resource "aws_cloudwatch_log_group" "ecs_log_group" {
  name              = "/ecs/${var.app_name}"
  retention_in_days = var.log_retention_days

  tags = {
    Name = "${var.app_name}-logs"
  }
}
