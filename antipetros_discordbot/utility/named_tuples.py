
# region [Imports]

from collections import namedtuple

# endregion[Imports]


LINK_DATA_ITEM = namedtuple('LinkDataItem', ['author', 'link_name', 'date_time', 'delete_date_time', 'link'])
SUGGESTION_DATA_ITEM = namedtuple('SuggestionDataItem', ['name', 'message_author', 'reaction_author', 'message', 'time', 'extra_data'], defaults=(None,))
