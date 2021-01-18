"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ------------------------------------------------------------------------------------------------------------------------------------>

# * Standard Library Imports -->
import os

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper

# * Third Party Imports ----------------------------------------------------------------------------------------------------------------------------------------->


# import requests

# import pyperclip

# import matplotlib.pyplot as plt

# from bs4 import BeautifulSoup

# from dotenv import load_dotenv

# from discord import Embed, File


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

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


def user_not_blacklisted(bot, logger):
    async def predicate(ctx):
        if bot.is_blacklisted(ctx.author):
            logger.warning('Tried invocation by blacklisted user: "%s", id: "%s"', ctx.author.name, str(ctx.author.id))
            await bot.command_call_blocked(ctx)

            return False

        return True
    return bot.add_check(predicate)


# region[Main_Exec]
if __name__ == '__main__':
    pass

# endregion[Main_Exec]
