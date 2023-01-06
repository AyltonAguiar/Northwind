with shippers as (
    select shipperid,
           companyname,
           phone
    from {{ source('renner', 'shippers') }}
    )

select * from shippers
