from fastapi import APIRouter
from organs.mind.mind_organ import MindOrgan

router = APIRouter()
mind = MindOrgan()

@router.get("/state")
def mind_state():
    return {"state": mind.get_state()}
