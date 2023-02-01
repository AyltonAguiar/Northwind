# Instruções
## 1 - Recursos

|Recursos | descrição|
|----------|---------|
|aws_iam_policy | Fornece uma política IAM|
|aws_iam_role | Fornece uma função IAM |
|aws_iam_role_policy_attachment | Anexa uma política IAM gerenciada a uma função IAM |
|aws_redshift_cluster |Fornece um recurso de cluster do Redshift|
|aws_redshift_cluster_iam_roles |Fornece um recurso de funções IAM do cluster do Redshift|
|aws_secretsmanager_secret |Fornece um recurso para gerenciar metadados secretos do AWS Secrets Manager|
|aws_secretsmanager_secret_version |Fornece um recurso para gerenciar a versão secreta do AWS Secrets Manager, incluindo seu valor secreto|
|aws_security_group_rule |Fornece um recurso de regra de grupo de segurança. Representa uma única regra de grupo de entrada ou saída, que pode ser adicionada a grupos de segurança externos|
|random_password |Idêntico a random_string com a exceção de que o resultado é tratado como confidencial e, portanto, não é exibido na saída do console|
|random_pet |O recurso random_pet gera nomes de animais de estimação aleatórios que devem ser usados como identificadores exclusivos para outros recursos|

## 1.1 - Variáveis

No main.tf existe o recurso *aws_security_group_rule* que possui o IP, é de extrema importancia fazer a alteração para seu IP externo para que possa utilizar os recursos.

```
resource "aws_security_group_rule" "security_rule" {
  description       = "Redshift Aylton"
  type              = "ingress"
  from_port         = 5439
  to_port           = 5439
  protocol          = "tcp"
  cidr_blocks       = ["xxx.xx.xx.xx/xx"] # MEU IP
  security_group_id = data.aws_security_group.security_group_data.id

}
```

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
