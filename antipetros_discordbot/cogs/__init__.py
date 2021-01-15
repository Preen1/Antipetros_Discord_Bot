# * Local Imports -->
from antipetros_discordbot.utility.gidtools_functions import loadjson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper

APPDATA = ParaStorageKeeper.get_appdata()


def get_aliases(command_name):
    data = loadjson(APPDATA['command_aliases.json'])
    return data.get(command_name, [])
