from typing import Dict, Any


class GenerativeOrgan:
    def step(self, narrative_out: Dict[str, Any]) -> Dict[str, Any]:
        scenarios = [
            {"name": "lateral_movement", "prob": 0.4},
            {"name": "recon", "prob": 0.35},
            {"name": "benign_scan", "prob": 0.25},
        ]
        entropy = 0.3
        metrics = {
            "narrative_coherence": narrative_out["metrics"]["narrative_coherence"],
            "prediction_entropy": entropy,
            "top_scenarios": scenarios,
            "generated_hypotheses": 3,
        }
        return {"metrics": metrics, "events": narrative_out.get("events", [])}
