from fastapi import APIRouter
from .organ import InfoField
from .models import FieldRequest, StepRequest

router = APIRouter(prefix="/infophyzx", tags=["infophyzx"])

# Global instance for now (same pattern as your other organs)
field: InfoField | None = None

@router.post("/field/init")
def init_field(req: FieldRequest):
    global field
    field = InfoField(nodes=req.nodes, edges=req.edges)
    return {
        "status": "initialized",
        "nodes": len(req.nodes),
        "edges": len(req.edges)
    }

@router.post("/field/step")
def step_field(req: StepRequest):
    global field
    if field is None:
        return {"error": "field not initialized"}
    return field.step(dt=req.dt)
