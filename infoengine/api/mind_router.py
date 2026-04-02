from fastapi import APIRouter

from infoengine.organs.mind.surprise_entropy.organ import SurpriseEntropyOrgan
from infoengine.organs.mind.systemofsystems.organ import SystemOfSystemsOrgan

router = APIRouter()

surprise = SurpriseEntropyOrgan()
system = SystemOfSystemsOrgan()


@router.get("/surprise-entropy")
def surprise_entropy():
    return surprise.state()


@router.get("/system-of-systems")
def system_of_systems():
    return system.state()
