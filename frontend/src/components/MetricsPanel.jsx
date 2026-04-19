export default function MetricsPanel({ metrics }) {
  if (!metrics) return <p>No metrics</p>;
  return (
    <div>
      <h3>Metrics</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(120px,1fr))', gap: 8 }}>
        {Object.entries(metrics).map(([k, v]) => (
          <div key={k} style={{ border: '1px solid #ddd', padding: 8 }}>
            <strong>{k}</strong>
            <div>{Number.isFinite(v) ? v.toFixed(4) : String(v)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
