# Variáveis de acesso
variable "aws_profile" {
  type        = string
  description = ""
  default     = "ayltonaguiar"

}

variable "aws_region" {
  type        = string
  description = ""
  default     = "us-east-1"
}


# Nome do Bucket
variable "environment" {
  type        = string
  description = ""
  default     = "engenharia-dados"
}