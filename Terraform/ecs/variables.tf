variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "fastapi"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

# VPC Variables
variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_1_cidr" {
  description = "Public subnet 1 CIDR"
  type        = string
  default     = "10.0.1.0/24"
}

variable "public_subnet_2_cidr" {
  description = "Public subnet 2 CIDR"
  type        = string
  default     = "10.0.2.0/24"
}

variable "private_subnet_1_cidr" {
  description = "Private subnet 1 CIDR"
  type        = string
  default     = "10.0.10.0/24"
}

variable "private_subnet_2_cidr" {
  description = "Private subnet 2 CIDR"
  type        = string
  default     = "10.0.11.0/24"
}

# ECS Variables
variable "container_port" {
  description = "Container port"
  type        = number
  default     = 8000
}

variable "task_cpu" {
  description = "Task CPU units (256, 512, 1024, 2048, etc.)"
  type        = string
  default     = "256"
}

variable "task_memory" {
  description = "Task memory in MB (512, 1024, 2048, etc.)"
  type        = string
  default     = "512"
}

variable "desired_task_count" {
  description = "Desired number of tasks"
  type        = number
  default     = 2
}

variable "min_task_count" {
  description = "Minimum number of tasks for auto-scaling"
  type        = number
  default     = 2
}

variable "max_task_count" {
  description = "Maximum number of tasks for auto-scaling"
  type        = number
  default     = 4
}

# ECR Variables
variable "ecr_repository_name" {
  description = "ECR repository name"
  type        = string
  default     = "fastapi-app"
}

variable "image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}

# CloudWatch Variables
variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 7
}

# ALB Variables
variable "health_check_path" {
  description = "Health check path"
  type        = string
  default     = "/"
}

# Optional: SSL Certificate (uncomment if using HTTPS)
# variable "ssl_certificate_arn" {
#   description = "SSL certificate ARN for HTTPS"
#   type        = string
#   default     = ""
# }
