import { useState } from 'react';

const defaultForm = {
  ticker: 'RELIANCE.NS',
  start_date: '2020-01-01',
  end_date: '2023-01-01',
  strategy: 'sma_crossover',
  params: { short_window: 20, long_window: 50 },
  initial_capital: 100000,
  transaction_cost: 0.001,
  slippage: 0.001,
};

export default function InputForm({ onSubmit, loading }) {
  const [form, setForm] = useState(defaultForm);

  function update(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSubmit(form); }}>
      <input value={form.ticker} onChange={(e) => update('ticker', e.target.value)} />
      <input type="date" value={form.start_date} onChange={(e) => update('start_date', e.target.value)} />
      <input type="date" value={form.end_date} onChange={(e) => update('end_date', e.target.value)} />
      <select value={form.strategy} onChange={(e) => update('strategy', e.target.value)}>
        <option value="sma_crossover">SMA Crossover</option>
        <option value="ema_crossover">EMA Crossover</option>
        <option value="rsi_strategy">RSI Strategy</option>
        <option value="buy_and_hold">Buy & Hold</option>
      </select>
      <input
        type="number"
        value={form.initial_capital}
        onChange={(e) => update('initial_capital', Number(e.target.value))}
      />
      <button type="submit" disabled={loading}>{loading ? 'Running...' : 'Run Backtest'}</button>
    </form>
  );
}
