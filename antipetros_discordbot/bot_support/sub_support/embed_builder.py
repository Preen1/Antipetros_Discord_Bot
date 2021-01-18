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
    embed_serialization_folder = pathmaker(APPDATA['fixed_data'], "embed_data")
    standard_embed_symbols_file = pathmaker(APPDATA["embed_data"], "embed_symbols.json")

    def __init__(self, bot, support):
        self.bot = bot
        self.support = support
        # self.loop = self.bot.loop
        # self.is_debug = self.bot.is_debug
        self.old_dir_hash = hash(self)
        self.embed_build_recipes = None
        self.collect_embed_build_recipes()
        self.embed_prototypes = {}
        self.collect_embed_prototypes()
        self.jinja_env = Environment(loader=BaseLoader)
        self.embed_subtypes = {'faq': 'standard'}  # TODO: maybe from config

        glog.class_init_notification(log, self)

    async def make_static_embed(self, category, name):
        return Embed.from_dict(self.embed_prototypes[category].get(name))

    async def make_embed(self, typus, **kwargs):
        return await self.embed_build_recipes.get(typus)(**kwargs)

    async def _get_embed_data(self, category, name):
        if hash(self) != self.old_dir_hash:
            self.collect_embed_prototypes()
        return self.embed_prototypes[category].get(name)

    async def _embed_recipe_faq(self, faq_number: int, faq_question: str, faq_answer: str, faq_link: str = None, timestamp: datetime = None):
        prototype = self.embed_prototypes['faq'].get(self.embed_subtypes['faq'])
        timestamp = datetime.utcnow() if timestamp is None else timestamp
        timestamp = datetime_isoformat_to_discord_format(timestamp)

        faq_link = faq_link if faq_link is not None else ''

        conv_callback = partial(self._convert_dict_values, replacements={k: v for k, v in locals().items() if k not in ['self', 'prototype']})

        mod_embed_dict = benedict(prototype)
        mod_embed_dict.traverse(conv_callback)
        return Embed.from_dict(mod_embed_dict)

    def collect_embed_prototypes(self):
        for file in self.serialized_files:
            category = os.path.splitext(file.name)[0].replace('_embeds', '').casefold()
            self.embed_prototypes[category] = loadjson(file.path)

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
    def serialized_files(self):
        self._ensure_folder_exists()
        _out = []
        for file in os.scandir(self.embed_serialization_folder):
            if file.is_file() and file.name.endswith('.json') and os.path.splitext(file.name)[0].endswith('_embeds'):
                _out.append(file)
        return _out

    @property
    def folder_exists(self):
        return os.path.isdir(self.embed_serialization_folder)

    @property
    def categories(self):
        return [key for key in self.embed_prototypes]

    def _convert_dict_values(self, source: benedict, key, value, replacements):
        try:
            as_template = self.jinja_env.from_string(value)
            source[key] = as_template.render(**replacements)
        except TypeError:
            pass

    def _ensure_folder_exists(self):
        create_folder(self.embed_serialization_folder)

    def __hash__(self):
        return hash(checksumdir.dirhash(self.embed_serialization_folder))

    async def if_ready(self):
        log.debug("'%s' sub_support is READY", str(self))

    async def update(self):
        log.debug("'%s' sub_support was UPDATED", str(self))

    def retire(self):
        log.debug("'%s' sub_support was RETIRED", str(self))

    # def __getattr__(self, attr_name):
    #     if attr_name.startswith('get_'):
    #         mod_attr_name = attr_name.replace('get_', '_embed_recipe_')
    #         if mod_attr_name in self.embed_build_recipes:
    #             return self.embed_build_recipes.get(mod_attr_name)
    #     raise AttributeError


def get_class():
    return EmbedBuilder
# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
