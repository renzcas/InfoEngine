from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ExteriorSignal:
    """
    What the outside world 'sees' from an object/agent.
    """
    source_id: str
    channel: str
    payload: Dict[str, Any]
    timestamp: float


@dataclass
class InteriorityUpdateContext:
    """
    Context passed into the organ each tick.
    """
    dt: float
    global_time: float
    external_signals: List[ExteriorSignal]
