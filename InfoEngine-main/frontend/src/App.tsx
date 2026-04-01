import React, { useState, useEffect } from "react";
import { Sidebar } from "./components/Sidebar";
import { CommandPalette } from "./components/CommandPalette";

// Cybersecurity panels (all removed — folder deleted)
// import { CORSPanel } from "./panels/Cybersecurity/CORSPanel";
// import { XSSPanel } from "./panels/Cybersecurity/XSSPanel";

// NEW — Spiral Panel
import { BloodhoundSpiralPanel } from "./panels/BloodhoundSpiralPanel";

// Computation
import CausalSetSpikePanel from "./panels/CausalSetSpikePanel";
import CausalSetSyntheticPanel from "./panels/CausalSetSyntheticPanel";
import HashPanel from "./panels/HashPanel";

// Physics
import PowerSpectrumPanel from "./panels/PowerSpectrumPanel";

// Placeholder physics panels
const LaplacePanel = () => <div>Laplace Panel</div>;
const KoopmanPanel = () => <div>Koopman Panel</div>;
const ZetaPanel = () => <div>Zeta-Gamma Panel</div>;

export default function App() {
  const [panel, setPanel] = useState("bh_spiral");
  const [fade, setFade] = useState(true);
  const [paletteOpen, setPaletteOpen] = useState(false);

  // Smooth fade animation on panel change
  useEffect(() => {
    setFade(false);
    const t = setTimeout(() => setFade(true), 150);
    return () => clearTimeout(t);
  }, [panel]);

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e) => {
      if (e.ctrlKey && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setPaletteOpen(true);
      }

      // Removed: bh_red, bh_blue, origin, cors, xss (files deleted)
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
        {/* Cybersecurity — all removed */}
        {panel === "bh_spiral" && <BloodhoundSpiralPanel />}

        {/* Computation */}
        {panel === "spike" && <CausalSetSpikePanel />}
        {panel === "synthetic" && <CausalSetSyntheticPanel />}
        {panel === "hash" && <HashPanel />}

        {/* Physics */}
        {panel === "power" && <PowerSpectrumPanel />}
        {panel === "laplace" && <LaplacePanel />}
        {panel === "koopman" && <KoopmanPanel />}
        {panel === "zeta" && <ZetaPanel />}
      </div>
    </div>
  );
}
