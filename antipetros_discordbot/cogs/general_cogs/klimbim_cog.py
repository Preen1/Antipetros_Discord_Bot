
# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
from datetime import datetime
import random
import secrets
import typing
import asyncio

# * Third Party Imports --------------------------------------------------------------------------------->
from pytz import timezone, country_timezones
from fuzzywuzzy import fuzz
from fuzzywuzzy import process as fuzzprocess
from discord.ext import commands
from discord import AllowedMentions
import discord
from pyfiglet import Figlet
# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.cogs import get_aliases, get_doc_data
from antipetros_discordbot.utility.misc import STANDARD_DATETIME_FORMAT, save_commands, CogConfigReadOnly, make_config_name, update_config
from antipetros_discordbot.utility.checks import in_allowed_channels, allowed_channel_and_allowed_role, has_attachments, command_enabled_checker, allowed_requester, allowed_channel_and_allowed_role_2
from antipetros_discordbot.utility.named_tuples import CITY_ITEM, COUNTRY_ITEM
from antipetros_discordbot.utility.gidtools_functions import loadjson, writejson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.discord_markdown_helper.the_dragon import THE_DRAGON
from antipetros_discordbot.utility.discord_markdown_helper.special_characters import ZERO_WIDTH

# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)


# endregion[Logging]

# region [Constants]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
# location of this file, does not work if app gets compiled to exe with pyinstaller
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

COG_NAME = "KlimBimCog"

CONFIG_NAME = make_config_name(COG_NAME)

get_command_enabled = command_enabled_checker(CONFIG_NAME)

# endregion[Constants]


class KlimBimCog(commands.Cog, command_attrs={'hidden': True, "name": COG_NAME}):
    """
    Soon
    """
    # region [ClassAttributes]
    config_name = CONFIG_NAME
    docattrs = {'show_in_readme': True,
                'is_ready': True}
    required_config_options = {}
    # endregion [ClassAttributes]

    # region [Init]

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

# endregion [Init]

# region [Properties]


# endregion [Properties]

# region [Setup]


    async def on_ready_setup(self):

        log.debug('setup for cog "%s" finished', str(self))

    async def update(self, typus):
        return
        log.debug('cog "%s" was updated', str(self))


# endregion [Setup]

# region [Loops]


# endregion [Loops]

# region [Listener]


# endregion [Listener]

# region [Commands]

    @ commands.command(aliases=get_aliases("the_dragon"), enabled=get_command_enabled('the_dragon'))
    @allowed_channel_and_allowed_role_2()
    @commands.cooldown(1, 60, commands.BucketType.channel)
    async def the_dragon(self, ctx):
        await ctx.send(THE_DRAGON)

    @ commands.command(aliases=get_aliases("flip_coin"), enabled=get_command_enabled('flip_coin'))
    @allowed_channel_and_allowed_role_2()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def flip_coin(self, ctx: commands.Context):
        with ctx.typing():
            result = (secrets.randbelow(2) + 1)
            if result % 2 == 0:
                coin = 'heads'
            else:
                coin = 'tails'
            await asyncio.sleep(2)
            coin_image = "https://i.postimg.cc/mDKvvG2J/antipetros-coin-head.png" if coin == 'heads' else "https://i.postimg.cc/yx9MBrDd/antipetros-coin-tails.png"
            embed = await self.bot.make_generic_embed(title=coin.title(), description=ZERO_WIDTH, image=coin_image, thumbnail='no_thumbnail')
            await ctx.reply(**embed, allowed_mentions=AllowedMentions.none())

    @ commands.command(aliases=get_aliases("urban"), enabled=get_command_enabled('urban_dictionary'))
    @allowed_channel_and_allowed_role_2()
    async def urban_dictionary(self, ctx, term: str):
        _out = {}
        x = await self.bot.urban_client.get_definition(term)
        for index, y in enumerate(x):
            if index < 15:
                definition = x[0].definition
                cleaned_definition = definition.replace('[', '**').replace(']', '**')
                cleaned_definition = definition.replace('[', '**').replace(']', '**')
                if cleaned_definition not in _out.values():
                    _out[str(index)] = cleaned_definition
        await ctx.send(f"```fix\n{_out['0']}```")

    @ commands.command(aliases=get_aliases("make_figlet"), enabled=get_command_enabled('make_figlet'))
    @allowed_channel_and_allowed_role_2()
    @commands.cooldown(1, 60, commands.BucketType.channel)
    async def make_figlet(self, ctx, *, text: str):

        figlet = Figlet(font='gothic', width=300)
        new_text = figlet.renderText(text.upper())
        await ctx.send(f"```fix\n{new_text}\n```")
# endregion [Commands]

# region [DataStorage]


# endregion [DataStorage]

# region [Embeds]


# endregion [Embeds]

# region [HelperMethods]


# endregion [HelperMethods]

# region [SpecialMethods]


    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.user.name})"

    def __str__(self):
        return self.qualified_name

    def cog_unload(self):

        pass


# endregion [SpecialMethods]


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(KlimBimCog(bot))
