# quantlite

Deterministic minimal backtesting web app (Phase 1).

## Backend

```bash
pip install -r requirements.txt
./run.sh
```

`POST /backtest` input:

```json
{
  "ticker": "RELIANCE.NS",
  "start_date": "2020-01-01",
  "end_date": "2023-01-01",
  "strategy": "sma_crossover",
  "params": {"short_window": 20, "long_window": 50},
  "initial_capital": 100000,
  "transaction_cost": 0.001,
  "slippage": 0.001
}
```

Response fields: `equity_curve`, `trades`, `metrics`.

## Frontend

Minimal React app in `frontend/src` that calls backend `/backtest` and renders form + results.

## Tests

```bash
pytest backend/tests -q
```
