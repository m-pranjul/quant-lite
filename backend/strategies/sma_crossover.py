"""SMA crossover strategy."""

import pandas as pd

from backend.strategies.base import BaseStrategy
from backend.utils.indicators import sma


class SMACrossoverStrategy(BaseStrategy):
    def validate_params(self) -> None:
        self.short_window = int(self.params.get("short_window", 20))
        self.long_window = int(self.params.get("long_window", 50))
        if self.short_window <= 0 or self.long_window <= 0:
            raise ValueError("windows must be > 0")
        if self.short_window >= self.long_window:
            raise ValueError("short_window must be less than long_window")

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        short = sma(data["close"], self.short_window)
        long = sma(data["close"], self.long_window)
        signal = pd.Series(0, index=data.index, dtype=int)
        signal[short > long] = 1
        signal[short < long] = -1
        return signal.shift(1).fillna(0).astype(int)
