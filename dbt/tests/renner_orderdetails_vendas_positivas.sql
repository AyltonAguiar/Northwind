select
      productid,
      orderid,
      sum(preco_vendido) as vendas      

from {{ref('stg_renner_orderdetails')}}
group by productid, orderid
having not (vendas >= 0)