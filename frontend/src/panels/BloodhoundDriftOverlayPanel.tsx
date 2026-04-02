import React, { useState } from "react";
import { api } from "../api";
import ForceGraph2D from "react-force-graph-2d";

export default function BloodhoundDriftOverlayPanel() {
  const [snapshot, setSnapshot] = useState(null);

  const load = async () => {
    const result = await api.get("/bloodhound/snapshot");
    setSnapshot(result);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Bloodhound Drift Overlay</h2>

      <button onClick={load}>Load Snapshot</button>

      {snapshot && (
        <ForceGraph2D
          graphData={{
            nodes: snapshot.nodes.map((n) => ({ id: n })),
            links: snapshot.edges.map(([s, t]) => ({
              source: s,
              target: t,
              color: "purple",
            })),
          }}
          linkColor={(l) => l.color}
          width={800}
          height={500}
        />
      )}
    </div>
  );
}
