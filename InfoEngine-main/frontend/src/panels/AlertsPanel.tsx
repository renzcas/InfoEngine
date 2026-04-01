// frontend/src/panels/AlertsPanel.tsx

export const AlertsPanel = ({ events, onThreatClick }) => {
  const alerts = events.filter(e => e.type === "alert");

  return (
    <div className="panel alerts-panel">
      <h2>Alerts</h2>
      <ul>
        {alerts.map(alert => (
          <li
            key={alert.id}
            className="alert-item"
            onClick={() => onThreatClick(alert)}
          >
            <strong>{alert.category}</strong> — {alert.reason}
          </li>
        ))}
      </ul>
    </div>
  );
};