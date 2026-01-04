terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "6.27.0"
    }
  }
}

provider "aws" {
    region = "us-east-1"
}
resource "aws_s3_bucket" "demo_bucket" {
  bucket = "my-first-bucketusing-terraform"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}