# backend/organs/cyberarena/engine.py
from backend.organs.agentdash.state import agent_state
from backend.organs.agentdash.phonons import emit_phonon

def handle_packet(decoded_packet):
    agent_state.store_info(decoded_packet, source="cyberarena", kind="packet")
    emit_phonon("packet_observed", target="agentdash", payload=decoded_packet, energy=0.7)
git