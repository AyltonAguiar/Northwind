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
