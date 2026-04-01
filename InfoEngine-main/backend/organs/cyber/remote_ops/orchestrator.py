from .ssh_client import run_ssh_command
from .models import SSHCommandResult

class RemoteOpsOrchestrator:
    def execute(self, host: str, username: str, key_path: str, command: str) -> SSHCommandResult:
        out, err, code = run_ssh_command(host, username, key_path, command)
        return SSHCommandResult(stdout=out, stderr=err, exit_code=code)