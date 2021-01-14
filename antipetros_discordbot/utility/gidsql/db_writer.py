# region [Imports]

# * Standard Library Imports -->
import os
import shutil
import sqlite3 as sqlite
import configparser
from sqlite3.dbapi2 import Error
from typing import Union
import enum
import logging
# * Gid Imports -->
import gidlogger as glog

import textwrap
from antipetros_discordbot.utility.gidsql.db_action_base import GidSqliteActionBase

# endregion [Imports]

__updated__ = '2020-11-26 17:04:24'


# region [Logging]

log = logging.getLogger('gidsql')

glog.import_notification(log, __name__)

# endregion [Logging]


# region [Class_1]

class GidSQLiteWriter(GidSqliteActionBase):
    def __init__(self, in_db_loc, in_pragmas=None):
        super().__init__(in_db_loc, in_pragmas)
        glog.class_init_notification(log, self)

    def write(self, sql_phrase: str, variables: Union[str, tuple, list] = None):
        conn = sqlite.connect(self.db_loc, isolation_level=None, detect_types=sqlite.PARSE_DECLTYPES)
        cursor = conn.cursor()
        try:
            self._execute_pragmas(cursor)
            if variables is not None:
                if isinstance(variables, str):
                    cursor.execute(sql_phrase, (variables,))
                    _log_sql_phrase = ' '.join(sql_phrase.replace('\n', ' ').split())
                    _log_args = textwrap.shorten(str(variables), width=200, placeholder='...')
                    log.debug(f"Executed sql phrase '{_log_sql_phrase}' with args {_log_args} successfully")
                elif isinstance(variables, tuple):
                    cursor.execute(sql_phrase, variables)
                    _log_sql_phrase = ' '.join(sql_phrase.replace('\n', ' ').split())
                    _log_args = textwrap.shorten(str(variables), width=200, placeholder='...')
                    log.debug(f"Executed sql phrase '{_log_sql_phrase}' with args {_log_args} successfully")
                elif isinstance(variables, list):
                    cursor.executemany(sql_phrase, variables)
                    _log_sql_phrase = ' '.join(sql_phrase.replace('\n', ' ').split())
                    _log_args = textwrap.shorten(str(variables), width=200, placeholder='...')
                    log.debug(f"ExecutedMany sql phrase from '{_log_sql_phrase}' with arg-iterable {_log_args} successfully")
            else:
                cursor.executescript(sql_phrase)
                _log_sql_phrase = ' '.join(sql_phrase.replace('\n', ' ').split())
                log.debug(f"ExecutedScript sql phrase '{_log_sql_phrase}' successfully")
            conn.commit()
        except sqlite.Error as error:
            _log_sql_phrase = ' '.join(sql_phrase.replace('\n', ' ').split())
            _log_args = textwrap.shorten(str(variables), width=200, placeholder='...')
            self._handle_error(error, _log_sql_phrase, _log_args)
        finally:
            conn.close()

    def __repr__(self):
        return f"{self.__class__.__name__} ('{self.db_loc}')"

    def __str__(self):
        return self.__class__.__name__
# endregion [Class_1]


if __name__ == '__main__':
    pass
