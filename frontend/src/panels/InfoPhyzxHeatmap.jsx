import React from "react";

export default function InfoPhyzxHeatmap({ state }) {
  if (!state) {
    return <div>No state yet</div>;
  }

  const nodes = Object.keys(state);
  const values = Object.values(state);

  // Normalize values to [0,1]
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;

  const normalize = v => (v - min) / range;

  const colorFor = v => {
    const t = normalize(v);
    const r = Math.floor(255 * t);
    const b = Math.floor(255 * (1 - t));
    return `rgb(${r}, 0, ${b})`;
  };

  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: `repeat(${nodes.length}, 40px)`,
      gap: "4px",
      marginTop: "20px"
    }}>
      {nodes.map(node => (
        <div key={node} style={{
          width: "40px",
          height: "40px",
          background: colorFor(state[node]),
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "white",
          fontSize: "12px",
          borderRadius: "4px"
        }}>
          {node}
        </div>
      ))}
    </div>
  );
}
