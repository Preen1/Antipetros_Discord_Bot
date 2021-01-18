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
from time import time, sleep
from pprint import pprint, pformat
from string import Formatter, digits, printable, whitespace, punctuation, ascii_letters, ascii_lowercase, ascii_uppercase
from timeit import Timer
from typing import Union, Callable, Iterable, Dict
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

# import discord

# import requests

# import pyperclip

# import matplotlib.pyplot as plt

# from bs4 import BeautifulSoup

# from dotenv import load_dotenv

# from discord import Embed, File

# from discord.ext import commands, tasks

# from github import Github, GithubException

# from jinja2 import BaseLoader, Environment

# from natsort import natsorted

# from fuzzywuzzy import fuzz, process

import autopep8

# * PyQt5 Imports ----------------------------------------------------------------------------------------------------------------------------------------------->

# from PyQt5.QtGui import QFont, QIcon, QBrush, QColor, QCursor, QPixmap, QStandardItem, QRegExpValidator

# from PyQt5.QtCore import (Qt, QRect, QSize, QObject, QRegExp, QThread, QMetaObject, QCoreApplication,
#                           QFileSystemWatcher, QPropertyAnimation, QAbstractTableModel, pyqtSlot, pyqtSignal)

# from PyQt5.QtWidgets import (QMenu, QFrame, QLabel, QAction, QDialog, QLayout, QWidget, QWizard, QMenuBar, QSpinBox, QCheckBox, QComboBox, QGroupBox, QLineEdit,
#                              QListView, QCompleter, QStatusBar, QTableView, QTabWidget, QDockWidget, QFileDialog, QFormLayout, QGridLayout, QHBoxLayout,
#                              QHeaderView, QListWidget, QMainWindow, QMessageBox, QPushButton, QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWizardPage,
#                              QApplication, QButtonGroup, QRadioButton, QFontComboBox, QStackedWidget, QListWidgetItem, QSystemTrayIcon, QTreeWidgetItem,
#                              QDialogButtonBox, QAbstractItemView, QCommandLinkButton, QAbstractScrollArea, QGraphicsOpacityEffect, QTreeWidgetItemIterator)


# * Gid Imports ------------------------------------------------------------------------------------------------------------------------------------------------->

import gidlogger as glog

# from gidtools.gidfiles import (QuickFile, readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
#                                dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)


# * Local Imports ----------------------------------------------------------------------------------------------------------------------------------------------->
from antipetros_discordbot.dev_tools_and_scripts.data.event_data import EVENT_MAPPING
from antipetros_discordbot.cogs import COGS_DIR
from antipetros_discordbot.utility.gidtools_functions import pathmaker, create_folder, create_file
from antipetros_discordbot.utility.exceptions import CogNameNotCamelCaseError
from antipetros_discordbot.dev_tools_and_scripts.template_handling.templates import TEMPLATES_DIR, TEMPLATE_MANAGER
from antipetros_discordbot.utility.misc import split_camel_case_string
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
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

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


class LoopTemplateItem:
    allowed_attributes_map = {"seconds": float,
                              "minutes": float,
                              "hours": float,
                              "count": int,
                              "reconnect": bool,
                              "loop": asyncio.AbstractEventLoop}

    def __init__(self, name):
        self.name = name
        self.all_attributes = {"seconds": 0.0, "minutes": 0.0, "hours": 0.0, "count": "None", "reconnect": True, "loop": "None"}

    def set_attribute(self, attribute_name, value):
        if attribute_name not in self.allowed_attributes_map:
            raise KeyError
        typus = self.allowed_attributes_map.get(attribute_name)
        if not isinstance(value, typus):
            raise TypeError
        self.all_attributes[attribute_name] = value


class ListenerTemplateItem:
    event_mapping = EVENT_MAPPING

    def __init__(self, name, event_name):
        self.name = name
        if event_name not in self.event_mapping:
            raise KeyError(f'unknown event "{event_name}"')
        self._event_name = event_name

    @property
    def args(self):
        return self.event_mapping.get(self.event_name, [])

    @property
    def event_name(self):
        return self._event_name

    @event_name.setter
    def event_name(self, value: str):
        if value not in self.event_mapping:
            raise KeyError(f'unknown event "{value}"')
        self._event_name = value


class CommandTemplateItem:
    allowed_check_config_keys = {'allowed_in_dm_key', 'allowed_roles_key', 'allowed_channel_key'}

    def __init__(self, name, dm_allowed=False, log_invocation=False, **check_config_keys: Dict[str, str]):
        self.name = name
        self.dm_allowed = dm_allowed
        self.log_invocation = log_invocation
        for key, value in check_config_keys.items():
            if key not in self.allowed_check_config_keys:
                raise KeyError(f'config_key "{key}" not allowed key, {self.allowed_check_config_keys=}')
            setattr(self, key, value)


