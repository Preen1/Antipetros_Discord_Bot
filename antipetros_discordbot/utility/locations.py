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
from glob import iglob

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
from gidtools.gidfiles import (QuickFile, readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                               dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file, work_in)
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG
import antipetros_discordbot
# endregion[Imports]

__updated__ = '2020-11-08 12:46:46'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


def find_path(path_fragment):
    """
    finds absolute path, to folder or file.


    Args:
        path_fragment (str): the fragment to find

    Returns:
        str: absolute path to the fragment
    """
    _main_dir = os.getenv('MAIN_DIR')
    with work_in(_main_dir):
        return pathmaker(os.path.abspath(list(iglob(f"**/{path_fragment}", recursive=bool))[0]))


# region[Main_Exec]

if __name__ == '__main__':
    pass

# endregion[Main_Exec]
