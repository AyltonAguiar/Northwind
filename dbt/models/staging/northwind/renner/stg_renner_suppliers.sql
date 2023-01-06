with suppliers as (
    select supplierid,
           companyname,
           contactname,
           contacttitle,
           address,
           city,
           region,
           postalcode,
           country,
           phone
    from {{source('renner', 'suppliers')}}
)

select * from suppliers