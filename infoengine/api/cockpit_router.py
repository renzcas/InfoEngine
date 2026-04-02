import asyncio
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect

router = APIRouter()


# ---------------------------------------------------------
# Cockpit Status
# ---------------------------------------------------------
@router.get("/status")
def cockpit_status():
    return {"status": "cockpit online"}


# ---------------------------------------------------------
# Cockpit Panels
# ---------------------------------------------------------
@router.get("/panels")
def panels():
    return {
        "cyber": {
            "red_paths": "/api/cyber/red/paths",
            "blue_defense": "/api/cyber/blue/defense",
            "cors": "/api/cyber/cors",
            "origin": "/api/cyber/origin",
            "origin_old": "/api/cyber/origin/old",
        },

        "physics": {
            "laplace": "/api/physics/laplace",
            "free_energy": "/api/physics/free-energy",
            "koopman": "/api/physics/koopman",
            "power_spectrum": "/api/physics/power-spectrum",
            "symplectic": "/api/physics/symplectic",
            "zeta_gamma": "/api/physics/zeta-gamma",
            "phase_space": "/api/physics/phase-space",
            "eigen": "/api/physics/eigen",
            "environment_heat": "/api/physics/environment-heat",
            "complex_plane": "/api/physics/complex-plane",
        },

        "mind": {
            "surprise_entropy": "/api/mind/surprise-entropy",
            "system_of_systems": "/api/mind/system-of-systems",
        },

        "hybrid": {
            "status": "/api/hybrid/status",
            "propagate": "/api/hybrid/propagate",
            "heartbeat": "/api/hybrid/heartbeat",
            "live_stream": "/api/cockpit/live/heartbeat",
        }
    }


# ---------------------------------------------------------
# Cockpit Heartbeat (HTTP)
# ---------------------------------------------------------
@router.get("/heartbeat")
def cockpit_heartbeat(request: Request):
    hybrid = request.app.state.organ_registry.get("hybrid")
    return hybrid.heartbeat(
        registry=request.app.state.organ_registry,
        event_bus=request.app.state.event_bus
    )


# ---------------------------------------------------------
# Cockpit Live Heartbeat Stream (WebSocket)
# ---------------------------------------------------------
@router.websocket("/live/heartbeat")
async def live_heartbeat(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            hybrid = websocket.app.state.organ_registry.get("hybrid")
            state = hybrid.heartbeat(
                registry=websocket.app.state.organ_registry,
                event_bus=websocket.app.state.event_bus
            )

            await websocket.send_json(state)
            await asyncio.sleep(0.1)  # 10 Hz live stream

    except WebSocketDisconnect:
        pass
