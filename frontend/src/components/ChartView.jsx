function toPath(values, width, height, pad = 12) {
  if (!values.length) return '';
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  return values
    .map((v, i) => {
      const x = pad + (i / Math.max(values.length - 1, 1)) * (width - 2 * pad);
      const y = height - pad - ((v - min) / span) * (height - 2 * pad);
      return `${i === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`;
    })
    .join(' ');
}

export default function ChartView({ equityCurve }) {
  if (!equityCurve?.length) {
    return (
      <section className="card">
        <h2>Equity Curve</h2>
        <p className="muted">Run a backtest to render the chart.</p>
      </section>
    );
  }

  const values = equityCurve.map((p) => Number(p.equity));
  const path = toPath(values, 960, 240);

  return (
    <section className="card">
      <h2>Equity Curve</h2>
      <svg viewBox="0 0 960 240" role="img" aria-label="Backtest equity curve">
        <path d={path} fill="none" stroke="#2563eb" strokeWidth="2.5" />
      </svg>
      <p className="muted" style={{ marginBottom: 0 }}>
        Start: {values[0].toFixed(2)} | End: {values[values.length - 1].toFixed(2)}
      </p>
    </section>
  );
}
