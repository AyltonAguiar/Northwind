with orderdetails as (
    select odd.orderid,
           odd.productid,
           odd.preco_vendido,
           odd.quantidade_vendida,
           po.produto,
           po.preco_tabela,
           po.categoryid,
           po.categoria,
           po.supplierid,
           po.fornecedores,
           po.fornecedores_contatos,
           orders.customerid,
           orders.employeeid,
           orders.shipperid,
           orders.orderdate,
           orders.requireddate,
           orders.shippeddate,
           orders.shipname,
           orders.shipcountry,
           orders.clientes_empresa,
           orders.clientes_nome,
           orders.transportadoras,
           orders.transportadoras_phone,
           orders.vendedor,
           (preco_tabela - preco_vendido) as diferenca,
           (preco_vendido * quantidade_vendida) as total,
           ((preco_tabela * quantidade_vendida) - total) as desconto,
           (date_part(year, orders.orderdate::date)||'-01-01')::date as ano


    from {{ref('stg_renner_orderdetails')}} as odd
    left join {{ref('fct_renner_products')}} as po ON (odd.productid = po.productid)
    left join {{ref('fct_renner_orders')}} as orders ON (odd.orderid = orders.orderid)
)


select * from orderdetails

