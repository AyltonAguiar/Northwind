# Outputs
output "cluster_identifier" {
  value = aws_redshift_cluster.cluster_reds.cluster_identifier
}

output "cluster_host" {
  value = aws_redshift_cluster.cluster_reds.endpoint
}

output "cluster_arn" {
  value = aws_redshift_cluster.cluster_reds.arn
}

output "cluster_security_group" {
  value = aws_redshift_cluster.cluster_reds.vpc_security_group_ids
}

output "cluster_type" {
  value = aws_redshift_cluster.cluster_reds.cluster_type
}

output "vpc" {
  value = data.aws_vpc.selected.id
}

output "iam_role_arn" {
  value = aws_iam_role.role_redshift.arn
}

# Dados essenciais

output "region_name" {
  value = var.aws_region
}

output "secrete_name" {
  value = aws_secretsmanager_secret.rd_secret.name
}

output "meu_ip" {
  value = ["${chomp(data.http.meu_ip.response_body)}/32"]
}