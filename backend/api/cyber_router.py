from fastapi import APIRouter

# Experiment Lab
from backend.organs.hacker_python_course.experiment_lab import run_experiment

# Drift + Agent + Health
from infoengine.organs.cyber.drift_engine import DriftEngine
from infoengine.organs.cyber.agent_loop_engine import AgentLoopEngine
from infoengine.organs.cyber.organ_health_engine import OrganHealthEngine
from infoengine.organs.cyber.organ_registry import REGISTRY

# Bloodhound Drift Adapter
from infoengine.organs.cyber.bloodhound_drift_adapter import BloodhoundDriftAdapter
from infoengine.organs.cyber.bloodhound_graph import BloodhoundGraph

router = APIRouter()

# ---------------------------------------------------------
# Experiment Lab
# ---------------------------------------------------------
@router.post("/lab/run")
def lab_run(payload: dict):
    return run_experiment(payload)

# ---------------------------------------------------------
# Drift Engine
# ---------------------------------------------------------
drift_engine = DriftEngine()

@router.get("/drift/timeline")
def drift_timeline():
    return {"timeline": drift_engine.get_timeline()}

@router.post("/drift/compute")
def drift_compute(payload: dict):
    return drift_engine.compute_drift(payload.get("t1"), payload.get("t2"))

# ---------------------------------------------------------
# Agent Loop
# ---------------------------------------------------------
agent_engine = AgentLoopEngine()

@router.post("/agent/start")
def agent_start(payload: dict):
    return agent_engine.start(payload.get("start"))

@router.post("/agent/step")
def agent_step():
    return agent_engine.step([])

@router.post("/agent/run")
def agent_run(payload: dict):
    return agent_engine.run_loop({}, payload.get("steps", 10))

# ---------------------------------------------------------
# Organ Health Dashboard
# ---------------------------------------------------------
health_engine = OrganHealthEngine(REGISTRY)

@router.get("/health/organs")
def organ_health():
    return health_engine.get_health()

# ---------------------------------------------------------
# Bloodhound Drift Overlay
# ---------------------------------------------------------
bh_graph = BloodhoundGraph()
bh_drift = BloodhoundDriftAdapter(bh_graph)

@router.get("/bloodhound/snapshot")
def bh_snapshot():
    return bh_drift.snapshot()
