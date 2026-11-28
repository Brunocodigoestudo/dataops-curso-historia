# Regra do faturamento em Python: decide quais pedidos entram na conta
# e calcula o valor de cada um.


def calcular_valor_total(pedidos: list[dict]) -> list[dict]:
    """Adiciona valor_total = quantidade * preco_unitario, ignorando cancelados."""
    return [
        # Para cada pedido, copia os dados e acrescenta o valor_total:
        # quantidade x preço, arredondado em 2 casas, como dinheiro.
        {**p, "valor_total": round(p["quantidade"] * p["preco_unitario"], 2)}
        for p in pedidos
        # Filtro: só entram no faturamento os pedidos que passam nesta condição.
        if p["status"] != "cancelado"
    ]
