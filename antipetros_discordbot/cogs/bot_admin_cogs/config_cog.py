from __future__ import annotations

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import random
from datetime import datetime

from configparser import ConfigParser, NoOptionError, NoSectionError
from collections import namedtuple
# * Third Party Imports --------------------------------------------------------------------------------->
import arrow
import discord
from discord import DiscordException
from humanize import naturaltime
from fuzzywuzzy import process as fuzzprocess
from discord.ext import commands
from typing import TYPE_CHECKING
from asyncstdlib.builtins import map as amap

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.cogs import get_aliases
from antipetros_discordbot.utility.misc import CogConfigReadOnly, day_to_second, save_commands, hour_to_second, minute_to_second
from antipetros_discordbot.utility.checks import allowed_channel_and_allowed_role, only_dm_only_allowed_id, log_invoker
from antipetros_discordbot.utility.named_tuples import FeatureSuggestionItem
from antipetros_discordbot.utility.embed_helpers import make_basic_embed
from antipetros_discordbot.utility.data_gathering import gather_data
from antipetros_discordbot.utility.message_helper import add_to_embed_listfield
from antipetros_discordbot.utility.gidtools_functions import loadjson, pickleit, pathmaker, writejson, get_pickled, readit
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.discord_markdown_helper.special_characters import ZERO_WIDTH
if TYPE_CHECKING:
    from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot
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

CONFIG_NAME = 'config'

_from_cog_config = CogConfigReadOnly(CONFIG_NAME)
# endregion[Constants]


class ConfigCog(commands.Cog, command_attrs={'hidden': True, "name": "ConfigCog"}):
    """
    Cog with commands to access and manipulate config files, also for changing command aliases.
    Almost all are only available in DM's

    commands are hidden from the help command.
    """
    # region [ClassAttributes]
    config_dir = APPDATA['config']
    alias_file = APPDATA['command_aliases.json']
    docattrs = {'show_in_readme': False,
                'is_ready': True}
    # endregion[ClassAttributes]

    # region [Init]

    def __init__(self, bot: AntiPetrosBot):
        self.bot = bot
        self.support = self.bot.support
        self.all_configs = [BASE_CONFIG, COGS_CONFIG]
        self.aliases = {}

        if os.environ.get('INFO_RUN', '') == "1":
            save_commands(self)
        glog.class_init_notification(log, self)


# endregion[Init]

# region [Properties]

    @property
    def all_command_aliases(self):
        """
        Property to create a set of all command aliases, to check if any alias is already used.

        Returns:
            [set]: all aliases
        """
        _out = []
        for com_name, aliases in self.aliases.items():
            _out += aliases
        return set(_out)

    @property
    def notify_when_changed(self):
        return _from_cog_config('notify_when_changed', bool)


# endregion[Properties]

