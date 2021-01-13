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
import sqlite3 as sqlite
import logging

# * Gid Imports -->
import gidlogger as glog


# endregion[Imports]

__updated__ = '2020-11-03 03:34:53'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = logging.getLogger('gidsql')

glog.import_notification(log, __name__)

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class GidSqlitePhraser:
    def __init__(self):
        self.template_folder = None
        self.created_scripts = {}


# region[Main_Exec]

if __name__ == '__main__':
    pass

# endregion[Main_Exec]
