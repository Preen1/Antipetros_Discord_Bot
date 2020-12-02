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
from jinja2 import BaseLoader, Environment, FileSystemLoader
# from natsort import natsorted
# from fuzzywuzzy import fuzz, process


# * Gid Imports -->
import gidlogger as glog
from antipetros_discordbot.utility.gidtools_functions import pathmaker, writeit, readit, readbin, writebin, appendwriteit, linereadit, writejson, loadjson, pickleit, get_pickled

from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG, COGS_CONFIG

# endregion[Imports]

__updated__ = '2020-12-02 21:43:23'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

TEMPLATE_PATH = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\antipetros_discordbot\data\data_storage\templates"

ENV = Environment(loader=FileSystemLoader(TEMPLATE_PATH, encoding='utf-8'))

# endregion[Constants]


def _render(template_name: str, in_item: namedtuple, variable_name: str):
    # sourcery skip: inline-immediately-returned-variable
    template = ENV.get_template(template_name + '.py.jinja')
    completed_item = in_item._replace(code=template.render(**{variable_name: in_item}))
    return completed_item


def _render_new_loop(loop_item: namedtuple):
    return _render('loop_template', loop_item, 'loop_item')


def _render_new_listener(listener_item: namedtuple):
    return _render('listener_template', listener_item, 'listener_item')


def _render_new_command(command_item: namedtuple):
    return _render('command_template', command_item, 'command_item')


def _render_new_cog(cog_item: namedtuple):
    return _render('cog_template', cog_item, 'cog_item')


def _edit_configs(cog_item: namedtuple):
    BASE_CONFIG.set('extensions', cog_item.import_location, 'no')
    COGS_CONFIG.add_section(cog_item.config_name)
    BASE_CONFIG.save()
    COGS_CONFIG.save()


def create_cog_file(cog_item: namedtuple, overwrite=False):
    file = pathmaker(cog_item.absolute_location)
    folder = pathmaker(os.path.dirname(file))
    if os.path.isdir(folder) is False:
        os.makedirs(folder)
        writeit(pathmaker(folder, '__init__.py'), '')
    if os.path.isfile(file) is False or overwrite is True:
        writeit(file, cog_item.code)
    _edit_configs(cog_item)

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
