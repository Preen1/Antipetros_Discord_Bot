"""
A Discord Bot for the Antistasi (ArmA 3) Community Discord Server
"""
__version__ = "0.1.10"


# * Standard Library Imports -->
import os
from importlib.metadata import metadata

# * Third Party Imports -->
from dotenv import load_dotenv

MAIN_DIR = os.path.abspath(os.path.dirname(__file__))
if os.path.islink(MAIN_DIR) is True:

    MAIN_DIR = os.readlink(MAIN_DIR).replace('\\\\?\\', '')

old_cd = os.getcwd()
os.chdir(MAIN_DIR)
dev_indicator_env_path = os.path.normpath(os.path.join(MAIN_DIR, '../tools/_project_devmeta.env'))

if os.path.isfile(dev_indicator_env_path):
    load_dotenv(dev_indicator_env_path)
    os.environ['IS_DEV'] = 'true'
else:
    os.environ['IS_DEV'] = 'false'
os.environ['APP_NAME'] = metadata(__name__).get('name')
os.environ['AUTHOR_NAME'] = metadata(__name__).get('author')
os.environ['BASE_FOLDER'] = MAIN_DIR
os.environ['LOG_FOLDER'] = MAIN_DIR
os.chdir(old_cd)
os.environ['DISABLE_IMPORT_LOGCALLS'] = "1"
