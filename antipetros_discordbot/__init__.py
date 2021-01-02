"""
A Discord Bot for the Antistasi (ArmA 3) Community Discord Server
"""
__version__ = "0.1.0"


from dotenv import load_dotenv
import os
from importlib.metadata import metadata
import platform


def install_uvloop_if_needed():
    try:
        import uvloop
    except ImportError:
        print("uvloop package not installed, installing now.\nYou may need to restart the application afterwards")
        import sys
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "package"])


if platform.system() == 'Linux':
    print('Platform detected as "Linux"')
    print('checking conditional dependencies')
    install_uvloop_if_needed()
elif platform.system() == "Windows":
    print('Platform detected as "Windows"')
    print('there are no conditional dependencies for "Windows"')

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
if os.path.islink(THIS_FILE_DIR) is True:

    THIS_FILE_DIR = os.readlink(THIS_FILE_DIR).replace('\\\\?\\', '')

old_cd = os.getcwd()
os.chdir(THIS_FILE_DIR)
dev_indicator_env_path = os.path.normpath(os.path.join(THIS_FILE_DIR, '../tools/_project_devmeta.env'))

if os.path.isfile(dev_indicator_env_path):
    load_dotenv(dev_indicator_env_path)
    os.environ['IS_DEV'] = 'true'
os.environ['APP_NAME'] = metadata(__name__).get('name')
os.environ['AUTHOR_NAME'] = metadata(__name__).get('author')
os.environ['BASE_FOLDER'] = THIS_FILE_DIR
os.environ['LOG_FOLDER'] = THIS_FILE_DIR
os.chdir(old_cd)
