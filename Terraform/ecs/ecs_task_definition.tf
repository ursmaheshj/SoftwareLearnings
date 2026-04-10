# Get ECR repository URL from data source
data "aws_ecr_repository" "fastapi" {
  name = var.ecr_repository_name
}

# ECS Task Definition
resource "aws_ecs_task_definition" "fastapi_task" {
  family                   = var.app_name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = var.app_name
      image     = "${data.aws_ecr_repository.fastapi.repository_url}:${var.image_tag}"
      essential = true
      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
          protocol      = "tcp"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs_log_group.name
          "awslogs-region"        = data.aws_region.current.name
          "awslogs-stream-prefix" = "ecs"
        }
      }

      environment = [
        {
          name  = "ENV"
          value = var.environment
        }
      ]

      # Optional: Add secrets from Secrets Manager
      # secrets = [
      #   {
      #     name      = "DATABASE_URL"
      #     valueFrom = aws_secretsmanager_secret.db_url.arn
      #   }
      # ]
    }
  ])

  tags = {
    Name = "${var.app_name}-task-def"
  }
}
