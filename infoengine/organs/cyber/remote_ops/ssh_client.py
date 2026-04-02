import paramiko
from contextlib import contextmanager

@contextmanager
def ssh_connection(host: str, username: str, key_path: str):
    key = paramiko.RSAKey.from_private_key_file(key_path)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, pkey=key)
    try:
        yield client
    finally:
        client.close()

def run_ssh_command(host: str, username: str, key_path: str, command: str):
    with ssh_connection(host, username, key_path) as client:
        stdin, stdout, stderr = client.exec_command(command)
        return (
            stdout.read().decode(),
            stderr.read().decode(),
            stdout.channel.recv_exit_status(),
        )