function formatMetric(name, value) {
  if (!Number.isFinite(value)) return String(value);
  if (name.includes('rate') || name.includes('return') || name.includes('drawdown') || name === 'cagr') {
    return `${(value * 100).toFixed(2)}%`;
  }
  return value.toFixed(4);
}

export default function MetricsPanel({ metrics }) {
  return (
    <section className="card">
      <h2>Metrics</h2>
      {!metrics ? (
        <p className="muted">No metrics yet.</p>
      ) : (
        <div className="metrics">
          {Object.entries(metrics).map(([k, v]) => (
            <div key={k} className="metric">
              <div className="name">{k.replaceAll('_', ' ')}</div>
              <div className="value">{formatMetric(k, v)}</div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
