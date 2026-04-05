from typing import List, Tuple, Dict
from .utils import zero_state, normalize

class InfoField:
    """
    Core InfoPhyzx field engine.
    Handles nodes, edges, and propagation steps.
    """

    def __init__(self, nodes: List[str], edges: List[Tuple[str, str]]):
        self.nodes = nodes
        self.edges = edges

        # Internal state: potentials, flows, etc.
        self.state = zero_state(nodes)

    def step(self, dt: float) -> Dict:
        """
        Advance the field by dt.
        Replace this with your real physics logic.
        """

        # Simple placeholder update
        for node in self.nodes:
            self.state[node] = normalize(self.state[node] + dt * 0.01)

        return {
            "status": "ok",
            "dt": dt,
            "state": self.state
        }
