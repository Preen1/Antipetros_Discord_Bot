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

# from antipetros_discordbot.utility.gidtools_functions import ( readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
#                                dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)


# * Local Imports ----------------------------------------------------------------------------------------------------------------------------------------------->


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


def bytes2human(n, annotate=False):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('Kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb')
    prefix = {s: 1 << (i + 1) * 10 for i, s in enumerate(symbols)}
    for s in reversed(symbols):
        if n >= prefix[s]:
            _out = float(n) / prefix[s]
            if annotate is True:
                _out = '%.1f %s' % (_out, s)
            return _out
    _out = n
    if annotate is True:
        _out = "%s b" % _out
    return _out


def pathmaker(first_segment, *in_path_segments, rev=False):
    """
    Normalizes input path or path fragments, replaces '\\\\' with '/' and combines fragments.

    Parameters
    ----------
    first_segment : str
        first path segment, if it is 'cwd' gets replaced by 'os.getcwd()'
    rev : bool, optional
        If 'True' reverts path back to Windows default, by default None

    Returns
    -------
    str
        New path from segments and normalized.
    """

    _path = first_segment

    _path = os.path.join(_path, *in_path_segments)
    if rev is True or sys.platform not in ['win32', 'linux']:
        return os.path.normpath(_path)
    return os.path.normpath(_path).replace(os.path.sep, '/')


class FileSystemWalkerItem(namedtuple('WalkerItem', ['name', 'path'])):
    byte = "byte"
    kilobyte = 'kilobyte'
    megabyte = 'megabyte'
    gigabyte = 'gigabyte'
    terrabyte = 'terrabyte'
    sgf = 1024  # SIZE_GENERAL_FACTOR
    size_conv = {'byte': {'factor': sgf**0, 'short_name': 'b'},
                 'kilobyte': {'factor': sgf**1, 'short_name': 'kb'},
                 'megabyte': {'factor': sgf**2, 'short_name': 'mb'},
                 'gigabyte': {'factor': sgf**3, 'short_name': 'gb'},
                 'terrabyte': {'factor': sgf**4, 'short_name': 'tb'}}

    def is_file(self):
        return os.path.isfile(self.path)

    def is_dir(self):
        return os.path.isdir(self.path)

    def exists(self):
        return os.path.exists(self.path)

    def _size(self):
        if self.is_file() is True:
            size_b = os.stat(self.path).st_size
        else:
            size_b = 0
            for dirname, folderlist, filelist in os.walk(self.path):
                for file in filelist:
                    full_path = pathmaker(dirname, file)
                    size_b += os.stat(full_path).st_size

        return size_b

    def _converted_size(self, target_unit):
        return round(self._size() / self.size_conv.get(target_unit).get('factor'), ndigits=3)

    @property
    def size_b(self):
        return self._converted_size('byte')

    @property
    def size_kb(self):
        return self._converted_size('kilobyte')

    @property
    def size_mb(self):
        return self._converted_size('megabyte')

    @property
    def size_gb(self):
        return self._converted_size('gigabyte')

    @property
    def size_tb(self):
        return self._converted_size('terrabyte')

    @property
    def pretty_size(self):
        return bytes2human(self._size(), annotate=True)

    @property
    def ext(self):
        return os.path.splitext(self.name)[1].replace('.', '')

    @property
    def dirname(self):
        return os.path.dirname(self.path)

    def delete(self, are_you_sure: bool = False):
        if are_you_sure is False:
            raise AssertionError
        os.remove(self.path)

    def __str__(self):
        return pathmaker(self.path)


def filesystem_walker(start_folder):
    for dirname, folderlist, filelist in os.walk(start_folder):
        for file in filelist:
            file_path = pathmaker(dirname, file)
            yield FileSystemWalkerItem(file, file_path)
        for folder in folderlist:
            folder_path = pathmaker(dirname, folder)
            yield FileSystemWalkerItem(folder, folder_path)


def filesystem_walker_files(start_folder):
    for item in filesystem_walker(start_folder):
        if item.is_file() is True:
            yield item


def filesystem_walker_folders(start_folder):
    for item in filesystem_walker(start_folder):
        if item.is_dir() is True:
            yield item


# region[Main_Exec]

if __name__ == '__main__':
    pass

# endregion[Main_Exec]
