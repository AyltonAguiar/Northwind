with products as (
    select productid,
           productname,
           supplierid,
           categoryid,
           unitprice,
           unitsinstock
    from {{source('renner', 'products')}}
)

select * from products