
# region [Imports]

# * Standard Library Imports -->
from collections import namedtuple

# endregion[Imports]


LINK_DATA_ITEM = namedtuple('LinkDataItem', ['author', 'link_name', 'date_time', 'delete_date_time', 'link'])
SUGGESTION_DATA_ITEM = namedtuple('SuggestionDataItem', ['name', 'message_author', 'reaction_author', 'message', 'time', 'extra_data'], defaults=(None,))


# for templates
NEW_COG_ITEM = namedtuple('NewCogItem', ['name', 'absolute_location', 'import_location', 'config_name', 'all_com_attr', 'all_loops', 'all_listeners', 'all_commands', 'extra_imports', 'code'], defaults=('', [], [], [], [], []))
NEW_COMMAND_ITEM = namedtuple('NewCommandItem', ['name', 'hidden', 'docstring', 'code'], defaults=('', None))
NEW_LISTENER_ITEM = namedtuple('NewListenerItem', ['name', 'event_name', 'docstring', 'code'], defaults=('', None))
NEW_LOOP_ITEM = namedtuple('NewLoopItem', ['name', 'all_attributes', 'docstring', 'code'], defaults=('', None))
DOCSTRING_ITEM = namedtuple('DocStringItem', ['short_description', 'extra_description', 'all_args'], defaults=(None, None))
