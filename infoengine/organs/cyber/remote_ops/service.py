from .orchestrator import RemoteOpsOrchestrator

class RemoteOpsService:
    def __init__(self):
        self.orchestrator = RemoteOpsOrchestrator()

    def run(self, host: str, username: str, key_path: str, command: str):
        return self.orchestrator.execute(host, username, key_path, command)