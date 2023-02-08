#  __Terraform__

[terraform desenvolvimento]: #terraform-desenvolvimento


##  __Provisionando remote state no S3__ {#create_remote_state}

No Script requisitamos o ID da conta AWS utilizando o __profile__ e __region__ para poder criar o bucket com Id único. Adicionamos tags, versionamento e acl private ao provisionamento do bucket S3.

=== ":octicons-file-code-16: `main.tf`"

    ``` yaml
    terraform\01_terraform_remote_state\main.tf
    ```

    [provisiosamento remote state]: #provisiosamento-remote-state

### *Recursos provisionados*

| Recursos do Provedor| Descrição|
|-----|-----|
| `aws_s3_bucket`| Fornece um recurso de bucket do S3|
| `aws_s3_bucket_acl`| Configuração de ACL no bucket|
| `aws_s3_bucket_versioning`| Configuração de versionamento no bucket|

### *Ordem da execução dos comandos* {#order_execute}

Abaixo clique em expandir para visualizar a ordem da execução dos comandos caso necessite. ==A mesma ordem será utilizada nos demais tópicos.==


1.  Inicializando a configuração do Terraform
```
terraform init
```
1.  Validando sua configuração
```
terraform validate
```
1.  Executando um plano de criação
```
terraform plan
```
1.  Após revisar o plano de criação, vamos aplicar e aprovar a execução automaticamente
```
terraform apply -auto-approve
```


##  __Provisionando bucket S3 com arquivos__ {#create_bucket}

Provisionamento do bucket S3 com adição de arquivos em csv e um jpg. É utlizado <b> backend </b> e <b> module </b> no script main.
O S3 contém ciclo de vida, versionamento, ACL e adição de objetos.

=== ":octicons-file-code-16: `main.tf`"

    ``` yaml
    terraform\02_aws_s3_and_files\main.tf
    ```

    [provisiosamento bucket S3]: #provisiosamento-bucket-S3

### *Recursos provisionados*

| Recursos do Provedor| Descrição|
|----------|---------|
| `aws_s3_bucket` | Esta funcionalidade é para gerenciar o S3 em uma<br> partição AWS|
| `aws_s3_bucket_acl` | Fornece um recurso de ACL de bucket do S3|
| `aws_s3_bucket_lifecycle_configuration` | Fornece um recurso de configuração independente para a configuração do ciclo de vida do bucket do S3|
| ~~`aws_s3_bucket_metric`~~ | ~~Fornece um recurso de configuração de métricas de bucket do S3~~|
| `aws_s3_bucket_versioning` | Fornece um recurso para controlar o controle de versão em um bucket do S3|
| `aws_s3_object` | Fornece um recurso de objeto S3|

| Recursos Terraform| Descrição|
|:----------|:---------|
| `random_pet` | Gera nomes de animais aleatórios que podem ser<br> usados como identificadores exclusivos para outros recursos|

### *Ordem da execução dos comandos*

