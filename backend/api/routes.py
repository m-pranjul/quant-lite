"""API routes."""

from fastapi import APIRouter, HTTPException

from backend.api.schemas import BacktestRequest, BacktestResponse
from backend.data.fetch import DataFetchError, fetch_ohlcv
from backend.data.preprocess import preprocess_data
from backend.engine.backtester import run_backtest
from backend.strategies.buy_and_hold import BuyAndHoldStrategy
from backend.strategies.ema_crossover import EMACrossoverStrategy
from backend.strategies.rsi_strategy import RSIStrategy
from backend.strategies.sma_crossover import SMACrossoverStrategy
from backend.utils.validation import validate_dates, validate_strategy_name

router = APIRouter()


def _strategy_factory(name: str, params: dict):
    mapping = {
        "sma_crossover": SMACrossoverStrategy,
        "ema_crossover": EMACrossoverStrategy,
        "rsi_strategy": RSIStrategy,
        "buy_and_hold": BuyAndHoldStrategy,
    }
    return mapping[name](params)


@router.post("/backtest", response_model=BacktestResponse)
def backtest(payload: BacktestRequest):
    try:
        validate_dates(payload.start_date, payload.end_date)
        validate_strategy_name(payload.strategy)
        raw = fetch_ohlcv(payload.ticker, str(payload.start_date), str(payload.end_date))
        data = preprocess_data(raw)
        strategy = _strategy_factory(payload.strategy, payload.params)
        signals = strategy.generate_signals(data)
        result = run_backtest(
            data=data,
            signals=signals,
            initial_capital=payload.initial_capital,
            transaction_cost=payload.transaction_cost,
            slippage=payload.slippage,
        )
        return result
    except DataFetchError as exc:
        raise HTTPException(status_code=400, detail=f"data provider error: {exc}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"data processing error: {exc}") from exc
    except Exception as exc:  # unexpected data provider issues etc.
        raise HTTPException(status_code=500, detail=f"internal error: {exc}") from exc
