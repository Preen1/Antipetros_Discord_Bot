from gidtools.gidsql.facade import GidSqliteDatabase
from antipetros_discordbot.utility.named_tuples import LINK_DATA_ITEM
from fuzzywuzzy import process as fuzzprocess
from datetime import datetime

DB_LOC_LINKS = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\antipetros_discordbot\data\data_storage\sqlite_data\save_link_db.db"
SCRIPT_LOC_LINKS = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\antipetros_discordbot\data\data_storage\sqlite_data\sql_procedures\save_link_sql"

DB_LOC_SUGGESTIONS = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\antipetros_discordbot\data\data_storage\sqlite_data\save_suggestion.db"
SCRIPT_LOC_SUGGESTIONS = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\antipetros_discordbot\data\data_storage\sqlite_data\sql_procedures\save_suggestion_sql"


class LinkDataStorageSQLite:
    def __init__(self):
        self.db = GidSqliteDatabase(DB_LOC_LINKS, SCRIPT_LOC_LINKS)
        self.db.startup_db()

    def add_data(self, item, message_id):
        if isinstance(item, LINK_DATA_ITEM):
            self.db.writer.write(self.db.scripter['insert_link_author'], (item.author.name, item.author.display_name, item.author.id, any(str(_role) == 'Member' for _role in item.author.roles)))
            self.db.writer.write(self.db.scripter['insert_saved_link'], (item.link_name, item.link, item.date_time, item.delete_date_time, item.author.id, message_id))

    @property
    def link_messages_to_remove(self):
        for item in self.db.query('SELECT "message_discord_id" FROM "saved_links_tbl" WHERE "is_removed"=0 AND "delete_time"<?', (datetime.utcnow(),)):
            yield item[0]

    @ property
    def all_link_names(self):
        _out_list = []
        for item in self.db.reader.query(self.db.scripter['list_of_name_save_link']):
            _out_list.append(item[0])
        return set(_out_list)

    def update_removed_status(self, message_id):
        self.db.write('update_removed', (message_id,))

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


class SuggestionDataStorageSQLite:
    def __init__(self):
        self.db = GidSqliteDatabase(DB_LOC_SUGGESTIONS, SCRIPT_LOC_SUGGESTIONS)
        self.db.startup_db()

    @property
    def category_emojis(self):
        _out = {}
        for item in self.db.query('SELECT "emoji", "name" FROM "category_tbl"', row_factory=True):
            _out[item['emoji']] = item['name']
        return _out

    def get_all_non_discussed_message_ids(self, as_set: bool = True):
        result = self.db.query('get_all_messages_not_discussed', row_factory=True)
        _out = [item['message_discord_id'] for item in result]
        if as_set is True:
            _out = set(_out)
        return _out

    def update_votes(self, vote_type, amount, message_id):
        phrase = 'update_upvotes' if vote_type == 'THUMBS UP SIGN' else 'update_downvotes'
        self.db.write(phrase, (amount, message_id))

    def update_category(self, category, message_id):
        self.db.write('update_category', (category, message_id))

    def get_all_message_ids(self, as_set: bool = True):
        result = self.db.query('get_all_message_ids', row_factory=True)

        _out = [item['message_discord_id'] for item in result]
        if as_set is True:
            _out = set(_out)
        return _out

    def add_suggestion(self, suggestion_item):

        for author in [suggestion_item.message_author, suggestion_item.reaction_author]:
            self.db.write('insert_author', (author.name,
                                            author.display_name,
                                            author.id,
                                            any(role.name == 'Member' for role in author.roles)))

        if suggestion_item.extra_data is None:
            sql_phrase = 'insert_suggestion'
            arguments = (suggestion_item.name,
                         suggestion_item.message.id,
                         suggestion_item.message_author.id,
                         suggestion_item.reaction_author.id,
                         suggestion_item.message.created_at,
                         suggestion_item.time,
                         suggestion_item.message.content)

        else:
            extra_data = suggestion_item.extra_data
            self.db.write('insert_extra_data', (extra_data[0], extra_data[1]))
            sql_phrase = 'insert_suggestion_with_data'
            arguments = (suggestion_item.name,
                         suggestion_item.message.id,
                         suggestion_item.message_author.id,
                         suggestion_item.reaction_author.id,
                         suggestion_item.message.created_at,
                         suggestion_item.time,
                         suggestion_item.message.content,
                         extra_data[0])
        self.db.write(sql_phrase, arguments)
