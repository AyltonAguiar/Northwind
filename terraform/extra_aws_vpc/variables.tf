variable "aws_profile" {
  type    = string
  default = "ayltonaguiar"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "tags" {
  type        = map(string)
  description = ""
  default = {
    name    = "Engdados-project"
    project = "Engenharia de dados"
  }

}

variable "environment" {
  type    = string
  default = "engdados-project"
}

variable "tag_subnet" {
  type    = string
  default = "engdados-sub"
}
