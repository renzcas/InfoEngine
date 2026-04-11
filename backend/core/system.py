# backend/core/system.py

import numpy as np
from typing import List, Dict, Any

from core.geometry_organ import GeometryOrgan
from core.interiority_field import InteriorityFieldOrgan, InteriorityUpdateContext
from core.traditional_organ import TraditionalOrgan
from core.generative_organ import GenerativeOrgan
from core.narrative_organ import NarrativeOrgan


class OrganismSystem:
    def __init__(self):
        self.time = 0.0

        # Layer 1
        self.traditional = TraditionalOrgan()

        # Layer 2
        self.narrative = NarrativeOrgan()
        self.generative = GenerativeOrgan()

        # Layer 3
        self.geometry = GeometryOrgan(grid_size=(32, 32))
        self.interiority = InteriorityFieldOrgan()

    def step(self, dt: float, raw_inputs: List[dict]) -> Dict[str, Any]:
        self.time += dt

        # Layer 1
        trad_out = self.traditional.step(raw_inputs)

        # Layer 2
        narrative_out = self.narrative.step(trad_out)
        gen_out = self.generative.step(narrative_out)

        # Layer 3
        geometry_snapshot = self.geometry.step(dt=dt, t=self.time)

        # Convert events to exterior signals
        signals = self._build_signals(trad_out, gen_out)

        inter_ctx = InteriorityUpdateContext(
            dt=dt,
            global_time=self.time,
            external_signals=signals
        )
        self.interiority.step(inter_ctx)

        return self._build_snapshot(trad_out, gen_out, geometry_snapshot)

    def _build_signals(self, trad_out, gen_out):
        signals = []
        for ev in trad_out.get("events", []):
            signals.append({
                "source_id": ev["source_id"],
                "channel": "traditional",
                "payload": ev,
                "timestamp": self.time
            })
        for ev in gen_out.get("events", []):
            signals.append({
                "source_id": ev["source_id"],
                "channel": "generative",
                "payload": ev,
                "timestamp": self.time
            })
        return signals

    def _build_snapshot(self, trad, gen, geom):
        states = list(self.interiority.all_states())

        return {
            "layer1_traditional": trad["metrics"],
            "layer2_generative": gen["metrics"],
            "layer3_emergent": {
                "global_tension": sum(s.tension for s in states),
                "mean_valence": sum(s.valence for s in states) / max(1, len(states)),
                "field_complexity": geom["complexity"],
                "geometry": geom,
                "agents": [
                    {
                        "id": s.id,
                        "valence": s.valence,
                        "tension": s.tension,
                        "surprise": s.surprise
                    }
                    for s in states
                ]
            }
        }
