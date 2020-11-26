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
from discord.ext import commands
from dotenv import load_dotenv

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

# * Gid Imports -->
import gidlogger as glog
from antipetros_discordbot.utility.gidtools_functions import writejson, pathmaker, loadjson
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG

# endregion[Imports]

__updated__ = '2020-11-26 03:25:53'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class AntiPetrosBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blacklist_user = BASE_CONFIG.getlist('blacklist', 'user')
        self.is_debug = BASE_CONFIG.getboolean('general_settings', 'is_debug')

    async def retrieve_member(self, guild_id, user_id):
        guild = self.get_guild(guild_id)
        return await guild.fetch_member(user_id)


# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
