import pandas as pd

from backend.engine.backtester import run_backtest


def _data(n=120):
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2022-01-01", periods=n, freq="D", tz="UTC"),
            "open": [100 + i for i in range(n)],
            "high": [101 + i for i in range(n)],
            "low": [99 + i for i in range(n)],
            "close": [100 + i for i in range(n)],
            "volume": [1000] * n,
        }
    )


def test_same_input_same_output():
    data = _data()
    signals = pd.Series([0] + [1] + [0] * 118)
    r1 = run_backtest(data, signals, 100000, 0.001, 0.001)
    r2 = run_backtest(data, signals, 100000, 0.001, 0.001)
    assert r1 == r2


def test_no_negative_equity():
    data = _data()
    signals = pd.Series([0] + [1] + [0] * 118)
    result = run_backtest(data, signals, 100000, 0.001, 0.001)
    assert min(point["equity"] for point in result["equity_curve"]) >= 0
