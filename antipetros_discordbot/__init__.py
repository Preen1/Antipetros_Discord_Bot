"""
A Discord Bot for the Antistasi (ArmA 3) Community Discord Server
"""
__version__ = "0.1"


from dotenv import load_dotenv
import os
from importlib.metadata import metadata
load_dotenv('../tools/_project_devmeta.env')
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

os.environ['APP_NAME'] = metadata(__name__).get('name')
os.environ['AUTHOR_NAME'] = metadata(__name__).get('author')


load_dotenv()
