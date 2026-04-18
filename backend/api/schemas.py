"""API schemas."""

from datetime import date

from pydantic import BaseModel, Field


class BacktestRequest(BaseModel):
    ticker: str = Field(..., min_length=1)
    start_date: date
    end_date: date
    strategy: str
    params: dict = Field(default_factory=dict)
    initial_capital: float = Field(..., gt=0)
    transaction_cost: float = Field(default=0.0, ge=0)
    slippage: float = Field(default=0.0, ge=0)


class BacktestResponse(BaseModel):
    equity_curve: list[dict]
    trades: list[dict]
    metrics: dict
