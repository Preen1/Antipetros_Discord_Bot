# region [Imports]

# * Standard Library Imports -->
import os
from collections import namedtuple

# * Third Party Imports -->
# from natsort import natsorted
# from fuzzywuzzy import fuzz, process
import autopep8

# import pyperclip
# from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.utility.named_tuples import NEW_COG_ITEM, NEW_LOOP_ITEM, NEW_COMMAND_ITEM, NEW_LISTENER_ITEM
from antipetros_discordbot.utility.gidtools_functions import writeit, pathmaker
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.dev_tools_and_scripts.templates import TEMPLATES_DIR

# endregion[Imports]


# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)


# endregion[Logging]

# region [Constants]
APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR, encoding='utf-8'))

# endregion[Constants]
# for templates
NEW_COG_ITEM = namedtuple('NewCogItem', ['name', 'absolute_location', 'import_location', 'config_name', 'all_com_attr', 'all_loops', 'all_listeners', 'all_commands', 'extra_imports', 'code'])
NEW_COMMAND_ITEM = namedtuple('NewCommandItem', ['name', 'dm_allowed', 'log_invocation', 'code'])
NEW_LISTENER_ITEM = namedtuple('NewListenerItem', ['name', 'event_name', 'args', 'code'])
NEW_LOOP_ITEM = namedtuple('NewLoopItem', ['name', 'all_attributes', 'code'])


def _render(template_name: str, in_item: namedtuple, variable_name: str):
    # sourcery skip: inline-immediately-returned-variable
    template = ENV.get_template(template_name + '.py.jinja')
    _code = template.render({variable_name: in_item})
    if template_name == 'cog_template':
        _code = autopep8.fix_code(_code)

    completed_item = in_item._replace(code=_code)
    return completed_item


def _render_new_loop(loop_item: namedtuple):

    return _render('loop_template', loop_item, 'loop_item')


def _render_new_listener(listener_item: namedtuple):

    return _render('listener_template', listener_item, 'listener_item')


def _render_new_command(command_item: namedtuple):

    return _render('command_template', command_item, 'command_item')


def _render_new_cog(cog_item: namedtuple):

    return _render('cog_template', cog_item, 'cog_item')


ITEM_HANDLING = {'NewCommandItem': _render_new_command,
                 'NewListenerItem': _render_new_listener,
                 'NewLoopItem': _render_new_loop}


def run_render(item):
    _render_func = ITEM_HANDLING.get(item.__class__.__name__)
    return _render_func(item)


def _edit_configs(cog_item: namedtuple):
    BASE_CONFIG.set('extensions', cog_item.import_location, 'no')
    COGS_CONFIG.add_section(cog_item.config_name)
    BASE_CONFIG.save()
    COGS_CONFIG.save()


def _make_folder(folder):
    if os.path.isdir(folder) is False:
        os.makedirs(folder)
        writeit(pathmaker(folder, '__init__.py'), '')


def create_cog_file(cog_item: namedtuple, overwrite=False):
    # IDEA: create gui for this
    file = pathmaker(cog_item.absolute_location)
    folder = pathmaker(os.path.dirname(file))
    for item_list_name in ["all_loops", "all_listeners", "all_commands"]:
        cog_item = cog_item._replace(**{item_list_name: list(map(run_render, getattr(cog_item, item_list_name)))})
    cog_item = _render_new_cog(cog_item)

    _make_folder(folder)
    if os.path.isfile(file) is False or overwrite is True:
        writeit(file, cog_item.code.replace('$$config_name$$', cog_item.config_name))
    _edit_configs(cog_item)

# region[Main_Exec]


if __name__ == '__main__':

    pass
# endregion[Main_Exec]
