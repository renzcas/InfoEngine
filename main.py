from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from infoengine.flask_app import flask_app

from infoengine.api.cyber_router import router as cyber_router
from infoengine.api.physics_router import router as physics_router
from infoengine.api.mind_router import router as mind_router
from infoengine.api.hybrid_router import router as hybrid_router
from infoengine.api.cockpit_router import router as cockpit_router

from infoengine.orchestrator.organ_registry import OrganRegistry
from infoengine.orchestrator.event_bus import EventBus


def create_app() -> FastAPI:
    app = FastAPI(
        title="InfoEngine Hybrid Server",
        version="1.0.0",
        description="Unified Cyber + Physics + Mind + Hybrid Organism",
    )

    organ_registry = OrganRegistry()
    event_bus = EventBus(organ_registry=organ_registry)

    app.state.organ_registry = organ_registry
    app.state.event_bus = event_bus

    app.include_router(cyber_router, prefix="/api/cyber", tags=["cyber"])
    app.include_router(physics_router, prefix="/api/physics", tags=["physics"])
    app.include_router(mind_router, prefix="/api/mind", tags=["mind"])
    app.include_router(hybrid_router, prefix="/api/hybrid", tags=["hybrid"])
    app.include_router(cockpit_router, prefix="/api/cockpit", tags=["cockpit"])

    app.mount("/flask", WSGIMiddleware(flask_app))

    return app


app = create_app()
