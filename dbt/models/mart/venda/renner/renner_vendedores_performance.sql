select vendedor,
       date_part(year, ano) as ano,
       sum(quantidade_vendida) as quantidade_vendida,
       sum(total) as total_venda,
       sum(desconto) as desconto_na_venda,
       row_number() over(partition by ano order by ano, total_venda desc) as rank_vendas_ano
from {{ref('dim_renner_orderdetails')}}
group by vendedor, ano
order by ano, total_venda desc
