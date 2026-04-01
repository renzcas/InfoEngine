from backend.organs.agentdash.state import agent_state
from backend.organs.agentdash.attention import attention_tensor
from backend.organs.agentdash.phonons import phonon_engine
from backend.organs.infophyzx.engine import resonance_engine
from backend.core.hooks import hooks


def run_geometry_cycle():
    # 1. Read the agent's internal state (manifold)
    state = agent_state.read()

    # 2. Attention decays → entropy collapse
    attention_tensor.decay()

    # 3. Process hooks (events, signals)
    hooks.process_pending_events()

    # 4. Resonance spikes → curvature increases
    curvature = resonance_engine.compute(state)

    # 5. Curvature changes → phonons emit
    emitted = phonon_engine.emit_from(curvature)

    # 6. Update the agent's state with new geometry
    agent_state.update(state, curvature, emitted)

    return {
        "state": state,
        "curvature": curvature,
        "phonons": emitted,
        "attention": attention_tensor.export(),
    }
