# Outputs
output "vpc" {
  value = aws_vpc.customVpc.id
}

output "internet_gateway" {
  value = aws_internet_gateway.igw.id
}

output "route" {
  value = aws_route.rota_engdados.route_table_id
}

output "subnets" {
  value = [aws_subnet.pub-a.id, aws_subnet.pub-b.id]
}

output "security_group" {
  value = aws_vpc.customVpc.default_security_group_id
}