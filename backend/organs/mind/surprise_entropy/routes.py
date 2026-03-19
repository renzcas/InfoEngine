from fastapi import APIRouter
from .organ import organ

router = APIRouter()


@router.post("/state")
def compute_surprise_entropy(payload: dict):
    """
    payload = {
      "system_state": {...},   # from system-of-systems
      "heat_state": {...},     # from environment heat
      "self_state": {...}      # from self-reference
    }
    """
    system_state = payload.get("system_state", {})
    heat_state = payload.get("heat_state", {})
    self_state = payload.get("self_state", {})
    return organ.compute_state(system_state, heat_state, self_state)


@router.get("/state/last")
def last_surprise_entropy_state():
    return organ.get_last_state() or {
        "surprise": 0.0,
        "entropy": 0.0,
        "panic": 0.0,
        "reward": 0.0,
        "coherence": 0.0,
        "anomaly": 0.0,
        "attention_vector": {},
        "system_state": {},
        "heat_state": {},
        "self_state": {},
        "timestamp": None,
    }
