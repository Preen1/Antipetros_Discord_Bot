
# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import gc
import os
import asyncio
import unicodedata
from datetime import datetime

# * Third Party Imports --------------------------------------------------------------------------------->
import aiohttp
import discord
from discord import File, Embed, DiscordException
from discord.ext import tasks, commands
from async_property import async_property

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.cogs import get_aliases
from antipetros_discordbot.utility.misc import CogConfigReadOnly, day_to_second, save_commands, hour_to_second, minute_to_second
from antipetros_discordbot.utility.enums import RequestStatus
from antipetros_discordbot.utility.checks import log_invoker, in_allowed_channels, allowed_channel_and_allowed_role
from antipetros_discordbot.utility.named_tuples import LINK_DATA_ITEM
from antipetros_discordbot.utility.embed_helpers import EMBED_SYMBOLS, make_basic_embed
from antipetros_discordbot.utility.sqldata_storager import LinkDataStorageSQLite
from antipetros_discordbot.utility.gidtools_functions import writeit, loadjson, pathmaker, writejson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.discord_markdown_helper.special_characters import ZERO_WIDTH

# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
glog.import_notification(log, __name__)

# endregion[Logging]

# region [Constants]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
# location of this file, does not work if app gets compiled to exe with pyinstaller
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_NAME = "faq"
# endregion[Constants]

# region [Helper]

_from_cog_config = CogConfigReadOnly(CONFIG_NAME)

# endregion [Helper]


class FaqCog(commands.Cog, command_attrs={'name': "FaqCog", "description": ""}):

    """
    [summary]

    [extended_summary]

    """
    faq_data_file = APPDATA["converted_faq_list.json"]
    q_emoji = "🇶"
    a_emoji = "🇦"
    faq_symbol = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/FAQ_icon.svg/1280px-FAQ_icon.svg.png"
    embed_color = "blue"
# region [ClassAttributes]

# endregion [ClassAttributes]

# region [Init]

    def __init__(self, bot):

        self.bot = bot
        self.support = self.bot.support
        self.faq_embeds = {}

        if os.environ.get('INFO_RUN', '') == "1":
            save_commands(self)
        glog.class_init_notification(log, self)

# endregion [Init]

# region [Properties]


# endregion [Properties]

# region [Setup]

    async def on_ready_setup(self):
        await self._load_faq_embeds()
        log.debug('setup for cog "%s" finished', str(self))

    async def _load_faq_embeds(self):
        self.faq_embeds = {}

        faq_data = loadjson(self.faq_data_file)
        for faq_item in faq_data:
            question = f"{self.q_emoji} {faq_item.get('question')}"
            answer = f"{ZERO_WIDTH} \n {self.a_emoji}\n{faq_item.get('answer')}\n{ZERO_WIDTH}"
            embed = Embed(title=question,
                          description=answer,
                          color=self.support.random_color.discord_color,
                          timestamp=datetime.strptime("1989-04-23_00-00-01", "%Y-%m-%d_%H-%M-%S"))
            embed.set_author(name=f"FAQ No {faq_item.get('number')}", url="https://discord.com/channels/449481990513754112/673410398510383115/673411275715510292", icon_url="https://pbs.twimg.com/profile_images/1123720788924932098/C5bG5UPq.jpg")
            # embed.set_thumbnail(url=self.faq_symbol)
            embed.set_footer(text='Antistasi Community', icon_url="https://s3.amazonaws.com/files.enjin.com/1218665/site_logo/NEW%20LOGO%20BANNER.png")
            self.faq_embeds[faq_item.get('number')] = embed


# endregion [Setup]

# region [Loops]


# endregion [Loops]

# region [Listener]

# !Proof of concept currently diabled, seems to be only way to be sure

    # @commands.Cog.listener(name='on_message')
    # async def answer_vindicta_mention(self, msg):
    #     if msg.author.bot is True:
    #         return
    #     if any(role.name == 'Member' for role in msg.author.roles):
    #         return
    #     channel = msg.channel
    #     log.debug("answer invicta invoked")
    #     if channel.name not in COGS_CONFIG.getlist(CONFIG_NAME, 'allowed_channels'):
    #         return
    #     log.debug("is correct channel")
    #     content = msg.content

    #     if "vindicta" in content.casefold().split():
    #         log.debug("vindicta in message")
    #         await channel.send(embed=self.faq_embeds.get(1).copy())
    #         await channel.send("this should only be an example of how the bot can react, normaly there is an check if it was said by an member and also a check so it only triggers with new users (it checks the join time). The faq is an example faq of one that would deal with vindicta stuff or you can use a message")

# endregion [Listener]

# region [Commands]

    @commands.command(aliases=get_aliases("post_faq_by_number"))
    @allowed_channel_and_allowed_role(config_name=CONFIG_NAME, in_dm_allowed=False)
    @commands.cooldown(1, 10, commands.BucketType.channel)
    async def post_faq_by_number(self, ctx, faq_numbers: commands.Greedy[int]):
        for faq_number in faq_numbers:
            log.debug(f"faq number provided is {faq_number} with type {type(faq_number)}")
            if faq_number not in self.faq_embeds:
                await ctx.send('No FAQ Entry with that number')
                continue
            embed = self.faq_embeds.get(faq_number).copy()
            await ctx.send(embed=embed)

    @commands.command(aliases=get_aliases("create_faqs_as_embed"))
    @allowed_channel_and_allowed_role(config_name=CONFIG_NAME, in_dm_allowed=False, allowed_channel_key="faq_channel", allowed_roles_key="special_commands_roles")
    @log_invoker(logger=log, level="info")
    @commands.cooldown(1, minute_to_second(5), commands.BucketType.channel)
    async def create_faqs_as_embed(self, ctx):
        for faq_number, faq_embed in self.faq_embeds.items():
            embed = faq_embed.copy()
            await ctx.send(embed=embed, delete_after=60.0)
            await asyncio.sleep(2)


# endregion [Commands]

# region [DataStorage]


# endregion [DataStorage]

# region [Embeds]


# endregion [Embeds]

# region [HelperMethods]


# endregion [HelperMethods]

# region [SpecialMethods]

    def cog_check(self, ctx):
        return True

    async def cog_command_error(self, ctx, error):
        pass

    async def cog_before_invoke(self, ctx):
        pass

    async def cog_after_invoke(self, ctx):
        pass

    def cog_unload(self):

        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.user.name})"

    def __str__(self):
        return self.__class__.__name__


# endregion [SpecialMethods]


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(FaqCog(bot))
