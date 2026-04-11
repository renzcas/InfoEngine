from typing import Dict, Iterable, Optional
import numpy as np

from .models import InteriorityState, InteriorityConfig
from .signals import ExteriorSignal, InteriorityUpdateContext


class InteriorityFieldOrgan:
    """
    Tracks and updates the interiority of every agent and object.
    """

    def __init__(self, config: Optional[InteriorityConfig] = None):
        self.config = config or InteriorityConfig()
        self._states: Dict[str, InteriorityState] = {}

    # ---------- Public API ----------

    def ensure_object(self, obj_id: str) -> InteriorityState:
        if obj_id not in self._states:
            self._states[obj_id] = InteriorityState.new(obj_id, self.config)
        return self._states[obj_id]

    def get_state(self, obj_id: str) -> Optional[InteriorityState]:
        return self._states.get(obj_id)

    def all_states(self) -> Iterable[InteriorityState]:
        return self._states.values()

    def step(self, ctx: InteriorityUpdateContext) -> None:
        """
        Main update entrypoint called each simulation tick.
        """
        signals_by_source = self._group_signals(ctx.external_signals)

        # Update existing states
        for obj_id, state in list(self._states.items()):
            obj_signals = signals_by_source.get(obj_id, [])
            self._update_single_state(state, obj_signals, ctx)

        # Create states for new signal sources
        for source_id in signals_by_source.keys():
            if source_id not in self._states:
                state = self.ensure_object(source_id)
                self._update_single_state(state, signals_by_source[source_id], ctx)

    # ---------- Internal mechanics ----------

    def _group_signals(self, signals: Iterable[ExteriorSignal]):
        grouped: Dict[str, list] = {}
        for s in signals:
            grouped.setdefault(s.source_id, []).append(s)
        return grouped

    def _update_single_state(
        self,
        state: InteriorityState,
        signals: Iterable[ExteriorSignal],
        ctx: InteriorityUpdateContext
    ) -> None:

        delta_valence = self._compute_valence_delta(state, signals, ctx)
        delta_tension = self._compute_tension_delta(state, signals, ctx)
        delta_surprise = self._compute_surprise_delta(state, signals, ctx)
        delta_hidden = self._compute_hidden_delta(state, signals, ctx)
        delta_memory = self._compute_memory_delta(state, signals, ctx)

        state.valence += delta_valence
        state.tension += delta_tension
        state.surprise += delta_surprise
        state.hidden_state += delta_hidden
        state.memory += delta_memory

        state.narrative_pointer += 1

        self._stabilize_state(state)

    # ---------- Placeholder dynamics ----------

    def _compute_valence_delta(self, state, signals, ctx) -> float:
        delta = 0.0
        for s in signals:
            if s.payload.get("type") == "reward":
                delta += 0.1
            if s.payload.get("type") == "threat":
                delta -= 0.1
        return delta

    def _compute_tension_delta(self, state, signals, ctx) -> float:
        return 0.0

    def _compute_surprise_delta(self, state, signals, ctx) -> float:
        return 0.0

    def _compute_hidden_delta(self, state, signals, ctx):
        return np.zeros_like(state.hidden_state)

    def _compute_memory_delta(self, state, signals, ctx):
        return np.zeros_like(state.memory)

    def _stabilize_state(self, state: InteriorityState) -> None:
        state.valence = float(np.clip(state.valence, -10.0, 10.0))
        state.tension = float(np.clip(state.tension, 0.0, 10.0))
        state.surprise = float(np.clip(state.surprise, 0.0, 10.0))
