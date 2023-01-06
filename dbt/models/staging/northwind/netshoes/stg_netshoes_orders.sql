{{ config(materialized='table') }}

with source as (

    select * from {{ source('netshoes', 'orders') }}

),

renamed as (

    select
        orderid,
        customerid,
        employeeid,
        orderdate,
        requireddate,
        shippeddate,
        shipvia,
        freight,
        shipname,
        shipaddress,
        shipcity,
        shipregion,
        shippostalcode,
        shipcountry,
        created_at,
        updated_at

    from source

)

select * from renamed
