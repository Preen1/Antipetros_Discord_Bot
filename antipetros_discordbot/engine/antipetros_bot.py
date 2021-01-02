# region [Imports]

# * Standard Library Imports -->
import os
from datetime import datetime
from collections import namedtuple
import traceback
import asyncio
from asyncio import Future
from contextlib import suppress
import sys
from inspect import iscoroutinefunction, iscoroutine
# * Third Party Imports -->
from discord.ext import commands, tasks
import discord

from async_property import async_property
from discord import Embed, File
from watchgod import awatch
from concurrent.futures import ThreadPoolExecutor
import aiohttp
from udpy import AsyncUrbanClient
# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.init_userdata.user_data_setup import SupportKeeper
from antipetros_discordbot.engine.special_prefix import when_mentioned_or_roles_or
from antipetros_discordbot.utility.gidtools_functions import loadjson, writejson, pathmaker, readit
from antipetros_discordbot.utility.misc import sync_to_async
from antipetros_discordbot.utility.embed_helpers import make_basic_embed
from antipetros_discordbot.utility.named_tuples import CreatorMember
from antipetros_discordbot.engine.staff_invoke_statistician import InvokeStatistician
from antipetros_discordbot.engine.staff_error_handler import ErrorHandler
from antipetros_discordbot.engine.global_checks import user_not_blacklisted
from antipetros_discordbot.engine.command_staff import CommandStaffRoster
# endregion[Imports]


# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
glog.import_notification(log, __name__)

# endregion[Logging]

# region [Constants]

APPDATA = SupportKeeper.get_appdata()
BASE_CONFIG = SupportKeeper.get_config('base_config')

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]

# TODO: create regions for this file
# TODO: Document and Docstrings
# IDEA: Use an assistant class to hold some of the properties and then use the __getattr__ to make it look as one object, just for structuring


