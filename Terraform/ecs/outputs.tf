output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.fastapi_alb.dns_name
}

output "alb_url" {
  description = "URL to access the application"
  value       = "http://${aws_lb.fastapi_alb.dns_name}"
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.fastapi_cluster.name
}

output "ecs_cluster_arn" {
  description = "ECS cluster ARN"
  value       = aws_ecs_cluster.fastapi_cluster.arn
}

output "ecs_service_name" {
  description = "ECS service name"
  value       = aws_ecs_service.fastapi_service.name
}

output "task_definition_arn" {
  description = "Task definition ARN"
  value       = aws_ecs_task_definition.fastapi_task.arn
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group name"
  value       = aws_cloudwatch_log_group.ecs_log_group.name
}

output "target_group_arn" {
  description = "Target group ARN"
  value       = aws_lb_target_group.fastapi_tg.arn
}
