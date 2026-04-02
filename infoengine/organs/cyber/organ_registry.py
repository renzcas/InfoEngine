"""
Unified Organ Registry
----------------------
This file centralizes all cyber organs into a single registry so the
router, cockpit, and experiment lab can access them cleanly.

This prevents scattered imports and keeps the architecture stable.
"""

from .bloodhound_red_organ import BloodhoundRedOrgan
from .bloodhound_blue_organ import BloodhoundBlueOrgan
from .cors_organ import CORSOrgan
from .cyber_origin_organ import CyberOriginOrgan
from .cyber_origin_organ_old import CyberOriginOrganOld
from .packet_analysis.service import PacketService
from .remote_ops.service import RemoteOpsService


REGISTRY = {
    "red": BloodhoundRedOrgan(),
    "blue": BloodhoundBlueOrgan(),
    "cors": CORSOrgan(),
    "origin": CyberOriginOrgan(),
    "origin_old": CyberOriginOrganOld(),
    "packet": PacketService(),
    "remote_ops": RemoteOpsService(),
}
