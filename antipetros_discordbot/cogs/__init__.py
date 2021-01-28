# * Local Imports -->
# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.utility.gidtools_functions import loadjson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
import os

APPDATA = ParaStorageKeeper.get_appdata()


def get_aliases(command_name):
    data = loadjson(APPDATA['command_aliases.json'])
    return data.get(command_name, [])


def get_brief(command_name):
    data = loadjson(APPDATA['command_help.json'])
    return data.get(command_name, {}).get('brief', None)


def get_description(command_name):
    data = loadjson(APPDATA['command_help.json'])
    return data.get(command_name, {}).get('description', "")


def get_usage(command_name):
    data = loadjson(APPDATA['command_help.json'])
    return data.get(command_name, {}).get('usage', None)

def get_help(command_name):
    data = loadjson(APPDATA['command_help.json'])
    return data.get(command_name, {}).get('help', None)


def get_doc_data(command_name):
    return loadjson(APPDATA['command_help.json']).get(command_name, {"brief": None,"description": "","help": None,"usage": None})

COGS_DIR = os.path.abspath(os.path.dirname(__file__))
if os.path.islink(COGS_DIR) is True:

    COGS_DIR = os.readlink(COGS_DIR).replace('\\\\?\\', '').replace(os.pathsep, '/')
