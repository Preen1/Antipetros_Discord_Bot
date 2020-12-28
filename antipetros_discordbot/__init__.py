"""
A Discord Bot for the Antistasi (ArmA 3) Community Discord Server
"""
__version__ = "0.1.1"


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
old_cd = os.getcwd()
os.chdir(THIS_FILE_DIR)

if os.path.isfile(r'D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\tools\_project_devmeta.env'):
    load_dotenv(r'D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\tools\_project_devmeta.env')
    os.environ['IS_DEV'] = 'true'
os.environ['APP_NAME'] = metadata(__name__).get('name')
os.environ['AUTHOR_NAME'] = metadata(__name__).get('author')
os.environ['BASE_FOLDER'] = os.getenv('TOPLEVELMODULE')
os.environ['LOG_FOLDER'] = os.path.join(os.getenv('TOPLEVELMODULE'))

os.chdir(old_cd)
