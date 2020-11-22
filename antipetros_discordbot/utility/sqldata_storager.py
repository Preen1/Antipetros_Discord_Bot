from gidtools.gidsql.facade import GidSqliteDatabase
from antipetros_discordbot.utility.named_tuples import LINK_DATA_ITEM
from fuzzywuzzy import process as fuzzprocess


DB_LOC = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\antipetros_discordbot\data\data_storage\sqlite_data\save_db.db"
SCRIPT_LOC = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\antipetros_discordbot\data\data_storage\sqlite_data\sql_procedures"


class LinkDataStorageSQLite:
    def __init__(self):
        self.db = GidSqliteDatabase(DB_LOC, SCRIPT_LOC)
        self.db.startup_db()

    def add_data(self, item):
        if isinstance(item, LINK_DATA_ITEM):
            self.db.writer.write(self.db.scripter['insert_link_author'], item.author.name)
            self.db.writer.write(self.db.scripter['insert_saved_link'], (item.link_name, item.link, item.date_time, item.delete_date_time, item.author.name))

    @property
    def all_link_names(self):
        _out_list = []
        for item in self.db.reader.query(self.db.scripter['list_of_name_save_link']):
            _out_list.append(item[0])
        return set(_out_list)

    def delete_all(self):
        self.db.startup_db(overwrite=True)

    def get_link(self, name):
        _name = fuzzprocess.extractOne(name, self.all_link_names)
        if _name is None:
            return f"no link found with name '{name}'"
        _name = _name[0]
        _out = self.db.reader.query(self.db.scripter['get_link'], (_name,))[0]

        return _out[0] + ' --> ' + _out[1]

    def get_all_links(self, in_format='plain'):
        if in_format == 'json':
            _out = {}
            for item in self.db.reader.query(self.db.scripter['get_all_links']):
                if item[2] not in _out:
                    _out[item[2]] = []
                _out[item[2]].append((item[0], item[1]))
        elif in_format == 'plain':
            _out = []
            for item in self.db.reader.query(self.db.scripter['get_all_links']):
                _out.append(item[0] + ' --> ' + item[1])
        return _out
