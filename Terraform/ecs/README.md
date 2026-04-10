# FastAPI ECS Deployment with Terraform

Complete infrastructure as code for deploying FastAPI application on AWS ECS with security best practices.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    AWS VPC (10.0.0.0/16)                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │          Internet Gateway & NAT Gateway          │   │
│  └────────────────┬─────────────────────────────────┘   │
│                   │                                      │
│  ┌────────────────┴────────────────────────────────┐    │
│  │     Application Load Balancer (ALB)             │    │
│  │     Public Subnets (10.0.1.0/24, 10.0.2.0/24)   │    │
│  └────────────────┬─────────────────────────────────┘   │
│                   │                                      │
│  ┌────────────────┴────────────────────────────────┐    │
│  │         ECS Service with 2+ Tasks               │    │
│  │   Private Subnets (10.0.10.0/24, 10.0.11.0/24) │    │
│  │  ┌──────────┐      ┌──────────┐                │    │
│  │  │ FastAPI  │      │ FastAPI  │                │    │
│  │  │Container │      │Container │                │    │
│  │  │(8000)    │      │(8000)    │                │    │
│  │  └──────────┘      └──────────┘                │    │
│  └───────────────────────────────────────────────┘     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Files Structure

```
ecs/
├── provider.tf              # AWS provider configuration
├── networking.tf            # VPC, subnets, NAT gateways
├── security_groups.tf       # ALB and ECS security groups
├── iam.tf                   # IAM roles and policies
├── alb.tf                   # Application Load Balancer
├── ecs_cluster.tf           # ECS cluster and CloudWatch logs
├── ecs_task_definition.tf   # ECS task definition (container specs)
├── ecs_service.tf           # ECS service and auto-scaling
├── variables.tf             # Variable definitions
├── outputs.tf               # Output values
├── terraform.tfvars         # Default variable values
└── README.md                # This file
```

## Security Features

1. **Network Isolation**
   - Private subnets for ECS tasks
   - Public subnets only for load balancer
   - NAT gateways for secure outbound traffic

2. **Security Groups**
   - ALB: Only allows HTTP (80) and HTTPS (443) from internet
   - ECS: Only allows traffic from ALB on container port
   - Least privilege principle

3. **IAM Security**
   - Separate execution role (pull images from ECR)
   - Separate task role (for app-level permissions)
   - No overly permissive policies

4. **Container Security**
   - Non-root user in Dockerfile (recommended)
   - Image scanning enabled in ECR
   - CloudWatch container logs for monitoring

## Prerequisites

- AWS CLI configured with credentials
- Terraform v1.0+
- AWS Account with ECR repository created (`fastapi-app`)
- Docker image already pushed to ECR

## Deployment Steps

### Step 1: Initialize Terraform

```bash
cd d:\SoftwareLearnings\Terraform\ecs
terraform init
```

This downloads the AWS provider and initializes the backend.

### Step 2: Review the Plan

```bash
terraform plan
```

Review what resources will be created. You should see:
- VPC and subnets (6 total)
- Internet Gateway and NAT Gateways (2)
- Security Groups (2)
- Application Load Balancer
- ECS Cluster, Task Definition, and Service
- Auto-scaling policies
- CloudWatch log group

### Step 3: Apply the Configuration

```bash
terraform apply
```

Type `yes` when prompted. This takes approximately 5-10 minutes to complete.

### Step 4: Verify Deployment

```bash
# Get the load balancer URL
terraform output alb_url

# Check ECS cluster status
aws ecs describe-clusters --clusters fastapi-cluster --region us-east-1

# Check ECS service status
aws ecs describe-services --cluster fastapi-cluster --services fastapi-service --region us-east-1

# Check running tasks
aws ecs list-tasks --cluster fastapi-cluster --region us-east-1
aws ecs describe-tasks --cluster fastapi-cluster --tasks <task-arn> --region us-east-1
```

### Step 5: Access Your Application

Once tasks are running (status = RUNNING in ~2-3 minutes):

```bash
# Get the ALB URL
ALB_URL=$(terraform output -raw alb_url)
echo $ALB_URL

# Test your application
curl $ALB_URL
```

## Customization Guide

### Change Container Port

Edit `terraform.tfvars`:
```hcl
container_port = 8000  # Change this
```

Update your FastAPI app to listen on this port.

### Change VPC CIDR Blocks

Edit `terraform.tfvars`:
```hcl
vpc_cidr               = "10.0.0.0/16"
public_subnet_1_cidr   = "10.0.1.0/24"
public_subnet_2_cidr   = "10.0.2.0/24"
private_subnet_1_cidr  = "10.0.10.0/24"
private_subnet_2_cidr  = "10.0.11.0/24"
```

### Scale Task Count

Edit `terraform.tfvars`:
```hcl
desired_task_count = 2  # Number of tasks to run
min_task_count     = 2  # Minimum for auto-scaling
max_task_count     = 4  # Maximum for auto-scaling
```

### Change Task Resources

Edit `terraform.tfvars`:
```hcl
task_cpu    = "256"   # CPU units: 256, 512, 1024, 2048
task_memory = "512"   # Memory in MB: 512, 1024, 2048, 4096, etc.
```

Valid CPU/Memory combinations:
- 256 CPU: 512, 1024, 2048 MB
- 512 CPU: 1024-4096 MB (1 GB increments)
- 1024 CPU: 2048-8192 MB (1 GB increments)
- 2048 CPU: 4096-16384 MB (1 GB increments)

