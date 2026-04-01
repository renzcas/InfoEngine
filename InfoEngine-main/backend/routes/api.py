from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np

router = APIRouter()

# =========================================================
# Shared Payload Models
# =========================================================

class SignalPayload(BaseModel):
    signal: list[float]
    sample_rate: float = 1.0


# =========================================================
# Physics Organs
# =========================================================

from backend.organs.physics.power_spectrum_organ import PowerSpectrumOrgan
from backend.organs.physics.laplace_organ import LaplaceOrgan
from backend.organs.physics.koopman_organ import KoopmanOrgan
from backend.organs.physics.zeta_gamma_organ import ZetaGammaOrgan
from backend.organs.physics.free_energy import FreeEnergyOrgan

@router.post("/organ/physics/power_spectrum")
def analyze_power_spectrum(payload: SignalPayload):
    organ = PowerSpectrumOrgan(sample_rate=payload.sample_rate)
    return organ.analyze(np.array(payload.signal))


@router.post("/organ/physics/koopman")
def analyze_koopman(payload: SignalPayload):
    organ = KoopmanOrgan()
    return organ.analyze(np.array(payload.signal))


@router.post("/organ/physics/zeta_gamma")
def analyze_zeta_gamma(payload: SignalPayload):
    organ = ZetaGammaOrgan()
    return organ.analyze(np.array(payload.signal))


@router.post("/organ/physics/free_energy")
def analyze_free_energy(payload: SignalPayload):
    organ = FreeEnergyOrgan()
    return organ.analyze(np.array(payload.signal))


# ---- Laplace Organ ----

class LaplacePayload(BaseModel):
    signal: list[float]
    sample_rate: float = 1.0
    method: str = "prony"
    order: int = 10

@router.post("/organ/physics/laplace")
def analyze_laplace(payload: LaplacePayload):
    organ = LaplaceOrgan(
        sample_rate=payload.sample_rate,
        method=payload.method,
        order=payload.order
    )
    return organ.analyze(np.array(payload.signal))


# ---- Physics Core ----

from backend.core.physics_core import PhysicsCore

physics_core = PhysicsCore()

class PhysicsEvolveRequest(BaseModel):
    x0: float
    p0: float
    H_name: str = "harmonic"
    params: dict | None = None

@router.post("/organ/physics/evolve")
def physics_evolve(req: PhysicsEvolveRequest):
    return physics_core.evolve(
        x0=req.x0,
        p0=req.p0,
        H_name=req.H_name,
        params=req.params,
    )


# =========================================================
# Computation Organs
# =========================================================

from backend.organs.computation.hash import HashOrgan
from backend.organs.computation.causal_set import CausalSetOrgan

@router.post("/organ/computation/hash")
def analyze_hash(payload: SignalPayload):
    organ = HashOrgan()
    return organ.analyze(np.array(payload.signal))


@router.post("/organ/computation/causal_set")
def analyze_causal_set(payload: SignalPayload):
    organ = CausalSetOrgan()
    return organ.analyze(np.array(payload.signal))


# =========================================================
# Mind Organs
# =========================================================

from backend.organs.mind.self_reference_organ import SelfReferenceOrgan
from backend.organs.mind.consciousness_organ import ConsciousnessOrgan

@router.post("/organ/mind/self_reference")
def analyze_self_reference(payload: SignalPayload):
    organ = SelfReferenceOrgan()
    return organ.analyze(np.array(payload.signal))


@router.post("/organ/mind/consciousness")
def analyze_consciousness(payload: SignalPayload):
    organ = ConsciousnessOrgan()
    return organ.analyze(np.array(payload.signal))


# =========================================================
# Cybersecurity Organs
# =========================================================

from backend.organs.cyber.bloodhound_red_organ import BloodHoundRedOrgan
from backend.organs.cyber.bloodhound_blue_organ import BloodHoundBlueOrgan
from backend.organs.cyber.cyber_origin_organ import CyberOriginOrgan
from backend.organs.cyber.cors_organ import CORSOrgan
from backend.organs.cyber.xss_organ import XSSOrgan


# ---- BloodHound Inputs ----

class BloodHoundInput(BaseModel):
    nodes: list
    edges: list
    high_value_nodes: list = []

@router.post("/organ/cyber/bloodhound/red")
def cyber_bloodhound_red(payload: BloodHoundInput):
    organ = BloodHoundRedOrgan()
    return organ.process(payload.model_dump())


@router.post("/organ/cyber/bloodhound/blue")
def cyber_bloodhound_blue(payload: BloodHoundInput):
    organ = BloodHoundBlueOrgan()
    return organ.process(payload.model_dump())


# ---- Cyber Origin ----

class CyberOriginInput(BaseModel):
    origins: list
    cors_rules: list = []
    xss_sinks: list = []

@router.post("/organ/cyber/origin")
def cyber_origin(payload: CyberOriginInput):
    organ = CyberOriginOrgan()
    return organ.process(payload.model_dump())


# ---- CORS ----

class CORSInput(BaseModel):
    rules: list

@router.post("/organ/cyber/cors")
def cyber_cors(payload: CORSInput):
    organ = CORSOrgan()
    return organ.process(payload.model_dump())


# ---- XSS ----

class XSSInput(BaseModel):
    sinks: list

@router.post("/organ/cyber/xss")
def cyber_xss(payload: XSSInput):
    organ = XSSOrgan()
    return organ.process(payload.model_dump())S