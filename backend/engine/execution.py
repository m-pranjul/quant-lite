"""Execution helpers."""


def buy_fill_price(price: float, slippage: float) -> float:
    return price * (1 + slippage)


def sell_fill_price(price: float, slippage: float) -> float:
    return price * (1 - slippage)


def transaction_fee(notional: float, transaction_cost: float) -> float:
    return abs(notional) * transaction_cost
