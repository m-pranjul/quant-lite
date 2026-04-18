import pandas as pd

from backend.strategies.sma_crossover import SMACrossoverStrategy


def _sample_data():
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2020-01-01", periods=100, freq="D", tz="UTC"),
            "open": range(100),
            "high": range(100),
            "low": range(100),
            "close": range(100),
            "volume": [1000] * 100,
        }
    )


def test_signals_use_past_data_via_shift():
    data = _sample_data()
    strat = SMACrossoverStrategy({"short_window": 5, "long_window": 10})
    signals = strat.generate_signals(data)
    unshifted = (data["close"].rolling(5).mean() > data["close"].rolling(10).mean()).astype(int)
    assert signals.iloc[0] == 0
    assert signals.iloc[11] == unshifted.iloc[10]
