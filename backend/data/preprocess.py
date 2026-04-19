"""Data cleanup and checks."""

import pandas as pd

from backend.core.constants import MIN_DATA_LENGTH


REQUIRED_PRICE_COLUMNS = ["open", "high", "low", "close"]


def preprocess_data(df: pd.DataFrame, min_length: int = MIN_DATA_LENGTH) -> pd.DataFrame:
    if df.empty:
        raise ValueError("empty data")

    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True, errors="coerce")

    for column in REQUIRED_PRICE_COLUMNS + ["volume"]:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce")

    out = out.sort_values("timestamp")
    out = out.drop_duplicates(subset=["timestamp"], keep="first")

    # Volume is optional for some symbols/providers; missing values should not invalidate price bars.
    if "volume" in out.columns:
        out["volume"] = out["volume"].fillna(0)

    out = out.dropna(subset=["timestamp", *REQUIRED_PRICE_COLUMNS])

    if out.empty:
        raise ValueError("no valid OHLC rows after preprocessing")
    if len(out) < min_length:
        raise ValueError("insufficient data")

    return out.reset_index(drop=True)
