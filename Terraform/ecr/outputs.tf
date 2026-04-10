output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.fastapi.repository_url
}

output "ecr_repository_arn" {
  description = "ECR repository ARN"
  value       = aws_ecr_repository.fastapi.arn
}

output "ecr_repository_name" {
  description = "ECR repository name"
  value       = aws_ecr_repository.fastapi.name
}

output "ecr_registry_id" {
  description = "ECR registry ID (AWS Account ID)"
  value       = aws_ecr_repository.fastapi.registry_id
}

output "login_command" {
  description = "Command to login to ECR"
  value       = "aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${aws_ecr_repository.fastapi.repository_url}"
  sensitive   = true
}
