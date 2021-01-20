# * Standard Library Imports ---------------------------------------------------------------------------->
import os
from time import sleep
from contextlib import contextmanager

# * Third Party Imports --------------------------------------------------------------------------------->
from paramiko import SSHClient, AutoAddPolicy

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    # * Local Imports --------------------------------------------------------------------------------------->
    from antipetros_discordbot import __version__
    return __version__


ANTIPETROS_START_CMD = "nohup antipetrosbot run -t token.env -save &"
ANTIPETROS_UPDATE_CMD = "python3.9 -m pip install --no-cache-dir --force-reinstall antipetros_discordbot"
ANTIPETROS_UPDATE_CMD_VERSION = ANTIPETROS_UPDATE_CMD + '==' + get_version()

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
    # run_command(ANTIPETROS_UPDATE_CMD_VERSION)
    # sleep(60)
    run_command(ANTIPETROS_START_CMD)
