provider "aws" {
  region = "us-east-1"
}

# ECS Cluster for Container Orchestration
resource "aws_ecs_cluster" "copilot_cluster" {
  name = "devsecops-copilot-cluster"
}

# Elastic Container Registry (ECR) repository
resource "aws_ecr_repository" "copilot_repo" {
  name = "devsecops-copilot"
}

output "ecr_repository_url" {
  value = aws_ecr_repository.copilot_repo.repository_url
}