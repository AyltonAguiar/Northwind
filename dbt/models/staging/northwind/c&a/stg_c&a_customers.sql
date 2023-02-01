--- Query com remoção de duplicados
with
    source as (
        select
            *,
            first_value(customerid) over (
                partition by companyname, contactname
                order by companyname
                rows between unbounded preceding and unbounded following
            ) as duplicado
        from {{ source("c&a", "customers") }}

    ),
    removidos as (select distinct duplicado from source),

    final_customers as (

        select
            customerid,
            companyname,
            contactname,
            contacttitle,
            address,
            city,
            region,
            postalcode,
            country,
            phone,
            created_at,
            updated_at

        from {{ source("c&a", "customers") }}
        where customerid in (select duplicado from removidos)

    )

select * from final_customers
