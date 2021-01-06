

# region [Imports]

# * Standard Library Imports -->
import os
from datetime import datetime, timedelta
from tempfile import TemporaryDirectory
from urllib.parse import urlparse
import asyncio
from pprint import pprint, pformat
# * Third Party Imports -->
import aiohttp
import discord
from discord.ext import tasks, commands
import discord
# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.utility.enums import RequestStatus
from antipetros_discordbot.utility.named_tuples import LINK_DATA_ITEM
from antipetros_discordbot.utility.sqldata_storager import LinkDataStorageSQLite
from antipetros_discordbot.utility.gidtools_functions import writeit, loadjson, pathmaker, writejson
from antipetros_discordbot.init_userdata.user_data_setup import SupportKeeper
from antipetros_discordbot.utility.embed_helpers import make_basic_embed
from antipetros_discordbot.utility.misc import save_commands
from antipetros_discordbot.cogs import get_aliases
# endregion [Imports]

# region [Logging]

log = glog.aux_logger(__name__)
glog.import_notification(log, __name__)

# endregion[Logging]

# region [Constants]
APPDATA = SupportKeeper.get_appdata()
BASE_CONFIG = SupportKeeper.get_config('base_config')
COGS_CONFIG = SupportKeeper.get_config('cogs_config')
# location of this file, does not work if app gets compiled to exe with pyinstaller
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


# endregion [Constants]

# region [TODO]

# TODO: create regions for this file
# TODO: Document and Docstrings


# endregion [TODO]


class GeneralDebugCog(commands.Cog, command_attrs={'hidden': True, "name": "GeneralDebugCog"}):

    config_name = 'general_debug'

    def __init__(self, bot):
        self.bot = bot
        if self.bot.is_debug:
            save_commands(self)
        glog.class_init_notification(log, self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.user.name})"

    def __str__(self):
        return self.__class__.__name__


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(GeneralDebugCog(bot))
