"""Portfolio state and actions."""

from dataclasses import dataclass

from backend.engine.execution import buy_fill_price, sell_fill_price, transaction_fee


@dataclass
class Portfolio:
    cash: float
    shares: int = 0

    def buy_all(self, timestamp: str, price: float, slippage: float, transaction_cost: float):
        fill = buy_fill_price(price, slippage)
        max_shares = int(self.cash // fill)
        if max_shares <= 0:
            return None
        notional = max_shares * fill
        fee = transaction_fee(notional, transaction_cost)
        total = notional + fee
        while total > self.cash and max_shares > 0:
            max_shares -= 1
            notional = max_shares * fill
            fee = transaction_fee(notional, transaction_cost)
            total = notional + fee
        if max_shares <= 0:
            return None
        self.cash -= total
        self.shares += max_shares
        return {
            "timestamp": timestamp,
            "side": "BUY",
            "shares": max_shares,
            "price": fill,
            "fee": fee,
            "notional": notional,
        }

    def sell_all(self, timestamp: str, price: float, slippage: float, transaction_cost: float):
        if self.shares <= 0:
            return None
        fill = sell_fill_price(price, slippage)
        notional = self.shares * fill
        fee = transaction_fee(notional, transaction_cost)
        proceeds = notional - fee
        sold = self.shares
        self.shares = 0
        self.cash += proceeds
        return {
            "timestamp": timestamp,
            "side": "SELL",
            "shares": sold,
            "price": fill,
            "fee": fee,
            "notional": notional,
        }

    def equity(self, close_price: float) -> float:
        return self.cash + self.shares * close_price
