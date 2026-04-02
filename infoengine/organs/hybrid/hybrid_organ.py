import time

class HybridOrgan:
    def __init__(self):
        self.state = {
            "ticks": 0,
            "last_event": None,
            "last_timestamp": None,
        }

    def heartbeat(self, registry=None, event_bus=None):
        """Primary organism heartbeat — called every tick."""
        self.state["ticks"] += 1
        self.state["last_timestamp"] = time.time()
        self.state["last_event"] = "heartbeat"

        # Emit heartbeat event
        if event_bus:
            event_bus.emit("heartbeat", {
                "tick": self.state["ticks"],
                "timestamp": self.state["last_timestamp"]
            })

        # Pulse all organs that support compute()
        if registry:
            for name, organ in registry.organs.items():
                if hasattr(organ, "compute"):
                    try:
                        organ.compute()
                    except Exception:
                        pass

        return self.state

    def propagate(self, registry=None, event_bus=None):
        """Alias for heartbeat — keeps old API stable."""
        return self.heartbeat(registry, event_bus)

    def status(self):
        return {
            "status": "hybrid online",
            "ticks": self.state["ticks"],
            "last_event": self.state["last_event"],
            "last_timestamp": self.state["last_timestamp"],
        }
