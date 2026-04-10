# Postgres docker start command
- docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres:16-alpine

# pgadminer for browser use of postgresql
host.docker.internal
System	 :PostgreSQL
Server	:host.docker.internal
Username	:postgres
Password	:mysecretpassword
Database	:postgres


# docker compose


# docker build command 
docker build -t fastapi-app:latest .

- Note: update AWS_ACCOUNT_ID with your aws_registry_id
# add Tag for AWS ECR
docker tag fastapi-app:latest AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/fastapi-app:latest

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Push to ECR
docker push AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/fastapi-app:latest