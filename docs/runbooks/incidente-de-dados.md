# Runbook · incidente de dados

Passo a passo para quem estiver de plantão quando um número chegar errado no relatório ou quando o CI ou o deploy ficar vermelho.

## 1. Se um número chegou errado no relatório

É o caminho da investigação do faturamento de outubro. Siga a ordem: o número, os arquivos, o banco, a regra e os testes.

1. **Reproduza o número.**

```bash
python -m src.ingestao
dbt build
python scripts/faturamento.py
```

2. **Olhe os arquivos.** Abra os CSVs em `data/` e procure o que mudou: um status novo, um valor estranho, uma linha repetida.
3. **Olhe o banco.** Confira se o dado chegou inteiro na camada `raw`. Exemplo para o status:

```bash
python scripts/consultar.py "select status, count(*) as pedidos from raw.pedidos group by status order by status"
```

4. **Olhe a regra.** Leia o modelo que gera o número (por exemplo, `models/marts/fct_pedidos.sql`) e o ADR da regra em `docs/adr/`.
5. **Olhe os testes.** Se nenhum teste falhou, falta um teste. Ele nasce no passo 3 abaixo.

## 2. Se o CI ou o deploy ficou vermelho

Abra a aba **Actions** do repositório e entre na execução vermelha. Veja qual step falhou:

| Step que falhou | O que costuma ser | Próximo passo |
| --- | --- | --- |
| Padrões (pre-commit) | Formatação, lint de Python ou de SQL | Rode `pre-commit run --all-files` e faça commit do que ele corrigir |
| Testes unitários e de integração | Mudança de código quebrou uma regra | Rode `pytest` e leia o teste que falhou |
| Build e testes do dbt | Um teste de dados falhou | Siga o passo 1, a partir dos arquivos |
| deploy-staging ou deploy-producao | Mesmo caso do dbt, no banco do ambiente | Siga o passo 1, a partir dos arquivos |

Testes de dados falham quando **o dado mudou**, mesmo sem ninguém mexer no código. No log, procure a linha com `FAIL` e o nome do teste (por exemplo, `accepted_values_stg_pedidos_status`) e reproduza no codespace com `dbt build --select stg_pedidos`.

## 3. Registre o incidente

1. Abra uma issue com a label `incidente`. A hora de abertura é o "detectado" das métricas.
2. Decida com o time de negócio se o dado novo é válido ou é um erro da origem.
3. Corrija, abra o PR e feche a issue quando a correção estiver em produção.
4. Escreva o postmortem em `docs/postmortems/`. Toda causa raiz vira pelo menos um teste novo.
