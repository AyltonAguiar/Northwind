# Projeto Engenheiro de Dados

## Descrição
O intuito do conteúdo é apresentar, de forma superficial, um conjunto de tecnologias para agregar com as resoluções do módulo de *Projeto Final 1* do curso de [Formação Engenharia de Dados [2022]: Domine Big Data!](https://www.udemy.com/course/engenheiro-de-dados). 

Aqui vamos criar a infraestrutura pelo terraform e adicionar os dados em conjunto. Com os dados armazenados na cloud, estaremos utilizando o python para consumir esses objetos e adicioná-los ao warehouse redshift. A organização dos dados será feita pelo dbt cloud, focando nas querys, tests, jobs e principalmente na documentação. Ao final estaremos permitindo que esses dados tratados possam ser acessados pelo looker studio. Enjoy! ;D

## Documentação

A documentação sobre o projeto encontra-se em [Northwind-Mkdocs](https://ayltonaguiar.github.io/Northwind-Mkdocs/).

## Stack
As seguintes ferramentas e tecnologias serão utilizadas no projeto:

| Tecnologia | Descrição |
| :------------- |:-------------|
| Python  | Linguagem de programação de alto nível |
| Visual Studio Code | Editor de código-fonte desenvolvido pela Microsoft para Windows, Linux e macOS |
| AWS | Plataforma de serviços de computação em nuvem da Amazon.com |
| Terraform | Ferramenta de código aberto para infraestrutura como configuração da HashiCorp |
| Dbt cloud | O dbt Cloud™ é a maneira mais rápida e confiável de implantar o dbt |
| Looker Studio | Ferramenta gratuita para transformar dados em relatórios e painéis informativos personalizados |

### Diagrama: 

![image](https://imgur.com/bv5ET3m.png)

## Pré-Requisitos
Para começar, você precisará:

1. Instalar a [CLI do Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
1. Instalar a [CLI da AWS](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/getting-started-install.html)
1. Criar uma [conta na AWS](https://aws.amazon.com/pt/free)
1. Configurar as [credenciais AWS](https://docs.aws.amazon.com/pt_br/General/latest/gr/aws-sec-cred-types.html)

Deverá ter criado: conta na AWS, as credenciais e configurado a CLI da AWS.

Observação: será utilizado o profile da [CLI AWS](https://docs.aws.amazon.com/cli/latest/reference/configure/index.html) para evitar compartilhamento de chaves de acesso.

## Dúvidas e Sugestões
Caso tenha dúvidas ou deseje fornecer sugestões, entre em contato. Agradecemos o seu feedback!

## Obrigado!