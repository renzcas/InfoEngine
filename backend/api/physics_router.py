from fastapi import APIRouter

# Existing physics organs
from infoengine.organs.physics.laplace_organ import LaplaceOrgan
from infoengine.organs.physics.free_energy import FreeEnergyOrgan
from infoengine.organs.physics.koopman_organ import KoopmanOrgan
from infoengine.organs.physics.power_spectrum_organ import PowerSpectrumOrgan
from infoengine.organs.physics.symplectic_organ import SymplecticOrgan
from infoengine.organs.physics.zeta_gamma_organ import ZetaGammaOrgan
from infoengine.organs.physics.phase_space import PhaseSpaceOrgan
from infoengine.organs.physics.eigen import EigenOrgan
from infoengine.organs.physics.environment_heat.organ import EnvironmentHeatOrgan
from infoengine.organs.physics.complex_plane.complex_plane_organ import ComplexPlaneOrgan

# NEW: InfoPhyzx organ
from infoengine.organs.infophyzx import router as infophyzx_router

router = APIRouter()

# Instantiate existing organs
laplace = LaplaceOrgan()
free_energy = FreeEnergyOrgan()
koopman = KoopmanOrgan()
power = PowerSpectrumOrgan()
symplectic = SymplecticOrgan()
zeta = ZetaGammaOrgan()
phase_space = PhaseSpaceOrgan()
eigen = EigenOrgan()
env_heat = EnvironmentHeatOrgan()
complex_plane = ComplexPlaneOrgan()

# ------------------------------
# Existing physics endpoints
# ------------------------------

@router.get("/laplace")
def laplace_route():
    return laplace.compute()

@router.get("/free-energy")
def free_energy_route():
    return free_energy.compute()

@router.get("/koopman")
def koopman_route():
    return koopman.compute()

@router.get("/power-spectrum")
def power_route():
    return power.compute()

@router.get("/symplectic")
def symplectic_route():
    return symplectic.compute()

@router.get("/zeta-gamma")
def zeta_route():
    return zeta.compute()

@router.get("/phase-space")
def phase_space_route():
    return phase_space.compute()

@router.get("/eigen")
def eigen_route():
    return eigen.compute()

@router.get("/environment-heat")
def env_heat_route():
    return env_heat.compute()

@router.get("/complex-plane")
def complex_plane_route():
    return complex_plane.generate_field()

# ------------------------------
# NEW: Mount InfoPhyzx organ
# ------------------------------

router.include_router(infophyzx_router)
