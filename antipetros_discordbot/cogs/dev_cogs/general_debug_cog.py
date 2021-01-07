

# region [Imports]

# * Standard Library Imports -->
import os
from datetime import datetime, timedelta
from tempfile import TemporaryDirectory
from urllib.parse import urlparse
import asyncio
from time import time, sleep
import random
from pprint import pprint, pformat
from statistics import mean, median, stdev, variance, mode, harmonic_mean, median_grouped, pvariance
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
from antipetros_discordbot.utility.misc import save_commands, async_seconds_to_pretty_normal
from antipetros_discordbot.cogs import get_aliases
from antipetros_discordbot.utility.checks import in_allowed_channels
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

    @commands.command(aliases=get_aliases("roll"))
    @ commands.has_any_role(*COGS_CONFIG.getlist("general_debug", 'allowed_roles'))
    @in_allowed_channels(set(COGS_CONFIG.getlist("general_debug", 'allowed_channels')))
    async def roll(self, ctx, target_time: int = 1):
        start_time = time()
        time_multiplier = 151267
        random_stats_funcs = [("mean", mean),
                              ("median", median),
                              ("stdev", stdev),
                              ("variance", variance),
                              ("mode", mode),
                              ("harmonic_mean", harmonic_mean),
                              ("median_grouped", median_grouped),
                              ("pvariance", pvariance),
                              ('amount', len),
                              ('sum', sum)]
        roll_data = []
        for i in range(target_time * time_multiplier):
            roll_data.append(random.randint(1, 10))
        stats_data = {}
        log.debug("starting calculating statistics")
        for key, func in random_stats_funcs:
            stats_data[key] = round(func(roll_data), ndigits=2)
            log.debug('finished calculating "%s"', key)
        time_taken_seconds = int(round(time() - start_time))
        time_taken = await async_seconds_to_pretty_normal(time_taken_seconds) if time_taken_seconds != 0 else "less than 1 second"
        await ctx.send(embed=await make_basic_embed(title='Roll Result', text='this is a long blocking command for debug purposes', symbol='debug_2', duration=time_taken, ** stats_data))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.user.name})"

    def __str__(self):
        return self.__class__.__name__


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(GeneralDebugCog(bot))
