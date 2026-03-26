import { useEffect, useState } from "react";
import { getAgentSnapshot } from "../api";

export default function AgentGeometryPanel() {
  const [snap, setSnap] = useState<any>(null);

  useEffect(() => {
    const id = setInterval(async () => {
      const data = await getAgentSnapshot();
      setSnap(data);
    }, 500); // update twice per second

    return () => clearInterval(id);
  }, []);

  if (!snap) return <div>Loading agent geometry…</div>;

  return (
    <div style={{ padding: "20px", fontFamily: "monospace" }}>
      <h1>Agent Geometry Panel</h1>

      <Section title="Attention Heatmap">
        <AttentionHeatmap attention={snap.attention} />
      </Section>

      <Section title="Curvature">
        <pre>{JSON.stringify(snap.curvature, null, 2)}</pre>
      </Section>

      <Section title="Phonons">
        <PhononStream phonons={snap.phonons} />
      </Section>

      <Section title="Raw State">
        <pre>{JSON.stringify(snap.state, null, 2)}</pre>
      </Section>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div style={{ marginBottom: "30px" }}>
      <h2>{title}</h2>
      {children}
    </div>
  );
}

function AttentionHeatmap({ attention }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "6px" }}>
      {Object.entries(attention).map(([kind, sources]) =>
        Object.entries(sources).map(([src, val]) => (
          <div
            key={`${kind}-${src}`}
            style={{
              padding: "10px",
              background: `rgba(0, 150, 255, ${Math.min(val, 1)})`,
              color: "white",
              borderRadius: "4px",
            }}
          >
            {kind}:{src}
          </div>
        ))
      )}
    </div>
  );
}

function PhononStream({ phonons }) {
  return (
    <ul>
      {phonons.map((p, i) => (
        <li key={i}>
          {p.kind} → energy {p.energy}
        </li>
      ))}
    </ul>
  );
}
