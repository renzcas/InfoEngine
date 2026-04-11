from typing import Dict, Any


class NarrativeOrgan:
    def __init__(self):
        self.coherence = 0.8

    def step(self, trad_out: Dict[str, Any]) -> Dict[str, Any]:
        v = trad_out["metrics"]["policy_violations"]
        self.coherence = max(0.0, min(1.0, self.coherence - 0.01 * v))
        return {
            "metrics": {"narrative_coherence": self.coherence},
            "events": trad_out.get("events", []),
        }
