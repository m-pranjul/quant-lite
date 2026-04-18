import pandas as pd
import pytest

from backend.data.preprocess import preprocess_data


def test_empty_data_rejected():
    df = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
    with pytest.raises(ValueError, match="empty data"):
        preprocess_data(df)


def test_invalid_ticker_like_empty_data():
    # invalid ticker fetch is expected to yield empty dataframe
    df = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
    with pytest.raises(ValueError):
        preprocess_data(df)
