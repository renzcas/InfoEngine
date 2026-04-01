from typing import Dict, Any
from fastapi import APIRouter
import math
import time

router = APIRouter()


class SurpriseEntropyOrgan:
    """
    Surprise–Entropy Organ

    Consumes:
    - system_state: from system-of-systems organ
    - heat_state: from environment heat organ
    - self_state: from self-reference organ

    Produces:
    - surprise: deviation from expected coherence/energy
    - entropy: combined uncertainty
    - panic: high-surprise/high-entropy/low-coherence
    - reward: training-compatible scalar
    - attention_vector: compact signal for attention organ
    """

    def __init__(self):
        self.last_state: Dict[str, Any] = {}
        # Simple running expectations (could later be learned)
        self.expected_coherence = 0.7
        self.expected_energy = 0.4
        self.expected_entropy = 0.4

    def _clamp(self, x: float, lo: float = 0.0, hi: float = 1.0) -> float:
        return max(lo, min(hi, x))

    def compute_state(
        self,
        system_state: Dict[str, Any],
        heat_state: Dict[str, Any],
        self_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        # Extract key signals
        coherence = self_state.get("coherence", 0.0)
        self_entropy = self_state.get("entropy", 0.0)
        anomaly = self_state.get("anomaly_score", 0.0)

        energy = heat_state.get("energy", 0.0)
        heat_entropy = heat_state.get("entropy", 0.0)

        sys_entropy = system_state.get("entropy", 0.0)
        num_organs = system_state.get("num_organs", 0)

        # --- Surprise: deviation from expected coherence/energy/entropy ---
        coh_err = abs(coherence - self.expected_coherence)
        eng_err = abs(energy - self.expected_energy)
        ent_err = abs(self_entropy - self.expected_entropy)

        surprise = self._clamp(0.4 * coh_err + 0.3 * eng_err + 0.3 * ent_err)

        # --- Combined entropy ---
        combined_entropy = self._clamp(
            0.4 * self_entropy + 0.3 * heat_entropy + 0.3 * sys_entropy
        )

        # --- Panic: high surprise + high entropy + high anomaly ---
        panic = self._clamp(
            0.4 * surprise + 0.3 * combined_entropy + 0.3 * anomaly
        )

        # --- Reward: prefer low surprise, low entropy, high coherence ---
        reward_raw = (
            0.4 * (1.0 - surprise) +
            0.3 * (1.0 - combined_entropy) +
            0.3 * coherence
        )
        reward = self._clamp(reward_raw)

        # --- Attention vector (for attention tensor organ) ---
        # You can expand this later; keep it compact for now.
        attention_vector = {
            "surprise": surprise,
            "entropy": combined_entropy,
            "panic": panic,
            "reward": reward,
            "coherence": coherence,
            "num_organs": num_organs,
        }

        state = {
            "timestamp": time.time(),
            "surprise": surprise,
            "entropy": combined_entropy,
            "panic": panic,
            "reward": reward,
            "coherence": coherence,
            "anomaly": anomaly,
            "attention_vector": attention_vector,
            "system_state": system_state,
            "heat_state": heat_state,
            "self_state": self_state,
        }

        self.last_state = state
        return state

    def get_last_state(self) -> Dict[str, Any]:
        return self.last_state


organ = SurpriseEntropyOrgan()
