from fastapi import APIRouter

from infoengine.organs.cyber.bloodhound_red_organ import BloodhoundRedOrgan
from infoengine.organs.cyber.bloodhound_blue_organ import BloodhoundBlueOrgan
from infoengine.organs.cyber.cors_organ import CORSOrgan
from infoengine.organs.cyber.cyber_origin_organ import CyberOriginOrgan
from infoengine.organs.cyber.cyber_origin_organ_old import CyberOriginOrganOld
from infoengine.organs.cyber.packet_analysis.service import PacketService
from infoengine.organs.cyber.remote_ops.service import RemoteOpsService

router = APIRouter()

red = BloodhoundRedOrgan()
blue = BloodhoundBlueOrgan()
cors = CORSOrgan()
origin = CyberOriginOrgan()
origin_old = CyberOriginOrganOld()
packet_service = PacketService()
remote_ops = RemoteOpsService()


@router.get("/red/paths")
def red_paths():
    return red.generate_attack_paths()


@router.get("/blue/defense")
def blue_defense():
    return blue.recommend_defenses()


@router.get("/cors")
def cors_info():
    return cors.check()


@router.get("/origin")
def origin_info():
    return origin.describe()


@router.get("/origin/old")
def origin_old_info():
    return origin_old.describe()


@router.get("/packet/summary")
def packet_summary():
    return packet_service.summary()


@router.get("/remote/ops")
def remote_ops_status():
    return remote_ops.status()
