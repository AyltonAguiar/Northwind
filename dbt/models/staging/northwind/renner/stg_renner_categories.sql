with categories as (
    select categoryid,
           categoryname,
           description
    from {{source('renner','categories')}}
)

select * from categories