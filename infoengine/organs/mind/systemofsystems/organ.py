from typing import Dict, Any
from fastapi import APIRouter
import time
import networkx as nx

router = APIRouter()


class SystemOfSystemsOrgan:
    """
    Treats all organs as nodes in a higher-level dynamical system.
    Builds a graph of influence and computes global state metrics.
    """

    def __init__(self):
        self.last_state: Dict[str, Any] = {}
        self.graph = nx.DiGraph()

    def build_graph(self, organ_states: Dict[str, Dict[str, Any]]):
        """
        organ_states = {
            "environment_heat": {...},
            "phase_space": {...},
            "cyber_origin": {...},
            ...
        }
        """

        self.graph.clear()

        # Add nodes
        for organ_name, state in organ_states.items():
            self.graph.add_node(organ_name, **state)

        # Simple influence rule:
        # physics → mind → cyber → computation → physics (loop)
        influence_order = [
            "environment_heat",
            "phase_space",
            "free_energy",
            "system_of_systems",
            "self_reference",
            "cyber_origin",
            "memory",
            "attention_tensor",
            "spike_neuron",
        ]

        for i in range(len(influence_order) - 1):
            a = influence_order[i]
            b = influence_order[i + 1]
            if a in organ_states and b in organ_states:
                self.graph.add_edge(a, b, weight=1.0)

        # Close the loop
        if influence_order[0] in organ_states and influence_order[-1] in organ_states:
            self.graph.add_edge(influence_order[-1], influence_order[0], weight=1.0)

    def compute_global_state(self) -> Dict[str, Any]:
        """
        Computes global metrics over the organ graph.
        """

        if len(self.graph.nodes) == 0:
            return {"error": "No organ states loaded"}

        centrality = nx.degree_centrality(self.graph)
        entropy = len(self.graph.edges) / (len(self.graph.nodes) ** 2 + 1e-9)

        global_state = {
            "timestamp": time.time(),
            "num_organs": len(self.graph.nodes),
            "num_edges": len(self.graph.edges),
            "centrality": centrality,
            "entropy": entropy,
        }

        self.last_state = global_state
        return global_state

    def get_last_state(self):
        return self.last_state


organ = SystemOfSystemsOrgan()
