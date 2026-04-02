from fastapi import APIRouter

from infoengine.organs.cyber.bloodhound_red_organ import BloodhoundRedOrgan
from infoengine.organs.cyber.bloodhound_blue_organ import BloodhoundBlueOrgan
from infoengine.organs.cyber.cors_organ import CORSOrgan
from infoengine.organs.cyber.cyber_origin_organ import CyberOriginOrgan
from infoengine.organs.cyber.cyber_origin_organ_old import CyberOriginOrganOld

router = APIRouter()

red = BloodhoundRedOrgan()
blue = BloodhoundBlueOrgan()
cors = CORSOrgan()
origin = CyberOriginOrgan()
origin_old = CyberOriginOrganOld()


@router.get("/red/paths")
def red_paths():
    return red.state()


@router.get("/blue/defense")
def blue_defense():
    return blue.state()


@router.get("/cors")
def cors_state():
    return cors.state()


@router.get("/origin")
def origin_state():
    return origin.state()


@router.get("/origin/old")
def origin_old_state():
    return origin_old.state()
