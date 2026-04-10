# AWS ECR Repository for FastAPI Application
resource "aws_ecr_repository" "fastapi" {
  name                 = var.repository_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = var.repository_name
    Environment = var.environment
    Application = "FastAPI"
  }
}

# ECR Repository Lifecycle Policy (keep only last 5 images)
resource "aws_ecr_lifecycle_policy" "fastapi" {
  repository = aws_ecr_repository.fastapi.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 5 images"
        selection = {
          tagStatus       = "any"
          countType       = "imageCountMoreThan"
          countNumber     = 5
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# Data source to get current AWS account ID
data "aws_caller_identity" "current" {}
