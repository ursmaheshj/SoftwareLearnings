variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "repository_name" {
  description = "ECR repository name for FastAPI application"
  type        = string
  default     = "fastapi-app"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}
