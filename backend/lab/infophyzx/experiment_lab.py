"""
Experiment Lab: InfoPhyzx Multi‑Step Propagation

This experiment:
- Initializes a field
- Runs N simulation steps
- Uses any physics mode (propagate, diffuse, wave, laplacian, etc.)
- Returns a time‑series of field states
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Tuple, Dict

from infoengine.organs.infophyzx.organ import InfoField


router = APIRouter(prefix="/lab/infophyzx", tags=["experiment-lab"])


# ---------------------------------------------------------
# Experiment request model
# ---------------------------------------------------------

class InfoPhyzxExperimentRequest(BaseModel):
    nodes: List[str]
    edges: List[Tuple[str, str]]

    steps: int = 50
    dt: float = 0.1
    D: float = 0.1
    influence: float = 0.05
    c: float = 1.0

    mode: str = "propagate"  
    use_normalized_laplacian: bool = False


# ---------------------------------------------------------
# Experiment endpoint
# ---------------------------------------------------------

@router.post("/run")
def run_infophyzx_experiment(req: InfoPhyzxExperimentRequest):
    """
    Run a multi‑step InfoPhyzx simulation and return a time‑series.
    """

    # Initialize field
    field = InfoField(nodes=req.nodes, edges=req.edges)

    timeline: List[Dict] = []

    for step in range(req.steps):

        result = field.step(
            mode=req.mode,
            dt=req.dt,
            D=req.D,
            influence=req.influence,
            c=req.c,
            use_normalized_laplacian=req.use_normalized_laplacian,
        )

        timeline.append({
            "step": step,
            "state": result.get("state"),
            "mode": result.get("mode"),
        })

    return {
        "status": "completed",
        "steps": req.steps,
        "mode": req.mode,
        "timeline": timeline,
    }
