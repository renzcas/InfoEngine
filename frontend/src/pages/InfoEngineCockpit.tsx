import React, { useState } from "react";
import { useCockpitData } from "../hooks/useCockpitData";
import { useTimeline } from "../hooks/useTimeline";
import { EmergentPanel } from "../components/EmergentPanel";

const TABS = ["Overview", "Emergent", "Organs", "Agents", "Logs"] as const;

export function InfoEngineCockpit() {
  const [activeTab, setActiveTab] = useState<(typeof TABS)[number]>("Emergent");

  // Live data from backend WebSocket
  const liveData = useCockpitData("ws://localhost:8000/cockpit");

  // Timeline buffer + time-travel
  const { current, timeline, index, setIndex } = useTimeline(liveData);

  // Agent history buffer (for detail panel)
  const [agentHistory, setAgentHistory] = useState<any[]>([]);

  // Append to history when live
  if (liveData && index === null) {
    const t = liveData.timestamp;
    liveData.layer3_emergent.agents.forEach(a => {
      setAgentHistory(prev => [
        ...prev.slice(-500),
        { ...a, timestamp: t }
      ]);
    });
  }

  return (
    <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", height: "100vh" }}>
      
      {/* Sidebar */}
      <aside style={{ background: "#050505", padding: 16, borderRight: "1px solid #222" }}>
        <h1>InfoEngine</h1>
        <nav>
          {TABS.map(tab => (
            <div
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                padding: "8px 12px",
                marginTop: 4,
                cursor: "pointer",
                background: activeTab === tab ? "#222" : "transparent"
              }}
            >
              {tab}
            </div>
          ))}
        </nav>
      </aside>

      {/* Main */}
      <main style={{ padding: 20, overflow: "auto", background: "#000" }}>
        {!current && <div>Connecting to InfoEngine…</div>}

        {current && activeTab === "Emergent" && (
          <EmergentPanel
            data={current}
            timeline={timeline}
            index={index}
            setIndex={setIndex}
            history={agentHistory}
          />
        )}

        {current && activeTab === "Overview" && (
          <div style={{ color: "#aaa" }}>Overview panel coming soon.</div>
        )}

        {current && activeTab === "Organs" && (
          <div style={{ color: "#aaa" }}>Organ metrics coming soon.</div>
        )}

        {current && activeTab === "Agents" && (
          <div style={{ color: "#aaa" }}>Agent list coming soon.</div>
        )}

        {current && activeTab === "Logs" && (
          <div style={{ color: "#aaa" }}>Event logs coming soon.</div>
        )}
      </main>
    </div>
  );
}
