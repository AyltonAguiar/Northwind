# Projeto Engenheiro de Dados


## Descrição
O intuito do conteúdo é apresentar, de forma superficial, um conjunto de tecnologias para agregar com as resoluções do módulo de *Projeto Final 1* do curso de [Formação Engenharia de Dados [2022]: Domine Big Data!](https://www.udemy.com/course/engenheiro-de-dados). 

Aqui vamos criar a infraestrutura pelo terraform e adicionar os dados em conjunto. Com os dados armazenados na cloud, estaremos utilizando o python para consumir esses objetos e adicioná-los ao warehouse redshift. A organização dos dados será feita pelo dbt cloud, focando nas querys, tests, jobs e principalmente na documentação. Ao final estaremos permitindo que esses dados tratados possam ser acessados pelo looker studio. Enjoy! ;D

## Documentação

A documentação sobre o projeto encontra-se em [Northwind-Mkdocs](https://ayltonaguiar.github.io/Northwind-Mkdocs/).


## Stack 

| Linguagens, ferramentas, etc| Descrição |
| :------------- |:-------------|
|Python  | Linguagem de programação de alto nível|
|Visual Studio Code  | Editor de código-fonte desenvolvido pela Microsoft para Windows, Linux e macOS |
|AWS  | Plataforma de serviços de computação em nuvem, que formam uma plataforma de computação na nuvem oferecida pela Amazon.com|
|Terraform  |  Ferramenta de software de código aberto, infraestrutura como configuração, criada pela HashiCorp|
|Dbt  | Ferramenta de linha de comando de código aberto que ajuda analistas e engenheiros a transformar dados em seu warehouse com mais eficiência|
|Looker Studio  | Ferramenta gratuita que transforma seus dados em relatórios e painéis informativos totalmente personalizáveis, fáceis de ler e de compartilhar|

### Diagrama: 

![image](https://imgur.com/bv5ET3m.png)


## Pré-Requisitos (links com os tutoriais de instalação)
1.	[CLI do Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
1.	[CLI da AWS](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/getting-started-install.html)
1.	[Conta da AWS](https://aws.amazon.com/pt/free)
1.	[Credenciais AWS](https://docs.aws.amazon.com/pt_br/general/latest/gr/aws-sec-cred-types.html)

Deverá ter criado: conta na AWS, as credenciais e configurado a CLI da AWS.

Observação: Será utilizado o profile da [cli aws](https://docs.aws.amazon.com/cli/latest/reference/configure/index.html), e o motivo desse é para evitar qualquer tipo de compartilhamento das suas chaves de acesso.


## Dúvidas e Sugestões

Alguma dúvida ou quer dar alguma sugestão?

Entre em contato que estarei agradecendo pelo feedback!


## Obrigado Galera!

