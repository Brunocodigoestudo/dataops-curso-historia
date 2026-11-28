"""Mostra o faturamento que aparece no relatório da loja, a partir do fct_pedidos."""

import os

import duckdb

# Caminho do banco: no Codespace é o dataops.duckdb; o CI troca pela variável DUCKDB_PATH.
BANCO = os.getenv("DUCKDB_PATH", "dataops.duckdb")


def formatar_reais(valor: float) -> str:
    """Formata 1234.5 como R$ 1.234,50."""
    # Primeiro no formato americano (1,234.50), depois troca vírgula e ponto.
    texto = f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {texto}"


def main() -> None:
    # Abre o banco só para leitura: o script olha, não mexe.
    con = duckdb.connect(BANCO, read_only=True)
    # Soma o valor de todos os pedidos da tabela do faturamento e conta quantos são.
    total, pedidos = con.execute(
        "SELECT coalesce(sum(valor_total), 0), count(*) FROM main.fct_pedidos"
    ).fetchone()
    con.close()
    print(f"Faturamento de outubro: {formatar_reais(total)} em {pedidos} pedidos")


if __name__ == "__main__":
    main()
