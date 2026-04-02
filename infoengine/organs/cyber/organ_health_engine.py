"""
Organ Health Engine
-------------------
Provides a unified health snapshot for all cyber organs.

This is the backend for the Organ Health Dashboard panel.
It is safe, internal, and does not touch any external systems.
"""

from typing import Dict, Any
import datetime


class OrganHealthEngine:
    def __init__(self, registry):
        """
        registry: the unified organ registry (dict of organ instances)
        """
        self.registry = registry

    def get_health(self) -> Dict[str, Any]:
        """
        Returns a health snapshot for every organ.
        """
        snapshot = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "organs": {}
        }

        for name, organ in self.registry.items():
            snapshot["organs"][name] = self._inspect_organ(organ)

        return snapshot

    def _inspect_organ(self, organ) -> Dict[str, Any]:
        """
        Inspect an organ and return a safe health summary.
        """
        health = {
            "status": "ok",
            "last_activity": None,
            "errors": [],
            "registers": {}
        }

        # Optional: organs may expose a .last_activity attribute
        if hasattr(organ, "last_activity"):
            health["last_activity"] = organ.last_activity

        # Optional: organs may expose a .errors list
        if hasattr(organ, "errors"):
            health["errors"] = organ.errors

        # Optional: organs may expose internal registers
        if hasattr(organ, "registers"):
            health["registers"] = organ.registers

        return health
