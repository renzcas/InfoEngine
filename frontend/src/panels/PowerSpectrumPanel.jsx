import React, { useState } from "react";

export default function PowerSpectrumPanel() {
  const [signal, setSignal] = useState("1, 2, 3, 4, 5");
  const [sampleRate, setSampleRate] = useState(1.0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    setLoading(true);

    const payload = {
      signal: signal.split(",").map(Number),
      sample_rate: parseFloat(sampleRate)
    };

    const res = await fetch("/api/organ/physics/power_spectrum", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={{ padding: "20px", border: "1px solid #444", borderRadius: "8px" }}>
      <h2>Power Spectrum Panel</h2>

      <label>Signal (comma-separated):</label>
      <input
        type="text"
        value={signal}
        onChange={(e) => setSignal(e.target.value)}
        style={{ width: "100%", marginBottom: "10px" }}
      />

      <label>Sample Rate:</label>
      <input
        type="number"
        value={sampleRate}
        onChange={(e) => setSampleRate(e.target.value)}
        style={{ width: "100%", marginBottom: "10px" }}
      />

      <button onClick={analyze} disabled={loading}>
        {loading ? "Analyzing..." : "Run Power Spectrum"}
      </button>

      {result && (
        <pre style={{ marginTop: "20px", background: "#222", padding: "10px" }}>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}