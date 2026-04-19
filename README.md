# quantlite

Deterministic minimal backtesting web app (Phase 1).

## Backend

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
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

```bash
cd frontend
npm install
npm run dev
```

The frontend calls `http://localhost:8000/backtest`.

## Tests

```bash
pytest backend/tests -q
```

## Troubleshooting

If `/backtest` returns `400` with a provider-style message (for example `unable to fetch market data`), Yahoo data retrieval failed in your environment.
This can happen due to network/proxy/country-specific blocking from Yahoo endpoints.
Try another ticker and verify your network can access Yahoo Finance.

If message starts with `data processing error`, the fetch worked but OHLC rows were invalid after cleanup (for example missing/NaN prices or too few rows).
