#  __dbt cloud__

[dbt desenvolvimento]: #dbt-desenvolvimento


## __Apresentação__

Aqui será realizado toda a parte de organização e criação das querys utilizando as boas práticas presentes nas aulas disponibilizadas pelo próprio dbt.

## __Configurações__ {#configurações}

### Configurando um novo projeto

Ao iniciar um projeto dbt cloud temos: 

1.  `Name your project`: Aqui você fornece um nome ao projeto. Atualmente não sei se há preenchimento automático, mas antigamente tinha o padrão que era `Analytics`.
2.  `Choose a warehouse`: Aqui você escolhe o warehouse, selecione uma das opções e pressione `next` para prosseguir.
3.  `Configure your environment`: Configuração do ambiente, dependendo do warehouse pode haver mais ou menos opções. fique atento ao preenchimento. __*O `username` será o `dbt_dev` e a `senha` basta copiar dos valores guardados no `secrets manager`*__.
4.  `Setup a Repository`: Escolha qual das opções será armazenado o código do projeto, pressione `Connect` e faça o vículo. Depois de configurado basta iniciar o projeto.

!!! Caution "Abaixo um tutorial do [Kahan](https://www.youtube.com/@KahanDataSolutions)!"

|tutorial|link||
|----|----|----|
| Configurando conta dbt cloud| [Kahan Data Solutions](https://youtu.be/vhq8g_r6bpA?t=40){:target='_blank'}| |

## __Convenções de nomenclatura__ {#convenções-de-nomenclatura}
Ao trabalhar neste projeto, estabelecemos algumas convenções para nomear nossos modelos.

[Convenções de nomenclatura]: #convenções-de-nomenclatura

* __`Fontes (src)`__ referem-se aos dados brutos da tabela que foram construídos no warehouse por meio de um processo de carregamento.
* __`Staging (stg)`__ refere-se a modelos que são construídos diretamente sobre as fontes. Eles têm um relacionamento um-para-um com as tabelas de origem.
Eles são usados para transformações muito leves que moldam os dados no que você deseja que sejam.
Esses modelos são usados para limpar e padronizar os dados antes de transformar os dados downstream. Nota: Normalmente, eles são materializados como exibições.

* __`Intermediário (int)`__ refere-se a quaisquer modelos existentes entre as tabelas de fatos e dimensões finais.
Eles devem ser construídos em modelos de preparação em vez de diretamente em fontes para aproveitar a limpeza de dados que foi feita na preparação.

* __`Fato (fct)`__ refere-se a qualquer dado que represente algo que ocorreu ou está ocorrendo. Os exemplos incluem sessões, transações, pedidos, histórias, votos. Geralmente são mesas finas e compridas.
* __`Dimensão (dim)`__ refere-se a dados que representam uma pessoa, lugar ou coisa. Exemplos incluem clientes, produtos, candidatos, edifícios, funcionários.

Nota: A convenção Fato e Dimensão é baseada em técnicas de modelagem normalizadas anteriores.


## __Explanando sobre a organização__ {#explanando-sobre-a-organização}

Os exemplos vão variar, cada cliente tem uma estrutura diferente de organização sobre os arquivos `sql` e `yaml`.

1.  `renner`: Apenas um `source` contendo todas as tabelas, algumas colunas e tests. Os arquivos `stg.sql` guardam as querys de consulta das fontes. Os arquivos `stg.yml` guardam as colunas brutas e descrições (foco documentação). Na pasta `mart` a subpasta `core` guarda apenas as dimensões, fatos e intermediários. Enquanto outras subpastas da `mart` guardam as querys por área.

[Explanando sobre a organização]: #explanando-sobre-a-organização

### dbt-project {#dbt-project}

Não foram feitas grandes alterações, somente na padronização da materialização.
O que estiver na _mart_ será table e o que estiver na _staging_ será view, mas podem mudar para o que acharem conveniente

=== ":octicons-file-code-16: `dbt\dbt_project.yml`"
```
...
models:
  engdados:
    mart:
      materialized: table
    staging:
      materialized: view
...
```
[dbt-project]: #dbt-project

### Models {#dbt-models}

Sobre os models, possuem dois diretórios: _mart_ e _staging_ .

*   `Mart`: No diretório de _mart_ são adicionados os modelos de intermediarios, fatos e dimensões.
Dependendo do caso podem surgir novos diretórios por área. Exemplo: Marketing, Financeiro.
*   `Staging`: No diretório de _staging_ são adicionados os modelos de configuração das fontes e preparação das fontes.
É aqui que encontrará os arquivos no formato YML, contendo as configurações das fontes.
Dependendo do caso podem sugir novos diretórios por fontes. Exemplo: Salesforce, Stripe, Segment.

#### Staging {#staging}

Em `staging` temos os arquivos `src`(source) e `stg`(staging). Os sources são arquivos em `yml` contendo configurações sobre o schema descrito. As estratégias para como organizar as configurações depende muito, um exemplo é código abaixo:

=== ":octicons-file-code-16: `dbt\models\staging\northwind\renner\src_renner.yml`"
``` yaml
version: 2

sources:
  - name: renner
    description: 'Database do setor de dados'
    database: northwind
    schema: "renner"
    tables:
      - name: employees
        description: "informações sobre os funcionários"
        columns:
          - name: employeeid
            tests:
            - unique
      - name: categories
      - name: customers
      - name: orderdetails
      - name: orders
      - name: products
      - name: shippers
      - name: suppliers
```

Os arquivos `staging` podem variar entre `sql` e possuir um `yml`. Exemplo: O arquivo `stg.yml` possui campos de descrições para adicionar informações, assim você deixa somente o "grosso" no `stg.sql`, permitindo uma leitura melhor sobre as querys. Abaixo um exemplo de `stg.yml` e `stg.sql`

=== ":octicons-file-code-16: `dbt\models\staging\northwind\netshoes\stg_netshoes_customers.yml`"

    ``` yaml
    version: 2

    models:
    - name: stg_netshoes_customers
        description: "Cópia da tabela original da costumers do banco northwind"
        columns:
        - name: customerid
            description: "Primary key da tabela costumers"

        - name: companyname
            description: "Nome da empresa integro"

        - name: contactname
            description: "Nome do responsável"

        - name: contacttitle
            description: "{{ doc('costumers_contacttitle') }}"
        ...
    ```
=== ":octicons-file-code-16: `dbt\models\staging\northwind\netshoes\stg_netshoes_customers.sql`"

    ``` sql
    {{ config(materialized='table') }}

    with source as (

        select * from {{ source('netshoes', 'customers') }}

    ),

    customers as (

        select
            customerid,
            companyname,
            contactname,
            contacttitle,
            address,
            city,
            region,
            postalcode,
            country,
            phone,
            created_at,
            CAST(updated_at AS TIMESTAMP) as updated_at

        from source

    )

    select * from customers
    ```

#### Mart {#mart}

O diretório `core` possui os `clientes`, e neles estão as dimensões, fatos e intermediários. Modelagem dimensão e fato, no exemplo abaixo:


=== ":octicons-file-code-16: `dbt\models\mart\core\renner\dim_renner_orderdetails.sql`"

    ``` sql
    with orderdetails as (
        select odd.orderid,
            odd.productid,
            odd.preco_vendido,
            ....
            orders.transportadoras,
            orders.transportadoras_phone,
            orders.vendedor,
            (preco_tabela - preco_vendido) as diferenca,
            (preco_vendido * quantidade_vendida) as total,
            ((preco_tabela * quantidade_vendida) - total) as desconto,
            (date_part(year, orders.orderdate::date)||'-01-01')::date as ano


        from {{ref('stg_renner_orderdetails')}} as odd
        left join {{ref('fct_renner_products')}} as po ON (odd.productid = po.productid)
        left join {{ref('fct_renner_orders')}} as orders ON (odd.orderid = orders.orderid)
    )

    select * from orderdetails
    ```
=== ":octicons-file-code-16: `dbt\models\mart\core\renner\fct_renner_products.sql`"

    ``` sql
    with products as (
        
        select products.productid,
            products.productname as produto,
            products.unitprice::decimal(10,3) as preco_tabela,
            categories.categoryid,
            categories.categoryname as categoria,
            suppliers.supplierid,
            suppliers.companyname as fornecedores,
            suppliers.contactname as fornecedores_contatos

        from {{ref('stg_renner_products')}} as products
        left join {{ref('stg_renner_categories')}} as categories on (products.categoryid = categories.categoryid) 
        left join {{ref('stg_renner_suppliers')}} as suppliers on (products.supplierid = suppliers.supplierid)

    )

    select * from products
    ```

Lembre-se que outros diretórios podem nascer por área, por exemplo: Venda.
Utilizei post_hook e adicionei um grupo específico para a visualização (reporters: looker).


=== ":octicons-file-code-16: `dbt\models\mart\venda\renner\renner_categorias_mais_vendidas.sql`"

    ``` sql
    {{ config(
        materialized='table',
        post_hook=["
        grant usage on schema {{target.schema}} to group reporters;
        grant select on table {{target.schema}}.renner_categorias_mais_vendidas to group reporters;"]
    ) }}

    with
        categorias as (
            select
                categoria,
                ano,
                sum(total) as total,
                row_number() over (
                    partition by ano order by sum(total) desc
                ) as rank_categoria
            from {{ ref("dim_renner_orderdetails") }}
            group by categoria, ano
        )

    select *
    from categorias
    where rank_categoria <= 5
    order by ano, rank_categoria
    ```


### Tests {#dbt-tests}
Os testes presentes no projeto são os `testes genéricos` e os `testes singulares`.

#### Testes genéricos {#testes-genericos}
São feitos nos arquivos `yml` dentro dos diretórios de staging, um exemplo de testes genéricos está aqui abaixo:

=== ":octicons-file-code-16: `dbt\models\staging\northwind\renner\stg_renner_shippers.yml`"
``` yaml
version: 2

models:
- name: dim_renner_orderdetails
    description: tabela dimensão da order details
    columns:
    - name: id
        description: É a primary key formada pelos ids das demais tabelas
        tests:
        - unique
        - not_null
    - name: transportadoras
        tests:
        - accepted_values:
            values: ['Speedy Express', 'United Package', 'Federal Shipping']
```

#### Testes singulares {#testes-singulares}
São adicionados no diretório _tests_. É um arquivo em sql que possui uma query construída para projetar valor nenhum e caso retorne algum valor o teste estará como falho. Exemplo abaixo:

=== ":octicons-file-code-16: `dbt\tests\renner_orderdetails_vendas_positivas.sql`"
``` sql
select
      productid,
      orderid,
      sum(preco_vendido) as vendas      

from {{ref('stg_renner_orderdetails')}}
group by productid, orderid
having not (vendas >= 0)
```

Há também os testes que podem serem introduzidos nas fontes (sources, src). No projeto um desses casos testa se a coluna id de uma tabela é única. Um exemplo é o:
=== ":octicons-file-code-16: `dbt\models\staging\northwind\renner\src_renner.yml`"
``` yaml
version: 2

sources:
  - name: renner
    description: 'Database do setor de dados'
    database: northwind
    schema: "renner"
    tables:
      - name: employees
        description: "informações sobre os funcionários"
        columns:
          - name: employeeid
            tests:
            - unique
      - name: categories
      - name: customers
      - name: orderdetails
      - name: orders
      - name: products
      - name: shippers
      - name: suppliers
```

### __Packages__ {#packages}
No arquivo packages.yml terá o dbt-utils, um pacote com utilidades interessantes.
O projeto possui:`codegen` e `dbt_utils`. Abaixo deixarei os links.

|dbt| links|
|----|-----|
|site       |[get_dbt](https://hub.getdbt.com)|
|packages   |[dbt_utils](https://hub.getdbt.com/dbt-labs/dbt_utils/latest/), [codegen](https://hub.getdbt.com/dbt-labs/codegen/latest/)|
|github     |[dbt-utils](https://github.com/dbt-labs/dbt-utils/tree/1.0.0/)|


#### Dbt_utils {#dbt-utils}

O `dbt_utils` contém macros que podem serem utilizados no projeto dbt.

!!! Warning "Ainda em construção!"
    

#### Codegen {#codegen}
O `codegen` gera código dbt e exibe na linha de comando.

!!! Question "Já imaginou ter que preencher na mão um arquivo de source com várias tabelas com/sem colunas?"
    Fora de questão, né? Por isso o `codegen` existe!


##### *generate_source* {#generate-source}

Essa macro gera um `yaml` contendo as informações necessárias para você copiar e colar no seu arquivo source. Ela contém vários argumentos, aumentando a variedade de formas que podem serem gerados.

=== ":octicons-file-code-16: `Gera com tabelas e colunas`"
```yaml
{{ codegen.generate_source(
    schema_name="c&a",
     database_name="northwind",
      generate_columns=True
) }}
```

!!! Hint "generate_source"
    - Gera um yaml do source
    - Fácil entendimento
    - Várias formas de gerar o source

##### *generate_base_model* {#generate-base-model}

Essa macro gera um `sql` contendo as informações necessárias para você copiar e colar no seu arquivo base model. Ela contém vários argumentos, aumentando a variedade de formas que podem serem gerados.

=== ":octicons-file-code-16: `Gera query com as colunas da tabela específicada`"
```yaml
{{ codegen.generate_base_model(
    source_name='c&a',
    table_name='customers'
) }}
```

!!! Hint "generate_base_model"
    - Gera um sql para um modelo base
    - Fácil entendimento
    - Várias formas de gerar o modelo base

##### *generate_model_yaml* {#generate-model-yml}

Essa macro gera um `yaml` contendo os nomes das colunas e descrições vazias para documentação. Ela contém 2 argumentos.

=== ":octicons-file-code-16: `Gera yml para tabela ou view específicada`"
```yaml
{{ codegen.generate_model_yaml(
    model_names=['stg_c&a_customers']
) }}
```

!!! Hint "generate_model_yaml"
    - Gera um yml com colunas e descrições
    - Fácil entendimento

## :material-format-list-checks: Check Objetivos

Os ícones :octicons-check-circle-fill-24:{ style="color: #00e676" } são os finalizados e os :octicons-check-circle-fill-24:{ style="color: var(--md-default-fg-color--lightest)" } são os em abertos.

- [x] [Configurações](#configurações)
- [x] [Convenções de nomenclatura](#convenções-de-nomenclatura)
- [x] [Project](#dbt-project)
- [x] [Models](#dbt-models)
- [x] [Testes](#dbt-tests)
- [x] [Packages](#packages)
- [ ] Jobs
    - [ ] Criação de Jobs
    - [ ] Integração com slack e e-mail
- [ ] Documentação sobre as querys
    - [ ] Utilização de dbt docs
- [ ] Utilização de Seeds
- [ ] Utilização dos macros
