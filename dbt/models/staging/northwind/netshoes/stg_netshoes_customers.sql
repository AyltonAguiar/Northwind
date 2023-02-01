{{ config(materialized='table') }}

with source as (

    select * from {{ source('netshoes', 'customers') }}

),

customers as (

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
        CAST(updated_at AS TIMESTAMP) as updated_at

    from source

)

select * from customers
