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

from cryptography.fernet import Fernet, InvalidToken, InvalidSignature

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
from antipetros_discordbot.utility.gidtools_functions import readbin, writebin, readit, writeit

from antipetros_discordbot.utility.general_decorator import debug_timing_print
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


def write_key(file_path):
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open(file_path, "wb") as key_file:
        key_file.write(key)


def load_key(file_path):
    """
    Loads the key from the current directory named `key.key`
    """
    with open(file_path, 'rb') as key_file:
        return key_file.read()


def encrypt_string(in_data: str, key=None, key_file=None):

    if key is None:
        if key_file is not None:
            if os.path.exists(key_file):
                key = load_key(key_file)
            else:
                write_key(key_file)
                key = load_key(key_file)
        else:
            raise RuntimeError
    fernet_crypt = Fernet(key)
    string_data = in_data.encode()
    return fernet_crypt.encrypt(string_data)


def decrypt_string(in_data: bytes, key=None, key_file=None):

    if key is None:
        if key_file is not None:
            if os.path.exists(key_file):
                key = load_key(key_file)

    if key is None:
        raise RuntimeError

    fernet_crypt = Fernet(key)
    return fernet_crypt.decrypt(in_data).decode()


@debug_timing_print
def encrypt_file(file_path, key=None, key_file=None):

    if key is None:
        if key_file is not None:
            if os.path.exists(key_file):
                key = load_key(key_file)
            else:
                write_key(key_file)
                key = load_key(key_file)
        else:
            raise RuntimeError
    fernet_crypt = Fernet(key)
    with open(file_path, 'rb') as in_f:
        file_data = in_f.read()
    encrypt_file_data = fernet_crypt.encrypt(file_data)
    with open(file_path, 'wb') as out_f:
        out_f.write(encrypt_file_data)


@debug_timing_print
def decrypt_file(file_path, key=None, key_file=None):

    if key is None:
        if key_file is not None:
            if os.path.exists(key_file):
                key = load_key(key_file)

    if key is None:
        raise RuntimeError

    fernet_crypt = Fernet(key)
    with open(file_path, 'rb') as in_f:
        file_data = in_f.read()
    decrypt_file_data = fernet_crypt.decrypt(file_data)
    with open(file_path, 'wb') as out_f:
        out_f.write(decrypt_file_data)


def new_db_key(token_file):
    new_key = Fernet.generate_key()
    token_content = readit(token_file)
    with open(token_file, 'w') as f:
        for line in token_content.splitlines():
            if line.split('=', maxsplit=1)[0] == 'DB_KEY':
                line = f"DB_KEY={new_key.decode()}"
            f.write(line + '\n')


def encrypt_db(key):
    for file in os.scandir(APPDATA['database']):
        if file.is_file() and file.name.endswith('.db'):
            encrypt_file(file.path, key=key)


def decrypt_db(key):

    for file in os.scandir(APPDATA['database']):
        if file.is_file() and file.name.endswith('.db'):
            try:
                decrypt_file(file, key=key)
            except InvalidToken as inval_token_error:
                log.error('InvalidToken encountered while decrypting DB, DB is probably not encrypted')


# region[Main_Exec]
if __name__ == '__main__':
    pass


# endregion[Main_Exec]
