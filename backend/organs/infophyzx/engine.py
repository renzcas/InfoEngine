# backend/organs/infophyzx/engine.py
from backend.organs.agentdash.state import agent_state
from backend.organs.agentdash.phonons import emit_phonon

def handle_resonance(res):
    agent_state.store_info(res, source="infophyzx", kind="resonance")
    emit_phonon("resonance_spike", target="agentdash", payload=res, energy=1.2)
