"""Data cleanup and checks."""

import pandas as pd

from backend.core.constants import MIN_DATA_LENGTH


def preprocess_data(df: pd.DataFrame, min_length: int = MIN_DATA_LENGTH) -> pd.DataFrame:
    if df.empty:
        raise ValueError("empty data")
    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True)
    out = out.sort_values("timestamp")
    out = out.dropna()
    out = out.drop_duplicates(subset=["timestamp"], keep="first")
    if len(out) < min_length:
        raise ValueError("insufficient data")
    return out.reset_index(drop=True)
