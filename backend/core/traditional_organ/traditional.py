from typing import List, Dict, Any


class TraditionalOrgan:
    def step(self, raw_inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        events = []
        counts = {"normal": 0, "suspicious": 0, "blocked": 0}
        active_rules = set()
        violations = 0

        for inp in raw_inputs:
            if inp.get("event") == "scan":
                counts["suspicious"] += 1
                active_rules.add("firewall.port_scan")
                events.append({"source_id": inp["source_id"], "type": "suspicious_scan"})
                violations += 1
            else:
                counts["normal"] += 1

        metrics = {
            "rule_firings_per_sec": len(active_rules),
            "active_rules": list(active_rules),
            "policy_violations": violations,
            "classification_counts": counts,
        }

        return {"metrics": metrics, "events": events}
