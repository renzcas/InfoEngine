class EventBus:
    def __init__(self, organ_registry):
        self.registry = organ_registry

    def emit(self, event: str, payload=None):
        return {"event": event, "payload": payload}
