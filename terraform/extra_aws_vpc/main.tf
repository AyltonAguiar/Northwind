# Versão do Terraform
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}


# Acesso - Perfil e região
provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}


# Resources
resource "aws_vpc" "customVpc" {
  cidr_block           = "10.0.0.0/16"
  instance_tenancy     = "default"
  enable_dns_hostnames = true

  tags = var.tags
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.customVpc.id

  tags = var.tags
}

resource "aws_route" "rota_engdados" {
  route_table_id         = aws_vpc.customVpc.default_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_subnet" "pub-a" {
  vpc_id            = aws_vpc.customVpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "${var.tag_subnet}-${"a"}"
  }
}

resource "aws_subnet" "pub-b" {
  vpc_id            = aws_vpc.customVpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "${var.tag_subnet}-${"b"}"
  }
}

resource "aws_security_group_rule" "security_rule" {
  type              = "ingress"
  from_port         = 5439
  to_port           = 5439
  protocol          = "tcp"
  cidr_blocks       = ["177.80.80.78/32"]
  security_group_id = aws_vpc.customVpc.default_security_group_id

}
