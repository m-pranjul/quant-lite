export default function TradesTable({ trades }) {
  if (!trades?.length) return <p>No trades</p>;
  return (
    <table>
      <thead>
        <tr><th>Timestamp</th><th>Side</th><th>Shares</th><th>Price</th><th>Fee</th></tr>
      </thead>
      <tbody>
        {trades.map((t, i) => (
          <tr key={`${t.timestamp}-${i}`}>
            <td>{t.timestamp}</td><td>{t.side}</td><td>{t.shares}</td><td>{t.price.toFixed(2)}</td><td>{t.fee.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
