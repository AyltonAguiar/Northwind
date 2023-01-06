with orders as (
    select orderid,
       customerid,
       employeeid,
       shipvia as shipperid,
       TO_DATE(orderdate, 'YYYYMMDD') as orderdate,
       TO_DATE(requireddate, 'YYYYMMDD') as requireddate,
       TO_DATE(shippeddate, 'YYYYMMDD') as shippeddate,
       shipname,
       shipcountry

 from {{ source('renner', 'orders') }}
)

select * from orders