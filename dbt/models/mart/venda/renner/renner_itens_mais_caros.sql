select
      productid,
      productname,
      unitprice::decimal(10,3)
from {{ref('stg_renner_products')}}
order by unitprice desc
limit 10