"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ------------------------------------------------------------------------------------------------------------------------------------>

import gc
import os
import re
import sys
import json
import lzma
import time
import queue
import base64
import pickle
import random
import shelve
import shutil
import asyncio
import logging
import sqlite3
import platform
import importlib
import subprocess
import unicodedata

from io import BytesIO
from abc import ABC, abstractmethod
from copy import copy, deepcopy
from enum import Enum, Flag, auto
from time import time, sleep, time_ns
from pprint import pprint, pformat
from string import Formatter, digits, printable, whitespace, punctuation, ascii_letters, ascii_lowercase, ascii_uppercase
from timeit import Timer
from typing import Union, Callable, Iterable
from inspect import stack, getdoc, getmodule, getsource, getmembers, getmodulename, getsourcefile, getfullargspec, getsourcelines
from zipfile import ZipFile
from datetime import tzinfo, datetime, timezone, timedelta
from tempfile import TemporaryDirectory
from textwrap import TextWrapper, fill, wrap, dedent, indent, shorten
from functools import wraps, partial, lru_cache, singledispatch, total_ordering
from importlib import import_module, invalidate_caches
from contextlib import contextmanager
from statistics import mean, mode, stdev, median, variance, pvariance, harmonic_mean, median_grouped
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from urllib.parse import urlparse
from importlib.util import find_spec, module_from_spec, spec_from_file_location
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from importlib.machinery import SourceFileLoader


# * Third Party Imports ----------------------------------------------------------------------------------------------------------------------------------------->


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

# * Gid Imports ------------------------------------------------------------------------------------------------------------------------------------------------->

import gidlogger as glog

from antipetros_discordbot.utility.gidtools_functions import (readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                                                              dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file, create_file)


# * Local Imports ----------------------------------------------------------------------------------------------------------------------------------------------->

from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.named_tuples import MemberRoleItem
# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]


# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


class BlacklistedUserItem:

    def __init__(self, warden, user_id: int, user_name: str, notified: bool = False, command_called: int = 0):
        self.warden = warden
        self.id = user_id
        self.name = user_name
        self._command_called = command_called
        self.notified = notified

    @property
    def command_called(self):
        return self._command_called

    def tried_calling(self):
        self._command_called += 1

    async def unblacklist(self):
        await self.warden.unblacklist_user(self)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return other == self.id
        elif isinstance(other, str):
            return other == self.name
        elif isinstance(other, BlacklistedUserItem):
            return other is self
        elif isinstance(other, discord.Member):
            return other.id == self.id
        elif isinstance(other, discord.User):
            return other.id == self.id

    def __hash__(self) -> int:
        return hash(self.notified) + hash(self._command_called) + hash(self.id) + hash(self.name)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'command_called': self._command_called, 'notified':self.notified}

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
