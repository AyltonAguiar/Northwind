# Instruções
## 1 - Recursos Provisionados

|Recursos | Nomes|
|----------|---------|
|aws_s3_bucket | remote_state|
|aws_s3_bucket_acl | remote_state_acl|
|aws_s3_bucket_versioning | remote_state_versioning|

## 2 - Ordem da execução dos comandos

1.  Inicializando a configuração do Terraform
```
terraform init
```
2.  Validando sua configuração
```
terraform validate
```
3.  Executando um plano de criação
```
terraform plan
```
4.  após revisar o plano de criação, vamos aplicar e aprovar a execução automaticamente
```
terraform apply -auto-approve
```

###### No final teremos o retorno do output:
```
Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

Outputs:

remote_state_bucket = "tfstate-531446036212"
remote_state_bucket_arn = "arn:aws:s3:::tfstate-531446036212"
```


## [Extra] Comandos

|Comandos | Nomes|
|----------|---------|
|terraform init | Inicializa a configuração do Terraform|
|terraform validate | Valida sua configuração|
|terraform plan | comando permite visualizar as ações que o Terraform executaria para modificar sua infraestrutura ou salvar um plano especulativo que pode ser aplicado posteriormente|
|terraform apply -auto-approve | executará todas as funções do plano e dará aprovação para fazer as alterações|
