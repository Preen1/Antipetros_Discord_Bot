"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ------------------------------------------------------------------------------------------------------------------------------------>

# * Standard Library Imports -->
import os
from inspect import iscoroutine, iscoroutinefunction
from functools import partial

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.bot_support.sub_support import SUB_SUPPORT_CLASSES

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


# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


class BotSupporter:

    def __init__(self, bot):
        self.bot = bot
        self.subsupports = []
        self.available_subsupport_classes = SUB_SUPPORT_CLASSES
        self.recruit_subsupports()
        log.info("subsupports loaded into command-staff: %s", ', '.join(map(str, self.subsupports)))

    def find_available_subsupport_classes(self):
        pass

    def recruit_subsupports(self):
        for subsupport_class in self.available_subsupport_classes:
            self.subsupports.append(subsupport_class(self.bot, self))

    def __getattr__(self, attribute_name):
        _out = None
        for subsupport in self.subsupports:
            if hasattr(subsupport, attribute_name):
                _out = getattr(subsupport, attribute_name)
                return _out
        return partial(self.log_attribute_not_found, attribute_name)

    def really_has_attribute(self, attribute_name):
        return hasattr(self, attribute_name) and all(hasattr(subsupport, attribute_name) is False for subsupport in self.subsupports)

    async def to_all_subsupports(self, attribute_name, *args, **kwargs):
        if self.really_has_attribute(attribute_name):
            if iscoroutine(getattr(self, attribute_name)):
                await getattr(self, attribute_name)(*args, **kwargs)
            else:
                getattr(self, attribute_name)(*args, **kwargs)
        for subsupport in self.subsupports:
            if hasattr(subsupport, attribute_name):
                if iscoroutinefunction(getattr(subsupport, attribute_name)):
                    await getattr(subsupport, attribute_name)(*args, **kwargs)
                else:
                    getattr(subsupport, attribute_name)(*args, **kwargs)

    def retire_subsupport(self):
        for subsupport in self.subsupports:
            subsupport.retire()

    @ staticmethod
    def log_attribute_not_found(*args, **kwargs):
        return log.critical("'%s' was not found in any subsupport, args used: '%s', kwargs used: '%s'", str(args[0]), str(args), str(kwargs))

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{str(self)}({', '.join([str(subsupport) for subsupport in self.subsupports])})"

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
