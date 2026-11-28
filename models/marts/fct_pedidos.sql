-- Tabela do faturamento: uma linha para cada pedido que entra na conta.
select
    id_pedido,
    id_cliente,
    criado_em,
    -- valor total = quantidade x preço, arredondado em 2 casas
    round(quantidade * preco_unitario, 2) as valor_total
-- lê os pedidos já padronizados, da camada staging
from {{ ref('stg_pedidos') }}
-- filtro: só entram no faturamento os pedidos que passam nesta condição
where status != 'cancelado'
