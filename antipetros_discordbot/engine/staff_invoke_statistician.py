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
from benedict import benedict

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

from antipetros_discordbot.utility.gidtools_functions import (readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                                                              dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)


# * Local Imports ----------------------------------------------------------------------------------------------------------------------------------------------->

from antipetros_discordbot.init_userdata.user_data_setup import SupportKeeper
from antipetros_discordbot.abstracts.command_staff_abstract import CommandStaffSoldierBase
from antipetros_discordbot.utility.named_tuples import InvokedCommandsDataItem
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

APPDATA = SupportKeeper.get_appdata()
BASE_CONFIG = SupportKeeper.get_config('base_config')

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


class InvokeStatistician(CommandStaffSoldierBase):
    save_folder = APPDATA['stats']
    overall_invoked_stats_file=pathmaker(save_folder, 'overall_invoked_stats.json')
    cog_invoked_stats_file=pathmaker(save_folder, 'cog_invoked_stats.json')
    command_invoked_stats_file = pathmaker(save_folder, 'command_invoked_stats.json')
    stat_files=[overall_invoked_stats_file, cog_invoked_stats_file, command_invoked_stats_file]

    def __init__(self, bot):
        self.bot = bot
        self.loop = self.bot.loop
        self.is_debug = self.bot.is_debug
        self.start_time = datetime.utcnow()
        self.overall_invoked_stats = None
        self.cog_invoked_stats=None
        self.command_invoked_stats=None
        glog.class_init_notification(log, self)
        self.after_action()


    def on_ready(self):
        for stat_file in self.stat_files:
            if os.path.isfile(stat_file) is False:
                if stat_file == self.overall_invoked_stats_file:
                    writejson({'overall':{"successful":0,'unsuccessful':0},'per_day':{}}, self.overall_invoked_stats_file, sort_keys=False, indent=4)
                elif  stat_file == self.cog_invoked_stats_file:
                    data = {"overall":{}, "per_day":{}}
                    for cog_name, cog_object in self.bot.cogs.items():
                        data['overall'][str(cog_object)]={"successful":0,'unsuccessful':0}
                    writejson(data, self.cog_invoked_stats_file, sort_keys=False, indent=4)
                elif stat_file == self.command_invoked_stats_file:
                    data = {"overall":{}, "per_day":{}}
                    for cog_name, cog_object in self.bot.cogs.items():
                        for command_object in cog_object.get_commands():
                            data['overall'][command_object.name]={"successful":0,'unsuccessful':0}
                    writejson(data, self.command_invoked_stats_file, sort_keys=False, indent=4)
        self.load_stats_files()


    def load_stats_files(self):
        if self.overall_invoked_stats is not None:
            writejson(self.overall_invoked_stats, self.overall_invoked_stats_file)
        if self.cog_invoked_stats is not None:
            writejson(self.cog_invoked_stats, self.cog_invoked_stats_file)
        if self.command_invoked_stats is not None:
            writejson(self.command_invoked_stats, self.command_invoked_stats_file)

        self.overall_invoked_stats = loadjson(self.overall_invoked_stats_file)
        if self.date_today not in self.overall_invoked_stats['per_day']:
            self.overall_invoked_stats['per_day'][self.date_today]={"successful":0,'unsuccessful':0}
            writejson(self.overall_invoked_stats, self.overall_invoked_stats_file, sort_keys=False, indent=4)

        self.cog_invoked_stats = loadjson(self.cog_invoked_stats_file)
        if self.date_today not in self.cog_invoked_stats['per_day']:
            self.cog_invoked_stats['per_day'][self.date_today]={}
            for cog_name, cog_object in self.bot.cogs.items():
                self.cog_invoked_stats['per_day'][self.date_today][str(cog_object)]= {"successful":0,'unsuccessful':0}
            writejson(self.cog_invoked_stats, self.cog_invoked_stats_file, sort_keys=False, indent=4)

        self.command_invoked_stats=loadjson(self.command_invoked_stats_file)
        if self.date_today not in self.command_invoked_stats['per_day']:
            self.command_invoked_stats['per_day'][self.date_today]={}
            for cog_name, cog_object in self.bot.cogs.items():
                for command in cog_object.get_commands():
                    if command.name not in ['die', "get_command_stats"]:
                        self.command_invoked_stats['per_day'][self.date_today][command.name]={"successful":0,'unsuccessful':0}
            writejson(self.command_invoked_stats,self.command_invoked_stats_file, sort_keys=False, indent=4)

    @property
    def date_today(self):
        return datetime.utcnow().strftime("%Y-%m-%d")


    def get_todays_invoke_data(self):
        overall_data = self.overall_invoked_stats['per_day'][self.date_today]
        data = '\n'.join([f"**{key}**: *{str(value)}*" for key,value in overall_data.items() if value != 0])
        overall_item = InvokedCommandsDataItem('overall', self.date_today, data)

        cogs_data = self.cog_invoked_stats['per_day'][self.date_today]
        data = '\n'.join([f"**{key}**: successful - *{value.get('successful')}* | unsuccessful - *{value.get('unsuccessful')}*" for key, value in cogs_data.items() if any(subvalue != 0 for subkey, subvalue in value.items())])
        cogs_item = InvokedCommandsDataItem('cogs', self.date_today, cogs_data)

        commands_data = self.command_invoked_stats['per_day'][self.date_today]
        data = '\n'.join([f"**{key}**: successful - *{value.get('successful')}* | unsuccessful - *{value.get('unsuccessful')}*" for key, value in commands_data.items() if any(subvalue != 0 for subkey, subvalue in value.items())])
        commands_item=InvokedCommandsDataItem('commands', self.date_today, commands_data)

        return overall_item, cogs_item, commands_item

    def update(self):
        self.load_stats_files()


    def retire(self):
        writejson(self.overall_invoked_stats, self.overall_invoked_stats_file)
        writejson(self.cog_invoked_stats, self.cog_invoked_stats_file)
        writejson(self.command_invoked_stats, self.command_invoked_stats_file)
        log.info("Soldier '%s' was retired", str(self))




    def after_action(self):

        async def record_command_invocation(ctx):
            _command = ctx.command
            _cog = _command.cog
            _command = _command.name
            _cog = str(_cog)
            if _command in ['die', "get_command_stats"]:
                return

            if ctx.command_failed is False:
                marker='successful'
            else:
                marker='unsuccessful'
            self.overall_invoked_stats['overall'][marker]+=1
            self.overall_invoked_stats['per_day'][self.date_today][marker]+=1


            self.cog_invoked_stats['overall'][_cog][marker]+=1
            self.cog_invoked_stats['per_day'][self.date_today][_cog][marker]+=1


            self.command_invoked_stats['overall'][_command][marker]+=1
            self.command_invoked_stats['per_day'][self.date_today][_command][marker]+=1
            log.debug("command invocations was recorded")

        return self.bot.after_invoke(record_command_invocation)

    def __str__(self) -> str:
        return self.__class__.__name__

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
