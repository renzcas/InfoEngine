from fastapi import APIRouter

from infoengine.organs.hybrid.hybrid_organ import HybridOrgan

router = APIRouter()

hybrid = HybridOrgan()


@router.get("/propagate")
def propagate():
    return hybrid.propagate()


@router.get("/status")
def status():
    return hybrid.status()
