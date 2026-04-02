from fastapi import APIRouter

from infoengine.organs.hybrid.hybrid_organ import HybridOrgan

router = APIRouter()

hybrid = HybridOrgan()


@router.get("/propagate")
def propagate():
    return hybrid.propagate()


@router.get("/heartbeat")
def heartbeat(request: Request):
    hybrid = request.app.state.organ_registry.get("hybrid")
    return hybrid.heartbeat(
        registry=request.app.state.organ_registry,
        event_bus=request.app.state.event_bus
    )


@router.get("/status")
def status():
    return hybrid.status()
