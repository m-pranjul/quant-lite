import pandas as pd

from backend.metrics.performance import profit_factor
from backend.metrics.risk import max_drawdown, sharpe_ratio


def test_drawdown_correctness():
    equity = pd.Series([100, 120, 90, 95, 80, 130])
    dd = max_drawdown(equity)
    assert round(dd, 4) == round((80 - 120) / 120, 4)


def test_no_divide_by_zero_crashes():
    assert sharpe_ratio(pd.Series([0, 0, 0])) == 0.0
    assert profit_factor([]) == 0.0
