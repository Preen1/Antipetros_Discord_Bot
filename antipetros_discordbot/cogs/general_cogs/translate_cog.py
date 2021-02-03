
# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
from datetime import datetime
import re
# * Third Party Imports --------------------------------------------------------------------------------->
from pytz import timezone, country_timezones
from fuzzywuzzy import fuzz
from fuzzywuzzy import process as fuzzprocess
from discord.ext import commands
from googletrans import LANGUAGES, Translator
from typing import Optional
import unicodedata
import emoji
from discord import AllowedMentions
# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.cogs import get_aliases
from antipetros_discordbot.utility.misc import CogConfigReadOnly, day_to_second, save_commands, hour_to_second, minute_to_second, update_config, make_config_name
from antipetros_discordbot.utility.checks import log_invoker, in_allowed_channels, allowed_channel_and_allowed_role, allowed_channel_and_allowed_role_2, allowed_requester, command_enabled_checker
from antipetros_discordbot.utility.named_tuples import CITY_ITEM, COUNTRY_ITEM
from antipetros_discordbot.utility.gidtools_functions import loadjson, writejson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.cogs import get_aliases, get_doc_data
from antipetros_discordbot.utility.converters import LanguageConverter
from antipetros_discordbot.utility.poor_mans_abc import attribute_checker
# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)


# endregion[Logging]

# region [Constants]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
# location of this file, does not work if app gets compiled to exe with pyinstaller
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
COG_NAME = "TranslateCog"
CONFIG_NAME = make_config_name(COG_NAME)
get_command_enabled = command_enabled_checker(CONFIG_NAME)

# endregion[Constants]


class TranslateCog(commands.Cog, command_attrs={'hidden': True, "name": COG_NAME}):
    """
    Soon
    """
    # region [ClassAttributes]

    language_dict = {value: key for key, value in LANGUAGES.items()}
    language_emoji_map = {'de': 'de',
                          'rs': 'ru',
                          'gb': 'en',
                          'au': 'en',
                          'us': 'en',
                          'gr': 'el',
                          'za': 'af',
                          }
    docattrs = {'show_in_readme': True,
                'is_ready': True}
    required_config_options = {}
    config_name = CONFIG_NAME
# endregion [ClassAttributes]

# region [Init]

    def __init__(self, bot):
        self.bot = bot
        self.support = self.bot.support
        self.translator = Translator()
        self.flag_emoji_regex = re.compile(r'REGIONAL INDICATOR SYMBOL LETTER (?P<letter>\w)')
        update_config(self)
        self.allowed_channels = allowed_requester(self, 'channels')
        self.allowed_roles = allowed_requester(self, 'roles')
        self.allowed_dm_ids = allowed_requester(self, 'dm_ids')
        if os.environ.get('INFO_RUN', '') == "1":
            save_commands(self)
        glog.class_init_notification(log, self)

# endregion [Init]

# region [Properties]


# endregion [Properties]

# region [Setup]


    async def on_ready_setup(self):

        log.debug('setup for cog "%s" finished', str(self))

    async def update(self, typus):
        return
        log.debug('cog "%s" was updated', str(self))

# endregion [Setup]

# region [Loops]


# endregion [Loops]

# region [Listener]

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def emoji_translate(self, payload):
        if get_command_enabled("emoji_translate") is False:
            return
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = payload.member
        if channel.name.casefold() not in self.allowed_channels("emoji_translate"):
            return

        if all(role.name.casefold() not in self.allowed_roles("emoji_translate") for role in user.roles):
            return

        if user.bot:

            return

        log.debug(self.get_emoji_name(payload.emoji.name))
        match = self.flag_emoji_regex.findall(self.get_emoji_name(payload.emoji.name))
        if match:
            country_code = self.language_emoji_map.get(''.join(match).lower())
            translated = self.translator.translate(text=message.content, dest=country_code, src="auto")
            await message.reply(f"**in {LANGUAGES.get(country_code)}:** *{translated.text}*", allowed_mentions=AllowedMentions.none())


# endregion [Listener]

# region [Commands]

    @commands.command(aliases=get_aliases('translate'), **get_doc_data('translate'))
    @allowed_channel_and_allowed_role_2()
    @commands.cooldown(1, 10, commands.BucketType.channel)
    async def translate(self, ctx, to_language_id: Optional[LanguageConverter] = "english", *, text_to_translate: str):
        """
        Translates text into multiple different languages.
        Tries to auto-guess input language.

        Args:
            text_to_translate (str): the text to translate, quotes are optional
            to_language_id (Optional[LanguageConverter], optional): either can be the name of the language or an language code (iso639-1 language codes). Defaults to "english".
        """
        translated = self.translator.translate(text=text_to_translate, dest=to_language_id, src="auto")
        await ctx.send(f"__from {ctx.author.display_name}:__ *{translated.text}*")


# endregion [Commands]

# region [DataStorage]


# endregion [DataStorage]

# region [Embeds]


# endregion [Embeds]

# region [HelperMethods]

    @staticmethod
    def get_emoji_name(s):
        return s.encode('ascii', 'namereplace').decode('utf-8', 'namereplace')


# endregion [HelperMethods]

# region [SpecialMethods]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.user.name})"

    def __str__(self):
        return self.qualified_name

    def cog_unload(self):

        pass


# endregion [SpecialMethods]


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(attribute_checker(TranslateCog(bot)))
