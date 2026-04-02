"""
Agent Loop Engine
-----------------
This module simulates an autonomous cyber agent moving through a graph
(BloodhoundGraph or any organ-provided structure).

It is intentionally safe, isolated, and purely internal.
"""

from typing import Dict, Any, List
import random
import datetime


class AgentLoopEngine:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.current_node = None

    def start(self, start_node: str):
        """
        Initialize the agent at a starting node.
        """
        self.current_node = start_node
        snapshot = self._record("start")
        return snapshot

    def step(self, neighbors: List[str]):
        """
        Move the agent to a random neighbor.
        """
        if not neighbors:
            return self._record("stuck")

        self.current_node = random.choice(neighbors)
        return self._record("step")

    def run_loop(self, graph: Dict[str, List[str]], steps: int = 10):
        """
        Run a multi-step simulation over a graph adjacency list.
        """
        if self.current_node is None:
            raise ValueError("Agent must be started before running loop.")

        for _ in range(steps):
            neighbors = graph.get(self.current_node, [])
            self.step(neighbors)

        return self.history

    def _record(self, event: str):
        """
        Internal helper to timestamp and store agent state.
        """
        snapshot = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "event": event,
            "node": self.current_node,
        }
        self.history.append(snapshot)
        return snapshot
