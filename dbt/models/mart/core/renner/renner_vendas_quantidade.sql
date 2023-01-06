select 
      count(case when preco_tabela > preco_vendido then 1 end) as vendido_preco_maior,
      count(case when preco_tabela < preco_vendido then 1 end) as vendido_preco_menor,
      count(case when preco_tabela = preco_vendido then 1 end) as vendido_preco_igual

from {{ref('dim_renner_orderdetails')}}
