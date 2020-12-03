# region [Imports]

# * Standard Library Imports -->
from datetime import datetime
from collections import namedtuple
# * Third Party Imports -->
from discord.ext import commands, tasks
from async_property import async_property
from discord.ext.commands import when_mentioned_or
from watchgod import awatch
# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG
from antipetros_discordbot.engine.special_prefix import when_mentioned_or_roles_or
# endregion[Imports]

__updated__ = '2020-12-03 01:32:41'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]

# TODO: create regions for this file
# TODO: Document and Docstrings
# TODO: Create run in thread method and executor classattr


class AntiPetrosBot(commands.Bot):

    def __init__(self, *args, **kwargs):

        self.start_time = datetime.utcnow()
        self.max_message_length = 2000
        self.bot_member = None
        self.all_my_roles = []

        super().__init__(*args, **kwargs)
        self.get_bot_roles_loop.start()

    @tasks.loop(minutes=10, reconnect=True)
    async def get_bot_roles_loop(self):
        log.info('Refreshing Bot Roles')
        self.all_my_roles = []
        self.bot_member = await self.retrieve_member(self.antistasi_guild.id, self.id)
        for index, role in enumerate(self.bot_member.roles):
            if index != 0:
                self.all_my_roles.append(role)
        if BASE_CONFIG.getboolean('prefix', 'invoke_by_role_and_mention') is True:
            self.command_prefix = when_mentioned_or_roles_or(BASE_CONFIG.get('prefix', 'command_prefix'))
        else:
            self.command_prefix = BASE_CONFIG.get('prefix', 'command_prefix')
        log.debug("command prefixes: %s", self.command_prefix(self, ''))

    @get_bot_roles_loop.before_loop
    async def before_get_bot_roles_loop(self):
        await self.wait_until_ready()

    @property
    def antistasi_guild(self):
        return self.get_guild(BASE_CONFIG.getint('general_settings', 'antistasi_guild_id'))

    @property
    def id(self):
        return self.user.id

    @property
    def display_name(self):
        return self.user.display_name

    @property
    def is_debug(self):
        return BASE_CONFIG.getboolean('general_settings', 'is_debug')

    @property
    def blacklist_user(self):
        return list(map(int, BASE_CONFIG.getlist('blacklist', 'user')))

    @property
    def contact_user(self):
        return BASE_CONFIG.get('blacklist', 'contact_user')

    async def retrieve_antistasi_member(self, user_id):
        return await self.antistasi_guild.fetch_member(user_id)

    async def retrieve_member(self, guild_id, user_id):
        guild = self.get_guild(guild_id)
        return await guild.fetch_member(user_id)

    async def split_to_messages(self, ctx, message, split_on='\n'):
        _out = ''
        chunks = message.split(split_on)
        for chunk in chunks:
            if sum(map(len, _out)) < self.max_message_length:
                _out += chunk + split_on
            else:
                print(len(_out))
                await ctx.send(_out)
                _out = ''
        await ctx.send(_out)

    async def channel_from_name(self, channel_name):
        for channel in self.antistasi_guild.channels:
            if channel.name.casefold() == channel_name.casefold():
                return channel

    async def member_by_name(self, member_name):
        member_name = member_name.casefold()
        for member in self.antistasi_guild.members:
            print(member.name)
            if member.name.casefold() == member_name:
                return member


# region[Main_Exec]
if __name__ == '__main__':
    pass

# endregion[Main_Exec]
