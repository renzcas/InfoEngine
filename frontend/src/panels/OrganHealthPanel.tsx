import React, { useState } from "react";
import { api } from "../api";

export default function OrganHealthPanel() {
  const [health, setHealth] = useState(null);

  const load = async () => {
    const result = await api.get("/health/organs");
    setHealth(result);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Organ Health Dashboard</h2>

      <button onClick={load}>Load Health</button>

      {health && (
        <pre style={{ background: "#111", color: "#0f0", padding: 10 }}>
          {JSON.stringify(health, null, 2)}
        </pre>
      )}
    </div>
  );
}
