"""Buy once and hold."""

import pandas as pd

from backend.strategies.base import BaseStrategy


class BuyAndHoldStrategy(BaseStrategy):
    def validate_params(self) -> None:
        return None

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        signal = pd.Series(0, index=data.index, dtype=int)
        if not signal.empty:
            signal.iloc[1] = 1 if len(signal) > 1 else 0
        return signal
