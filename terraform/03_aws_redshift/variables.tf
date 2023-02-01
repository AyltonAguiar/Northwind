variable "aws_profile" {
  type    = string
  default = "ayltonaguiar"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type        = string
  description = ""
  default     = "engdados-tf"
}

variable "tags" {
  type        = map(string)
  description = ""
  default = {
    name    = "Engdados-project"
    project = "Engenharia de dados"
  }

}

variable "meu_ip" {
  default = ""
}