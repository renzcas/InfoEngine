import React, { useState, useEffect, useRef } from "react";
import InfoPhyzxHeatmap from "./InfoPhyzxHeatmap";

export default function InfoPhyzxSuperPanel() {
  // -------------------------------------------------------
  // State
  // -------------------------------------------------------
  const [nodes, setNodes] = useState("A,B,C,D");
  const [edges, setEdges] = useState("A-B,B-C,C-D");

  const [mode, setMode] = useState("propagate");
  const [dt, setDt] = useState(0.1);
  const [D, setD] = useState(0.1);
  const [influence, setInfluence] = useState(0.05);
  const [c, setC] = useState(1.0);

  const [steps, setSteps] = useState(50);
  const [timeline, setTimeline] = useState([]);
  const [frame, setFrame] = useState(0);
  const [playing, setPlaying] = useState(false);

  const [liveState, setLiveState] = useState(null);
  const [liveConnected, setLiveConnected] = useState(false);

  const wsRef = useRef(null);
  const intervalRef = useRef(null);

  // -------------------------------------------------------
  // Field Init
  // -------------------------------------------------------
  const initField = async () => {
    const nodeList = nodes.split(",").map(n => n.trim());
    const edgeList = edges.split(",").map(e => {
      const [a, b] = e.split("-");
      return [a.trim(), b.trim()];
    });

    await fetch("/infophyzx/field/init", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nodes: nodeList, edges: edgeList })
    });
  };

  // -------------------------------------------------------
  // Manual Step
  // -------------------------------------------------------
  const runStep = async () => {
    const res = await fetch("/infophyzx/step", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode, dt, D, influence, c })
    });

    const data = await res.json();
    setLiveState(data.state);
  };

  // -------------------------------------------------------
  // Animation (Experiment Lab)
  // -------------------------------------------------------
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

  // -------------------------------------------------------
  // WebSocket Live Stream
  // -------------------------------------------------------
  const connectLive = () => {
    if (wsRef.current) return;

    const ws = new WebSocket("ws://localhost:8000/infophyzx/live");
    wsRef.current = ws;

    ws.onopen = () => setLiveConnected(true);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.state) setLiveState(data.state);
      } catch (err) {
        console.error("Bad WS message:", err);
      }
    };

    ws.onclose = () => {
      setLiveConnected(false);
      wsRef.current = null;
    };
  };

  const disconnectLive = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      clearInterval(intervalRef.current);
      disconnectLive();
    };
  }, []);

  // -------------------------------------------------------
  // Render
  // -------------------------------------------------------
  const currentFrameState = timeline[frame]?.state;

  return (
    <div className="panel">
      <h1>InfoPhyzx Super Panel</h1>

      {/* Controls */}
      <div className="controls">
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
        <input type="number" step="0.01" value={dt} onChange={e => setDt(parseFloat(e.target.value))} />

        <label>D</label>
        <input type="number" step="0.01" value={D} onChange={e => setD(parseFloat(e.target.value))} />

        <label>Influence</label>
        <input type="number" step="0.01" value={influence} onChange={e => setInfluence(parseFloat(e.target.value))} />

        <label>c</label>
        <input type="number" step="0.1" value={c} onChange={e => setC(parseFloat(e.target.value))} />

        <button onClick={initField}>Init Field</button>
        <button onClick={runStep}>Step</button>
      </div>

      {/* Live Stream */}
      <h2>Live Stream</h2>
      <button onClick={connectLive} disabled={liveConnected}>Connect</button>
      <button onClick={disconnectLive} disabled={!liveConnected}>Disconnect</button>
      <InfoPhyzxHeatmap state={liveState} />

      {/* Animation */}
      <h2>Animation</h2>
      <label>Steps</label>
      <input type="number" value={steps} onChange={e => setSteps(parseInt(e.target.value))} />

      <button onClick={runExperiment}>Run Simulation</button>
      <button onClick={play} disabled={playing || !timeline.length}>Play</button>
      <button onClick={pause} disabled={!playing}>Pause</button>
      <button onClick={reset} disabled={!timeline.length}>Reset</button>

      {timeline.length > 0 && (
        <input
          type="range"
          min={0}
          max={timeline.length - 1}
          value={frame}
          onChange={e => setFrame(parseInt(e.target.value))}
          style={{ width: "100%", marginTop: "10px" }}
        />
      )}

      <InfoPhyzxHeatmap state={currentFrameState} />
      <div>Frame {frame + 1} / {timeline.length}</div>
    </div>
  );
}
