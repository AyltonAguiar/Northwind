select employeeid,
       firstname||' '||lastname as nome,
       title as cargo,
       (date_part(year, current_date) - date_part(year, birthdate::date)) as idade,
       (date_part(year, current_date) - date_part(year, hiredate::date)) as tempo_de_contratacao
from {{source('renner','employees')}}