# * Local Imports -->
# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.utility.gidtools_functions import loadjson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper

APPDATA = ParaStorageKeeper.get_appdata()


def get_aliases(command_name):
    data = loadjson(APPDATA['command_aliases.json'])
    return data.get(command_name, [])


# * Standard Library Imports ---------------------------------------------------------------------------->
import os

COGS_DIR = os.path.abspath(os.path.dirname(__file__))
if os.path.islink(COGS_DIR) is True:

    COGS_DIR = os.readlink(COGS_DIR).replace('\\\\?\\', '').replace(os.pathsep, '/')
