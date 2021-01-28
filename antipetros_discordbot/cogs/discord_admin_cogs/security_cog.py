# jinja2: trim_blocks:True
# jinja2: lstrip_blocks :True
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
from typing import Union, TYPE_CHECKING
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
import magic
# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.utility.enums import RequestStatus
from antipetros_discordbot.utility.named_tuples import LINK_DATA_ITEM, ListenerContext
from antipetros_discordbot.utility.sqldata_storager import LinkDataStorageSQLite
from antipetros_discordbot.utility.gidtools_functions import writeit, loadjson, pathmaker, writejson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.embed_helpers import make_basic_embed, EMBED_SYMBOLS
from antipetros_discordbot.utility.misc import save_commands, CogConfigReadOnly
from antipetros_discordbot.utility.checks import in_allowed_channels, allowed_channel_and_allowed_role, log_invoker
from antipetros_discordbot.cogs import get_aliases

if TYPE_CHECKING:
    from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot


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
CONFIG_NAME = "security"

# endregion[Constants]

# region [Helper]

_from_cog_config = CogConfigReadOnly(CONFIG_NAME)

# endregion [Helper]


class SecurityCog(commands.Cog, command_attrs={'name': "SecurityCog", "description": ""}):
    """
    [summary]

    [extended_summary]

    """
# region [ClassAttributes]

# endregion [ClassAttributes]

# region [Init]

    def __init__(self, bot: AntiPetrosBot):
        self.bot = bot
        self.support = self.bot.support
        self.file_magic = magic.Magic(mime=True, uncompress=True)
        if os.environ.get('INFO_RUN', '') == "1":
            save_commands(self)
        glog.class_init_notification(log, self)

# endregion [Init]

# region [Properties]

    @property
    def forbidden_extensions(self):
        return [ext.casefold() for ext in _from_cog_config('forbidden_file_extensions', list)]

    @property
    def forbidden_mime_types(self):
        return _from_cog_config('forbidden_mime_types', list)


# endregion [Properties]

# region [Setup]

    async def on_ready_setup(self):
        log.debug('setup for cog "%s" finished', str(self))

# endregion [Setup]

# region [Loops]


# endregion [Loops]

# region [Listener]


    @ commands.Cog.listener(name="on_message")
    async def attachment_scanner(self, message: discord.Message):
        if _from_cog_config('enable_attachment_scanner', bool) is False or len(message.attachments) == 0 or await self._attachment_scanner_exclusion_check(message) is True:
            return
        listener_context = ListenerContext(message=message,
                                           content=message.content,
                                           channel=message.channel,
                                           author=message.author,
                                           creation_time=message.created_at,
                                           reactions=message.reactions,
                                           attachments=message.attachments)

        for attachment in listener_context.attachments:
            filename = attachment.filename
            extension = filename.split('.')[-1]
            if extension.casefold() in self.forbidden_extensions:
                await self._handle_forbidden_attachment(listener_context, filename)
                return
            bytes_content = await attachment.read()
            if self.file_magic.from_buffer(bytes_content) in self.forbidden_mime_types:
                await self._handle_forbidden_attachment(listener_context, filename)
                return

# endregion [Listener]

# region [Commands]

# endregion [Commands]

# region [DataStorage]

# endregion [DataStorage]

# region [HelperMethods]

    async def _attachment_scanner_exclusion_check(self, msg):
        if msg.author.name.casefold() in [name.casefold() for name in _from_cog_config('attachment_scanner_exclude_user', list)]:
            return True
        allowed_roles = [role_name.casefold() for role_name in _from_cog_config('attachment_scanner_exclude_roles', list)]
        if any(role.name.casefold() in allowed_roles for role in msg.author.roles):
            return True
        if msg.channel.name.casefold in [channel_name.casefold() for channel_name in _from_cog_config('attachment_scanner_exclude_channels', list)]:
            return True
        return False

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
    bot.add_cog(SecurityCog(bot))


# region [Main_Exec]

if __name__ == '__main__':
    pass

# endregion [Main_Exec]
