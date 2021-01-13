# region [Imports]

# * Standard Library Imports -->
import os
import shutil
import sqlite3 as sqlite
import configparser
from sqlite3.dbapi2 import Error
import logging
# * Gid Imports -->
import gidlogger as glog


# endregion [Imports]

__updated__ = '2020-10-25 16:43:43'


# region [Logging]

log = logging.getLogger('gidsql')

glog.import_notification(log, __name__)

# endregion [Logging]
