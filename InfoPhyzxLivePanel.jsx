import React, { useState, useEffect, useRef } from "react";
import InfoPhyzxHeatmap from "./InfoPhyzxHeatmap";

export default function InfoPhyzxLivePanel() {
  const [connected, setConnected] = useState(false);
  const [state, setState] = useState(null);

  const wsRef = useRef(null);

  const connect = () => {
    if (wsRef.current) return;

    const ws = new WebSocket("ws://localhost:8000/infophyzx/live");
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.state) {
          setState(data.state);
        }
      } catch (err) {
        console.error("Bad WS message:", err);
      }
    };

    ws.onclose = () => {
      setConnected(false);
      wsRef.current = null;
    };
  };

  const disconnect = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  };

  useEffect(() => {
    return () => disconnect();
  }, []);

  return (
    <div className="panel">
      <h2>InfoPhyzx Live Stream</h2>

      <button onClick={connect} disabled={connected}>
        Connect
      </button>
      <button onClick={disconnect} disabled={!connected} style={{ marginLeft: "10px" }}>
        Disconnect
      </button>

      <div style={{ marginTop: "20px" }}>
        <InfoPhyzxHeatmap state={state} />
      </div>

      <div style={{ marginTop: "10px" }}>
        {connected ? "Connected" : "Disconnected"}
      </div>
    </div>
  );
}
