with 
    
    menor_preco_vendido as (
    select count(*) as quantidade_registros,
           'vendido_preco_menor' as tipo_registro
    from {{ref('dim_renner_orderdetails')}} 
    where preco_vendido < preco_tabela
    ),

    igual_preco as (
        select count(*) as quantidade_registros,
               'vendido_preco_igual' as tipo_registro
    from {{ref('dim_renner_orderdetails')}} 
    where preco_vendido = preco_tabela
    ),

    maior_preco_vendido as(
        select count(*) as quantidade_registros,
               'vendido_preco_maior' as tipo_registro
    from {{ref('dim_renner_orderdetails')}} 
    where preco_vendido > preco_tabela
    ),

    unificacao_count as (
        select quantidade_registros, tipo_registro
         from menor_preco_vendido

        union
        select quantidade_registros, tipo_registro
        from maior_preco_vendido
        
        union
        select quantidade_registros, tipo_registro
        from igual_preco
        )

select * from unificacao_count order by tipo_registro
