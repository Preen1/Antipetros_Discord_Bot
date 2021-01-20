
# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import gc
import os
import unicodedata
from datetime import datetime

# * Third Party Imports --------------------------------------------------------------------------------->
import aiohttp
import discord
from discord import File, Embed, DiscordException
from dateparser import parse as date_parse
from discord.ext import tasks, commands
from async_property import async_property

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.cogs import get_aliases
from antipetros_discordbot.utility.misc import CogConfigReadOnly, save_commands
from antipetros_discordbot.utility.enums import RequestStatus
from antipetros_discordbot.utility.checks import log_invoker, in_allowed_channels, allowed_channel_and_allowed_role
from antipetros_discordbot.utility.named_tuples import LINK_DATA_ITEM, GiveAwayEventItem
from antipetros_discordbot.utility.embed_helpers import EMBED_SYMBOLS, make_basic_embed
from antipetros_discordbot.utility.sqldata_storager import LinkDataStorageSQLite
from antipetros_discordbot.utility.gidtools_functions import writeit, loadjson, pathmaker, writejson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper

# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
glog.import_notification(log, __name__)

# endregion[Logging]

# region [Constants]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
# location of this file, does not work if app gets compiled to exe with pyinstaller
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_NAME = "give_away"
# endregion[Constants]

# region [Helper]

_from_cog_config = CogConfigReadOnly(CONFIG_NAME)

# endregion [Helper]

# "GiveAwayEventItem" =  ['name', 'channel_name', 'message_id', 'enter_emoji', 'end_date_time', 'end_message', 'amount_winners']


class GiveAwayCog(commands.Cog, command_attrs={'name': "GiveAwayCog", "description": ""}):
    """
    [summary]

    [extended_summary]

    """
# region [ClassAttributes]

# endregion [ClassAttributes]

# region [Init]

    def __init__(self, bot):

        self.bot = bot
        self.support = self.bot.support
        self.give_aways = []
        if os.environ.get('INFO_RUN', '') == "1":
            save_commands(self)
        glog.class_init_notification(log, self)

# endregion [Init]

# region [Properties]


# endregion [Properties]

# region [Setup]


    async def on_ready_setup(self):
        log.debug('setup for cog "%s" finished', str(self))

# endregion [Setup]

# region [Loops]

    @tasks.loop(seconds=5, reconnect=True)
    async def check_give_away_ended_loop(self):
        for give_away_event in self.give_aways:
            if datetime.utcnow() >= give_away_event.end_date_time:
                await self.give_away_finished(give_away_event)

# endregion [Loops]

# region [Listener]


# endregion [Listener]

# region [Commands]


    @commands.command(aliases=get_aliases("check_datetime_stuff"))
    @allowed_channel_and_allowed_role(config_name=CONFIG_NAME, in_dm_allowed=False)
    @log_invoker(logger=log, level="info")
    async def check_datetime_stuff(self, ctx, *, date_string: str):
        conv_string = date_parse(date_string)
        await ctx.send(conv_string)

    @commands.command(aliases=get_aliases("start_giveaway"))
    @allowed_channel_and_allowed_role(config_name=CONFIG_NAME, in_dm_allowed=False)
    @log_invoker(logger=log, level="info")
    async def create_giveaway(self, ctx):
        pass

    @commands.command(aliases=get_aliases("start_giveaway"))
    @allowed_channel_and_allowed_role(config_name=CONFIG_NAME, in_dm_allowed=False)
    @log_invoker(logger=log, level="info")
    async def start_giveaway(self, ctx):
        pass

    @commands.command(aliases=get_aliases("abort_give_away"))
    @allowed_channel_and_allowed_role(config_name=CONFIG_NAME, in_dm_allowed=False)
    @log_invoker(logger=log, level="info")
    async def abort_give_away(self, ctx):
        pass

    @commands.command(aliases=get_aliases("finish_give_away"))
    @allowed_channel_and_allowed_role(config_name=CONFIG_NAME, in_dm_allowed=False)
    @log_invoker(logger=log, level="info")
    async def finish_give_away(self, ctx):
        pass


# endregion [Commands]

# region [DataStorage]


# endregion [DataStorage]

# region [Embeds]


# endregion [Embeds]

# region [HelperMethods]


# endregion [HelperMethods]

# region [SpecialMethods]


    def cog_check(self, ctx):
        return True

    async def cog_command_error(self, ctx, error):
        pass

    async def cog_before_invoke(self, ctx):
        pass

    async def cog_after_invoke(self, ctx):
        pass

    def cog_unload(self):

        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.user.name})"

    def __str__(self):
        return self.__class__.__name__


# endregion [SpecialMethods]


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(GiveAwayCog(bot))
