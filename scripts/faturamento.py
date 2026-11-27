"""Mostra o faturamento que aparece no relatório da loja, a partir do fct_pedidos."""

import os

import duckdb

BANCO = os.getenv("DUCKDB_PATH", "dataops.duckdb")


def formatar_reais(valor: float) -> str:
    """Formata 1234.5 como R$ 1.234,50."""
    texto = f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {texto}"


def main() -> None:
    con = duckdb.connect(BANCO, read_only=True)
    total, pedidos = con.execute(
        "SELECT coalesce(sum(valor_total), 0), count(*) FROM main.fct_pedidos"
    ).fetchone()
    con.close()
    print(f"Faturamento de outubro: {formatar_reais(total)} em {pedidos} pedidos")


if __name__ == "__main__":
    main()
