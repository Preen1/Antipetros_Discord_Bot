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
from typing import Union, List
from functools import partial
from time import time, sleep, time_ns
from antipetros_discordbot.abstracts.subsupport_abstract import SubSupportBase
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from benedict import benedict
from discord import Embed, File, Color as DiscordColor
from antipetros_discordbot.utility.gidtools_functions import (readit, clearit, readbin, work_in, writeit, loadjson, pickleit, splitoff, writebin, pathmaker, writejson, dir_change,
                                                              linereadit, bytes2human, create_file, file_walker, get_pickled, ishash_same, ext_splitter, appendwriteit, create_folder,
                                                              number_rename, timenamemaker, cascade_rename, file_name_time, absolute_listdir, hash_to_solidcfg, path_part_remove,
                                                              from_dict_to_file, get_absolute_path, file_name_modifier, limit_amount_of_files, limit_amount_files_absolute)

from antipetros_discordbot.utility.misc import datetime_isoformat_to_discord_format
from antipetros_discordbot.utility.exceptions import FuzzyMatchError
from antipetros_discordbot.utility.enums import EmbedType
from dateparser import parse as date_parse
import arrow
from tempfile import TemporaryDirectory
from PIL import Image as PillowImage
from io import BytesIO
from random import randint
from antipetros_discordbot.utility.named_tuples import EmbedFieldItem
from antipetros_discordbot.utility.discord_markdown_helper.special_characters import ZERO_WIDTH
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
    default_embed_data_file = pathmaker(APPDATA['default_embed_data.json'])
    allowed_embed_types = [embed_type_member.value for embed_type_member in EmbedType]
    datetime_parser = date_parse
    datetime_int_parser = arrow.get
    generic_image_name_range = (1, 9999)
    field_item = EmbedFieldItem

    def __init__(self, bot, support):
        self.bot = bot
        self.support = support
        self.loop = self.bot.loop
        self.is_debug = self.bot.is_debug
        self._ensure_folder_exists()
        self.embed_build_recipes = None
        self.default_empty = Embed.Empty
        self.special_authors = {'bot_author': {'name': self.bot.display_name, 'url': self.bot.github_url, 'icon_url': self.bot.github_image},
                                'default_author': self.default_author}
        self.special_footers = {'feature_request_footer': {'text': "For feature suggestions and feature request, contact @Giddi".title(), "icon_url": self.bot.creator_member.member_object.avatar_url},
                                'default_footer': self.default_footer}
        self.replacement_map = {"$BOT_NAME$": self.bot.display_name}
        self.default_field_name_num = 1

        glog.class_init_notification(log, self)

    def _validate_color(self, color):
        if isinstance(color, str):
            if color == 'random':
                return self.bot.random_color.discord_color
            else:
                try:
                    return self.bot.get_discord_color(color)
                except FuzzyMatchError:
                    return self.default_color.discord_color
        elif isinstance(color, DiscordColor):
            return color
        else:
            raise TypeError(f"'color' needs to either be a string or and discord_color not '{type(color)}'")

    def _validate_type(self, typus):
        if isinstance(typus, EmbedType):
            return typus.value
        elif isinstance(typus, str) and typus in self.allowed_embed_types:
            return typus
        else:
            raise KeyError(f"'type' either needs to be an 'EmbedType' enum or one of '{[embed_type_member.value for embed_type_member in EmbedType]}' not {typus}")

    def _validate_timestamp(self, timestamp):
        if isinstance(timestamp, datetime):
            return timestamp
        elif isinstance(timestamp, str):
            return self.datetime_parser(timestamp)
        elif isinstance(timestamp, int):
            return self.datetime_int_parser(timestamp)
        else:
            raise TypeError("'timestamp' has to be either of type 'datetime', 'str' or 'int' not '{type(timestamp)}'")

    def _validate_image(self, image):
        if isinstance(image, str):
            if os.path.isfile(image):
                file_name = os.path.basename(image).replace('_', '')

                file = File(fp=image, filename=file_name)
                image = f"attachment://{file_name}"
                return image, file
            else:
                return image, None
        elif isinstance(image, PillowImage):
            with BytesIO() as image_binary:
                image_format = 'PNG' if image.format is None else image.format
                image.save(image_binary, image_format, optimize=True)
                image_binary.seek(0)
                file_name = os.path.basename(image.filename).replace('_', '') if image.filename != '' else f"image{randint(*self.generic_image_name_range)}.{image_format.lower()}"
                file = File(fp=image_binary, filename=file_name)
                image = f"attachment://{file_name}"
                return image, file
        elif image is None:
            return None, None
        else:
            raise TypeError(f"'image' has to be of type 'str' or '{type(PillowImage)}' and not '{type(image)}'")

    def _fix_field_item(self, field_item, ):
        if field_item.name is None:
            field_item = field_item._replace(name=str(self.default_field_name_num) + '.')
            self.default_field_name_num += 1
        if field_item.value is None:
            field_item = field_item._replace(value=ZERO_WIDTH)
        if field_item.inline is None:
            field_item = field_item._replace(inline=self.default_inline_value)
        return field_item

    async def make_generic_embed(self, author: Union[str, dict] = None, footer: Union[str, dict] = None, fields: List[EmbedFieldItem] = None, **kwargs):
        if isinstance(author, str):
            author = self.special_authors.get(author, self.default_author) if author != 'not_set' else None
        if isinstance(footer, str):
            footer = self.special_footers.get(footer, self.default_footer) if author != 'not_set' else None

        files = []
        generic_embed = Embed(title=str(kwargs.get("title", self.default_title)),
                              description=str(kwargs.get('description', self.default_description)),
                              color=self._validate_color(kwargs.get('color', self.default_color.discord_color)),
                              timestamp=self._validate_timestamp(kwargs.get('timestamp', self.default_timestamp)),
                              type=self._validate_type(kwargs.get('type', self.default_type)))

        image, image_file = self._validate_image(kwargs.get('image', (None, None)))
        files.append(image_file)
        thumbnail, thumbnail_file = self._validate_image(kwargs.get('thumbnail', self.default_thumbnail)) if kwargs.get('thumbnail', self.default_thumbnail) != 'no_thumbnail' else (None, None)
        files.append(thumbnail_file)

        if author is not None:
            generic_embed.set_author(**author)
        if footer is not None:
            generic_embed.set_footer(**footer)
        if thumbnail is not None:
            generic_embed.set_thumbnail(url=thumbnail)
        if image is not None:
            generic_embed.set_image(url=image)

        if fields is not None:
            for field in fields:
                field = self._fix_field_item(field)
                generic_embed.add_field(name=field.name, value=field.value, inline=field.inline)
        self.default_field_name_num = 1
        _out = {"embed": generic_embed}
        files = [file_item for file_item in files if file_item is not None]
        if len(files) == 1:
            _out["file"] = files[0]
        elif len(files) > 1:
            _out['files'] = files
        return _out

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
    def default_inline_value(self):
        """
        "default_inline_value": [true or false]
        """
        return loadjson(self.default_embed_data_file).get('default_inline_value')

    @property
    def default_title(self):
        """
        "default_title": ""
        replace template strings:   - $BOT_NAME$ for bot.display_name

        """

        _out = loadjson(self.default_embed_data_file).get('default_title')
        for replace_marker, replace_value in self.replacement_map.items():
            _out = _out.replace(replace_marker, replace_value)
        return _out

    @property
    def default_description(self):
        """
        "default_description": ""
        replace template strings:   - $BOT_NAME$ for bot.display_name
        """
        _out = loadjson(self.default_embed_data_file).get('default_description')
        for replace_marker, replace_value in self.replacement_map.items():
            _out = _out.replace(replace_marker, replace_value)
        return _out

    @property
    def default_author(self):
        """
        "default_author": {"name": "", "url": "", "icon_url": ""}
        """
        return loadjson(self.default_embed_data_file).get('default_author')

    @property
    def default_footer(self):
        """

        "default_footer": {"text": "", "icon_url": ""},

        """
        return loadjson(self.default_embed_data_file).get('default_footer')

    @property
    def default_thumbnail(self):
        """

        "default_thumbnail": ""

        """
        return loadjson(self.default_embed_data_file).get('default_thumbnail')

    @property
    def default_color(self):
        """
        "default_color": ""
        """
        return loadjson(self.default_embed_data_file).get('default_color')

    @property
    def default_timestamp(self):
        """
        optional!
        "default_timestamp": ""
        """
        return loadjson(self.default_embed_data_file).get('default_timestamp', datetime.now(tz=timezone("Europe/Berlin")))

    @property
    def default_type(self):
        """
        """
        return 'rich'

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
