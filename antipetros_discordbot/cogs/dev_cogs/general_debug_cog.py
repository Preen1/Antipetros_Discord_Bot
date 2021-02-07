

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import random
from time import time
from statistics import mean, mode, stdev, median, variance, pvariance, harmonic_mean, median_grouped
import asyncio
from io import BytesIO
# * Third Party Imports --------------------------------------------------------------------------------->
import discord
from discord.ext import commands
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
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
from antipetros_discordbot.utility.poor_mans_abc import attribute_checker
from antipetros_discordbot.utility.enums import CogState
from antipetros_discordbot.utility.replacements.command_replacement import auto_meta_info_command
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
    command_enabled = get_command_enabled
    config_name = CONFIG_NAME
    docattrs = {'show_in_readme': False,
                'is_ready': (CogState.WORKING | CogState.OPEN_TODOS | CogState.UNTESTED | CogState.FEATURE_MISSING | CogState.NEEDS_REFRACTORING,
                             "2021-02-06 05:26:32",
                             "a296317ad6ce67b66c11e18769b28ef24060e5dac5a0b61a9b00653ffbbd9f4e521b2481189f075d029a4e9745892052413d2364e0666a97d9ffc7561a022b07")}
    required_config_options = {}

    def __init__(self, bot):
        self.bot = bot
        self.support = self.bot.support
        update_config(self)
        self.allowed_channels = allowed_requester(self, 'channels')
        self.allowed_roles = allowed_requester(self, 'roles')
        self.allowed_dm_ids = allowed_requester(self, 'dm_ids')
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
    @log_invoker(log, 'debug')
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

    @auto_meta_info_command()
    @allowed_channel_and_allowed_role_2()
    @log_invoker(log, 'debug')
    async def check_random(self, ctx, amount_data_points: int = 10000, amount_possible_values: int = 100):
        async with ctx.typing():
            _sleep_marker = 1000 if amount_data_points >= 100000 else 100
            _results = {pos_num + 1: 0 for pos_num in range(amount_possible_values)}
            for i in range(amount_data_points):
                point = random.randint(1, amount_possible_values)
                _results[point] += 1
                if (i + 1) % (amount_data_points // _sleep_marker) == 0:
                    percent = round(((i + 1) / amount_data_points) * 100, ndigits=1)
                    log.debug(f"reached {i+1}, {percent}% done!")
                    await asyncio.sleep(1 / random.randint(1, 100))
            await asyncio.sleep(2)
            x = []
            y = []
            for key, value in _results.items():
                x.append(key)
                y.append(value)
            plt.plot(x, y, 's-b', markersize=4, linewidth=0.2, alpha=1)

            plt.axis(ymin=0, ymax=max(value for key, value in _results.items()) * 1.05, xmax=amount_possible_values, xmin=1)
            with BytesIO() as image_binary:
                plt.savefig(image_binary, format='png')
                plt.close()
                image_binary.seek(0)

                await ctx.send(file=discord.File(image_binary, filename='checkrandomgraph.png'), delete_after=120)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.user.name})"

    def __str__(self):
        return self.qualified_name

    @commands.command(aliases=get_aliases("request_server_restart"))
    @allowed_channel_and_allowed_role_2()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def request_server_restart(self, ctx):

        if ctx.prefix != "<@&800769712879042612> ":

            return

        servers = ["COMMUNITY_SERVER_1", "TEST_SERVER_1", "TEST_SERVER_2"]
        await ctx.send(f"please specify the server name in the next 20 seconds | OPTIONS: {', '.join(servers)}")
        user = ctx.author
        channel = ctx.channel

        def check(m):
            return m.author.name == user.name and m.channel.name == channel.name
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=20.0)
            if any(server.casefold() in msg.content.casefold() for server in servers):
                for server in servers:
                    if server.casefold() in msg.content.casefold():
                        _server = server
            else:
                await ctx.send('No valid answer received, aborting request, you can always try again')
                return
            await ctx.send("Did the commander save and is everyone ready for a restart? answer time: 20 seconds | OPTIONS: YES, NO")
            try:
                msg_2 = await self.bot.wait_for('message', check=check, timeout=20.0)
                if msg_2.content.casefold() == 'yes':
                    is_saved = 'yes'
                elif msg_2.content.casefold() == 'no':
                    is_saved = 'no'
                else:
                    await ctx.send('No valid answer received, aborting request, you can always try again')
                    return
                await ctx.send("notifying admin now")
                member = await self.bot.retrieve_antistasi_member(576522029470056450)
                await member.send(f"This is a notification from {ctx.author.name}!\nHe requests a server restart for server {_server}, saved and ready: {is_saved}")
                await ctx.send(f"I have notified {member.name} per DM!")
            except asyncio.TimeoutError:
                await ctx.send('No answer received, aborting request, you can always try again')
                return

        except asyncio.TimeoutError:
            await ctx.send('No answer received, aborting request, you can always try again')
            return


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(attribute_checker(GeneralDebugCog(bot)))
