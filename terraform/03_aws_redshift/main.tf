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


# Resource Random
resource "random_pet" "this" {
  length = 1
  prefix = var.environment
}
resource "random_password" "password" {
  count = 6
  length = 16
  min_upper = 2
  min_lower = 2
  special = true
  numeric = true
  min_numeric = 2
  override_special = "!$%&*()-_=+[]{}<>:?"
}


# Data Sources para setar posteriormente o ID padrão da VPC e do security group
data "aws_vpc" "selected" {
  default = true
}

data "aws_security_group" "security_group_data" {
  vpc_id = data.aws_vpc.selected.id
  filter {
    name   = "group-name"
    values = ["default"]
  }
}

# Resources Redshift - Modelo de Especifícação do Redshift gratuito
resource "aws_redshift_cluster" "cluster_reds" {
  cluster_identifier  = random_pet.this.id
  database_name       = "northwind"
  master_username     = "aylton"
  master_password     = random_password.password[0].result
  port                = 5439
  node_type           = "dc2.large"
  cluster_type        = "single-node"
  publicly_accessible = true
  apply_immediately = true  # Necessário para destroy do cluster quando tiver snapshot
  skip_final_snapshot = true  # Necessário para destroy do cluster quando tiver snapshot
  tags = var.tags
}

# Resources Secrect Manager - reservar as credenciais na AWS
resource "aws_secretsmanager_secret" "rd_secret" {
  description = "Redshift Details"
  name = "rd_secret${random_pet.this.id}"
}

resource "aws_secretsmanager_secret_version" "rd_secret_version" {
  secret_id = aws_secretsmanager_secret.rd_secret.id
  secret_string = jsonencode({
    engine = "redshift"
    data_base = aws_redshift_cluster.cluster_reds.database_name
    username = aws_redshift_cluster.cluster_reds.master_username
    password = aws_redshift_cluster.cluster_reds.master_password
    port = aws_redshift_cluster.cluster_reds.port
    host = aws_redshift_cluster.cluster_reds.endpoint
    dbClusterIdentifier = aws_redshift_cluster.cluster_reds.cluster_identifier
    dbt_prod = "dbt_prod"
    dbt_prod_password = random_password.password[1].result
    dbt_dev = "dbt_dev"
    dbt_dev_password = random_password.password[2].result
    looker_user = "looker"
    looker_password = random_password.password[3].result
  })
}


# Resources Security group rule - Adição de nova regra de entrada para o IP disponibilizado em cidr_blocks
resource "aws_security_group_rule" "security_rule" {
  description       = "Redshift Aylton"
  type              = "ingress"
  from_port         = 5439
  to_port           = 5439
  protocol          = "tcp"
  cidr_blocks       = ["186.216.177.214/32"] # meu IP
  security_group_id = data.aws_security_group.security_group_data.id

}

resource "aws_security_group_rule" "security_rule_dbt" {
  description       = "DBT 52.45"
  type              = "ingress"
  from_port         = 5439
  to_port           = 5439
  protocol          = "tcp"
  cidr_blocks       = ["52.45.144.63/32", "54.81.134.249/32", "52.22.161.231/32"] # IP dbt
  security_group_id = data.aws_security_group.security_group_data.id

}

resource "aws_security_group_rule" "security_rule_lookerstudio" {
  description       = "looker_studio"
  type              = "ingress"
  from_port         = 5439
  to_port           = 5439
  protocol          = "tcp"
  cidr_blocks       = ["142.251.74.0/23", "74.125.0.0/16"] # IP Looker studio
  security_group_id = data.aws_security_group.security_group_data.id

}


# Resources IAM - Função para permissão Redshift e S3
resource "aws_iam_role" "role_redshift" {
  name = "redshift-S3Read"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole"
            ],
            "Principal": {
                "Service": [
                    "redshift.amazonaws.com"
                ]
            }
        }
    ]
}
EOF
}

resource "aws_iam_policy" "policy" {
  name        = "S3ReadOnlyAccess_Redshift"
  description = "Read Only Access S3"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*",
                "s3-object-lambda:Get*",
                "s3-object-lambda:List*"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "s3-redshift-attach" {
  role       = aws_iam_role.role_redshift.name
  policy_arn = aws_iam_policy.policy.arn
}

resource "aws_redshift_cluster_iam_roles" "s3-readonly" {
  cluster_identifier = aws_redshift_cluster.cluster_reds.cluster_identifier
  iam_role_arns      = [aws_iam_role.role_redshift.arn]
}

/*
# Revogar os privilégios e deletar usuário
# exemplo: grupos para o database
resource "aws_redshiftdata_statement" "revoke_users" {
  for_each = local.users_groups
  cluster_identifier = aws_redshift_cluster.cluster_reds.cluster_identifier
  database           = aws_redshift_cluster.cluster_reds.database_name
  db_user            = aws_redshift_cluster.cluster_reds.master_username
  sql                = "revoke ALL PRIVILEGES ON DATABASE ${aws_redshift_cluster.cluster_reds.database_name} from ${each.key}; drop user if exists ${each.key};"
}

*/

# Criação de grupos no redshift
# exemplo: grupos para o database
resource "aws_redshiftdata_statement" "groups_database" {
  for_each = local.groups
  cluster_identifier = aws_redshift_cluster.cluster_reds.cluster_identifier
  database           = aws_redshift_cluster.cluster_reds.database_name
  db_user            = aws_redshift_cluster.cluster_reds.master_username
  sql                = "CREATE GROUP ${each.key};"
  lifecycle {
    ignore_changes = all
  }
   depends_on = [
    aws_redshift_cluster.cluster_reds, aws_redshift_cluster_iam_roles.s3-readonly
  ]
}

# Criação de usuários no redshift
# exemplo: usuários para o database
resource "aws_redshiftdata_statement" "users_database" {
  for_each = local.users_groups
  cluster_identifier = aws_redshift_cluster.cluster_reds.cluster_identifier
  database           = aws_redshift_cluster.cluster_reds.database_name
  db_user            = aws_redshift_cluster.cluster_reds.master_username
  sql                = "create user ${each.key} with password '${random_password.password[each.value].result}';"
  lifecycle {
    ignore_changes = all
  }
   depends_on = [
    aws_redshift_cluster.cluster_reds, aws_redshift_cluster_iam_roles.s3-readonly
  ]
}

# Criação de adição de usuários aos grupos no redshift
# exemplo: looker para bi_users, dbt_dev para dbt_users
resource "aws_redshiftdata_statement" "users_groups_database" {
  for_each = local.groups_category
  cluster_identifier = aws_redshift_cluster.cluster_reds.cluster_identifier
  database           = aws_redshift_cluster.cluster_reds.database_name
  db_user            = aws_redshift_cluster.cluster_reds.master_username
  sql                = "alter group ${each.value} add user ${each.key};"
  lifecycle {
    ignore_changes = all
  }
  depends_on = [
    aws_redshiftdata_statement.groups_database, aws_redshiftdata_statement.users_database
  ]
}
