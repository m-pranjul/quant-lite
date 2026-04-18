"""Risk metrics."""

import numpy as np
import pandas as pd

from backend.core.constants import TRADING_DAYS_PER_YEAR


def max_drawdown(equity_curve: pd.Series) -> float:
    if equity_curve.empty:
        return 0.0
    running_max = equity_curve.cummax()
    drawdown = (equity_curve - running_max) / running_max.replace(0, np.nan)
    return float(drawdown.min()) if not drawdown.empty else 0.0


def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    if returns.empty:
        return 0.0
    excess = returns - (risk_free_rate / TRADING_DAYS_PER_YEAR)
    std = excess.std(ddof=0)
    if std == 0 or np.isnan(std):
        return 0.0
    return float((excess.mean() / std) * np.sqrt(TRADING_DAYS_PER_YEAR))
