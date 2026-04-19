"""Market data fetcher."""

from __future__ import annotations

import pandas as pd
import yfinance as yf


REQUIRED_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


class DataFetchError(ValueError):
    """Raised when remote data could not be downloaded."""


def _normalize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    data = df.copy()
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [c[0] for c in data.columns]

    data = data.reset_index().rename(
        columns={
            "index": "timestamp",
            "Date": "timestamp",
            "Datetime": "timestamp",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "close",
            "Volume": "volume",
        }
    )

    missing = [col for col in REQUIRED_COLUMNS if col not in data.columns]
    if missing:
        raise DataFetchError(f"missing expected columns from provider: {missing}")

    return data[REQUIRED_COLUMNS]


def _download_with_fallback(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    last_error: Exception | None = None

    try:
        primary = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=False,
            threads=False,
            group_by="column",
        )
        if not primary.empty:
            return primary
    except Exception as exc:  # pragma: no cover - provider/network dependent
        last_error = exc

    try:
        history = yf.Ticker(ticker).history(
            start=start_date,
            end=end_date,
            auto_adjust=False,
            actions=False,
        )
        if not history.empty:
            return history
    except Exception as exc:  # pragma: no cover - provider/network dependent
        last_error = exc

    if last_error is not None:
        raise DataFetchError(f"unable to fetch market data for '{ticker}': {last_error}") from last_error
    raise DataFetchError(f"unable to fetch market data for '{ticker}' from provider")


def fetch_ohlcv(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    cleaned_ticker = ticker.strip().upper()
    raw = _download_with_fallback(cleaned_ticker, start_date, end_date)
    return _normalize_ohlcv(raw)
