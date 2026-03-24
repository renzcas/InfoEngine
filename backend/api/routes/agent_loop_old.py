from fastapi import APIRouter
from backend.organs.agentdash.state import agent_state
from backend.organs.agentdash.attention import attention_tensor
from backend.organs.agentdash.phonons import phonon_engine
from backend.organs.infophyzx.engine import resonance_engine
from backend.core.hooks import hooks

router = APIRouter(prefix="/agent")

@router.get("/loop")
def geometric_agent_loop():
    state = agent_state.read()
    attention_tensor.decay()
    hooks.process_pending_events()
    curvature = resonance_engine.compute(state)
    emitted = phonon_engine.emit_from(curvature)
    agent_state.update(state, curvature, emitted)

    return {
        "state": state,
        "curvature": curvature,
        "phonons": emitted,
        "attention": attention_tensor.export()
    }
