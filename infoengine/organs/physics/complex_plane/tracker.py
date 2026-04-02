# organs/complex_plane/tracker.py
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import math
import time

@dataclass
class LoopState:
    name: str
    z0: complex
    trajectory: List[complex] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)

    def add_step(self, z: complex):
        self.trajectory.append(z)

class ComplexPlaneTracker:
    def __init__(self, max_steps: int = 128):
        self.loops: Dict[str, LoopState] = {}
        self.max_steps = max_steps

    def register_loop(self, name: str, z0: complex):
        if name not in self.loops:
            self.loops[name] = LoopState(name=name, z0=z0, trajectory=[z0])

    def step_loop(self, name: str, z_next: complex):
        if name not in self.loops:
            self.register_loop(name, z_next)
        state = self.loops[name]
        state.add_step(z_next)
        if len(state.trajectory) > self.max_steps:
            state.trajectory = state.trajectory[-self.max_steps:]

    def get_trajectories(self) -> Dict[str, List[complex]]:
        return {k: v.trajectory for k, v in self.loops.items()}

    def divergence_rate(self, name: str) -> float:
        state = self.loops.get(name)
        if not state or len(state.trajectory) < 2:
            return 0.0
        mags = [abs(z) for z in state.trajectory]
        return mags[-1] - mags[0]

    def summary(self):
        out = []
        for name, state in self.loops.items():
            traj = state.trajectory
            out.append({
                "name": name,
                "steps": len(traj),
                "z_last": traj[-1] if traj else None,
                "divergence_rate": self.divergence_rate(name),
            })
        return out

tracker = ComplexPlaneTracker()
