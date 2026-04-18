"""Market data fetcher."""

import pandas as pd
import yfinance as yf


REQUIRED_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


def fetch_ohlcv(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)
    if data.empty:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    df = data.reset_index().rename(
        columns={
            "Date": "timestamp",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )
    df = df[REQUIRED_COLUMNS]
    return df
