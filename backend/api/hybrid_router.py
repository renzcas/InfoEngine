from fastapi import APIRouter
from organs.hybrid.hybrid_organ import HybridOrgan

router = APIRouter()
hybrid = HybridOrgan()

@router.get("/propagate")
def propagate():
    return {"result": hybrid.propagate()}
