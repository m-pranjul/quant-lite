import { useMemo, useState } from 'react';

const defaultsByStrategy = {
  sma_crossover: { short_window: 20, long_window: 50 },
  ema_crossover: { short_window: 12, long_window: 26 },
  rsi_strategy: { window: 14, oversold: 30, overbought: 70 },
  buy_and_hold: {},
};

const defaultForm = {
  ticker: 'RELIANCE.NS',
  start_date: '2020-01-01',
  end_date: '2023-01-01',
  strategy: 'sma_crossover',
  initial_capital: 100000,
  transaction_cost: 0.001,
  slippage: 0.001,
};

function fieldDefs(strategy) {
  if (strategy === 'buy_and_hold') return [];
  if (strategy === 'rsi_strategy') {
    return [
      ['window', 'Window'],
      ['oversold', 'Oversold'],
      ['overbought', 'Overbought'],
    ];
  }
  return [
    ['short_window', 'Short Window'],
    ['long_window', 'Long Window'],
  ];
}

export default function InputForm({ onSubmit, loading }) {
  const [form, setForm] = useState(defaultForm);
  const [params, setParams] = useState(defaultsByStrategy[defaultForm.strategy]);

  const dynamicFields = useMemo(() => fieldDefs(form.strategy), [form.strategy]);

  function update(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  function updateStrategy(strategy) {
    setForm((prev) => ({ ...prev, strategy }));
    setParams(defaultsByStrategy[strategy]);
  }

  function updateParam(key, value) {
    setParams((prev) => ({ ...prev, [key]: Number(value) }));
  }

  function submit(evt) {
    evt.preventDefault();
    onSubmit({ ...form, params });
  }

  return (
    <section className="card">
      <h2>Run Backtest</h2>
      <form onSubmit={submit}>
        <div className="grid">
          <label>
            Ticker
            <input value={form.ticker} onChange={(e) => update('ticker', e.target.value)} required />
          </label>
          <label>
            Start Date
            <input type="date" value={form.start_date} onChange={(e) => update('start_date', e.target.value)} required />
          </label>
          <label>
            End Date
            <input type="date" value={form.end_date} onChange={(e) => update('end_date', e.target.value)} required />
          </label>
          <label>
            Strategy
            <select value={form.strategy} onChange={(e) => updateStrategy(e.target.value)}>
              <option value="sma_crossover">SMA Crossover</option>
              <option value="ema_crossover">EMA Crossover</option>
              <option value="rsi_strategy">RSI Strategy</option>
              <option value="buy_and_hold">Buy & Hold</option>
            </select>
          </label>
          <label>
            Initial Capital
            <input type="number" min="1" step="1" value={form.initial_capital} onChange={(e) => update('initial_capital', Number(e.target.value))} required />
          </label>
          <label>
            Transaction Cost
            <input type="number" min="0" step="0.0001" value={form.transaction_cost} onChange={(e) => update('transaction_cost', Number(e.target.value))} required />
          </label>
          <label>
            Slippage
            <input type="number" min="0" step="0.0001" value={form.slippage} onChange={(e) => update('slippage', Number(e.target.value))} required />
          </label>
          {dynamicFields.map(([key, label]) => (
            <label key={key}>
              {label}
              <input
                type="number"
                min="0"
                step="1"
                value={params[key] ?? ''}
                onChange={(e) => updateParam(key, e.target.value)}
                required
              />
            </label>
          ))}
        </div>
        <div style={{ marginTop: 12 }}>
          <button type="submit" disabled={loading}>{loading ? 'Running…' : 'Run Backtest'}</button>
        </div>
      </form>
    </section>
  );
}
