from fastapi import APIRouter
from .organ import organ

router = APIRouter()

@router.post("/heat_state")
def compute_heat_state(env_inputs: dict):
    return organ.compute_heat_state(env_inputs)

@router.get("/heat_state/last")
def get_last_heat_state():
    return organ.get_last_state()
