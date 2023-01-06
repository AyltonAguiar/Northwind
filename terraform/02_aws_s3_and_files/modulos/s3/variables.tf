# Variáveis comuns
variable "name" {
  type        = string
  description = "Bucket name"
}

variable "acl" {
  type        = string
  description = ""
  default     = "private"
}

variable "policy" {
  type        = string
  description = ""
  default     = null
}

variable "tags" {
  type        = map(string)
  description = ""
  default = {
    name    = "Engdados-project"
    project = "Armazenamento do projeto"
  }

}

variable "files" {
  type    = string
  default = ""
}

variable "key_prefix" {
  type    = string
  default = ""
}
