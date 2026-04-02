from typing import Dict, Any
from fastapi import APIRouter
import math
import time

router = APIRouter()


class EnvironmentHeatOrgan:
    """
    Environment Heat Organ

    Treats the environment as a thermodynamic field:
    - load, noise, traffic, error rates, etc. become 'heat sources'
    - outputs a compact heat state the rest of the system can use
    """

    def __init__(self):
        self.last_state: Dict[str, Any] = {}
        self.last_update_ts: float = 0.0

    def compute_heat_state(self, env_inputs: Dict[str, float]) -> Dict[str, Any]:
        """
        env_inputs can include things like:
        - cpu_load: 0..1
        - memory_pressure: 0..1
        - network_traffic: 0..1
        - error_rate: 0..1
        - request_rate: 0..1
        """

        cpu = env_inputs.get("cpu_load", 0.0)
        mem = env_inputs.get("memory_pressure", 0.0)
        net = env_inputs.get("network_traffic", 0.0)
        err = env_inputs.get("error_rate", 0.0)
        req = env_inputs.get("request_rate", 0.0)

        # Simple “energy” proxy: weighted sum
        energy = (
            0.30 * cpu +
            0.25 * mem +
            0.20 * net +
            0.15 * err +
            0.10 * req
        )

        # Entropy proxy: how “spread out” the load is
        components = [cpu, mem, net, err, req]
        total = sum(components) + 1e-9
        probs = [c / total for c in components]
        entropy = -sum(p * math.log(p + 1e-9) for p in probs)

        # Normalize entropy to 0..1-ish
        entropy_norm = entropy / math.log(len(components) + 1e-9)

        heat_state = {
            "energy": energy,
            "entropy": entropy_norm,
            "inputs": env_inputs,
            "timestamp": time.time(),
        }

        self.last_state = heat_state
        self.last_update_ts = heat_state["timestamp"]
        return heat_state

    def get_last_state(self) -> Dict[str, Any]:
        return self.last_state


organ = EnvironmentHeatOrgan()


@router.post("/heat_state")
def compute_heat_state(env_inputs: Dict[str, float]) -> Dict[str, Any]:
    """
    Compute a fresh heat state from environment inputs.
    """
    return organ.compute_heat_state(env_inputs)


@router.get("/heat_state/last")
def get_last_heat_state() -> Dict[str, Any]:
    """
    Return the last computed heat state (if any).
    """
    return organ.get_last_state() or {
        "energy": 0.0,
        "entropy": 0.0,
        "inputs": {},
        "timestamp": None,
    }
