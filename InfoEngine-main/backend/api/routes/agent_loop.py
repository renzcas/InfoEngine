from fastapi import APIRouter

from backend.organs.agentdash.state import agent_state
from backend.organs.agentdash.attention import attention_tensor
from backend.organs.agentdash.phonons import phonon_engine
from backend.organs.infophyzx.engine import resonance_engine
from backend.core.hooks import hooks

router = APIRouter(prefix="/agent")


@router.get("/loop")
def geometric_agent_loop():
    # 1. Read the manifold (agent state)
    state = agent_state.read()

    # 2. Metric update (entropy collapse)
    attention_tensor.decay()

    # 3. Connection transport (hooks)
    hooks.process_pending_events()

    # 4. Curvature (resonance)
    curvature = resonance_engine.compute(state)

    # 5. Geodesic deviation (phonons)
    emitted = phonon_engine.emit_from(curvature)

    # 6. Update manifold
    agent_state.update(state, curvature, emitted)

    return {
        "state": state,
        "curvature": curvature,
        "phonons": emitted,
        "attention": attention_tensor.export(),
    }