class AntiPetrosBot(commands.Bot):
    creator = CreatorMember('Giddi', 576522029470056450, None, None)
    executor = ThreadPoolExecutor(6, thread_name_prefix='Bot_Thread')
    admin_cog_import_path = "antipetros_discordbot.cogs.admin_cogs.admin_cog"
    bot_feature_suggestion_folder = APPDATA["bot_feature_suggestion_data"]
    bot_feature_suggestion_json_file = APPDATA['bot_feature_suggestions.json']
    cog_import_base_path = BASE_CONFIG.get('general_settings', 'cogs_location')
    available_staff = (InvokeStatistician,ErrorHandler)

    def __init__(self, *args, ** kwargs):
        super().__init__(*args, owner_id=self.creator.id, **kwargs)
        self.case_insensitive = BASE_CONFIG.getboolean('command_settings', 'invocation_case_insensitive')
        self.description = readit(APPDATA['bot_description.md'])
        self.command_staff = CommandStaffRoster(self, self.available_staff)
        self.general_data = loadjson(APPDATA['general_data.json'])
        self.max_message_length = 1900
        self.commands_executed = 0
        self.bot_member = None
        self.aio_request_session = None
        self.urban_client = None
        self.all_bot_roles = []
        self.current_day = datetime.utcnow().day
        user_not_blacklisted(self, log)

        if BASE_CONFIG.getboolean('startup_message', 'use_startup_message') is True:
            self.startup_message = (BASE_CONFIG.getint('startup_message', 'channel'), BASE_CONFIG.get('startup_message', 'message'))
        else:
            self.startup_message = None
        self._setup()

        glog.class_init_notification(log, self)
        if self.is_debug:
            log.warning('!!!!!!!!!!!!!!!!! DEBUG MODE !!!!!!!!!!!!!!!!!')

    def _setup(self):
        self._get_initial_cogs()
        self.get_bot_roles_loop.start()


    async def on_ready(self):
        log.info('%s has connected to Discord!', self.user.name)
        channel = self.get_channel(BASE_CONFIG.getint('startup_message', 'channel'))
        if self.startup_message is not None:
            delete_time = 240 if self.is_debug is True else 600
            await self.get_channel(self.startup_message[0]).send(self.startup_message[1], delete_after=delete_time)
        await asyncio.sleep(2)
        self.command_staff.staff_memo(attribute_name='on_ready')
        if self.is_debug:
            await self.debug_function()

    def _get_initial_cogs(self):
        load_dev = BASE_CONFIG.getboolean('general_settings', 'load_dev_cogs')
        self.load_extension(self.admin_cog_import_path)
        log.debug("loaded extension\cog: '%s' from '%s'", self.admin_cog_import_path.split('.')[-1], self.admin_cog_import_path)
        for _cog in BASE_CONFIG.options('extensions'):
            if BASE_CONFIG.getboolean('extensions', _cog) is True:
                name = _cog.split('.')[-1]
                full_import_path = self.cog_import_base_path + '.' + _cog
                self.load_extension(full_import_path)
                log.debug("loaded extension-cog: '%s' from '%s'", name, full_import_path)

        log.info("extensions-cogs loaded: %s", ', '.join(self.cogs))

    async def close(self):
        # TODO: check the needs for everything here, currently copied from official Python Discord Bot
        self.command_staff.staff_memo('retire')
        for ext in list(self.extensions):
            with suppress(Exception):
                self.unload_extension(ext)

        if self.aio_request_session:
            await self.aio_request_session.close()
            log.debug('aiosession closed: %s', str(self.aio_request_session.closed))
        await super().close()
        if self.loop.is_closed():
            sys.exit()

    @staticmethod
    def activity_from_config(option='standard_activity'):
        activity_dict = {'playing': discord.ActivityType.playing,
                         'watching': discord.ActivityType.watching,
                         'listening': discord.ActivityType.listening,
                         'streaming': discord.ActivityType.streaming}
        text, activity_type = BASE_CONFIG.getlist('activity', option)
        if activity_type not in activity_dict:
            log.critical("'%s' is not an Valid ActivityType, aborting activity change")
            return
        activity_type = activity_dict.get(activity_type)

        return discord.Activity(name=text, type=activity_type)

    async def on_command_error(self, ctx, error):
        _call_item = self.command_staff.handle_errors
        if iscoroutinefunction(_call_item):
            await _call_item(ctx,error)
        else:
            _call_item(ctx,error)

    #     elif isinstance(error, commands.CommandOnCooldown):
    #         await ctx.channel.send(f'{ctx.author.mention} your mother was a hamster and your father smelt of elderberries, STOP SPAMMING!', delete_after=30)
    #         await ctx.message.delete()
    #     else:
    #         log.error('Ignoring exception in command {}:'.format(ctx.command))
    #         log.error(str(error), exc_info=True)

    @tasks.loop(minutes=10, reconnect=True)
    async def update_check_loop(self):
        if self.current_day != datetime.utcnow().day:
            self.current_day = datetime.utcnow().day
            self.command_staff.staff_memo('update')


    @tasks.loop(minutes=30, reconnect=True)
    async def get_bot_roles_loop(self):
        log.info('Starting Refreshing Bot Roles')
        if self.aio_request_session is None:
            self.aio_request_session = aiohttp.ClientSession(loop=self.loop)
        if self.urban_client is None:
            self.urban_client = AsyncUrbanClient()
        self.all_bot_roles = []
        self.bot_member = await self.retrieve_member(self.antistasi_guild.id, self.id)
        for index, role in enumerate(self.bot_member.roles):
            if index != 0:
                self.all_bot_roles.append(role)
        if BASE_CONFIG.getboolean('prefix', 'invoke_by_role_and_mention') is True:
            self.command_prefix = when_mentioned_or_roles_or(BASE_CONFIG.get('prefix', 'command_prefix'))
        else:
            self.command_prefix = BASE_CONFIG.get('prefix', 'command_prefix')

        AntiPetrosBot.creator = self.creator._replace(**{'member_object': await self.retrieve_antistasi_member(self.creator.id), 'user_object': await self.fetch_user(self.creator.id)})
        log.info('Finished Refreshing Bot Roles')

    @get_bot_roles_loop.before_loop
    async def before_get_bot_roles_loop(self):
        await self.wait_until_ready()

    @property
    def antistasi_guild(self):
        return self.get_guild(self.general_data.get('antistasi_guild_id'))

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
    def blacklisted_users(self):
        return loadjson(APPDATA['blacklist.json'])

    @property
    def notify_contact_member(self):
        return BASE_CONFIG.get('blacklist', 'notify_contact_member')

    @property
    def std_date_time_format(self):
        return "%Y-%m-%d %H:%M:%S"

    def blacklisted_user_ids(self):
        for user_item in self.blacklisted_users:
            yield user_item.get('id')

    async def message_creator(self, message=None, embed=None, file=None):
        if message is None and embed is None:
            message = 'message has no content'
        await self.creator.member_object.send(content=message, embed=embed, file=file)

    async def retrieve_antistasi_member(self, user_id):
        return await self.antistasi_guild.fetch_member(user_id)

    async def retrieve_member(self, guild_id, user_id):
        guild = self.get_guild(guild_id)
        return await guild.fetch_member(user_id)

    async def split_to_messages(self, ctx, message, split_on='\n'):
        _out = ''
        chunks = message.split(split_on)
        for chunk in chunks:
            if sum(map(len, _out)) + len(chunk + split_on) < self.max_message_length:
                _out += chunk + split_on
            else:
                await ctx.send(_out)
                await asyncio.sleep(0.25)
                _out = ''
        await ctx.send(_out)

    @sync_to_async
    def channel_from_name(self, channel_name):
        return discord.utils.get(self.antistasi_guild.channels, name=channel_name)

    @sync_to_async
    def member_by_name(self, member_name):
        member_name = member_name.casefold()
        for member in self.antistasi_guild.members:

            if member.name.casefold() == member_name:
                return member

    async def execute_in_thread(self, func, *args, **kwargs):
        return await self.loop.run_in_executor(self.executor, func, *args, **kwargs)

    def save_bin_file(self, path, data):
        with open(path, 'wb') as f:
            f.write(data)

    async def save_feature_suggestion_extra_data(self, data_name, data_content):
        path = pathmaker(self.bot_feature_suggestion_folder, data_name)
        await self.execute_in_thread(self.save_bin_file, path, data_content)
        return path

    async def add_to_feature_suggestions(self, item):
        feat_suggest_json = loadjson(self.bot_feature_suggestion_json_file)
        feat_suggest_json.append(item._asdict())
        writejson(feat_suggest_json, self.bot_feature_suggestion_json_file)


    async def debug_function(self):
        log.debug("debug function triggered")
        log.warning('nothing set in debug function for "%s"', self.user.name)




    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return self.__class__.__name__