### Update Docker Image

```bash
# 1. Build new image
docker build -t fastapi-app:v1.1 -f fastapi1/Dockerfile FastAPI/

# 2. Push to ECR
docker tag fastapi-app:v1.1 <ECR_URL>:v1.1
docker push <ECR_URL>:v1.1

# 3. Update Terraform variable
# Edit terraform.tfvars:
image_tag = "v1.1"

# 4. Apply changes
terraform plan
terraform apply
```

### Enable HTTPS with SSL Certificate

1. Create/import SSL certificate in ACM:
```bash
aws acm request-certificate \
  --domain-name example.com \
  --validation-method DNS \
  --region us-east-1
```

2. Uncomment HTTPS listener in `alb.tf` and update `terraform.tfvars`:
```hcl
ssl_certificate_arn = "arn:aws:acm:us-east-1:123456789:certificate/..."
```

3. Apply changes:
```bash
terraform apply
```

### Monitor Logs

```bash
# Stream real-time logs
aws logs tail /ecs/fastapi --follow --region us-east-1

# View specific time range
aws logs filter-log-events \
  --log-group-name /ecs/fastapi \
  --start-time $(($(date +%s) - 3600))000 \
  --region us-east-1
```

### Monitor Metrics

```bash
# CPU utilization
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --dimensions Name=ServiceName,Value=fastapi-service Name=ClusterName,Value=fastapi-cluster \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average \
  --region us-east-1
```

## Maintenance

### Update Task Definition (new image version)

```bash
# Option 1: Change in Terraform
terraform apply -var="image_tag=v1.1"

# Option 2: Modify terraform.tfvars and apply
terraform apply
```

### Scale Tasks Manually

```bash
# Using AWS CLI
aws ecs update-service \
  --cluster fastapi-cluster \
  --service fastapi-service \
  --desired-count 3 \
  --region us-east-1

# Or modify Terraform
# Edit terraform.tfvars: desired_task_count = 3
terraform apply
```

### View Task Logs

```bash
# List running tasks
aws ecs list-tasks --cluster fastapi-cluster --region us-east-1

# View specific task logs
aws logs get-log-events \
  --log-group-name /ecs/fastapi \
  --log-stream-name ecs/fastapi/<task-id> \
  --region us-east-1
```

## Troubleshooting

### Tasks Not Running

```bash
# Check task status
aws ecs describe-tasks --cluster fastapi-cluster --tasks <task-arn> --region us-east-1

# Check task logs
aws logs tail /ecs/fastapi --follow --region us-east-1

# Common issues:
# - Image not found in ECR: Verify image_tag matches pushed tag
# - Insufficient resources: Check account limits or task CPU/memory
# - Port already in use: Ensure health check is configured correctly
```

### Load Balancer Health Check Failing

```bash
# Check target group health
aws elbv2 describe-target-health \
  --target-group-arn <tg-arn> \
  --region us-east-1

# Verify health check path
# Edit terraform.tfvars:
health_check_path = "/"  # or your custom path

# Ensure your FastAPI app responds to this path
```

### Cannot Access Application

```bash
# Verify ALB exists and is active
aws elbv2 describe-load-balancers --names fastapi-alb --region us-east-1

# Check security group rules
aws ec2 describe-security-groups --region us-east-1 | grep fastapi

# Test connectivity
curl http://<alb-dns>/
```

## Cleanup

To destroy all resources and stop incurring charges:

```bash
terraform destroy
```

This will remove:
- ECS service and tasks
- ECS cluster
- Load balancer
- VPC and all subnets
- Security groups
- IAM roles
- CloudWatch logs (if not in retention period)

## Cost Estimation

Monthly costs depend on:
- **ECS Fargate**: ~$15-30 (2 tasks × 256 CPU × 512 MB)
- **ALB**: ~$20 (with minimal requests)
- **NAT Gateway**: ~$32 (2 NAT gateways)
- **Data Transfer**: Variable

Typical total: **$70-100/month** for development setup

## Advanced Topics

### Add Database

Modify `ecs_task_definition.tf` to add environment variables:
```hcl
environment = [
  {
    name  = "DATABASE_URL"
    value = "postgresql://user:pass@db.example.com/dbname"
  }
]
```

Or use Secrets Manager for sensitive data:
```hcl
secrets = [
  {
    name      = "DATABASE_URL"
    valueFrom = aws_secretsmanager_secret.db_url.arn
  }
]
```

### Add CI/CD Pipeline

Example GitHub Actions:
```yaml
- name: Build and push to ECR
  run: |
    docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
    docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
    
- name: Update ECS service
  run: |
    aws ecs update-service --cluster fastapi-cluster \
      --service fastapi-service --force-new-deployment
```

### Add RDS Database

Create separate RDS Terraform files and reference security group:
```hcl
resource "aws_db_instance" "fastapi_db" {
  # Configuration...
  vpc_security_group_ids = [aws_security_group.ecs_sg.id]
}
```

## Next Steps

1. Test application with load
2. Set up CI/CD pipeline for automatic deployments
3. Add custom domain with Route53
4. Configure CloudWatch alarms
5. Implement backup strategy
6. Set up WAF rules for security

## Support & Documentation

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
