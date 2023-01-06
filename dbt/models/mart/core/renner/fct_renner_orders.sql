with transportadoras as (
    select * from {{ref('stg_renner_shippers')}}
 ),
 vendedores as (
     select * from {{ref('stg_renner_employees')}}
 ),
 clientes as (
     select * from {{ref('stg_renner_customers')}}
 ),
 orders as (
     select od.*,

       cl.companyname as clientes_empresa,
       cl.contactname as clientes_nome,

       tp.companyname as transportadoras,
       tp.phone as transportadoras_phone,
       vdd.nome as vendedor

    from {{ref('stg_renner_orders')}} as od
    left join transportadoras as tp ON (od.shipperid=tp.shipperid)
    left join clientes as cl ON (od.customerid = cl.customerid)
    left join vendedores as vdd ON (od.employeeid = vdd.employeeid)
)

select * from orders