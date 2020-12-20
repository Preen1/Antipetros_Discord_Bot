"""
A Discord Bot for the Antistasi (ArmA 3) Community Discord Server
"""
__version__ = "0.1"


from dotenv import load_dotenv
import os
from importlib.metadata import metadata

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
old_cd = os.getcwd()
os.chdir(THIS_FILE_DIR)

load_dotenv(r'D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\tools\_project_devmeta.env')
os.environ['APP_NAME'] = metadata(__name__).get('name')
os.environ['AUTHOR_NAME'] = metadata(__name__).get('author')
os.environ['BASE_FOLDER'] = os.getenv('TOPLEVELMODULE')
os.environ['LOG_FOLDER'] = os.path.join(os.getenv('TOPLEVELMODULE'))
load_dotenv()
os.chdir(old_cd)
