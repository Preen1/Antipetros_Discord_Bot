import discord
from discord import DiscordException
from discord.ext import commands
from github import Github, GithubException
from datetime import datetime, timedelta
from gidtools.gidfiles import writejson, loadjson, pathmaker
import os
from collections import namedtuple
from pprint import pformat
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG, COGS_CONFIG, CONFIG_DIR
from urllib.parse import urlparse
from antipetros_discordbot.utility.misc import config_channels_convert
from fuzzywuzzy import process as fuzzprocess
from antipetros_discordbot.utility.message_helper import add_to_embed_listfield
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


class Administration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.all_configs = [BASE_CONFIG, COGS_CONFIG]
        self.allowed_channels = config_channels_convert(COGS_CONFIG.getlist('save_suggestions', 'allowed_channels'))
        self.allowed_dm_invoker_ids = list(map(int, COGS_CONFIG.getlist('admin', 'allowed_dm_ids')))
        self.config_dir = CONFIG_DIR

    @commands.Cog.listener(name='on_ready')
    async def extra_cog_setup(self):
        print(f"\n{'-' * 30}\n{self.__class__.__name__} Cog ----> nothing to set up\n{'-' * 30}")

    async def get_available_configs(self):  # sourcery skip: dict-comprehension
        found_configs = {}
        for _file in os.scandir(self.config_dir):
            if 'config' in _file.name and os.path.splitext(_file.name)[1] in ['.ini', '.json', '.yaml', '.toml']:
                found_configs[os.path.splitext(_file.name)[0]] = _file.name
        return found_configs

    async def config_file_to_discord_file(self, config_name):
        config_path = pathmaker(self.config_dir, config_name) if '/' not in config_name else config_name
        return discord.File(config_path, config_name)

    async def match_config_name(self, config_name_input):
        available_configs = await self.get_available_configs()
        _result = fuzzprocess.extractOne(config_name_input, choices=available_configs.keys(), score_cutoff=80)
        if _result is None:
            return None
        else:
            return pathmaker(self.config_dir, available_configs[_result[0]])

    @commands.command()
    @commands.has_any_role(*COGS_CONFIG.getlist('admin', 'allowed_roles'))
    async def reload_all_ext(self, ctx):
        if ctx.channel.name in self.allowed_channels:
            _extensions_list = []
            _base_location = BASE_CONFIG.get('general_settings', 'cogs_location')
            for _extension in BASE_CONFIG.options('extensions'):
                if BASE_CONFIG.getboolean('extensions', _extension) is True:
                    try:
                        self.bot.reload_extension(_base_location + '.' + _extension)
                        _extensions_list.append(_extension)
                    except DiscordException as error:
                        print(str(error))
            reloaded_extensions = '\n'.join(_extensions_list)
            await ctx.send(f"**successfully reloaded the following extensions:**\n{reloaded_extensions}")

    @commands.command(name='die_antipetros_die')
    @commands.has_any_role(*COGS_CONFIG.getlist('admin', 'allowed_roles'))
    async def shutdown(self, ctx):
        if ctx.channel.name in self.allowed_channels:
            await ctx.send('cya!')
            await self.bot.logout()

    @commands.command(name='list_configs')
    @commands.dm_only()
    async def list_configs(self, ctx):
        if ctx.author.id in self.allowed_dm_invoker_ids:
            available_configs = await self.get_available_configs()
            _embed = discord.Embed(title="Anti Petros Report")
            await add_to_embed_listfield(_embed, 'Available Configs', available_configs.keys(), prefix='-')
            await ctx.send(embed=_embed)
            print('config list send to ' + ctx.author.name)

    @commands.command(name='send_config')
    @commands.dm_only()
    async def config_request(self, ctx, config_name='all'):
        if ctx.author.id in self.allowed_dm_invoker_ids:
            available_configs = await self.get_available_configs()
            requested_configs = []
            if config_name.casefold() == 'all':
                requested_configs = [conf_file_name for key, conf_file_name in available_configs.items()]

            else:
                _req_config_path = await self.match_config_name(config_name)
                requested_configs.append(os.path.basename(_req_config_path))

            if requested_configs == []:
                await ctx.send(f'I was **NOT** able to find a config named `{config_name}`!\nTry again with `all` as argument, or request the available configs with the command `list_configs`')
            else:
                for req_config in requested_configs:
                    _msg = f"Here is the file for the requested config `{req_config}`"
                    _file = await self.config_file_to_discord_file(req_config)
                    await ctx.send(_msg, file=_file)
                print(f'requested configs ({", ".join(requested_configs)}) send to ' + ctx.author.name)

    @commands.command(name='overwrite_config')
    @commands.dm_only()
    async def overwrite_config_from_file(self, ctx, config_name):
        if ctx.author.id not in self.allowed_dm_invoker_ids:
            return
        if len(ctx.message.attachments) > 1:
            await ctx.send('please only send a single file with the command')
            return
        _file = ctx.message.attachments[0]
        _config_path = await self.match_config_name(config_name)
        if _config_path is None:
            await ctx.send(f'could not find a config that fuzzy matches `{config_name}`')
        else:
            await _file.save(_config_path)
            for cfg in self.all_configs:
                cfg.read()
            await ctx.send(f'saved your file as `{os.path.basename(_config_path)}`.\n\n_You may have to reload the Cogs or restart the bot for it to take effect!_')


def setup(bot):
    bot.add_cog(Administration(bot))
