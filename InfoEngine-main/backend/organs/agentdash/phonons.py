# backend/organs/agentdash/phonons.py
from backend.core.hooks import hooks
from backend.organs.agentdash.state import agent_state

def emit_phonon(kind: str, target: str, payload: dict, energy: float = 1.0):
    phonon = {
        "kind": kind,
        "target": target,
        "payload": payload,
        "energy": energy,
    }
    agent_state.emissions.append(phonon)
    hooks.trigger("info_phonon_emitted", phonon=phonon)
