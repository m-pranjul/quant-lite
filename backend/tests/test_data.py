import pandas as pd
import pytest

from backend.data import fetch
from backend.data.fetch import DataFetchError, fetch_ohlcv
from backend.data.preprocess import preprocess_data


class _DummyTicker:
    def __init__(self, history_df):
        self._history_df = history_df

    def history(self, **_kwargs):
        return self._history_df


def test_empty_data_rejected():
    df = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
    with pytest.raises(ValueError, match="empty data"):
        preprocess_data(df)


def test_preprocess_keeps_rows_with_missing_volume():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range("2023-01-01", periods=35, freq="D"),
            "open": [100.0] * 35,
            "high": [101.0] * 35,
            "low": [99.0] * 35,
            "close": [100.5] * 35,
            "volume": [None] * 35,
        }
    )
    out = preprocess_data(df)
    assert len(out) == 35
    assert out["volume"].eq(0).all()


def test_fetch_uses_fallback_history(monkeypatch):
    monkeypatch.setattr(fetch.yf, "download", lambda *args, **kwargs: pd.DataFrame())

    history_df = pd.DataFrame(
        {
            "Open": [100.0, 101.0],
            "High": [102.0, 103.0],
            "Low": [99.0, 100.0],
            "Close": [101.0, 102.0],
            "Volume": [1000, 1200],
        },
        index=pd.to_datetime(["2023-01-01", "2023-01-02"]),
    )
    monkeypatch.setattr(fetch.yf, "Ticker", lambda *_args, **_kwargs: _DummyTicker(history_df))

    out = fetch_ohlcv("aapl", "2023-01-01", "2023-01-03")
    assert list(out.columns) == ["timestamp", "open", "high", "low", "close", "volume"]
    assert len(out) == 2


def test_fetch_raises_clear_error_when_provider_fails(monkeypatch):
    def boom(*_args, **_kwargs):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(fetch.yf, "download", boom)
    monkeypatch.setattr(fetch.yf, "Ticker", lambda *_args, **_kwargs: _DummyTicker(pd.DataFrame()))

    with pytest.raises(DataFetchError):
        fetch_ohlcv("INVALID", "2023-01-01", "2023-01-03")
