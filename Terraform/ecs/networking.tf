# VPC
resource "aws_vpc" "fastapi_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.app_name}-vpc"
  }
}

# Public Subnets
resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = aws_vpc.fastapi_vpc.id
  cidr_block              = var.public_subnet_1_cidr
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.app_name}-public-subnet-1"
  }
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id                  = aws_vpc.fastapi_vpc.id
  cidr_block              = var.public_subnet_2_cidr
  availability_zone       = data.aws_availability_zones.available.names[1]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.app_name}-public-subnet-2"
  }
}

# Private Subnets
resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.fastapi_vpc.id
  cidr_block        = var.private_subnet_1_cidr
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.app_name}-private-subnet-1"
  }
}

resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.fastapi_vpc.id
  cidr_block        = var.private_subnet_2_cidr
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "${var.app_name}-private-subnet-2"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "fastapi_igw" {
  vpc_id = aws_vpc.fastapi_vpc.id

  tags = {
    Name = "${var.app_name}-igw"
  }
}

# Elastic IPs for NAT Gateways
resource "aws_eip" "nat_eip_1" {
  domain = "vpc"
  depends_on = [aws_internet_gateway.fastapi_igw]

  tags = {
    Name = "${var.app_name}-nat-eip-1"
  }
}

# NAT Gateways
resource "aws_nat_gateway" "nat_gateway_1" {
  allocation_id = aws_eip.nat_eip_1.id
  subnet_id     = aws_subnet.public_subnet_1.id
  depends_on    = [aws_internet_gateway.fastapi_igw]

  tags = {
    Name = "${var.app_name}-nat-gateway-1"
  }
}

# Public Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.fastapi_vpc.id

  route {
    cidr_block      = "0.0.0.0/0"
    gateway_id      = aws_internet_gateway.fastapi_igw.id
  }

  tags = {
    Name = "${var.app_name}-public-rt"
  }
}

# Private Route Table
resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.fastapi_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway_1.id
  }

  tags = {
    Name = "${var.app_name}-private-rt"
  }
}

# Route Table Associations
resource "aws_route_table_association" "public_subnet_1_assoc" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_subnet_2_assoc" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "private_subnet_1_assoc" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_route_table_association" "private_subnet_2_assoc" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_rt.id
}

# Data source for availability zones
data "aws_availability_zones" "available" {
  state = "available"
}
