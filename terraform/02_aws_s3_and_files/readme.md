## Terraform
Será utilizado o terraform para provisionar a infraestrutura da AWS.

É inegavél o aumento de visibilidade nos útimos anos do terraform nas comunidades, e vou elencar algumas razões de tê-lo escolhido para este projeto:

1.  *Software livre*
2.  *Plataforma independente*
3.  *Infraestrutura imutável*


### Pré-Requisitos
1.  CLI do terraform
2.  CLI da AWS

Devem estarem instalados e configurados conforme o tutorial inicial.


### Inicio
O objetivo é provisionar os recursos da AWS de maneira rápida, fácil e escalável.
A estrutura organizacional dos arquivos na pasta terraform é sempre tentando reduzir o código do arquivo "main.tf" para deixá-lo mais legível e compreensível, tornando-o de mais fácil manutenção.

## 1 - Recursos Provisionados

|Recursos | Nomes|
|----------|---------|
|random_pet | O recurso random_pet gera nomes de animais de estimação aleatórios que devem ser usados como identificadores exclusivos para outros recursos|
|aws_s3_bucket | Esta funcionalidade é para gerenciar o S3 em uma partição AWS|
|aws_s3_bucket_acl | Fornece um recurso de ACL de bucket do S3|
|aws_s3_bucket_lifecycle_configuration | Fornece um recurso de configuração independente para a configuração do ciclo de vida do bucket do S3|
|aws_s3_bucket_metric | Fornece um recurso de configuração de métricas de bucket do S3|
|aws_s3_bucket_versioning | Fornece um recurso para controlar o controle de versão em um bucket do S3|
|aws_s3_object | Fornece um recurso de objeto S3|

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

## [Extra] Comandos
| comandos  | descrição |
| :------------- |:-------------|
| terraform init     | Inicializa a configuração do Terraform |
| terraform plan     | comando permite visualizar as ações que o Terraform executaria para modificar sua infraestrutura ou salvar um plano especulativo que pode ser aplicado posteriormente |
| terraform destroy     | Destrói a configuração provisionada |
| terraform validate     | Valida sua configuração |
| terraform plan -out="tfplan.out"     | Gera um arquivo .out do resultado executado pelo terraform plan |
| terraform apply "tfplan.out"     | Executa modificações com base no arquivo marcado |
| terraform plan -destroy -out="des.plan"     | Gera um arquivo .plan do resultado executado pelo terraform destroy |
| terraform apply "des.plan"     | Executa modificações de acordo com o arquivo marcado |
