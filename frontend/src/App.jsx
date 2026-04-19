import { useState } from 'react';
import InputForm from './components/InputForm';
import ChartView from './components/ChartView';
import MetricsPanel from './components/MetricsPanel';
import TradesTable from './components/TradesTable';
import { runBacktest } from './services/api';

export default function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function onSubmit(payload) {
    setLoading(true);
    setError('');
    try {
      const data = await runBacktest(payload);
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: 960, margin: '0 auto', padding: 16 }}>
      <h1>quantlite</h1>
      <InputForm onSubmit={onSubmit} loading={loading} />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <MetricsPanel metrics={result?.metrics} />
      <ChartView equityCurve={result?.equity_curve} />
      <TradesTable trades={result?.trades} />
    </main>
  );
}
