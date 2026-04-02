"""
Experiment Lab — Safe sandbox for InfoEngine experiments.
This file is intentionally isolated so experiments never break core organs.
"""

from typing import Dict, Any


def run_experiment(payload: Dict[str, Any]) -> Dict[str, Any]:
    result = {
        "received": payload,
        "message": "Experiment executed safely."
    }

    # ---------------------------------------------------------
    # GRAPH TEST
    # ---------------------------------------------------------
    if payload.get("test") == "graph":
        import networkx as nx
        G = nx.DiGraph()
        G.add_edge("A", "B")
        G.add_edge("B", "C")

        result["graph_nodes"] = list(G.nodes())
        result["graph_edges"] = list(G.edges())

    # ---------------------------------------------------------
    # RED ORGAN TEST
    # ---------------------------------------------------------
    if payload.get("test") == "red":
        from infoengine.organs.cyber.bloodhound_red_organ import BloodhoundRedOrgan
        red = BloodhoundRedOrgan()
        result["red_paths"] = red.generate_attack_paths()

    # ---------------------------------------------------------
    # BLUE ORGAN TEST
    # ---------------------------------------------------------
    if payload.get("test") == "blue":
        from infoengine.organs.cyber.bloodhound_blue_organ import BloodhoundBlueOrgan
        blue = BloodhoundBlueOrgan()
        result["blue_defense"] = blue.recommend_defenses()

    # ---------------------------------------------------------
    # RED + BLUE OVERLAY
    # ---------------------------------------------------------
    if payload.get("test") == "overlay":
        from infoengine.organs.cyber.bloodhound_red_organ import BloodhoundRedOrgan
        from infoengine.organs.cyber.bloodhound_blue_organ import BloodhoundBlueOrgan

        red = BloodhoundRedOrgan()
        blue = BloodhoundBlueOrgan()

        red_paths = red.generate_attack_paths()
        blue_def = blue.recommend_defenses()

        result["overlay"] = {
            "red_paths": red_paths.get("attack_paths", []),
            "blue_defense": blue_def.get("defenses", []),
        }

    # ---------------------------------------------------------
    # DRIFT (placeholder — ready for real engine)
    # ---------------------------------------------------------
    if payload.get("test") == "drift":
        timestamp = payload.get("time", "unknown")
        result["drift"] = f"Drift simulation placeholder at {timestamp}"

    return result