# region [HelperMethods]


    async def on_ready_setup(self):
        """
        standard setup async method.
        The Bot calls this method on all cogs when he has succesfully connected.
        """
        self.refresh_command_aliases()
        log.debug('setup for cog "%s" finished', str(self))

    async def _get_available_configs(self):  # sourcery skip: dict-comprehension
        """
        Methods to collect all available config file names, that are in the config folder

        Returns:
            [dict]: dictionary with file names without the extension as keys and the full file name as value
        """
        found_configs = {}
        for _file in os.scandir(self.config_dir):
            if 'config' in _file.name and os.path.splitext(_file.name)[1] in ['.ini', '.json', '.yaml', '.toml']:
                found_configs[os.path.splitext(_file.name)[0]] = _file.name
        return found_configs

    async def _config_file_to_discord_file(self, config_name: str):
        """
        Converts a config file to a sendable discord File object.

        Args:
            config_name ([str]): the config you want to convert, with extension

        Returns:
            [discord.File]: the converted config file
        """
        config_name = config_name + '.ini' if not config_name.endswith('.ini') else config_name
        config_path = pathmaker(self.config_dir, config_name) if '/' not in config_name else config_name
        return discord.File(config_path, config_name)

    async def _match_config_name(self, config_name_input):
        available_configs = await self._get_available_configs()
        _result = fuzzprocess.extractOne(config_name_input, choices=available_configs.keys(), score_cutoff=80)
        if _result is None:
            return None
        else:
            return pathmaker(self.config_dir, available_configs[_result[0]])

    def save_command_aliases(self):
        writejson(self.aliases, self.alias_file)

    def refresh_command_aliases(self):
        self.aliases = loadjson(self.alias_file)

    def get_alias_variations(self, alias):
        variations = [lambda x: x.replace('_', '-'),
                      lambda x: x.replace('-', '').replace('_', ''),
                      lambda x: x.replace('-', '.').replace('_', '.')]
        _out = [alias]
        for variation_func in variations:
            _out.append(variation_func(alias))
        return list(set(_out))

    @staticmethod
    async def config_to_set(config: ConfigParser):
        as_dict = {section_name: dict(config[section_name]) for section_name in config.sections()}
        _out = []
        for section, options in as_dict.items():
            for option, value in options.items():
                _out.append((section, option, value))
        return set(_out)

    async def compare_configs(self, old_config: str, new_config: str):
        config_old = ConfigParser().read_string(old_config)
        config_new = ConfigParser().read_string(new_config)
        old_config_set = await self.config_to_set(config_old)
        new_config_set = await self.config_to_set(config_new)
        config_difference = new_config_set - old_config_set
        _out = []
        DiffItem = namedtuple('DiffItem', ['section', 'option', 'old_value', 'new_value'])
        for change_item in config_difference:
            try:
                old_value = config_old.get(change_item[0], change_item[1])
            except NoOptionError:
                old_value = 'NEW OPTION'
            except NoSectionError:
                old_value = 'NEW SECTION'
            _out.append(DiffItem(change_item[0], change_item[1], old_value, change_item[2]))
        return _out

    async def _make_notify_changed_config_embed(self, ctx, change_items):
        return await self.bot.make_generic_embed(title='Changed config file uploaded Notification',
                                                 author={'name': ctx.author.name, 'icon_url': ctx.author.avatar_url},
                                                 timestamp=ctx.message.created_at,
                                                 color='RED',
                                                 fields=[self.bot.field_item(name=item.section, value=f"{item.option}\n{item.old_value} -> {item.new_value}", inline=False) for item in change_items])

    async def changed_config_uploaded(self, ctx, old_config: str, new_config: str):
        # TODO: Dont know how but test this thing, could very well explode
        changes = await self.compare_configs(old_config, new_config)

        roles_to_notify = await amap(self.bot.role_from_string, _from_cog_config('notify_by_role', list))
        members_to_notify = await amap(self.bot.member_by_name, _from_cog_config('notfiy_by_name', list))

        if self.bot.creator.member_object not in members_to_notify:
            members_to_notify.append(self.bot.creator.member_object)

        if _from_cog_config('notify_via', str).casefold() == 'dm':
            for role in roles_to_notify:
                members_to_notify += await self.bot.all_members_with_role(role)
        for member in members_to_notify:
            _embed = await self._make_notify_changed_config_embed(ctx, change_items=changes)
            await member.send(**_embed)
        if _from_cog_config('notify_via', str).casefold() == 'CHANNEL':
            channel = await self.bot.channel_from_name(_from_cog_config('notification_channel', str))
            content = ' '.join((role.mention for role in roles_to_notify)) + ' ' + ' '.join((member.mention for member in members_to_notify))
            _embed = await self._make_notify_changed_config_embed(ctx, change_items=changes)
            await channel.send(content=content, **_embed)

# endregion [HelperMethods]

