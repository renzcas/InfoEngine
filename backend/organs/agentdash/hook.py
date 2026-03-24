# backend/organs/agentdash/hooks.py
from backend.core.hooks import hooks
from backend.organs.agentdash.attention import attention_tensor

def _phonon_hook(phonon):
    kind = phonon["kind"]
    source = phonon["target"]
    energy = phonon["energy"]
    attention_tensor.bump(kind, source, energy)

def register_agentdash_hooks():
    hooks.register("info_phonon_emitted", _phonon_hook)
