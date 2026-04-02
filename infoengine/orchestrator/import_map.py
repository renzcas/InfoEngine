# Central import map for all organs in the organism.

from infoengine.organs.cyber.bloodhound_red_organ import BloodhoundRedOrgan
from infoengine.organs.cyber.bloodhound_blue_organ import BloodhoundBlueOrgan
from infoengine.organs.cyber.cors_organ import CORSOrgan
from infoengine.organs.cyber.cyber_origin_organ import CyberOriginOrgan
from infoengine.organs.cyber.cyber_origin_organ_old import CyberOriginOrganOld

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

from infoengine.organs.mind.surprise_entropy.organ import SurpriseEntropyOrgan
from infoengine.organs.mind.systemofsystems.organ import SystemOfSystemsOrgan

from infoengine.organs.hybrid.hybrid_organ import HybridOrgan

IMPORT_MAP = {
    "bloodhound_red": BloodhoundRedOrgan,
    "bloodhound_blue": BloodhoundBlueOrgan,
    "cors": CORSOrgan,
    "cyber_origin": CyberOriginOrgan,
    "cyber_origin_old": CyberOriginOrganOld,

    "laplace": LaplaceOrgan,
    "free_energy": FreeEnergyOrgan,
    "koopman": KoopmanOrgan,
    "power_spectrum": PowerSpectrumOrgan,
    "symplectic": SymplecticOrgan,
    "zeta_gamma": ZetaGammaOrgan,
    "phase_space": PhaseSpaceOrgan,
    "eigen": EigenOrgan,
    "environment_heat": EnvironmentHeatOrgan,
    "complex_plane": ComplexPlaneOrgan,

    "surprise_entropy": SurpriseEntropyOrgan,
    "system_of_systems": SystemOfSystemsOrgan,

    "hybrid": HybridOrgan,
}
