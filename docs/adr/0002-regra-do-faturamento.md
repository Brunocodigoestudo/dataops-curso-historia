# 0002 · Regra do faturamento

## Contexto
O faturamento de outubro chegou errado na reunião de resultados. A origem passou
a enviar pedidos com status "estornado", e a regra só tirava os cancelados da
conta. A regra existia apenas no código, e ninguém do time sabia explicá-la.

## Decisão
O faturamento soma o valor dos pedidos com status "pago" e "aberto".
Pedidos "cancelado" e "estornado" ficam de fora. Um status novo só entra no
projeto depois de uma conversa com o negócio, e o teste `accepted_values` do
staging barra qualquer status que não esteja na lista.

## Consequências
- A regra está escrita e versionada junto com o código.
- A mesma regra vale no dbt (`fct_pedidos`) e no Python (`calcular_valor_total`),
  e cada uma tem o seu teste.
- Todo status novo para o build até alguém decidir o que fazer com ele.
