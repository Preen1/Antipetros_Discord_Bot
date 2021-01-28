
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
from antipetros_discordbot.utility.misc import CogConfigReadOnly, day_to_second, save_commands, hour_to_second, minute_to_second
from antipetros_discordbot.utility.checks import log_invoker, in_allowed_channels, allowed_channel_and_allowed_role
from antipetros_discordbot.utility.named_tuples import CITY_ITEM, COUNTRY_ITEM
from antipetros_discordbot.utility.gidtools_functions import loadjson, writejson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.cogs import get_aliases, get_doc_data
from antipetros_discordbot.utility.converters import LanguageConverter
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

CONFIG_NAME = 'translate'
_from_cog_config = CogConfigReadOnly(CONFIG_NAME)

# endregion[Constants]


class TranslateCog(commands.Cog, command_attrs={'hidden': True, "name": "TranslateCog"}):
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
# endregion [ClassAttributes]

# region [Init]

    def __init__(self, bot):
        self.bot = bot
        self.support = self.bot.support
        self.translator = Translator()
        self.flag_emoji_regex = re.compile(r'REGIONAL INDICATOR SYMBOL LETTER (?P<letter>\w)')
        if os.environ.get('INFO_RUN', '') == "1":
            save_commands(self)
        glog.class_init_notification(log, self)

# endregion [Init]

# region [Properties]


# endregion [Properties]

# region [Setup]


    async def on_ready_setup(self):
        log.debug('setup for cog "%s" finished', str(self))

# endregion [Setup]

# region [Loops]


# endregion [Loops]

# region [Listener]


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if _from_cog_config('enable_translate_by_emoji', typus=bool) is False:
            return
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = payload.member
        if channel.name not in _from_cog_config('allowed_channels', typus=list):
            return

        if all(role.name not in _from_cog_config('allowed_roles', typus=list) for role in user.roles):
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
    @allowed_channel_and_allowed_role(CONFIG_NAME)
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
    bot.add_cog(TranslateCog(bot))
