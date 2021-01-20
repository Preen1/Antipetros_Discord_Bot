
# region [Imports]

# * Standard Library Imports -->
import gc
import os
import re
import sys
import json
import lzma
import time
import queue
import logging
import platform
import subprocess
from enum import Enum, Flag, auto
from time import sleep
from pprint import pprint, pformat
from typing import Union
from datetime import tzinfo, datetime, timezone, timedelta
from functools import wraps, lru_cache, singledispatch, total_ordering, partial
from contextlib import contextmanager
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from tempfile import TemporaryDirectory
from urllib.parse import urlparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import unicodedata
from io import BytesIO

# * Third Party Imports -->
# import requests
# import pyperclip
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# from github import Github, GithubException
# from jinja2 import BaseLoader, Environment
# from natsort import natsorted
# from fuzzywuzzy import fuzz, process
import aiohttp
import discord
from discord.ext import tasks, commands
from discord import DiscordException, Embed, File
from async_property import async_property

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.utility.enums import RequestStatus
from antipetros_discordbot.utility.named_tuples import LINK_DATA_ITEM
from antipetros_discordbot.utility.sqldata_storager import LinkDataStorageSQLite
from antipetros_discordbot.utility.gidtools_functions import writeit, loadjson, pathmaker, writejson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.embed_helpers import make_basic_embed, EMBED_SYMBOLS
from antipetros_discordbot.utility.misc import save_commands, CogConfigReadOnly
from antipetros_discordbot.utility.checks import in_allowed_channels, allowed_channel_and_allowed_role, log_invoker
from antipetros_discordbot.cogs import get_aliases
from antipetros_discordbot.utility.named_tuples import GiveAwayEventItem
from dateparser import parse as date_parse
import arrow
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
