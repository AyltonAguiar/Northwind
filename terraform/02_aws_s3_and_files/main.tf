terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"

  backend "s3" {
    bucket  = "tfstate-531446036269" # ATENÇÃO: MODIFICAR PARA O SEU REMOTE STATE BUCKET GERADO
    key     = "engdados/terraform_remote_state/terraform.tfstate"
    region  = "us-east-1"
    profile = "ayltonaguiar"
  }

}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

resource "random_pet" "this" {
  length = 2
  prefix = var.environment
}

module "bucket" {
  source = "./modulos/s3"
  name   = random_pet.this.id
  # files = "${path.root}/csv"
  files = "./clientes"
}
