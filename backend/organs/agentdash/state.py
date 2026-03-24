# backend/organs/agentdash/state.py
from collections import deque

class AgentState:
    def __init__(self, max_memory=512):
        self.memory = deque(maxlen=max_memory)  # stored info
        self.emissions = []                    # recent phonons

    def store_info(self, payload: dict, source: str, kind: str):
        self.memory.append({
            "source": source,
            "kind": kind,
            "payload": payload,
        })

agent_state = AgentState()
