terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "mj_free_tier_demo" {
  ami = "ami-0720c0a2e1e125edd"
    instance_type = "t4g.small"
     tags = {
       Name="demo"
       Environment="dev"
     }
}