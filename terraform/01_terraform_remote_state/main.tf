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

# Requisitando o ID da conta da aws
data "aws_caller_identity" "current" {

}


# Bucket, ACL e Versionamento
resource "aws_s3_bucket" "remote_state" {
  bucket        = "tfstate-${data.aws_caller_identity.current.account_id}"
  force_destroy = true
  tags = {
    Description = "Armazenamento do remote state"
    ManagedBy   = "Terraform"
    Owner       = "Aylton Aguiar"
    CreatedAt   = "2023-01-18"
  }
}

resource "aws_s3_bucket_acl" "remote_state_acl" {
  bucket = aws_s3_bucket.remote_state.id
  acl    = "private"

}

resource "aws_s3_bucket_versioning" "remote_state_versioning" {
  bucket = aws_s3_bucket.remote_state.id
  versioning_configuration {
    status = "Enabled"
  }
}
