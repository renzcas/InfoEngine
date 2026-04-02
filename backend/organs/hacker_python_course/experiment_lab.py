"""
Experiment Lab — Your permanent safe sandbox.

Use this file to run experiments on:
- graphs
- privilege drift
- BloodhoundRed/Blue
- agent loops
- math
- InfoPhyzx ideas
- anything you want to test

This file NEVER gets deleted or rewritten.
"""

from typing import Dict, Any

def run_experiment(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for all experiments.
    Modify inside this function ONLY.
    Everything else in InfoEngine stays untouched.
    """

    # Example: echo back payload
    result = {
        "received": payload,
        "message": "Experiment executed safely.",
    }

    # You can add your experiments here:
    # ---------------------------------
    # Example: simple graph test
    if payload.get("test") == "graph":
        import networkx as nx
        G = nx.DiGraph()
        G.add_edge("A", "B")
        G.add_edge("B", "C")
        result["graph_nodes"] = list(G.nodes())
        result["graph_edges"] = list(G.edges())

    # Example: privilege drift test
    if payload.get("test") == "drift":
        result["drift"] = "Drift simulation placeholder"

    # Example: BloodhoundRed test
    if payload.get("test") == "red":
        from infoengine.organs.cyber.bloodhound_red_organ import BloodhoundRedOrgan
        red = BloodhoundRedOrgan()
        result["red_paths"] = red.generate_attack_paths()

    # Example: BloodhoundBlue test
    if payload.get("test") == "blue":
        from infoengine.organs.cyber.bloodhound_blue_organ import BloodhoundBlueOrgan
        blue = BloodhoundBlueOrgan()
        result["blue_defense"] = blue.recommend_defenses()

    return result
