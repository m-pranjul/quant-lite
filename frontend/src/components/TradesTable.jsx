export default function TradesTable({ trades }) {
  return (
    <section className="card">
      <h2>Trades</h2>
      {!trades?.length ? (
        <p className="muted">No trades generated.</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Side</th>
                <th>Shares</th>
                <th>Price</th>
                <th>Notional</th>
                <th>Fee</th>
              </tr>
            </thead>
            <tbody>
              {trades.map((t, i) => (
                <tr key={`${t.timestamp}-${i}`}>
                  <td>{new Date(t.timestamp).toLocaleString()}</td>
                  <td>{t.side}</td>
                  <td>{t.shares}</td>
                  <td>{Number(t.price).toFixed(2)}</td>
                  <td>{Number(t.notional).toFixed(2)}</td>
                  <td>{Number(t.fee).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
