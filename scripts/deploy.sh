#!/usr/bin/env bash
# Deploy simulado: constrói e testa o pipeline inteiro no banco do ambiente
set -euo pipefail                      # para o script no primeiro erro

AMBIENTE="$1"                          # staging ou production
export DBT_PROFILES_DIR=.
export DUCKDB_PATH="${AMBIENTE}.duckdb"

echo "Secret recebido: $EXEMPLO_SECRET"  # o GitHub mostra *** no log
python -m src.ingestao                 # carrega os CSVs no banco do ambiente
dbt build --target "$AMBIENTE"         # monta as tabelas e roda os testes
echo "Deploy em $AMBIENTE concluído."
