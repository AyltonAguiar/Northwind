resource "aws_s3_bucket" "this" {
  bucket = var.name
  policy = var.policy
  tags   = var.tags
  force_destroy = true

}

resource "aws_s3_bucket_acl" "this" {
  bucket = aws_s3_bucket.this.id
  acl    = "private"
}

# Recurso de cilo de vida dos objetos no bucket
resource "aws_s3_bucket_lifecycle_configuration" "this" {
  bucket = aws_s3_bucket.this.id
  rule {
    id     = "regra-1"
    status = "Enabled"
    expiration {
      days = 90
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 60
      storage_class = "GLACIER"
    }
  }
}

# Recurso de versionamento dos arquivos
resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Módulo de Leitura dos arquivos para adição no s3
module "objects" {
  source = "./object"

  for_each = var.files != "" ? fileset(var.files, "**") : []

  bucket = aws_s3_bucket.this.bucket
  key    = "${var.key_prefix}/${each.value}"
  src    = "${var.files}/${each.value}"
}