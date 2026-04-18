export default function ChartView({ equityCurve }) {
  if (!equityCurve?.length) return <p>No equity data</p>;
  return (
    <div>
      <h3>Equity Curve</h3>
      <pre style={{ maxHeight: 200, overflow: 'auto' }}>{JSON.stringify(equityCurve.slice(-20), null, 2)}</pre>
    </div>
  );
}
