## __Objetivo__

Descrever o conjunto de tecnologias (stack) utilizadas no mini-projeto.

Os elementos do conjunto são:

```
1. AWS
2. Python
3. Terraform
4. dbt Cloud
5. Looker Studio
```


## __Diagrama__

[ ![diagrama](../../../assets/diagrama/diagrama.png) ](../../../assets/diagrama/diagrama.png){ target="_blank"}


## __Tecnologias Utilizadas__

| Linguagens, ferramentas, etc| Descrição |
| :------------- |:-------------|
|Python  | Linguagem de programação de alto nível|
|AWS  | Plataforma de serviços de computação em nuvem, que formam uma plataforma de computação na nuvem oferecida pela Amazon.com|
|Terraform  |  Ferramenta de software de código aberto, infraestrutura como configuração, criada pela HashiCorp|
|dbt Cloud | O dbt Cloud™ é a maneira mais rápida e confiável de implantar o dbt. Desenvolva, teste, programe e investigue modelos de dados, tudo em uma interface do usuário baseada na web.|
|Looker Studio  | Ferramenta gratuita que transforma seus dados em relatórios e painéis informativos totalmente personalizáveis, fáceis de ler e de compartilhar|

## __Estruturas__

Sobre as estruturas e códigos que existem no projeto.

### *Terraform*

```bash
📂Terraform
┣ 📂01_terraform_remote_state # (1)
┃ ┣ 📜main.tf
┃ ┣ 📜outputs.tf
┃ ┗ 📜variables.tf
┣ 📂02_aws_s3_and_files 
┃ ┣ 📂clientes # (2)
┃ ┃ ┣ 📂cliente1
┃ ┃ ┃ ┣ 📜file1.csv
┃ ┃ ┃ ┗ 📜file2.csv
┃ ┃ ┣ 📂cliente2
┃ ┃ ┗ 📂cliente3
┃ ┣ 📂modulos # (3)
┃ ┃ ┣ 📂s3
┃ ┃ ┃ ┣ 📂object
┃ ┃ ┃ ┃ ┣ 📜main.tf
┃ ┃ ┃ ┃ ┣ 📜outputs.tf
┃ ┃ ┃ ┃ ┗ 📜variables.tf
┃ ┃ ┃ ┣ 📜main.tf
┃ ┃ ┃ ┣ 📜outputs.tf
┃ ┃ ┃ ┗ 📜variables.tf
┃ ┣ 📜main.tf
┃ ┣ 📜outputs.tf
┃ ┗ 📜variables.tf
┣ 📂03_aws_redshift
┃ ┣ 📜locals.tf # (4)
┃ ┣ 📜main.tf
┃ ┣ 📜outputs.tf
┃ ┗ 📜variables.tf
┗ 📜.gitignore 
```

1. Normalmente a pasta do terraform terá: `main.tf`, `outputs.tf`, `variables.tf`.
2. Arquivos que serão adicionados ao bucket durante a criação
3. Módulos, estão com os recursos e 'subrecursos'.
4. Um exemplar de `locals.tf` adicionado para guardar nomes dos usuários, grupos e vínculo entre eles. Referente ao banco de dados Redshift.

### *Python*

Uma visão do Python.

```bash
📂Python
┣ 📂engdados # (1)
┃ ┣ 📜mod_aws.py
┃ ┣ 📜mod_terraform.py
┃ ┗ 📜s3_redshift_load_files.py
┣ 📂scripts # (2)
┣ 📂testes # (3)
┃ ┗ 📜s3_to_redshift.py
┣ 📜.gitignore
┗ 📜requirements.txt
```

1. Armazena os scripts principais.
2. Ainda em construção
3. Contém script alternativo. Inciado, mas não finalizado.

### *dbt*

Uma visão do dbt, parcialmente.

```bash
📂dbt
┣ 📂analyses
┃ ┗ 📜.gitkeep
┣ 📂macros
┣ 📂models # (1)
┃ ┣ 📂mart 
┃ ┃ ┣ 📂core # (4)
┃ ┃ ┃ ┣ 📂renner
┃ ┃ ┃ ┃ ┗ 📜fct_renner_orders.sql
┃ ┃ ┗ 📂venda # (5)
┃ ┃ ┃ ┗ 📜fct_renner_orders.sql
┃ ┗ 📂staging # (3)
┃ ┃ ┗ 📂northwind
┃ ┃ ┃ ┣ 📂c&a
┃ ┃ ┃ ┃ ┗ 📜stg_c&a_customers.sql
┃ ┃ ┃ ┗ 📂renner
┃ ┃ ┃ ┃ ┣ 📜src_renner.yml
┃ ┃ ┃ ┃ ┗ 📜stg_renner_customers.sql
┣ 📂seeds
┣ 📂snapshots
┣ 📂testes # (2)
┃ ┗ 📜renner_orderdetails_vendas_positivas.sql
┣ 📜.gitignore
┣ 📜dbt_project.yml
┗ 📜packages.yml
```

1. Contém scripts de dimensões, fatos, configurações das fontes, etc.
2. Contém scripts para realizar testes singulares.
3. Scripts de configurações de fontes: staging, source, etc.
4. Scripts de dimensões, fatos e intermediários.
5. Scripts do setor de Venda.