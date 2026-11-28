# Testes da regra de faturamento (src/transformacoes.py).
# Cada teste monta pedidos de exemplo, passa pela regra
# e confere se o resultado é o esperado.

from src.transformacoes import calcular_valor_total


def test_calcula_valor_total():
    # Um pedido pago: 2 unidades de R$ 10,50.
    pedidos = [{"quantidade": 2, "preco_unitario": 10.5, "status": "pago"}]
    resultado = calcular_valor_total(pedidos)
    # O valor total tem que ser quantidade x preço: R$ 21,00.
    assert resultado[0]["valor_total"] == 21.0


def test_remove_pedidos_cancelados():
    # Pedido cancelado não é venda: não pode entrar no faturamento.
    pedidos = [{"quantidade": 1, "preco_unitario": 5, "status": "cancelado"}]
    # A lista vazia mostra que a regra tirou o pedido.
    assert calcular_valor_total(pedidos) == []


def test_remove_pedidos_estornados():
    # O ERRO DA REUNIÃO: o estorno é dinheiro que voltou para o cliente.
    # A regra antiga somava o estorno, e o faturamento foi para mais.
    # Este teste garante que o erro não volta.
    pedidos = [{"quantidade": 1, "preco_unitario": 89.9, "status": "estornado"}]
    assert calcular_valor_total(pedidos) == []
