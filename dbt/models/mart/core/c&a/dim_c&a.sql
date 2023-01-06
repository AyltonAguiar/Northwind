with
    prod as (
        select
            products.productid,
            products.productname,
            products.unitprice,
            suppliers.supplierid,
            suppliers.companyname,
            suppliers.contactname,
            suppliers.phone,
            categories.categoryid,
            categories.categoryname
        from {{ source("c&a", "products") }} as products
        left join
            {{ source("c&a", "suppliers") }} as suppliers
            on (suppliers.supplierid = products.supplierid)
        left join
            {{ source("c&a", "categories") }} as categories
            on (categories.categoryid = products.categoryid)
    ),
    orderdetails as (
        select prod.*, orderdetails.orderid, orderdetails.quantity, orderdetails.desconto
         from {{ref('fct_c&a_orderdetails')}} as orderdetails
         left join prod on (prod.productid = orderdetails.productid)
    ),
    orders as (
        select orders.orderdate, orders.orderid,
               customers.companyname as customers,
               employees.name as employees,
               employees.idade as idade,
               employees.tempo_emprego as tempo_emprego_anos

         from {{source('c&a','orders')}} as orders
         left join {{ref('stg_c&a_customers')}} as customers on (customers.customerid = orders.customerid)
         left join {{ref('stg_c&a_employees')}} as employees on (employees.employeeid = orders.employeeid)
         left join {{source('c&a', 'shippers')}} as shippers on (shippers.shipperid = orders.shipvia)

    ), final_orders as (

        select odtails.*, od.orderdate::date, od.customers, od.employees, od.idade, od.tempo_emprego_anos
        from orderdetails as odtails
        inner join orders as od on (odtails.orderid = od.orderid)
    )

select * from final_orders