[Clique aqui para ir na ordem dos comandos](#order_execute)


##  __Provisionando Redshift e outros recursos necessários.__ {#create_cluster_redshift}

O script possui a criação do cluster Redshift, criação de usuários e grupos para Redshift, adição de role e policy, criação de secrets manager com adição de informações criadas no processo para não utilizar as senhas diretamente no código, adição de IP'S para acesso aos recursos provisionados.

<mark>Pontuarei apenas algumas partes que precisam de modificações:</mark>

=== ":octicons-file-code-16: `main.tf`"

    ``` yaml
    terraform\03_terraform_remote_state\main.tf
    ```

    [Provisionando Redshift]: #provisionando-redshift

### __*Criação Cluster Redshift*__

Esse cluster atende as caracteristicas do modelo free tier, caso esteja dentro do prazo.
Pode-se modificar `master_username` e `database_name`.

``` json
resource "aws_redshift_cluster" "cluster_reds" 
{
  cluster_identifier  = random_pet.this.id
  database_name       = "northwind"
  master_username     = "aylton"
  master_password     = random_password.password[0].result
  port                = 5439
  node_type           = "dc2.large"
  cluster_type        = "single-node"
  publicly_accessible = true
  apply_immediately = true  # Necessário para destroy do cluster quando tiver snapshot
  skip_final_snapshot = true  # Necessário para destroy do cluster quando tiver snapshot
  tags = var.tags
}
```

### __*Adição de entrada CIDR*__ {#adição-de-entrada-cidr}

Foram criadas 3 adições de CIDR: Meu IP, Entrada para o dbt e Entrada do Looker Studio. E
Faça alteração para seu IP, sem ele você não conseguirá realizar operações futuras.
Pode-se modificar `description` e `cidr_blocks`.

=== ":octicons-code-24: `"security_rule"`"

    ``` json
    resource "aws_security_group_rule" "security_rule"
    {
    description       = "Redshift Aylton"
    type              = "ingress"
    from_port         = 5439
    to_port           = 5439
    protocol          = "tcp"
    cidr_blocks       = ["${chomp(data.http.meu_ip.response_body)}/32"] # meu IP
    security_group_id = data.aws_security_group.security_group_data.id
    }
    ```

=== ":octicons-code-24: `"security_rule_dbt"`"

    ``` json
    resource "aws_security_group_rule" "security_rule_dbt"
    {
      description       = "DBT 52.45"
      type              = "ingress"
      from_port         = 5439
      to_port           = 5439
      protocol          = "tcp"
      cidr_blocks       = ["52.45.144.63/32", "54.81.134.249/32", "52.22.161.231/32"] # IP dbt
      security_group_id = data.aws_security_group.security_group_data.id
    }
    ```

=== ":octicons-code-24: `"security_rule_lookerstudio"`"

    ``` json
    resource "aws_security_group_rule" "security_rule_lookerstudio"
    {
      description       = "looker_studio"
      type              = "ingress"
      from_port         = 5439
      to_port           = 5439
      protocol          = "tcp"
      cidr_blocks       = ["142.251.74.0/23", "74.125.0.0/16"] # IP Looker studio
      security_group_id = data.aws_security_group.security_group_data.id
    }
    ```

!!! tip "Adicionado dado de captura automática ip"
    
    ``` json
    data "http" "meu_ip" {
      url = "https://ipv4.icanhazip.com"
    }
    ```
    Agora toda vez que seu Ip mudar, você não precisa mais alterar manualmente o número do IP. 
    Basta usar o `terraform plan` para verificar as mudanças e `terraform apply -auto-approve` para aplicá-las.

### __*Criação de usuários, grupos e adição de usuário ao grupo*__ {#criação-de-usuários-grupos-e-adição-de-usuário-ao-grupo}

!!! Bug "Recurso Removido"
    
    Os recursos específicos para este tópico estavam gerando instabilidades no terraform,
     então a criação dos usuários, grupos e adição de usuários ao grupos foram movidos para o `python` no tópico [Criação de usuários, grupos e vinculos](python.md#criar-usuarios-grupos-vinculos-python)

### __*Salvando usuários e senhas no Secret Manager*__ {#salvando-usuários-e-senhas-no-secret-manager}

Um recurso muito importante quando trata-se de guardar dados mais sensíveis, principalmente quando estamos gerando senhas e logins como é caso desse pequeno projeto. O script vai guardar os logins e senhas referente ao Redshift, além de outras informações para serem utilizadas no python futuramente.

``` json
resource "aws_secretsmanager_secret_version" "rd_secret_version"
{
  secret_id = aws_secretsmanager_secret.rd_secret.id
  secret_string = jsonencode({
    engine = "redshift"
    data_base = aws_redshift_cluster.cluster_reds.database_name
    username = aws_redshift_cluster.cluster_reds.master_username
    password = aws_redshift_cluster.cluster_reds.master_password
    port = aws_redshift_cluster.cluster_reds.port
    host = aws_redshift_cluster.cluster_reds.endpoint
    dbClusterIdentifier = aws_redshift_cluster.cluster_reds.cluster_identifier
    dbt_prod = "dbt_prod"
    dbt_prod_password = random_password.password[1].result
    dbt_dev = "dbt_dev"
    dbt_dev_password = random_password.password[2].result
    looker_user = "looker"
    looker_password = random_password.password[3].result
  })
}
```

### *Recursos provisionados*

| Recursos do Provedor| Descrição|
|----------|---------|
| `aws_iam_policy` | Fornece uma política IAM|
| `aws_iam_role` | Fornece uma função IAM |
| `aws_iam_role_policy_attachment` | Anexa uma política IAM gerenciada a uma função IAM|
| `aws_redshift_cluster` | Fornece um recurso de cluster do Redshift|
| `aws_redshift_cluster_iam_roles` | Fornece um recurso de funções IAM do cluster do Redshift|
| `aws_secretsmanager_secret` | Fornece um recurso para gerenciar metadados secretos do AWS Secrets Manager|
| `aws_secretsmanager_secret_version` | Fornece um recurso para gerenciar a versão secreta<br> do AWS Secrets Manager, incluindo seu valor secreto|
| `aws_security_group_rule` | Fornece um recurso de regra de grupo de segurança.<br> Representa uma única regra de grupo de entrada ou saída, que pode ser adicionada a grupos de segurança externos|

| Recursos do Terraform| Descrição|
|--------|--------|
| `random_password` | Idêntico a random_string com a exceção de que o resultado<br> é tratado como confidencial e, portanto, não é exibido na saída do console|
| `random_pet` | O recurso random_pet gera nomes de animais de estimação aleatórios que devem ser usados como identificadores exclusivos para outros recursos|

### *Ordem da execução dos comandos*

[Clique aqui para ir na ordem dos comandos](#order_execute)


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

## :material-format-list-checks: Check Objetivos

Os ícones :octicons-check-circle-fill-24:{ style="color: #00e676" } são os finalizados e os :octicons-check-circle-fill-24:{ style="color: var(--md-default-fg-color--lightest)" } são os em abertos.

- [x] [Criação de um remote state](#create_remote_state)
- [x] [Criação de um bucket S3](#create_bucket)
- [x] [Criação de um cluster Redshift](#create_cluster_redshift)
  1.  - [x] [Adição de entradas cidr](#adição-de-entrada-cidr)
  2.  - [x] [Criando grupos e usuários](#criação-de-usuários-grupos-e-adição-de-usuário-ao-grupo)
  3.  - [x] [Salvando dados sensíveis no Secrets Manager](#salvando-usuários-e-senhas-no-secret-manager)

