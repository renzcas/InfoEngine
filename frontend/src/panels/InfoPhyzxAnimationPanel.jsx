import React, { useState, useEffect, useRef } from "react";
import InfoPhyzxHeatmap from "./InfoPhyzxHeatmap";

export default function InfoPhyzxAnimationPanel() {
  const [nodes, setNodes] = useState("A,B,C,D");
  const [edges, setEdges] = useState("A-B,B-C,C-D");
  const [steps, setSteps] = useState(50);
  const [dt, setDt] = useState(0.1);
  const [mode, setMode] = useState("propagate");

  const [timeline, setTimeline] = useState([]);
  const [frame, setFrame] = useState(0);
  const [playing, setPlaying] = useState(false);

  const intervalRef = useRef(null);

  const runExperiment = async () => {
    const nodeList = nodes.split(",").map(n => n.trim());
    const edgeList = edges.split(",").map(e => {
      const [a, b] = e.split("-");
      return [a.trim(), b.trim()];
    });

    const res = await fetch("/lab/infophyzx/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nodes: nodeList,
        edges: edgeList,
        steps,
        dt,
        mode
      })
    });

    const data = await res.json();
    setTimeline(data.timeline || []);
    setFrame(0);
    setPlaying(false);
    clearInterval(intervalRef.current);
  };

  const play = () => {
    if (!timeline.length) return;
    setPlaying(true);

    intervalRef.current = setInterval(() => {
      setFrame(f => {
        if (f + 1 >= timeline.length) {
          clearInterval(intervalRef.current);
          setPlaying(false);
          return f;
        }
        return f + 1;
      });
    }, 150);
  };

  const pause = () => {
    setPlaying(false);
    clearInterval(intervalRef.current);
  };

  const reset = () => {
    setPlaying(false);
    clearInterval(intervalRef.current);
    setFrame(0);
  };

  useEffect(() => {
    return () => clearInterval(intervalRef.current);
  }, []);

  const currentState = timeline[frame]?.state;

  const onScrub = (e: React.ChangeEvent<HTMLInputElement>) => {
    const idx = parseInt(e.target.value, 10);
    setFrame(idx);
  };

  return (
    <div className="panel">
      <h2>InfoPhyzx Animation Panel</h2>

      <label>Nodes</label>
      <input value={nodes} onChange={e => setNodes(e.target.value)} />

      <label>Edges</label>
      <input value={edges} onChange={e => setEdges(e.target.value)} />

      <label>Steps</label>
      <input
        type="number"
        value={steps}
        onChange={e => setSteps(parseInt(e.target.value, 10))}
      />

      <label>dt</label>
      <input
        type="number"
        step="0.01"
        value={dt}
        onChange={e => setDt(parseFloat(e.target.value))}
      />

      <label>Mode</label>
      <select value={mode} onChange={e => setMode(e.target.value)}>
        <option value="propagate">Propagate</option>
        <option value="diffuse">Diffuse</option>
        <option value="wave">Wave</option>
        <option value="laplacian">Laplacian</option>
        <option value="laplacian_normalized">Normalized Laplacian</option>
      </select>

      <button onClick={runExperiment}>Run Simulation</button>

      <div style={{ marginTop: "10px" }}>
        <button onClick={play} disabled={playing || !timeline.length}>Play</button>
        <button onClick={pause} disabled={!playing}>Pause</button>
        <button onClick={reset} disabled={!timeline.length}>Reset</button>
      </div>

      {timeline.length > 0 && (
        <div style={{ marginTop: "10px" }}>
          <input
            type="range"
            min={0}
            max={timeline.length - 1}
            value={frame}
            onChange={onScrub}
            style={{ width: "100%" }}
          />
        </div>
      )}

      <div style={{ marginTop: "20px" }}>
        <InfoPhyzxHeatmap state={currentState} />
      </div>

      <div style={{ marginTop: "10px" }}>
        Frame {timeline.length ? frame + 1 : 0} / {timeline.length}
      </div>
    </div>
  );
}