class CogTemplateItem:
    allowed_command_attr = {"hidden": bool, "enabled": bool}
    standard_template_name = 'cog_template.py.jinja'
    template_var_name = 'cog_item'

    def __init__(self, name: str, category: str, overwrite: bool = False):
        self.name = name
        self._check_name()
        self.category = category
        self.overwrite = overwrite
        self.all_loops = []
        self.all_listeners = []
        self.all_commands = []
        self.all_com_attr = {}
        self.extra_imports = []
        self.config_options = []
        self._template_name = self.standard_template_name
        self.format_code = True

    def add_extra_import(self, package_name, typus=None, *members):
        import_statement = ''
        if typus is None:
            import_statement = f"import {package_name}"
        elif typus == 'from':
            if members in [None, [], '']:
                raise RuntimeError("if typus is 'from' you need to declare members")
            import_statement = f"from {package_name} import {', '.join(members)}"
        self.extra_imports.append(import_statement)

    def set_command_attribute(self, key, value):
        if key not in self.allowed_command_attr:
            raise KeyError(f"{key=} is not a valid cog_command_attribute, {self.allowed_command_attr=}")
        typus = self.allowed_command_attr.get(key)
        if not isinstance(value, typus):
            raise TypeError(f"cog_command_attribute '{key}' has to be type '{typus.__name__}'")
        self.all_com_attr[key] = value

    def add_command(self, command_name, dm_allowed=False, log_invocation=False, **check_config_keys: Dict[str, str]):
        self.all_commands.append(CommandTemplateItem(command_name, dm_allowed, log_invocation, **check_config_keys))
        for key, value in check_config_keys.items():
            if value not in self.config_options:
                self.config_options.append(value)

    def remove_command(self, command_name):
        to_delete_index = None
        for index, command in enumerate(self.all_commands):
            if command.name == command_name:
                to_delete_index = index
        if to_delete_index is None:
            raise IndexError
        self.all_commands.pop(to_delete_index)

    def add_listener(self, listener_name, listener_event):
        self.all_listeners.append(ListenerTemplateItem(listener_name, listener_event))

    def remove_listener(self, listener_name):
        to_delete_index = None
        for index, listener in enumerate(self.all_listeners):
            if listener.name == listener_name:
                to_delete_index = index
        if to_delete_index is None:
            raise IndexError
        self.all_listeners.pop(to_delete_index)

    def add_loop(self, loop_name, **loop_attributes):
        loop_item = LoopTemplateItem(loop_name)
        for key, value in loop_attributes.items():
            loop_item.set_attribute(key, value)
        self.all_loops.append(loop_item)

    def remove_loop(self, loop_name):
        to_delete_index = None
        for index, loop in enumerate(self.all_loops):
            if loop.name == loop_name:
                to_delete_index = index
        if to_delete_index is None:
            raise IndexError
        self.all_loops.pop(to_delete_index)

    @property
    def _alt_name(self):
        return split_camel_case_string(self.name).replace(' ', '_').lower()

    @property
    def config_name(self):
        return self._alt_name. replace('_cog', '')

    @property
    def file_name(self):
        return self._alt_name + '.py'

    @property
    def category_folder(self):
        return self.category + '_cogs'

    @property
    def category_folder_path(self):
        return pathmaker(COGS_DIR, self.category_folder)

    @property
    def file_path(self):
        return pathmaker(COGS_DIR, self.category_folder, self.file_name)

    @property
    def code(self):
        code = self._render()
        if self.format_code is True:
            return autopep8.fix_code(code)
        return code

    @property
    def template_name(self):
        return self._template_name

    @template_name.setter
    def template_name(self, value: str):
        if not value.endswith('.jinja'):
            value = value + '.jinja'

        if value not in TEMPLATE_MANAGER:
            raise KeyError(f'unknown template name "template_name={value}"')

        self._template_name = value

    @property
    def template(self):
        return TEMPLATE_MANAGER.fetch_template(self.template_name)

    @code.setter
    def code(self, value: str):
        if value in [None, '']:
            raise ValueError(f"cannot set '{value=}'' as value for 'code'")

        self._code = value

    def _check_name(self):
        if any(char.upper() == char for char in self.name) is False or any(forbidden_char in self.name for forbidden_char in ['_', ' ']):
            raise CogNameNotCamelCaseError(f'Cog name must be camel case not "{self.name}"')
        if not self.name.endswith('Cog'):
            self.name = self.name + 'Cog'

    def _render(self):
        return self.template(**{self.template_var_name: self})

    def add_to_config(self):
        if self.config_name in COGS_CONFIG:
            return
        COGS_CONFIG.add_section(self.config_name)
        for option in self.config_options:
            COGS_CONFIG.set(self.config_name, option, "")
        COGS_CONFIG.save()

    def write(self):
        if os.path.isfile(self.file_path) is True and self.overwrite is False:
            raise FileExistsError(f"Cog file '{self.file_path}' allready exists and '{self.overwrite=}'")
        with open(self.file_path, 'w') as f:
            f.write(self.code)

    def generate(self):
        create_folder(self.category_folder_path)
        create_file(pathmaker(self.category_folder_path, '__init__.py'))
        self.write()
        self.add_to_config()


# region[Main_Exec]
if __name__ == '__main__':
    x = CogTemplateItem('FaqCog', 'special_channels', False)
    x.add_command('post_faq_by_number', log_invocation=True)
    x.add_command('create_faqs_as_embed', log_invocation=True, allowed_channel_key="faq_channel", allowed_roles_key="special_commands_roles")
    x.generate()
# endregion[Main_Exec]
