import React, { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

// ------------------------------------------------------------
// Utility: color logic for agents
// ------------------------------------------------------------
function colorForAgent(valence: number, tension: number) {
  const v = Math.max(-1, Math.min(1, valence));
  const t = Math.max(0, Math.min(10, tension)) / 10;
  const base = v >= 0 ? [0, 200, 120] : [220, 60, 60];
  const mix = (c: number) => Math.round(c * (0.4 + 0.6 * t));
  return `rgb(${mix(base[0])}, ${mix(base[1])}, ${mix(base[2])})`;
}

// ------------------------------------------------------------
// 2D Geometry Field (curvature heatmap + flow vectors + attractors)
// ------------------------------------------------------------
function GeometryField2D({ geometry }) {
  const { grid_size, curvature_field, flow_vectors, attractors } = geometry;
  const [w, h] = grid_size;

  return (
    <svg width={400} height={400} style={{ background: "#050505", borderRadius: 8 }}>
      {curvature_field.map((c, i) => {
        const x = i % w;
        const y = Math.floor(i / w);
        const v = Math.max(0, Math.min(1, (c + 1) / 2));
        const color = `rgba(${Math.round(255 * v)}, 0, ${Math.round(255 * (1 - v))}, 0.7)`;
        return (
          <rect
            key={i}
            x={(x / w) * 400}
            y={(y / h) * 400}
            width={400 / w}
            height={400 / h}
            fill={color}
          />
        );
      })}

      {flow_vectors.map((v, i) => (
        <line
          key={`v-${i}`}
          x1={v.x * 400}
          y1={v.y * 400}
          x2={(v.x + v.vx * 0.05) * 400}
          y2={(v.y + v.vy * 0.05) * 400}
          stroke="#ffffff55"
          strokeWidth={1}
        />
      ))}

      {attractors.map(a => (
        <circle
          key={a.id}
          cx={a.x * 400}
          cy={a.y * 400}
          r={6 + a.strength * 3}
          fill="#ffcc00"
        />
      ))}
    </svg>
  );
}

// ------------------------------------------------------------
// Agent Scatter Plot (valence vs tension, size = surprise)
// ------------------------------------------------------------
function AgentScatterPlot({ agents, onSelect }) {
  return (
    <svg width={400} height={260} style={{ background: "#111", borderRadius: 8 }}>
      {agents.map(a => (
        <circle
          key={a.id}
          cx={200 + a.tension * 20}
          cy={130 - a.valence * 40}
          r={6 + a.surprise * 4}
          fill={colorForAgent(a.valence, a.tension)}
          onClick={() => onSelect(a.id)}
          style={{ cursor: "pointer" }}
        />
      ))}
    </svg>
  );
}

// ------------------------------------------------------------
// Agent Detail Panel
// ------------------------------------------------------------
function AgentDetailPanel({ agentId, history }) {
  if (!agentId) return <div style={{ color: "#777" }}>Select an agent…</div>;

  const series = history.filter(h => h.id === agentId);

  return (
    <div style={{ padding: 12, background: "#111", borderRadius: 8 }}>
      <h3>Agent {agentId}</h3>
      <ul>
        {series.slice(-20).map((s, i) => (
          <li key={i}>
            t={s.timestamp.toFixed(1)} · v={s.valence.toFixed(2)} · τ={s.tension.toFixed(2)} · σ={s.surprise.toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
}

// ------------------------------------------------------------
// Time Travel Scrubber
// ------------------------------------------------------------
function TimelineScrubber({ timeline, index, setIndex }) {
  if (!timeline.length) return null;

  return (
    <div style={{ marginTop: 10 }}>
      <input
        type="range"
        min={0}
        max={timeline.length - 1}
        value={index ?? timeline.length - 1}
        onChange={e => setIndex(Number(e.target.value))}
        style={{ width: "100%" }}
      />
      <button onClick={() => setIndex(null)} style={{ marginTop: 4 }}>
        Live
      </button>
    </div>
  );
}

// ------------------------------------------------------------
// 3D Field Visualization
// ------------------------------------------------------------
function Field3D({ geometry, agents }) {
  const { grid_size } = geometry;
  const [w, h] = grid_size;

  return (
    <Canvas camera={{ position: [0, 0, 5] }}>
      <color attach="background" args={["#000"]} />
      <ambientLight intensity={0.4} />
      <pointLight position={[5, 5, 5]} />

      <mesh rotation-x={-Math.PI / 2}>
        <planeGeometry args={[4, 4, w - 1, h - 1]} />
        <meshStandardMaterial color="#222" wireframe />
      </mesh>

      {agents.map(a => (
        <mesh key={a.id} position={[a.valence, a.tension / 3, a.surprise]}>
          <sphereGeometry args={[0.05 + a.surprise * 0.1, 16, 16]} />
          <meshStandardMaterial color={colorForAgent(a.valence, a.tension)} />
        </mesh>
      ))}

      <OrbitControls />
    </Canvas>
  );
}

// ------------------------------------------------------------
// EMERGENT PANEL (FINAL COMPONENT)
// ------------------------------------------------------------
export function EmergentPanel({ data, timeline, index, setIndex, history }) {
  const layer = data.layer3_emergent;
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [show3D, setShow3D] = useState(false);

  return (
    <div style={{ display: "grid", gap: 20 }}>
      <h2>Layer 3 · Emergent Intelligence</h2>

      <div style={{ display: "flex", gap: 20 }}>
        <GeometryField2D geometry={layer.geometry} />
        <AgentScatterPlot agents={layer.agents} onSelect={setSelectedAgent} />
      </div>

      <AgentDetailPanel agentId={selectedAgent} history={history} />

      <TimelineScrubber timeline={timeline} index={index} setIndex={setIndex} />

      <button onClick={() => setShow3D(!show3D)}>
        {show3D ? "Hide 3D Field" : "Show 3D Field"}
      </button>

      {show3D && (
        <div style={{ height: 400 }}>
          <Field3D geometry={layer.geometry} agents={layer.agents} />
        </div>
      )}
    </div>
  );
}
