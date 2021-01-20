"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ------------------------------------------------------------------------------------------------------------------------------------>


import os
import json
from datetime import datetime, timezone
from pytz import timezone
from jinja2 import Environment, BaseLoader
from pprint import pprint, pformat
from inspect import getmembers, isfunction, isclass, ismethod, ismodule, isawaitable, signature, getargspec, iscoroutine, iscoroutinefunction, getfullargspec
import gidlogger as glog
import checksumdir
from functools import partial
from time import time, sleep, time_ns
from antipetros_discordbot.abstracts.subsupport_abstract import SubSupportBase
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from benedict import benedict
from discord import Embed, File
from antipetros_discordbot.utility.gidtools_functions import (readit, clearit, readbin, work_in, writeit, loadjson, pickleit, splitoff, writebin, pathmaker, writejson, dir_change,
                                                              linereadit, bytes2human, create_file, file_walker, get_pickled, ishash_same, ext_splitter, appendwriteit, create_folder,
                                                              number_rename, timenamemaker, cascade_rename, file_name_time, absolute_listdir, hash_to_solidcfg, path_part_remove,
                                                              from_dict_to_file, get_absolute_path, file_name_modifier, limit_amount_of_files, limit_amount_files_absolute)

from antipetros_discordbot.utility.misc import datetime_isoformat_to_discord_format
# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]


# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


class EmbedBuilder(SubSupportBase):
    """
    [summary]

    [extended_summary]

    Args:
        SubSupportBase ([type]): [description]

    Returns:
        [type]: [description]
    """
    embed_data_folder = pathmaker(APPDATA['fixed_data'], "embed_data")
    standard_embed_symbols_file = pathmaker(APPDATA["embed_data"], "embed_symbols.json")
    default_embed_data = pathmaker(APPDATA['default_embed_data.json'])

    def __init__(self, bot, support):
        self.bot = bot
        self.support = support
        # self.loop = self.bot.loop
        # self.is_debug = self.bot.is_debug
        self._ensure_folder_exists()
        self.embed_build_recipes = None
        self.default_empty = Embed.Empty

        glog.class_init_notification(log, self)

    async def make_static_embed(self, category, name):
        pass

    async def make_embed(self, typus, **kwargs):
        pass

    def collect_embed_build_recipes(self):
        self.embed_build_recipes = {}
        # for method_name, method_object in getmembers(self.__class__, iscoroutinefunction):
        for method_name, method_object in getmembers(self.__class__):
            if method_name.startswith('_embed_recipe_'):
                self.embed_build_recipes[method_name.replace("_embed_recipe_", "")] = getattr(self, method_name)

    @property
    def standard_embed_symbols(self):
        create_file(self.standard_embed_symbols_file)
        return loadjson(self.standard_embed_symbols_file)

    @property
    def folder_exists(self):
        return os.path.isdir(self.embed_data_folder)

    def _ensure_folder_exists(self):
        create_folder(self.embed_data_folder)

    @property
    def default_author(self):
        """
        {'name': '', 'url': '', 'icon_url': ''}
        """
        pass

    @property
    def default_footer(self):
        """
        {'text': '', 'icon_url': ''}
        """
        pass

    @property
    def default_thumbnail(self):
        """
        {'url': ''}
        """
        pass

    @property
    def default_color(self):
        """
        {'color': ''}
        """
        pass

    @property
    def default_timestamp(self):
        """
        {'timestamp': ''}
        """
        return {'timestamp': datetime.now(tz=timezone("Europe/Berlin"))}

    @property
    def default_type(self):
        """
        {'type': 'rich'}
        """
        return {'type': 'rich'}

    async def if_ready(self):
        self.collect_embed_build_recipes()
        log.debug("'%s' sub_support is READY", str(self))

    async def update(self):
        log.debug("'%s' sub_support was UPDATED", str(self))

    def retire(self):
        log.debug("'%s' sub_support was RETIRED", str(self))


def get_class():
    return EmbedBuilder
# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
