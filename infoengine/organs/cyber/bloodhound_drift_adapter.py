"""
BloodhoundGraph Drift Adapter
-----------------------------
This module connects BloodhoundGraph to the DriftEngine and AgentLoopEngine.

It provides:
- Snapshot extraction from BloodhoundGraph
- Drift recording
- Agent loop integration
- A clean API for cockpit visualization

This file does NOT modify BloodhoundGraph itself.
"""

from typing import Dict, Any
from .drift_engine import DriftEngine
from .agent_loop_engine import AgentLoopEngine


class BloodhoundDriftAdapter:
    def __init__(self, graph):
        """
        graph: an instance of BloodhoundGraph or any graph-like organ
        """
        self.graph = graph
        self.drift = DriftEngine()
        self.agent = AgentLoopEngine()

    # ---------------------------------------------------------
    # SNAPSHOTS
    # ---------------------------------------------------------
    def snapshot(self) -> Dict[str, Any]:
        """
        Extract a safe snapshot of the graph:
        - nodes
        - edges
        - privileges (if available)
        """
        nodes = list(self.graph.nodes()) if hasattr(self.graph, "nodes") else []
        edges = list(self.graph.edges()) if hasattr(self.graph, "edges") else []

        snapshot = {
            "nodes": nodes,
            "edges": edges,
        }

        # Optional: privilege levels
        if hasattr(self.graph, "privileges"):
            snapshot["privileges"] = self.graph.privileges

        return self.drift.record_snapshot(snapshot)

    # ---------------------------------------------------------
    # DRIFT TIMELINE
    # ---------------------------------------------------------
    def timeline(self):
        return self.drift.get_timeline()

    def compute_drift(self, t1: str, t2: str):
        return self.drift.compute_drift(t1, t2)

    # ---------------------------------------------------------
    # AGENT LOOP
    # ---------------------------------------------------------
    def start_agent(self, start_node: str):
        return self.agent.start(start_node)

    def step_agent(self):
        """
        Move agent based on graph adjacency.
        """
        if not hasattr(self.graph, "neighbors"):
            return {"error": "Graph does not support neighbors()"}

        neighbors = list(self.graph.neighbors(self.agent.current_node))
        return self.agent.step(neighbors)

    def run_agent_loop(self, steps: int = 10):
        """
        Run a multi-step agent simulation.
        """
        if not hasattr(self.graph, "neighbors"):
            return {"error": "Graph does not support neighbors()"}

        adjacency = {
            node: list(self.graph.neighbors(node))
            for node in self.graph.nodes()
        }

        return self.agent.run_loop(adjacency, steps)
