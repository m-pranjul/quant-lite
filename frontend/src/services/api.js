export async function runBacktest(payload) {
  const response = await fetch('http://localhost:8000/backtest', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail || 'Backtest failed');
  }
  return response.json();
}
