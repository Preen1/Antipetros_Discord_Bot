

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import random
from time import time
from statistics import mean, mode, stdev, median, variance, pvariance, harmonic_mean, median_grouped
import asyncio
# * Third Party Imports --------------------------------------------------------------------------------->
import discord
from discord.ext import commands

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.cogs import get_aliases
from antipetros_discordbot.utility.misc import save_commands, color_hex_embed, async_seconds_to_pretty_normal, make_config_name, update_config
from antipetros_discordbot.utility.checks import log_invoker, in_allowed_channels, allowed_channel_and_allowed_role, allowed_channel_and_allowed_role_2, command_enabled_checker, allowed_requester
from antipetros_discordbot.utility.named_tuples import MovieQuoteItem
from antipetros_discordbot.utility.embed_helpers import make_basic_embed
from antipetros_discordbot.utility.gidtools_functions import loadjson, writejson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper

# endregion [Imports]

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

COG_NAME = "GeneralDebugCog"
CONFIG_NAME = make_config_name(COG_NAME)

get_command_enabled = command_enabled_checker(CONFIG_NAME)

# endregion [Constants]

# region [TODO]

# TODO: create regions for this file
# TODO: Document and Docstrings


# endregion [TODO]


class GeneralDebugCog(commands.Cog, command_attrs={'hidden': True, "name": COG_NAME}):
    """
    Cog for debug or test commands, should not be enabled fo normal Bot operations.
    """
    config_name = CONFIG_NAME
    docattrs = {'show_in_readme': False,
                'is_ready': True}
    required_config_options = {}

    def __init__(self, bot):
        self.bot = bot
        self.support = self.bot.support
        update_config(self)
        self.allowed_channels_checker = allowed_requester(self, 'channels')
        self.allowed_roles_checker = allowed_requester(self, 'roles')
        self.allowed_dm_ids_checker = allowed_requester(self, 'dm_ids')
        if os.environ.get('INFO_RUN', '') == "1":
            save_commands(self)

        glog.class_init_notification(log, self)

    async def on_ready_setup(self):

        log.debug('setup for cog "%s" finished', str(self))

    async def update(self, typus):
        return
        log.debug('cog "%s" was updated', str(self))

    @commands.command(aliases=get_aliases("roll"), enabled=get_command_enabled('roll'))
    @allowed_channel_and_allowed_role_2()
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
        roll_data = [random.randint(1, 10) for _ in range(target_time * time_multiplier)]

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
        return self.qualified_name


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(GeneralDebugCog(bot))
