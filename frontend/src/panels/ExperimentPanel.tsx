import React, { useState } from "react";
import { api } from "../api";

export default function ExperimentPanel() {
  const [input, setInput] = useState("{}");
  const [output, setOutput] = useState(null);

  const run = async () => {
    try {
      const payload = JSON.parse(input);
      const result = await api.post("/lab/run", payload);
      setOutput(result);
    } catch (err) {
      setOutput({ error: "Invalid JSON input" });
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Experiment Lab</h2>

      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        rows={8}
        style={{ width: "100%", fontFamily: "monospace" }}
      />

      <button onClick={run} style={{ marginTop: "10px" }}>
        Run Experiment
      </button>

      {output && (
        <pre style={{ marginTop: "20px", background: "#111", color: "#0f0", padding: "10px" }}>
          {JSON.stringify(output, null, 2)}
        </pre>
      )}
    </div>
  );
}
