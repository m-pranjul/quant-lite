"""RSI mean-reversion strategy."""

import pandas as pd

from backend.strategies.base import BaseStrategy
from backend.utils.indicators import rsi


class RSIStrategy(BaseStrategy):
    def validate_params(self) -> None:
        self.window = int(self.params.get("window", 14))
        self.oversold = float(self.params.get("oversold", 30))
        self.overbought = float(self.params.get("overbought", 70))
        if self.window <= 0:
            raise ValueError("window must be > 0")
        if not (0 <= self.oversold < self.overbought <= 100):
            raise ValueError("invalid RSI bounds")

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        values = rsi(data["close"], self.window)
        signal = pd.Series(0, index=data.index, dtype=int)
        signal[values < self.oversold] = 1
        signal[values > self.overbought] = -1
        return signal.shift(1).fillna(0).astype(int)
