from fastapi import FastAPI

# Existing RemoteOps router
from api.routes import remote_ops

# New Agent Geometry router
from api.routes.agent_loop import router as agent_router

app = FastAPI()

# Mount RemoteOps
app.include_router(
    remote_ops.router,
    prefix="/remote",
    tags=["RemoteOps"]
)

# Mount Agent Geometry Loop
app.include_router(
    agent_router,
    prefix="/agent",
    tags=["AgentGeometry"]
)
