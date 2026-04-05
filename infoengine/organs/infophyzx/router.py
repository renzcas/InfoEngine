from fastapi import APIRouter
from .organ import InfoField
from .models import (
    FieldRequest,
    StepRequest,
    WaveStepRequest,
    LaplacianRequest,
    PropagationRequest,
)

router = APIRouter(prefix="/infophyzx", tags=["infophyzx"])

# Persistent field instance
field: InfoField | None = None


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------

@router.post("/field/init")
def init_field(req: FieldRequest):
    global field
    field = InfoField(nodes=req.nodes, edges=req.edges)
    return {
        "status": "initialized",
        "nodes": len(req.nodes),
        "edges": len(req.edges),
    }


# ---------------------------------------------------------
# Laplacian
# ---------------------------------------------------------

@router.post("/laplacian")
def laplacian_route(req: LaplacianRequest):
    if field is None:
        return {"error": "field not initialized"}
    return field.compute_laplacian(normalized=False)


@router.post("/laplacian/normalized")
def laplacian_normalized_route(req: LaplacianRequest):
    if field is None:
        return {"error": "field not initialized"}
    return field.compute_laplacian(normalized=True)


# ---------------------------------------------------------
# Diffusion
# ---------------------------------------------------------

@router.post("/diffuse")
def diffuse_route(req: StepRequest):
    if field is None:
        return {"error": "field not initialized"}
    return field.diffuse_step(dt=req.dt, D=req.D)


# ---------------------------------------------------------
# Wave equation
# ---------------------------------------------------------

@router.post("/wave")
def wave_route(req: WaveStepRequest):
    if field is None:
        return {"error": "field not initialized"}
    return field.wave_step(dt=req.dt, c=req.c)


# ---------------------------------------------------------
# Full propagation
# ---------------------------------------------------------

@router.post("/propagate")
def propagate_route(req: PropagationRequest):
    if field is None:
        return {"error": "field not initialized"}
    return field.propagate(
        dt=req.dt,
        D=req.D,
        influence=req.influence,
        use_normalized_laplacian=req.use_normalized_laplacian,
    )


# ---------------------------------------------------------
# Unified step interface
# ---------------------------------------------------------

@router.post("/step")
def unified_step(req: StepRequest):
    if field is None:
        return {"error": "field not initialized"}
    return field.step(
        mode=req.mode,
        dt=req.dt,
        D=req.D,
        influence=req.influence,
    )

# ---------------------------------------------------------
# WebSocket Live Stream
# ---------------------------------------------------------

import asyncio
from fastapi import WebSocket

@router.websocket("/live")
async def live_stream(ws: WebSocket):
    await ws.accept()

    global field
    if field is None:
        await ws.send_json({"error": "field not initialized"})
        await ws.close()
        return

    try:
        while True:
            # Perform a small propagation step
            result = field.step(
                mode="propagate",
                dt=0.05,
                D=0.1,
                influence=0.05
            )

            await ws.send_json(result)
            await asyncio.sleep(0.1)  # ~10 updates per second

    except Exception:
        # Client disconnected or error — exit loop gracefully
        pass
