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
from configparser import ConfigParser

# * Third Party Imports -->
# import pyperclip
# from dotenv import load_dotenv
# from jinja2 import BaseLoader, Environment, FileSystemLoader
# from natsort import natsorted
# from fuzzywuzzy import fuzz, process


# * Gid Imports -->
import gidlogger as glog
from antipetros_discordbot.utility.gidtools_functions import pathmaker, writeit, readit, readbin, writebin, appendwriteit, linereadit, writejson, loadjson, pickleit, get_pickled

from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG, COGS_CONFIG

# endregion[Imports]

__updated__ = '2020-12-03 01:33:51'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]


# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
