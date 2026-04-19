output "ecr_repository_url" {
  description = "ECR repository URL — used in GitHub Actions"
  value       = aws_ecr_repository.app.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name — used in GitHub Actions"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "ECS service name — used in GitHub Actions"
  value       = aws_ecs_service.app.name
}

output "alb_dns_name" {
  description = "Application URL — open this in your browser"
  value       = "http://${aws_lb.app.dns_name}"
}