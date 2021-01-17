from paramiko import SSHClient, AutoAddPolicy
import os
from contextlib import contextmanager


ANTIPETROS_START_CMD = "nohup antipetrosbot run -t token.env -save &"
ANTIPETROS_UPDATE_CMD = "python3.9 -m pip install --no-cache-dir --force-reinstall antipetros_discordbot"


USERNAME = 'root'
PWD = os.getenv('DEVANTISTASI_AUXILIARY_KEY')
channel_files_to_close = []


@contextmanager
def start_client():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(hostname="192.248.189.227", username=USERNAME, password=PWD)
    yield client
    client.close()


def run_command(command: str):
    with start_client() as client:
        stdin, stdout, stderr = client.exec_command(command)
        if command != ANTIPETROS_START_CMD:
            print('##### STDOUT #####')
            print(stdout.read().decode())
            print('##### STDERR #####')
            print(stderr.read().decode())


if __name__ == '__main__':
    run_command(ANTIPETROS_START_CMD)
