"""
A Discord Bot for the Antistasi (ArmA 3) Community Discord Server
"""
__version__ = "0.1"


from dotenv import load_dotenv
import os
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DEVMETA_FILE = os.path.normpath(os.path.join('../tools/_project_devmeta.env'))

if os.path.isfile(PROJECT_DEVMETA_FILE) is True:
    load_dotenv(PROJECT_DEVMETA_FILE)
    print('set devmeta')
else:
    print('devmeta not set')
    print(PROJECT_DEVMETA_FILE)

load_dotenv()
