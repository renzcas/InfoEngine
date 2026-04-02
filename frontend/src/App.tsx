import React, { useState, useEffect } from "react";
import { Sidebar } from "./components/Sidebar";
import { CommandPalette } from "./components/CommandPalette";

// Core Panels
import { BloodhoundSpiralPanel } from "./panels/BloodhoundSpiralPanel";
import CausalSetSpikePanel from "./panels/CausalSetSpikePanel";
import CausalSetSyntheticPanel from "./panels/CausalSetSyntheticPanel";
import HashPanel from "./panels/HashPanel";
import PowerSpectrumPanel from "./panels/PowerSpectrumPanel";

// Experiment Lab
import ExperimentPanel from "./panels/ExperimentPanel";

// New Analysis Panels
import DriftTimelinePanel from "./panels/DriftTimelinePanel";
import AgentLoopPanel from "./panels/AgentLoopPanel";
import OrganHealthPanel from "./panels/OrganHealthPanel";
import BloodhoundDriftOverlayPanel from "./panels/BloodhoundDriftOverlayPanel";

// Placeholder physics
const LaplacePanel = () => <div>Laplace Panel</div>;
const KoopmanPanel = () => <div>Koopman Panel</div>;
const ZetaPanel = () => <div>Zeta-Gamma Panel</div>;

export default function App() {
  const [panel, setPanel] = useState("bh_spiral");
  const [fade, setFade] = useState(true);
  const [paletteOpen, setPaletteOpen] = useState(false);

  useEffect(() => {
    setFade(false);
    const t = setTimeout(() => setFade(true), 150);
    return () => clearTimeout(t);
  }, [panel]);

  useEffect(() => {
    const handler = (e) => {
      if (e.ctrlKey && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setPaletteOpen(true);
      }
      if (e.key === "6") setPanel("power");
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  return (
    <div className="app-container">
      <Sidebar setPanel={setPanel} />

      <CommandPalette
        open={paletteOpen}
        setOpen={setPaletteOpen}
        setPanel={setPanel}
      />

      <div className={`panel-container ${fade ? "fade-in" : "fade-out"}`}>
        {/* Core */}
        {panel === "bh_spiral" && <BloodhoundSpiralPanel />}
        {panel === "spike" && <CausalSetSpikePanel />}
        {panel === "synthetic" && <CausalSetSyntheticPanel />}
        {panel === "hash" && <HashPanel />}

        {/* Physics */}
        {panel === "power" && <PowerSpectrumPanel />}
        {panel === "laplace" && <LaplacePanel />}
        {panel === "koopman" && <KoopmanPanel />}
        {panel === "zeta" && <ZetaPanel />}

        {/* Experiment Lab */}
        {panel === "experiment" && <ExperimentPanel />}

        {/* Analysis */}
        {panel === "drift_timeline" && <DriftTimelinePanel />}
        {panel === "agent_loop" && <AgentLoopPanel />}
        {panel === "organ_health" && <OrganHealthPanel />}
        {panel === "bh_drift_overlay" && <BloodhoundDriftOverlayPanel />}
      </div>
    </div>
  );
}
