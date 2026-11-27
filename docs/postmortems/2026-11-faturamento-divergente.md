# Postmortem · faturamento de outubro divergente na reunião

Formato blameless: o foco é o sistema que permitiu o erro, não a pessoa.

## O que aconteceu
Na reunião de resultados, o relatório mostrou R$ 153,00 de faturamento em
outubro. O financeiro tinha fechado R$ 63,10. O pipeline rodou sem erro, e
ninguém soube explicar de onde veio a diferença.

## Linha do tempo
- HH:MM a diferença apareceu na reunião de resultados
- HH:MM issue aberta com a label `incidente`
- HH:MM investigação: os arquivos e o banco estavam inteiros; o pedido 6, com
  status "estornado", estava somado no `fct_pedidos`
- HH:MM negócio confirmou: estorno é válido e não entra no faturamento
- HH:MM correção em produção e issue fechada

## Causa raiz
A origem passou a enviar pedidos com status "estornado". A regra do
faturamento só tirava os cancelados, e não havia nenhum teste no projeto para
avisar. A regra existia só no código.

## O que funcionou
A investigação seguiu uma ordem (número, arquivos, banco, regra, testes) e
achou a causa sem mexer em nada antes de entender o erro.

## Ações
- [x] Tirar "estornado" do faturamento (dbt e Python)
- [x] Unit test no dbt: `valor_total_ignora_estornados`
- [x] Teste no pytest: `test_remove_pedidos_estornados`
- [x] `accepted_values` no staging barra qualquer status desconhecido
- [x] CI em todo pull request barra a regra antiga
- [x] ADR 0002 com a regra do faturamento e runbook de incidente de dados
- [ ] Combinar com o time da origem um aviso prévio para novos status
