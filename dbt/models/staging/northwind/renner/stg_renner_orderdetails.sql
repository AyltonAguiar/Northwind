with orderdetails as (
    select orderid,
       productid,
       unitprice::decimal(10,3) as preco_vendido,
       quantity::int as quantidade_vendida
 from {{source('renner', 'orderdetails')}}
)

select * from orderdetails