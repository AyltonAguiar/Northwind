--- Comparativo entre o total das fornecedoras de 2020 e 2021
--- Observação: Poderia ter utilizado with, mas opnei por usar um case
--- por ser simples e reduzir a quantidade de linhas (nesse caso).

select supplierid as fornecedor_id,
       fornecedores,
       sum(case when date_part(year, orderdate)='2020' then total end) as total_2020,
       sum(case when date_part(year, orderdate)='2021' then total end) as total_2021,
       (total_2021 - total_2020) as resultado_comparativo

from {{ref('dim_renner_orderdetails')}}
group by supplierid, fornecedores, diferenca
order by diferenca desc