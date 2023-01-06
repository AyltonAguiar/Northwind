select * from {{ref('dim_c&a')}} as main
 where date_part(year, main.orderdate) = 2022
