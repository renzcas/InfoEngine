from fastapi import APIRouter
from .organ import organ

router = APIRouter()

@router.post("/build")
def build_graph(organ_states: dict):
    organ.build_graph(organ_states)
    return {"status": "graph built", "nodes": len(organ.graph.nodes)}

@router.get("/global_state")
def global_state():
    return organ.compute_global_state()

@router.get("/last")
def last_state():
    return organ.get_last_state()
