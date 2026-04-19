"""Strategy abstraction."""

from abc import ABC, abstractmethod

import pandas as pd


class BaseStrategy(ABC):
    def __init__(self, params: dict | None = None) -> None:
        self.params = params or {}
        self.validate_params()

    @abstractmethod
    def validate_params(self) -> None:
        """Validate strategy parameters."""

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Return {-1,0,1} signals indexed like input data."""
