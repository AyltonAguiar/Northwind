with orderdetails as (
select  od.orderid,
        od.productid,
        od.unitprice,
        od.quantity,
        pr.productname,
        pr.supplierid,
        pr.categoryid,
        (od.unitprice::decimal(10,2) * od.quantity::decimal(10,2)) as total,
        ((pr.unitprice::decimal(10,2) * od.quantity::int) - total) as desconto

from {{source('c&a','orderdetails')}} od
left join {{source('c&a','products')}} pr using (productid)
)

select * from orderdetails