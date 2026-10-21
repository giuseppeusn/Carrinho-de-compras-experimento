from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any


class Carrinho:
    FRETE = Decimal("20.00")
    LIMITE_FRETE_GRATIS = Decimal("150.00")

    def __init__(self) -> None:
        self._itens: list[dict[str, Any]] = []

    def adicionar_item(
        self, nome: str, preco: float, quantidade: int = 1
    ) -> None:
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        try:
            preco_decimal = Decimal(str(preco))
        except (InvalidOperation, ValueError):
            raise ValueError("O preço deve ser um valor válido.") from None

        if preco_decimal < 0:
            raise ValueError("O preço não pode ser negativo.")

        for item in self._itens:
            if item["nome"] == nome:
                item["quantidade"] += quantidade
                return

        self._itens.append(
            {"nome": nome, "preco": float(preco_decimal), "quantidade": quantidade}
        )

    def remover_item(self, nome: str) -> None:
        for indice, item in enumerate(self._itens):
            if item["nome"] == nome:
                del self._itens[indice]
                return
        raise ValueError("Item não encontrado no carrinho.")

    def show(self) -> list[dict[str, Any]]:
        return [item.copy() for item in self._itens]

    def total(self) -> float:
        subtotal = sum(
            (Decimal(str(item["preco"])) * item["quantidade"] for item in self._itens),
            Decimal("0.00"),
        )
        if subtotal == 0:
            return 0.00

        if subtotal >= Decimal("500.00"):
            desconto = subtotal * Decimal("0.15")
        elif subtotal >= Decimal("200.00"):
            desconto = subtotal * Decimal("0.10")
        else:
            desconto = Decimal("0.00")

        valor_com_desconto = subtotal - desconto
        frete = (
            Decimal("0.00")
            if valor_com_desconto >= self.LIMITE_FRETE_GRATIS
            else self.FRETE
        )
        total = valor_com_desconto + frete
        return float(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
