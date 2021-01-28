

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
from typing import Optional

# * Third Party Imports --------------------------------------------------------------------------------->
import discord
from discord.ext import commands

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.cogs import get_aliases
from antipetros_discordbot.utility.misc import save_commands
from antipetros_discordbot.utility.checks import in_allowed_channels
from antipetros_discordbot.utility.converters import DateOnlyConverter
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper

# endregion[Imports]

# region [TODO]


# TODO: get_logs command
# TODO: get_appdata_location command


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
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_NAME = "purge_message"

# endregion[Constants]


class PurgeMessagesCog(commands.Cog, command_attrs={'hidden': True, "name": "PurgeMessagesCog"}):
    """
    Soon
    """
    config_name = CONFIG_NAME
    docattrs = {'show_in_readme': False,
                'is_ready': True}

    def __init__(self, bot):
        self.bot = bot
        self.support = self.bot.support
        if os.environ.get('INFO_RUN', '') == "1":
            save_commands(self)
        glog.class_init_notification(log, self)

    @commands.command(aliases=get_aliases("purge_antipetros"))
    @commands.is_owner()
    @in_allowed_channels(set(COGS_CONFIG.getlist(CONFIG_NAME, 'allowed_channels')))
    async def purge_antipetros(self, ctx, and_giddi: Optional[str] = None, number_of_messages: Optional[int] = 1000):

        def is_antipetros(message):
            if and_giddi != "and_giddi":
                return message.author.id == self.bot.id
            return message.author.id in [self.bot.id, self.bot.creator.id]

        await ctx.channel.purge(limit=number_of_messages, check=is_antipetros, bulk=True)

    def __repr__(self):
        return f"{self.name}({self.bot.user.name})"

    def __str__(self):
        return self.qualified_name

    @commands.command(aliases=get_aliases("purge_msg_from_user"))
    @ commands.has_any_role(*COGS_CONFIG.getlist("general_debug", 'allowed_roles'))
    @in_allowed_channels(set(COGS_CONFIG.getlist(CONFIG_NAME, 'allowed_channels')))
    async def purge_msg_from_user(self, ctx, user: discord.User, number_of_messages: Optional[int] = 1000, since: Optional[DateOnlyConverter] = None):

        def is_user(message):
            return message.author.id == user.id

        messages_deleted = await ctx.channel.purge(limit=number_of_messages, check=is_user, after=since, bulk=True)
        await ctx.send(f"deleted {len(messages_deleted)} messages from {user.name}")

# region[Main_Exec]


def setup(bot):
    bot.add_cog(PurgeMessagesCog(bot))

# endregion[Main_Exec]
