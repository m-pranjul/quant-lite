import pandas as pd

from backend.utils.indicators import rsi, sma


def test_sma_correctness():
    s = pd.Series([1, 2, 3, 4, 5])
    out = sma(s, 3)
    assert out.iloc[2] == 2
    assert out.iloc[4] == 4


def test_rsi_in_range():
    s = pd.Series([10, 11, 10, 12, 11, 13, 14, 12, 13, 15, 16, 15, 17, 18, 17, 19])
    out = rsi(s, 14).dropna()
    assert ((out >= 0) & (out <= 100)).all()
