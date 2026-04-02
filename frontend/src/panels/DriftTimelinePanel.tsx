import React, { useState } from "react";
import { api } from "../api";

export default function DriftTimelinePanel() {
  const [timeline, setTimeline] = useState([]);
  const [drift, setDrift] = useState(null);
  const [t1, setT1] = useState("");
  const [t2, setT2] = useState("");

  const loadTimeline = async () => {
    const result = await api.get("/drift/timeline");
    setTimeline(result.timeline || []);
  };

  const compute = async () => {
    const result = await api.post("/drift/compute", { t1, t2 });
    setDrift(result);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Drift Timeline</h2>

      <button onClick={loadTimeline}>Load Timeline</button>

      <pre style={{ background: "#111", color: "#0f0", padding: 10 }}>
        {JSON.stringify(timeline, null, 2)}
      </pre>

      <h3>Compute Drift</h3>
      <input
        placeholder="Timestamp 1"
        value={t1}
        onChange={(e) => setT1(e.target.value)}
      />
      <input
        placeholder="Timestamp 2"
        value={t2}
        onChange={(e) => setT2(e.target.value)}
      />
      <button onClick={compute}>Compute</button>

      {drift && (
        <pre style={{ background: "#111", color: "#0f0", padding: 10 }}>
          {JSON.stringify(drift, null, 2)}
        </pre>
      )}
    </div>
  );
}
