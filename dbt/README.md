## Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test

## Apresentação

Aqui será realizado toda a parte de organização e criação das querys utilizando as boas práticas presentes nas aulas disponibilizadas pelo próprio dbt.

## Convenções de nomenclatura 
Ao trabalhar neste projeto, estabelecemos algumas convenções para nomear nossos modelos.

* Fontes (src) referem-se aos dados brutos da tabela que foram construídos no warehouse por meio de um processo de carregamento.
* Staging (stg) refere-se a modelos que são construídos diretamente sobre as fontes. Eles têm um relacionamento um-para-um com as tabelas de origem.
Eles são usados para transformações muito leves que moldam os dados no que você deseja que sejam.
Esses modelos são usados para limpar e padronizar os dados antes de transformar os dados downstream. Nota: Normalmente, eles são materializados como exibições.

* Intermediário (int) refere-se a quaisquer modelos existentes entre as tabelas de fatos e dimensões finais.
Eles devem ser construídos em modelos de preparação em vez de diretamente em fontes para aproveitar a limpeza de dados que foi feita na preparação.

* Fato (fct) refere-se a qualquer dado que represente algo que ocorreu ou está ocorrendo. Os exemplos incluem sessões, transações, pedidos, histórias, votos. Geralmente são mesas finas e compridas.
* Dimensão (dim) refere-se a dados que representam uma pessoa, lugar ou coisa. Exemplos incluem clientes, produtos, candidatos, edifícios, funcionários.

Nota: A convenção Fato e Dimensão é baseada em técnicas de modelagem normalizadas anteriores.

## 1- models

Sobre os models, possuem dois diretórios: _marts_ e _staging_ .

### 1.1 Marts
No diretório de _marts_ são adicionados os modelos de intermediarios, fatos e dimensões.
Dependendo do caso podem surgir novos diretórios por área. Exemplo: Marketing, Financeiro.

### 1.2 Staging
No diretório de _staging_ são adicionados os modelos de configuração das fontes e preparação das fontes.
É aqui que encontrará os arquivos no formato YML, contendo as configurações das fontes.
Dependendo do caso podem sugir novos diretórios por fontes. Exemplo: Salesforce, Stripe, Segment.

## 2- testes
Os testes presentes no projeto são os *_testes genéricos_* e os *_testes singulares_*.
Os testes genéricos são feitos nos arquivos YML dentro dos diretórios de staging, um exemplo de testes genéricos está aqui:
* stg_renner_shippers.yml

Os testes singulares que são adicionados no diretório _tests_. É um arquivo em sql que possui uma query construída para projetar valor nenhum e caso retorne algum valor o teste estará como falho.
Exemplo no projeto é o:
* renner_orderdetails_vendas_positivas.sql

Há também os testes que podem serem introduzidos nas fontes (sources, src). No projeto um desses casos testa se a coluna id de uma tabela é única.
Um exemplo no projeto é o:
* src_renner.yml

## 3- Packages
No arquivo packages.yml terá o dbt-utils, um pacote com utilidades interessantes.
O projeto possui um exemplo da utilização de um package que é o **codegen**. Abaixo deixarei os links.

|site                              |packages                                                      | github                                                        |
| ------------- |:-------------:|-------------:|
|  [get_dbt](https://hub.getdbt.com)|[dbt_utils](https://hub.getdbt.com/dbt-labs/dbt_utils/latest/)|[dbt-utils](https://github.com/dbt-labs/dbt-utils/tree/1.0.0/) |
|                                   |[codegen](https://hub.getdbt.com/dbt-labs/codegen/latest/)    |                                                               |

## 

Clicar em **Expandir** para visualizar os exemplos.

Dentro das imagens na parte superior temos o código referente ao exemplo e abaixo podemos visualizar o resultado após executar pelo botão <b> '</> compile' </b>.

Uma breve descrição sobre os recursos generate:

1. <b> generate_source </b>: <i> utilizado para gerar uma estrutura YAML de source, que você pode colar em um schema file. </i>
    1. <details> <summary><b>Expandir Exemplo generate_source </b></summary> <img src="https://user-images.githubusercontent.com/85959427/209717052-dfcaba4c-badf-44dc-be59-f38561570718.png" width="800" height="500"></img> </details>

1. <b> generate_base_model </b>:<i> Essa macro gera o SQL para um base model, que você pode colar em um model. </i>
    1. <details> <summary><b>Expandir Exemplo generate_base_model </b></summary> <img src="https://imgur.com/QKAWB1j.png" width="800" height="600"></img> </details>

1. <b> generate_model_yaml </b>:<i> Essa macro gera o YAML para uma lista de modelos, que você pode colar em um arquivo schema.yml.</i>
    1. <details> <summary><b>Expandir Exemplo generate_model_yaml </b></summary> <img src="https://imgur.com/kYMC7gz.png" width="800" height="600"></img> </details>

## 

## dbt-project

Não foram feitas grandes alterações, somente na padronização da materialização.
O que estiver na _marts_ será table e o que estiver na _staging_ será view, mas podem mudar para o que acharem conveniente

###### line 34
```
models:
  engdados:
    mart:
      materialized: table
    staging:
      materialized: view
```
