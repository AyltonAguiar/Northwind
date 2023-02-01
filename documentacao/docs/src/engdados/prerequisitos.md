---
title: Pré-requisitos
---

## __Objetivo__

Necessários para prosseguir na construção do projeto. Cada tópico dos pré-requisitos possuem links com os tutoriais de instalações para auxiliar caso não possua.


### __Contas__

São os principais para conseguir avançar no projeto, seja para provisionamento na AWS ou na criação das visualizações, tabelas no DBT.

|Atalhos|Descrição|
|:---|:----:|
|<a href="https://aws.amazon.com/pt/free" target="_blank"> Criar conta gratuita da AWS</a>| Site da AWS|
|<a href="https://www.getdbt.com/signup/" target="_blank"> Criar conta gratuita do Dbt</a>| Site do Dbt|


### __CLI Terraform__

Abaixo o tutorial de instalação disponibilizado pela Hashicorp. Necessário para que possamos trabalhar com terraform na nossa máquina.

|Atalhos|Descrição|
|:---|:----:|
|<a href="https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli" target="_blank"> Tutorial de instalação CLI Terraform</a>| CLI Terraform|


### __CLI Aws__ {#requisito-aws-cli}

<mark> Não faz parte das boas práticas a geração de uma chave de acesso na conta raiz </mark>. Entendido isso, vamos aos links abaixo:

[CLI Aws]: #requisito-aws-cli

|Atalhos|Descrição|
|-----|---------|
|<a href="https://docs.aws.amazon.com/pt_br/cli/latest/userguide/getting-started-install.html" target="_blank"> Tutorial de instalação CLI AWS </a>| CLI AWS|
|<a href="https://docs.aws.amazon.com/accounts/latest/reference/root-user-access-key.html" target="_blank"> Criar e excluir chave de acesso </a>| AWS Key Access|


<strong>Observação:</strong> Será utilizado o profile da cli aws, e o motivo desse é para evitar qualquer tipo de compartilhamento das suas chaves de acesso.

|Atalhos|Descrição|
|-----|---------|
|<a href="https://docs.aws.amazon.com/cli/latest/reference/configure/index.html" target="_blank"> Configurando profile da cli aws </a>| AWS CLI Command Reference |

### __Python__ {#tutorial-python}

Abaixo guia oficial de instalação e link de download

|Atalhos|Descrição|
|-----|---------|
|<a href="https://wiki.python.org/moin/BeginnersGuide/Download" target="_blank"> Tutorial de instalação Python </a>| Site Python.org|
|<a href="https://www.python.org/downloads/" target="_blank"> Página de Download Python </a>| Site Python.org, Lista para download |

Abaixo Tutoriais de instalação:

|Streaming|Descrição|Autor|OS|
|---|---|----|-----|
| <a href="https://www.youtube.com/watch?v=XQwHJc1uO_g" target="_blank"> <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"> </a> | <a href="https://www.youtube.com/watch?v=XQwHJc1uO_g" target="_blank"> Tutorial Python + Visual Studio Code </a>|<a href="https://www.youtube.com/@OtavioMiranda" target="_blank"> Otávio Miranda </a>| Windows |

[Tutorial python]:(#tutorial-python)

## __Guidelines do projeto__

- [Arquitetura do Projeto](./arquitetura/arquitetura.md)

