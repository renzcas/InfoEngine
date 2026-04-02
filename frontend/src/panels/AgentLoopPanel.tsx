import React, { useState } from "react";
import { api } from "../api";

export default function AgentLoopPanel() {
  const [startNode, setStartNode] = useState("A");
  const [history, setHistory] = useState([]);

  const start = async () => {
    const result = await api.post("/agent/start", { start: startNode });
    setHistory([result]);
  };

  const step = async () => {
    const result = await api.post("/agent/step", {});
    setHistory((h) => [...h, result]);
  };

  const run = async () => {
    const result = await api.post("/agent/run", { steps: 10 });
    setHistory(result);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Agent Loop Visualizer</h2>

      <input
        value={startNode}
        onChange={(e) => setStartNode(e.target.value)}
        placeholder="Start Node"
      />

      <div style={{ display: "flex", gap: 10, marginTop: 10 }}>
        <button onClick={start}>Start</button>
        <button onClick={step}>Step</button>
        <button onClick={run}>Run Loop</button>
      </div>

      <pre style={{ background: "#111", color: "#0f0", padding: 10 }}>
        {JSON.stringify(history, null, 2)}
      </pre>
    </div>
  );
}
