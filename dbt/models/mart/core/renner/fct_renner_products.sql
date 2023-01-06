with products as (
    
    select products.productid,
           products.productname as produto,
           products.unitprice::decimal(10,3) as preco_tabela,
           categories.categoryid,
           categories.categoryname as categoria,
           suppliers.supplierid,
           suppliers.companyname as fornecedores,
           suppliers.contactname as fornecedores_contatos

    from {{ref('stg_renner_products')}} as products
    left join {{ref('stg_renner_categories')}} as categories on (products.categoryid = categories.categoryid) 
    left join {{ref('stg_renner_suppliers')}} as suppliers on (products.supplierid = suppliers.supplierid)

)

select * from products