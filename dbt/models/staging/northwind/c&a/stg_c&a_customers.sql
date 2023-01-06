with customers as (select *,
                          first_value(customerid) over (partition by companyname, contactname order by companyname
                              rows between unbounded preceding and unbounded following) as duplicado
                   from {{ source('c&a', 'customers') }}),
     removidos as (select distinct duplicado from customers),
     final_customers as (select * from {{ source('c&a', 'customers') }} where customerid in (select duplicado from removidos))
select *
from final_customers