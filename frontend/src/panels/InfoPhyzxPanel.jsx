import React, { useState } from "react";
import InfoPhyzxHeatmap from "./InfoPhyzxHeatmap";

export default function InfoPhyzxPanel() {
  const [nodes, setNodes] = useState("A,B,C,D");
  const [edges, setEdges] = useState("A-B,B-C,C-D");
  const [mode, setMode] = useState("propagate");
  const [dt, setDt] = useState(0.1);
  const [D, setD] = useState(0.1);
  const [influence, setInfluence] = useState(0.05);
  const [c, setC] = useState(1.0);
  const [output, setOutput] = useState(null);

  const initField = async () => {
    const nodeList = nodes.split(",").map(n => n.trim());
    const edgeList = edges.split(",").map(e => {
      const [a, b] = e.split("-");
      return [a.trim(), b.trim()];
    });

    await fetch("/infophyzx/field/init", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nodes: nodeList,
        edges: edgeList
      })
    });
  };

  const runStep = async () => {
    const res = await fetch("/infophyzx/step", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mode,
        dt,
        D,
        influence,
        c
      })
    });

    const data = await res.json();
    setOutput(data);
  };

  return (
    <div className="panel">
      <h2>InfoPhyzx Field Engine</h2>

      <label>Nodes</label>
      <input value={nodes} onChange={e => setNodes(e.target.value)} />

      <label>Edges</label>
      <input value={edges} onChange={e => setEdges(e.target.value)} />

      <label>Mode</label>
      <select value={mode} onChange={e => setMode(e.target.value)}>
        <option value="propagate">Propagate</option>
        <option value="diffuse">Diffuse</option>
        <option value="wave">Wave</option>
        <option value="laplacian">Laplacian</option>
        <option value="laplacian_normalized">Normalized Laplacian</option>
      </select>

      <label>dt</label>
      <input
        type="number"
        step="0.01"
        value={dt}
        onChange={e => setDt(parseFloat(e.target.value))}
      />

      <label>D (diffusion)</label>
      <input
        type="number"
        step="0.01"
        value={D}
        onChange={e => setD(parseFloat(e.target.value))}
      />

      <label>Influence</label>
      <input
        type="number"
        step="0.01"
        value={influence}
        onChange={e => setInfluence(parseFloat(e.target.value))}
      />

      <label>c (wave speed)</label>
      <input
        type="number"
        step="0.1"
        value={c}
        onChange={e => setC(parseFloat(e.target.value))}
      />

      <div style={{ marginTop: "10px" }}>
        <button onClick={initField}>Init Field</button>
        <button onClick={runStep} style={{ marginLeft: "10px" }}>
          Run Step
        </button>
      </div>

      <div style={{ marginTop: "20px" }}>
        <InfoPhyzxHeatmap state={output?.state} />
      </div>
    </div>
  );
}
