import React from "react";

export function Sidebar({ setPanel }) {
  return (
    <div className="sidebar">
      <h2 className="sidebar-title">InfoEngine</h2>

      {/* Spiral */}
      <button onClick={() => setPanel("bh_spiral")}>
        Bloodhound Spiral
      </button>

      {/* Computation */}
      <h3 className="sidebar-section">Computation</h3>
      <button onClick={() => setPanel("spike")}>Causal Spike</button>
      <button onClick={() => setPanel("synthetic")}>Synthetic Causal Set</button>
      <button onClick={() => setPanel("hash")}>Hash Panel</button>

      {/* Physics */}
      <h3 className="sidebar-section">Physics</h3>
      <button onClick={() => setPanel("power")}>Power Spectrum</button>
      <button onClick={() => setPanel("laplace")}>Laplace</button>
      <button onClick={() => setPanel("koopman")}>Koopman</button>
      <button onClick={() => setPanel("zeta")}>Zeta-Gamma</button>

      {/* Labs */}
      <h3 className="sidebar-section">Labs</h3>
      <button onClick={() => setPanel("experiment")}>
        Experiment Lab
      </button>

      {/* Analysis */}
      <h3 className="sidebar-section">Analysis</h3>
      <button onClick={() => setPanel("drift_timeline")}>Drift Timeline</button>
      <button onClick={() => setPanel("agent_loop")}>Agent Loop</button>
      <button onClick={() => setPanel("organ_health")}>Organ Health</button>
      <button onClick={() => setPanel("bh_drift_overlay")}>BH Drift Overlay</button>
    </div>
  );
}
