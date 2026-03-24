from dataclasses import dataclass

@dataclass
class SSHCommandResult:
    stdout: str
    stderr: str
    exit_code: int