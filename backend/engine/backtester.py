"""Deterministic backtesting engine."""

import pandas as pd

from backend.engine.portfolio import Portfolio
from backend.metrics.performance import cagr, profit_factor, total_return, win_rate
from backend.metrics.risk import max_drawdown, sharpe_ratio


def run_backtest(
    data: pd.DataFrame,
    signals: pd.Series,
    initial_capital: float,
    transaction_cost: float,
    slippage: float,
) -> dict:
    portfolio = Portfolio(cash=float(initial_capital))
    trades: list[dict] = []
    equity_points: list[dict] = []

    for idx, row in data.iterrows():
        price = float(row["close"])
        ts = row["timestamp"].isoformat()
        sig = int(signals.iloc[idx])

        if sig == 1 and portfolio.shares == 0:
            trade = portfolio.buy_all(ts, price, slippage, transaction_cost)
            if trade:
                trades.append(trade)
        elif sig == -1 and portfolio.shares > 0:
            trade = portfolio.sell_all(ts, price, slippage, transaction_cost)
            if trade:
                trades.append(trade)

        equity_points.append({"timestamp": ts, "equity": portfolio.equity(price)})

    if portfolio.shares > 0:
        last = data.iloc[-1]
        trade = portfolio.sell_all(last["timestamp"].isoformat(), float(last["close"]), slippage, transaction_cost)
        if trade:
            trades.append(trade)
            equity_points[-1]["equity"] = portfolio.equity(float(last["close"]))

    equity_curve = pd.Series([pt["equity"] for pt in equity_points])
    rets = equity_curve.pct_change().fillna(0)
    metrics = {
        "total_return": total_return(equity_curve),
        "cagr": cagr(equity_curve),
        "win_rate": win_rate(trades),
        "profit_factor": profit_factor(trades),
        "max_drawdown": max_drawdown(equity_curve),
        "sharpe_ratio": sharpe_ratio(rets),
    }
    return {"equity_curve": equity_points, "trades": trades, "metrics": metrics}
