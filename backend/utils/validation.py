"""Validation helpers."""

from datetime import date

from backend.core.constants import SUPPORTED_STRATEGIES


def validate_dates(start_date: date, end_date: date) -> None:
    if start_date > end_date:
        raise ValueError("start_date cannot be greater than end_date")


def validate_strategy_name(name: str) -> None:
    if name not in SUPPORTED_STRATEGIES:
        raise ValueError(f"unsupported strategy: {name}")
