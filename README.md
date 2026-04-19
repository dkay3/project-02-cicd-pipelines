# Project 02 — CI/CD Pipeline with GitHub Actions

Automated build → test → scan → deploy pipeline. Every push to `main`
runs the full pipeline. No manual deployments. No SSH. No console clicks.

## Pipeline flow

```
git push → GitHub Actions → Test → Build Docker →  Push ECR → Deploy ECS → Slack notify
```

## What this automates

| Stage | Tool | What it does |
|---|---|---|
| Test | pytest | Runs unit tests, fails pipeline on any failure |
| Build | Docker | Multi-stage build, non-root user |
| Push | AWS ECR | Stores image tagged with git SHA |
| Deploy | AWS ECS | Rolling update, waits for health checks |
| Notify | Slack | Posts pass/fail with commit info |

## Architecture

```
Developer → GitHub → GitHub Actions
                         │
                    ┌────▼─────┐
                    │  Test     │  pytest · flake8
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │  Build    │  Docker multi-stage
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │  Push     │  AWS ECR (tagged: git SHA)
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │  Deploy   │  ECS Fargate rolling update
                    └────┬─────┘
                         │
                    ┌────▼─────┐
                    │  Notify   │  Slack webhook
                    └──────────┘
```

## Prerequisites

- AWS account with programmatic access
- GitHub repository with Actions enabled
- Docker Desktop or Docker in WSL2
- Terraform >= 1.6.0 (for ECS infrastructure)
- Slack workspace with incoming webhooks enabled

## Setup

### 1. Deploy ECS infrastructure

```bash
cd terraform
# Update terraform.tfvars with your VPC ID and subnet IDs from Project 01
terraform init
terraform apply
# Note the ecr_repository_url and alb_dns_name outputs
```

### 2. Create GitHub Actions IAM user

```bash
aws iam create-user --user-name github-actions-deployer
aws iam attach-user-policy --user-name github-actions-deployer \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
aws iam attach-user-policy --user-name github-actions-deployer \
  --policy-arn arn:aws:iam::aws:policy/AmazonECS_FullAccess
aws iam create-access-key --user-name github-actions-deployer
```

### 3. Add GitHub Secrets

Go to repo Settings → Secrets and variables → Actions:

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `SLACK_WEBHOOK_URL` | Slack incoming webhook URL |

### 4. Push and watch

```bash
git push origin main
# Go to GitHub → Actions tab to watch the pipeline run
```

## Key concepts demonstrated

- **Pipeline as code** — entire CI/CD process lives in `.github/workflows/deploy.yml`
- **Shift-left security** — Trivy scans the image before it ever reaches production
- **Immutable deployments** — every image is tagged with the git SHA, never overwrite
- **Deployment safety** — ECS circuit breaker auto-rolls back if health checks fail
- **Separation of concerns** — dedicated IAM user for GitHub Actions with minimal permissions

## How to fork and use this

1. Fork this repo
2. Deploy the Terraform infrastructure in `/terraform`
3. Create a GitHub Actions IAM user and add the three secrets
4. Push any change to `main` to trigger the pipeline

## Part of the DevOps Portfolio Series

| Project | Description |
|---|---|
| Project 01 | Terraform AWS Infrastructure |
| **Project 02** ← you are here | CI/CD Pipeline with GitHub Actions |
| Project 03 | Kubernetes on EKS |
| Project 04 | Prometheus + Grafana Observability Stack |
| Project 05 | DevSecOps Pipeline |
| Project 06 | Capstone — End-to-End Production Platform |

---
Built on WSL2 · GitHub Actions · Docker · AWS ECR · AWS ECS Fargate
