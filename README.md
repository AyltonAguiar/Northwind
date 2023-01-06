# Projeto Engenheiro de Dados

## Descrição
O intuito do conteúdo é apresentar, de forma superficial, um cenário para agregar com as resoluções do módulo de *Projeto Final 1* e *Projeto Final 2* do curso de [Formação Engenharia de Dados [2022]: Domine Big Data!](https://www.udemy.com/course/engenheiro-de-dados). 


## Índice
1.  Cenário
1.  Pré-Requisitos
1.  Preparação do ambiente
1.  Projeto Final 1
1.  Projeto Final 2
1.  Considerações Finais

## 1.   Cenário

Fazemos parte de uma equipe de dados da empresa **_comic levels_**.
Nosso setor precisa receber/pegar dados dos clientes e trabalhar neles, portanto fizemos um levantamento do que utilizaremos.

### 1.1 Stack 

| Linguagens, ferramentas, etc| Descrição |
| :------------- |:-------------|
|Python  | Linguagem de programação de alto nível|
|Visual Studio Code  | Editor de código-fonte desenvolvido pela Microsoft para Windows, Linux e macOS |
|AWS  | Plataforma de serviços de computação em nuvem, que formam uma plataforma de computação na nuvem oferecida pela Amazon.com|
|Terraform  |  Ferramenta de software de código aberto, infraestrutura como configuração, criada pela HashiCorp|
|Dbt  | Ferramenta de linha de comando de código aberto que ajuda analistas e engenheiros a transformar dados em seu warehouse com mais eficiência|
|Looker Studio  | Ferramenta gratuita que transforma seus dados em relatórios e painéis informativos totalmente personalizáveis, fáceis de ler e de compartilhar|

### 1.2 Diagrama
Reservamos 3 espaços para os times:
* __*Engenharia de Dados*__, responsável pelo provisionamento da infraestrutura, extração e carregamento dos dados.

* __*Engenharia Analítica*__, responsável pelos testes, transformações, implantações e documentação dos dados.

* __*Análise de Dados*__, responsável pela análise dos dados tratados.

###### Diagrama: 

![image](https://imgur.com/YZrcGbn.png)


## 2.   Pré-Requisitos (links com os tutoriais de instalação)
1.	[CLI do Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
1.	[CLI da AWS](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/getting-started-install.html)
1.	[Conta da AWS](https://aws.amazon.com/pt/free)
1.	[Credenciais AWS](https://docs.aws.amazon.com/pt_br/general/latest/gr/aws-sec-cred-types.html)

Deverá ter criado: conta na AWS, as credenciais e configurado a CLI da AWS.

Observação: Será utilizado o profile da [cli aws](https://docs.aws.amazon.com/cli/latest/reference/configure/index.html), e o motivo desse é para evitar qualquer tipo de compartilhamento das suas chaves de acesso.


## 3. Preparação do ambiente

1.  Criação de Cluster
1.  Criação do Banco de dados Northwind
1.  Criação da estrutura do Banco de dados
1.  Criação de Credenciais - AWS
1.  Carregamento de dados (csv) para Bucket
1.  Execução de copy para carregamento de dados


## Área de Dados





### Exibição dos Dados
1.	Looker Studio - Utilizada para transformar os dados em relatórios e painéis (antigo Data Studio)


Infraestrutura > [ Extração dos dados > Carregamento dos dados > transformação dos dados ] > Exibição dos dados


dito isto, vamos ao início do projetinho de engenharia de dados. yhuuuulll ;)


## Atividade

1.	Problemática: Cliente deseja saber se existe um número grande de vendas com valores abaixo do preço tabelar.
	Adicionais: Quantidade das vendas ordenado pela diferença.
