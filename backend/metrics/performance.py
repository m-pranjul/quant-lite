"""Performance metrics."""

import pandas as pd

from backend.core.constants import TRADING_DAYS_PER_YEAR


def total_return(equity_curve: pd.Series) -> float:
    if equity_curve.empty or equity_curve.iloc[0] == 0:
        return 0.0
    return float((equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1)


def cagr(equity_curve: pd.Series) -> float:
    if len(equity_curve) < 2 or equity_curve.iloc[0] <= 0:
        return 0.0
    years = len(equity_curve) / TRADING_DAYS_PER_YEAR
    if years <= 0:
        return 0.0
    return float((equity_curve.iloc[-1] / equity_curve.iloc[0]) ** (1 / years) - 1)


def win_rate(trades: list[dict]) -> float:
    pairs = _trade_pairs(trades)
    if not pairs:
        return 0.0
    wins = sum(1 for pnl in pairs if pnl > 0)
    return wins / len(pairs)


def profit_factor(trades: list[dict]) -> float:
    pairs = _trade_pairs(trades)
    profits = sum(p for p in pairs if p > 0)
    losses = abs(sum(p for p in pairs if p < 0))
    if losses == 0:
        return float("inf") if profits > 0 else 0.0
    return profits / losses


def _trade_pairs(trades: list[dict]) -> list[float]:
    pnls: list[float] = []
    open_trade: dict | None = None
    for trade in trades:
        if trade["side"] == "BUY":
            open_trade = trade
        elif trade["side"] == "SELL" and open_trade is not None:
            buy_cost = open_trade["notional"] + open_trade["fee"]
            sell_proceeds = trade["notional"] - trade["fee"]
            pnls.append(sell_proceeds - buy_cost)
            open_trade = None
    return pnls