# region [Commands]

    @ commands.command(aliases=get_aliases("list_configs"))
    @only_dm_only_allowed_id(CONFIG_NAME)
    async def list_configs(self, ctx):
        """
        Lists all available configs, usefull to get the name for the other commands

        Args:
            ctx ([discord.ext.commands.Context]): mandatory argument for discord bot commands, contains the invocation context
        """
        log.debug("list_configs command passed check")
        available_configs = await self._get_available_configs()
        log.debug(f"{available_configs=}")
        _fields = []
        for available_config in available_configs:
            _fields.append(self.bot.field_item('--> ' + available_config, ZERO_WIDTH, False))
        _embed = await self.bot.make_generic_embed(fields=_fields)
        await ctx.send(**_embed)

        log.info("config list send to '%s'", ctx.author.name)

    @ commands.command(aliases=get_aliases("config_request"))
    @only_dm_only_allowed_id(CONFIG_NAME)
    async def config_request(self, ctx, config_name: str = 'all'):
        """
        Sends config files via discord as attachments.
        If config_name is 'all' it sends all available configs.

        Args:
            ctx ([discord.ext.commands.Context]): mandatory argument for discord bot commands, contains the invocation context
            config_name (str, optional): the name of the config file, will be fuzzy matched to an actula config. Defaults to 'all'.
        """
        available_configs = await self._get_available_configs()
        requested_configs = []
        if config_name.casefold() == 'all':
            requested_configs = [conf_file_name for key, conf_file_name in available_configs.items()]

        else:
            _req_config_path = await self._match_config_name(config_name)
            requested_configs.append(os.path.basename(_req_config_path))

        if requested_configs == []:
            # TODO: make as embed
            await ctx.send(f'I was **NOT** able to find a config named `{config_name}`!\nTry again with `all` as argument, or request the available configs with the command `list_configs`')
        else:
            for req_config in requested_configs:
                _msg = f"Here is the file for the requested config `{req_config}`"
                _file = await self._config_file_to_discord_file(req_config)
                # TODO: make as embed
                await ctx.send(_msg, file=_file)
            log.info("requested configs (%s) send to %s", ", ".join(requested_configs), ctx.author.name)

    @ commands.command(aliases=get_aliases("overwrite_config_from_file"))
    @only_dm_only_allowed_id(CONFIG_NAME)
    @log_invoker(log, 'critical')
    async def overwrite_config_from_file(self, ctx):
        """
        Accepts and config file as attachments and replaces the existing config with it.
        Config File need to have the matching name to overwrite.

        Args:
            ctx ([discord.ext.commands.Context]): mandatory argument for discord bot commands, contains the invocation context
        """
        if len(ctx.message.attachments) > 1:
            # TODO: Test Embed
            _embed = await self.bot.make_generic_embed(title="Too many Attachments",
                                                             description='please only send a single file with the command')
            await ctx.send(**_embed)
            return

        _file = ctx.message.attachments[0]
        _file_name = _file.filename
        config_name = os.path.splitext(_file_name)[0]
        _config_path = await self._match_config_name(config_name)
        if _config_path is None:
            # TODO: Test Embed
            _embed = await self.bot.make_generic_embed(title="Config Name not found",
                                                             description=f'could not find a config that fuzzy matches `{config_name}`')
            await ctx.send(**_embed)
            return
        old_config_content = readit(_config_path)
        await _file.save(_config_path)
        new_config_content = readit(_config_path)
        for cfg in self.all_configs:
            cfg.read()
        # TODO: Test Embed
        _embed = await self.bot.make_generic_embed(title="Config Saved!",
                                                         description=f'saved your file as `{os.path.basename(_config_path)}`',
                                                         footer={'text': "You may have to reload the Cogs or restart the bot for it to take effect!"})
        await ctx.send(**_embed)

        if self.notify_when_changed is True:
            await self.changed_config_uploaded(ctx, config_name, old_config_content, new_config_content)

    @commands.command(aliases=get_aliases("change_setting_to"))
    @only_dm_only_allowed_id(CONFIG_NAME)
    async def change_setting_to(self, ctx, config, section, option, value):
        """
        Command to change a single config setting.

        Args:
            ctx ([discord.ext.commands.Context]): mandatory argument for discord bot commands, contains the invocation context
            config (str): the config name, will be fuzzy matched
            section (str): config section name
            option (str): config option name
            value (str): new value to set
        """

        if config.casefold() in ['base_config', 'cogs_config']:
            if config.casefold() == 'base_config':
                _config = BASE_CONFIG
            elif config.casefold() == 'cogs_config':
                _config = COGS_CONFIG

            if section in _config.sections():
                log.debug(f"{_config=}")
                _config.read()

                _config.set(section, option, value)
                _config.save()
                await ctx.send(f"change the setting '{option}' in section '{section}' to '{value}'")
            else:
                await ctx.send('no such section in the specified config')
        else:
            await ctx.send('config you specified does not exist!')

    @commands.command(aliases=get_aliases("show_config_content"))
    @only_dm_only_allowed_id(CONFIG_NAME)
    async def show_config_content(self, ctx: commands.Context, config_name: str = "all"):

        config_name = config_name.casefold()
        requested_configs = []
        if config_name == 'all':
            requested_configs = self.all_configs
        elif config_name in ['cogs_config', 'cogs', 'cogsconfig']:
            requested_configs.append(COGS_CONFIG)
        elif config_name in ['base_config', "base", "baseconfig"]:
            requested_configs.append(BASE_CONFIG)
        for config in requested_configs:
            fields = []
            defaults = config.defaults()
            default_values = [ZERO_WIDTH]
            if defaults:
                for key, value in defaults.items():
                    default_values.append(f"__{key}__ \t=\t *{value}*")
                default_values += ['-' * 20, ZERO_WIDTH]
                fields.append(self.bot.field_item('__**DEFAULT**__', '\n'.join(default_values), False))
            for section in config.sections():
                options_values = [ZERO_WIDTH]
                for option in config.options(section):
                    if option not in defaults:
                        options_values.append(f"__{option}__ \t=\t *{config.get(section, option)}*")
                    else:
                        options_values.append("")
                options_values += ['-' * 50, ZERO_WIDTH]
                fields.append(self.bot.field_item(f"__**{section.upper()}**__", ZERO_WIDTH + '\n'.join([opt for opt in options_values if opt != ""]), False))
            embed = await self.bot.make_generic_embed(title=str(config), description='here are the sections, options and values for the config', fields=fields, footer="not_set", thumbnail="https://icon-library.com/images/configuration-icon/configuration-icon-13.jpg")
            await ctx.send(**embed)

    @commands.command(aliases=get_aliases("show_config_content_raw"))
    @only_dm_only_allowed_id(CONFIG_NAME)
    async def show_config_content_raw(self, ctx: commands.Context, config_name: str = "all"):

        available_configs = await self._get_available_configs()
        requested_configs = []
        if config_name.casefold() == 'all':
            requested_configs = [conf_file_name for key, conf_file_name in available_configs.items()]

        else:
            _req_config_path = await self._match_config_name(config_name)
            requested_configs.append(os.path.basename(_req_config_path))

        if requested_configs == []:
            # TODO: make as embed
            await ctx.send(f'I was **NOT** able to find a config named `{config_name}`!\nTry again with `all` as argument, or request the available configs with the command `list_configs`')
        else:
            for req_config in requested_configs:
                embed = await self.bot.make_generic_embed(thumbnail='no_thumbnail', title=os.path.splitext(os.path.basename(APPDATA[req_config]))[0].upper(), description=f"```ini\n{readit(APPDATA[req_config])}\n```")
                await ctx.send(**embed)

    @ commands.command(aliases=get_aliases("add_alias"))
    @only_dm_only_allowed_id(CONFIG_NAME)
    async def add_alias(self, ctx: commands.Context, command_name: str, alias: str):

        self.refresh_command_aliases()
        if command_name not in self.aliases:
            await ctx.send(f"I was not able to find the command with the name '{command_name}'")
            return
        variant_aliases = self.get_alias_variations(alias)
        if any(mod_alias in self.all_command_aliases for mod_alias in variant_aliases):
            await ctx.send(f"Alias '{alias}' or its standard variations ({', '.join(variant_aliases)}) are already in use, and cant be set")
            return
        for variant in variant_aliases:
            self.aliases[command_name].append(variant)
        self.save_command_aliases()
        await ctx.send(f"successfully added '{alias}' and {', '.join(variant_aliases)} to the command aliases")

# endregion [Commands]

# region [SpecialMethods]

    def __repr__(self):
        return f"{self.name}({self.bot.user.name})"

    def __str__(self):
        return self.__class__.__name__

# endregion [SpecialMethods]


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(ConfigCog(bot))
