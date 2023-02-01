# __Escopo__ {#escopo-do-projeto}

[Escopo do Projeto]:(#escopo-do-projeto)

## __Terraform para Provisionamento de uma infraestrutura cloud por código__.
1.  Criar um exemplo de estado remoto (Remote state) do terraform na Amazon S3 (para compartilhar o projeto).
2.  Criar um bucket (balde) na Amazom S3 juntamente com os arquivos csv's (exemplo de código hcl com módulo).
    1.  Criar regras de ciclo de vida para os dados armazenados.
    2.  Criar regras de controle de acesso ao bucket, básico.
    3.  Criar versionamento no bucket.
3.  Criar um Banco de dados (Redshift).
    1.  Vincular ao VPC padrão.
    2.  Vincular ao grupo de segurança padrão.
3.  Criar Grupos e usuários do Banco de dados e armazenar dados no Secrets Manager.
    1.  Grupos: dbt_users, loaders_users, bi_users.
    2.  Usuários: dbt_prod, dbt_dev, looker, airbyte.
4. Criar regras de entrada ao grupo de segurança.
5. Criar função para permissão entre Redshift e S3.
## __Python para trabalhar com os csv's, arquivos do terraform e com o Redshift__.
1.  Pegar dados dos arquivos terraform.tfstate.
2.  Pegar os arquivos csv's armazenados na amazom S3.
3.  Pegar dados armazenados no Secrets Manager.
4.  Criar esquemas, tabelas e gerar copys com base nos arquivos csv's e bucket.
5.  Dar permissão aos usuários de grupos específicos sobre esquemas criados.
## __Data build tools cloud (dbt cloud) para transformação dos dados e organização das querys__.
1. Organização da estrutura.
    1. Models, Tests, Packages.
        1. src, fct, dim, stg.
2. Tratamento de dados.
    1. Tratamento de duplicados direto numa query de staging (exemplo "stg_c&a_customers")
    2. Criação de tabelas fatos ("fct_c&a_orderdeatails")
    3. Criação de tabelas dimensões ("dim_c&a")
3. Testes
    1. Testes genéricos ("stg_renner_shippers")
    2. Testes singulares ("renner_orderdetails_vendas_positivas")
4. Packages
    1. dbt_utils
    2. codegen
5. Jobs
    1. Criação de job
    2. Integração com Slack e e-mail
6. Documentação sobre as querys
    1. Utilização de docs
## __Looker Studio como construtor das dashboards__.
1. Conexão com o Redshift
## __Extras__.
1. Extensões para Visual Code Studio
    1.  Infracost
    2.  AWS boto3
    3.  GitLens
    4.  HashiCorp Terraform
    5.  Python
    6.  Markdown All in One

