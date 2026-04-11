from dataclasses import dataclass, field
from typing import Any, Dict
import numpy as np


@dataclass
class InteriorityConfig:
    """
    Global configuration for the Interiority Field Organ.
    """
    hidden_dim: int = 16
    memory_dim: int = 8
    default_valence: float = 0.0
    default_tension: float = 0.0
    default_surprise: float = 0.0


@dataclass
class InteriorityState:
    """
    The 'inside' of an agent or object.
    """
    id: str
    valence: float
    tension: float
    surprise: float
    memory: np.ndarray
    hidden_state: np.ndarray
    narrative_pointer: int = 0
    meta: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def new(cls, obj_id: str, cfg: InteriorityConfig) -> "InteriorityState":
        return cls(
            id=obj_id,
            valence=cfg.default_valence,
            tension=cfg.default_tension,
            surprise=cfg.default_surprise,
            memory=np.zeros(cfg.memory_dim),
            hidden_state=np.zeros(cfg.hidden_dim),
            narrative_pointer=0,
            meta={}
        )
