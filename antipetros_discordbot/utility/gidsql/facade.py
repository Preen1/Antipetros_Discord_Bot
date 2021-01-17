# region [Imports]

# * Standard Library Imports -->
import os
import logging
from enum import Enum, auto
from typing import Union

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.utility.gidsql.phrasers import GidSqliteInserter
from antipetros_discordbot.utility.gidsql.db_reader import Fetch, GidSqliteReader
from antipetros_discordbot.utility.gidsql.db_writer import GidSQLiteWriter
from antipetros_discordbot.utility.gidsql.script_handling import GidSqliteScriptProvider

# endregion[Imports]

__updated__ = '2020-11-28 03:29:05'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = logging.getLogger('gidsql')

glog.import_notification(log, __name__)

# endregion[Logging]

# region [Constants]
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
# endregion[Constants]


class PhraseType(Enum):
    Insert = auto()
    Query = auto()
    Create = auto()
    Drop = auto()


class GidSqliteDatabase:
    Insert = PhraseType.Insert
    Query = PhraseType.Query
    Create = PhraseType.Create
    Drop = PhraseType.Drop

    All = Fetch.All
    One = Fetch.One

    phrase_objects = {Insert: GidSqliteInserter, Query: None, Create: None, Drop: None}

    def __init__(self, db_location, script_location, config=None):
        self.path = db_location
        self.script_location = script_location
        self.config = config
        self.pragmas = None
        if self.config is not None:
            self.pragmas = self.config.getlist('general_settings', 'pragmas')
        self.writer = GidSQLiteWriter(self.path, self.pragmas)
        self.reader = GidSqliteReader(self.path, self.pragmas)
        self.scripter = GidSqliteScriptProvider(self.script_location)
        self.config = config

    def startup_db(self, overwrite=False):
        if os.path.exists(self.path) is True and overwrite is False:
            return None
        if os.path.exists(self.path) is True:
            os.remove(self.path)
        for script in self.scripter.setup_scripts:
            self.writer.write(script)

    def new_phrase(self, typus: PhraseType):
        return self.phrase_objects.get(typus)()

    def write(self, phrase, variables=None):
        if isinstance(phrase, str):
            sql_phrase = self.scripter.get(phrase, None)
            if sql_phrase is None:
                sql_phrase = phrase
            self.writer.write(sql_phrase, variables)

    def query(self, phrase, variables=None, fetch: Fetch = Fetch.All, row_factory: Union[bool, any] = False):
        if row_factory:
            _factory = None if isinstance(row_factory, bool) is True else row_factory
            self.reader.enable_row_factory(in_factory=_factory)
        sql_phrase = self.scripter.get(phrase, None)
        if sql_phrase is None:
            sql_phrase = phrase
        _out = self.reader.query(sql_phrase, variables=variables, fetch=fetch)
        self.reader.disable_row_factory()
        return _out

    def vacuum(self):
        self.write('VACUUM')

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path}, {self.script_location}, {self.config})"

    def __str__(self) -> str:
        return self.__class__.__name__

    # region[Main_Exec]


if __name__ == '__main__':
    # x = GidSqliteDatabase(pathmaker(THIS_FILE_DIR, "test_db.db"), r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils\tests\test_gidsql")
    # x.startup_db()
    # # x.writer.write('INSERT INTO "main_tbl" ("name", "info") VALUES (?,?)', ("first_name", "first_info"))
    # print(x.reader.query('SELECT * FROM main_tbl'))
    pass
# endregion[Main_Exec]
