from typing import List, Tuple, Dict

from .utils import (
    zero_state,
    laplacian,
    normalized_laplacian,
    diffuse,
    wave_step,
    propagate_step,
)


class InfoField:
    """
    InfoPhyzx Organ: Physics-based field engine for InfoEngine.

    Supports:
    - Graph Laplacian (combinatorial + normalized)
    - Diffusion (heat equation)
    - Wave equation (2nd order PDE)
    - Full propagation (diffusion + vector influence)
    """

    def __init__(self, nodes: List[str], edges: List[Tuple[str, str]]):
        self.nodes = nodes
        self.edges = edges

        # Persistent field states
        self.state: Dict[str, float] = zero_state(nodes)
        self.prev_state: Dict[str, float] = zero_state(nodes)  # for wave equation

    # -----------------------------------------------------
    # Internal helpers
    # -----------------------------------------------------

    def _snapshot(self) -> Dict[str, float]:
        """Return a copy of the current field state."""
        return dict(self.state)

    # -----------------------------------------------------
    # Laplacian operations
    # -----------------------------------------------------

    def compute_laplacian(self, normalized: bool = False) -> Dict[str, float]:
        """
        Compute Laplacian or normalized Laplacian of the field.
        """
        if normalized:
            L = normalized_laplacian(self.state, self.edges)
            mode = "normalized-laplacian"
        else:
            L = laplacian(self.state, self.edges)
            mode = "laplacian"

        return {
            "mode": mode,
            "laplacian": L,
        }

    # -----------------------------------------------------
    # Diffusion (heat equation)
    # -----------------------------------------------------

    def diffuse_step(self, dt: float, D: float) -> Dict[str, float]:
        """
        Heat equation:
            φ(t+dt) = φ(t) + dt * D * Laplacian(φ)
        """
        self.prev_state = self._snapshot()
        self.state = diffuse(self.state, self.edges, D=D, dt=dt)

        return {
            "mode": "diffuse",
            "dt": dt,
            "D": D,
            "state": self._snapshot(),
        }

    # -----------------------------------------------------
    # Wave equation
    # -----------------------------------------------------

    def wave_step(self, dt: float, c: float) -> Dict[str, float]:
        """
        Wave equation:
            φ(t+dt) = 2φ(t) - φ(t-dt) + c² dt² Lφ
        """
        new_state = wave_step(
            state=self.state,
            prev_state=self.prev_state,
            edges=self.edges,
            c=c,
            dt=dt,
        )

        # Shift states
        self.prev_state = self._snapshot()
        self.state = new_state

        return {
            "mode": "wave",
            "dt": dt,
            "c": c,
            "state": self._snapshot(),
        }

    # -----------------------------------------------------
    # Full propagation engine
    # -----------------------------------------------------

    def propagate(
        self,
        dt: float,
        D: float = 0.1,
        influence: float = 0.05,
        use_normalized_laplacian: bool = False,
    ) -> Dict[str, float]:
        """
        Combined propagation:
        - diffusion
        - optional normalized Laplacian
        - vector-field influence
        """
        self.prev_state = self._snapshot()

        self.state = propagate_step(
            state=self.state,
            edges=self.edges,
            dt=dt,
            D=D,
            influence=influence,
            use_normalized_laplacian=use_normalized_laplacian,
        )

        return {
            "mode": "propagate",
            "dt": dt,
            "D": D,
            "influence": influence,
            "use_normalized_laplacian": use_normalized_laplacian,
            "state": self._snapshot(),
        }

    # -----------------------------------------------------
    # Unified step interface (router uses this)
    # -----------------------------------------------------

    def step(
        self,
        mode: str,
        dt: float,
        D: float = 0.1,
        influence: float = 0.05,
        c: float = 1.0,
        use_normalized_laplacian: bool = False,
    ) -> Dict[str, float]:
        """
        Unified physics step interface.

        mode options:
        - "propagate"
        - "diffuse"
        - "wave"
        - "laplacian"
        - "laplacian_normalized"
        """

        if mode == "diffuse":
            return self.diffuse_step(dt=dt, D=D)

        if mode == "wave":
            return self.wave_step(dt=dt, c=c)

        if mode == "laplacian":
            return self.compute_laplacian(normalized=False)

        if mode == "laplacian_normalized":
            return self.compute_laplacian(normalized=True)

        # Default: full propagation
        return self.propagate(
            dt=dt,
            D=D,
            influence=influence,
            use_normalized_laplacian=use_normalized_laplacian,
        )
