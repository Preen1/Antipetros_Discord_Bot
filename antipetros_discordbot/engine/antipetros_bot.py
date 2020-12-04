# region [Imports]

# * Standard Library Imports -->
from datetime import datetime
from collections import namedtuple
# * Third Party Imports -->
from discord.ext import commands, tasks
from async_property import async_property
from discord import Embed, File
from watchgod import awatch
from concurrent.futures import ThreadPoolExecutor
# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG
from antipetros_discordbot.engine.special_prefix import when_mentioned_or_roles_or
from antipetros_discordbot.utility.gidtools_functions import loadjson, writejson
# endregion[Imports]


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
    executor = ThreadPoolExecutor(3, thread_name_prefix='Bot_Thread')
    std_date_time_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = datetime.utcnow()
        self.max_message_length = 2000
        self.embed_symbols = loadjson(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\antipetros_discordbot\data\data_storage\json_data\embed_symbols.json")
        self.commands_executed = 0
        self.bot_member = None
        self.all_my_roles = []

        self.get_bot_roles_loop.start()
        glog.class_initiated(self)

    @tasks.loop(minutes=10, reconnect=True)
    async def get_bot_roles_loop(self):
        log.info('Starting Refreshing Bot Roles')
        self.all_my_roles = []
        self.bot_member = await self.retrieve_member(self.antistasi_guild.id, self.id)
        for index, role in enumerate(self.bot_member.roles):
            if index != 0:
                self.all_my_roles.append(role)
        if BASE_CONFIG.getboolean('prefix', 'invoke_by_role_and_mention') is True:
            self.command_prefix = when_mentioned_or_roles_or(BASE_CONFIG.get('prefix', 'command_prefix'))
        else:
            self.command_prefix = BASE_CONFIG.get('prefix', 'command_prefix')
        log.info('Finished Refreshing Bot Roles')

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
    def notify_contact_member(self):
        return BASE_CONFIG.get('blacklist', 'notify_contact_member')

    @property
    def standard_embed_color(self):
        color_string = BASE_CONFIG.get('embeds', 'standard_embed_color')
        return int(color_string, base=16)

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

    async def execute_in_thread(self, func, *args, **kwargs):
        return await self.loop.run_in_executor(self.executor, func, *args, **kwargs)

    async def make_basic_embed(self, title, text=None, footer=None, symbol=None, **kwargs):
        embed_title = str(title).title()
        embed_text = '' if text is None else str(text)

        basic_embed = Embed(title=embed_title, description=embed_text, color=self.standard_embed_color)
        if symbol is not None:
            basic_embed.set_thumbnail(url=self.embed_symbols.get(symbol.casefold(), None))
        for key, value in kwargs.items():
            field_name = key.replace('_', ' ').title()
            if isinstance(value, tuple):
                field_value = str(value[0])
                field_in_line = value[1]
            else:
                field_value = str(value)
                field_in_line = False
            basic_embed.add_field(name=field_name, value=field_value, inline=field_in_line)
        if footer is not None:
            if isinstance(footer, tuple):
                footer_icon_url = self.embed_symbols.get(footer[1].casefold(), None)
                basic_embed.set_footer(str(footer[0]), icon_url=footer_icon_url)
            else:
                basic_embed.set_footer(str(footer))
        return basic_embed

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return self.__class__.__name__


# region[Main_Exec]
if __name__ == '__main__':
    pass

# endregion[Main_Exec]
