# region [Imports]

# * Standard Library Imports -->
import enum
import logging
import sqlite3 as sqlite
import textwrap

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.utility.gidsql.db_action_base import GidSqliteActionBase

# endregion[Imports]

__updated__ = '2020-11-28 02:04:13'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = logging.getLogger('gidsql')

glog.import_notification(log, __name__)

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class Fetch(enum.Enum):
    All = enum.auto()
    One = enum.auto()


class GidSqliteReader(GidSqliteActionBase):
    def __init__(self, in_db_loc, in_pragmas=None):
        super().__init__(in_db_loc, in_pragmas)
        self.row_factory = None
        glog.class_init_notification(log, self)

    def query(self, sql_phrase, variables: tuple = None, fetch: Fetch = Fetch.All):
        conn = sqlite.connect(self.db_loc, isolation_level=None, detect_types=sqlite.PARSE_DECLTYPES)
        if self.row_factory is not None:
            conn.row_factory = self.row_factory
        cursor = conn.cursor()
        try:
            self._execute_pragmas(cursor)
            if variables is not None:
                cursor.execute(sql_phrase, variables)
                _log_sql_phrase = ' '.join(sql_phrase.replace('\n', ' ').split())
                _log_args = textwrap.shorten(str(variables), width=200, placeholder='...')
                log.debug(f"Queried sql phrase '{_log_sql_phrase}' with args {_log_args} successfully")
            else:
                cursor.execute(sql_phrase)
                _log_sql_phrase = ' '.join(sql_phrase.replace('\n', ' ').split())
                log.debug(f"Queried Script sql phrase '{_log_sql_phrase}' successfully")
            _out = cursor.fetchone() if fetch is Fetch.One else cursor.fetchall()
        except sqlite.Error as error:
            _log_sql_phrase = ' '.join(sql_phrase.replace('\n', ' ').split())
            _log_args = textwrap.shorten(str(variables), width=200, placeholder='...')
            self._handle_error(error, _log_sql_phrase, _log_args)
        finally:
            conn.close()
        return _out

    def enable_row_factory(self, in_factory=None):
        self.row_factory = in_factory if in_factory is not None else sqlite.Row

    def disable_row_factory(self):
        self.row_factory = None
# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
