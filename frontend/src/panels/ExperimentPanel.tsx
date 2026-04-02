import React, { useState } from "react";
import { api } from "../api";
import ForceGraph2D from "react-force-graph-2d";

export default function ExperimentPanel() {
  const [input, setInput] = useState('{ "test": "graph" }');
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

      <div style={{ display: "flex", gap: "10px", marginBottom: "10px" }}>
        <button onClick={() => setInput('{ "test": "graph" }')}>Graph</button>
        <button onClick={() => setInput('{ "test": "red" }')}>Red</button>
        <button onClick={() => setInput('{ "test": "blue" }')}>Blue</button>
        <button onClick={() => setInput('{ "test": "overlay" }')}>Overlay</button>
      </div>

      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        rows={6}
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

      {/* Graph Viewer */}
      {output?.graph_nodes && output?.graph_edges && (
        <ForceGraph2D
          graphData={{
            nodes: output.graph_nodes.map((n) => ({ id: n })),
            links: output.graph_edges.map(([s, t]) => ({ source: s, target: t })),
          }}
          width={800}
          height={500}
        />
      )}

      {/* Red + Blue Overlay Viewer */}
      {output?.overlay && (
        <ForceGraph2D
          graphData={{
            nodes: [
              ...new Set([
                ...output.overlay.red_paths.flatMap((p) => p.path),
                ...output.overlay.blue_defense.flatMap((d) => d.nodes || []),
              ]),
            ].map((n) => ({ id: n })),

            links: [
              ...output.overlay.red_paths.flatMap((p) =>
                p.path.slice(0, -1).map((s, i) => ({
                  source: s,
                  target: p.path[i + 1],
                  color: "red",
                }))
              ),
              ...output.overlay.blue_defense.flatMap((d) =>
                (d.nodes || []).slice(0, -1).map((s, i) => ({
                  source: s,
                  target: d.nodes[i + 1],
                  color: "blue",
                }))
              ),
            ],
          }}
          linkColor={(link) => link.color}
          width={800}
          height={500}
        />
      )}
    </div>
  );
}
