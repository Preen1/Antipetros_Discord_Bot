"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ------------------------------------------------------------------------------------------------------------------------------------>

# * Standard Library Imports -->
import os

# * Third Party Imports -->
import click
import autopep8
from jinja2 import Environment, FileSystemLoader

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.utility.misc import split_camel_case_string
from antipetros_discordbot.utility.named_tuples import NewCommandStaffItem

# * Local Imports ----------------------------------------------------------------------------------------------------------------------------------------------->
from antipetros_discordbot.bot_support.sub_support import SUB_SUPPORT_DIR
from antipetros_discordbot.utility.gidtools_functions import writeit, pathmaker
from antipetros_discordbot.dev_tools_and_scripts.templates import TEMPLATES_DIR

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
ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR, encoding='utf-8'))
# endregion[Constants]


@click.command()
@click.argument('sub-support-name', required=True, type=str, )
def new_sub_supporter_class(sub_support_name: str):

    split_sub_support_name = split_camel_case_string(sub_support_name)

    file_name = split_sub_support_name.replace(' ', '_').lower() + '.py'
    full_path = pathmaker(SUB_SUPPORT_DIR, file_name)
    new_sub_supporter_item = NewCommandStaffItem(sub_support_name)
    template = ENV.get_template('sub_supporter_template.py.jinja')
    new_code = autopep8.fix_code(template.render(sub_supporter=new_sub_supporter_item))
    writeit(full_path, new_code)


# region[Main_Exec]

if __name__ == '__main__':
    pass

# endregion[Main_Exec]
