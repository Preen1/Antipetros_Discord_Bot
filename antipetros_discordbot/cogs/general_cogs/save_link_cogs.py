import discord
from discord.ext import commands
from github import Github, GithubException
from datetime import datetime, timedelta
from gidtools.gidfiles import writejson, loadjson, pathmaker
import os
from collections import namedtuple
from pprint import pformat
from urllib.parse import urlparse
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG, COGS_CONFIG
from antipetros_discordbot.utility.locations import find_path
from antipetros_discordbot.utility.misc import config_channels_convert

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
FORBIDDEN_LINKS = []


class SaveLink(commands.Cog):
    channel_settings = namedtuple('ChannelSettings', ['name', 'id', 'save_file'])

    def __init__(self, bot):
        self.bot = bot
        self.number = '1'
        self.save_file = pathmaker(THIS_FILE_DIR, 'link_test.json')
        self.allowed_channels = config_channels_convert(COGS_CONFIG.getlist('save_link', 'allowed_channels'))

    async def save_to_json(self, inputer, link_name, now_time, delete_time, link):
        if os.path.isfile(self.save_file) is True:
            _json = loadjson(self.save_file)
        else:
            _json = {}
        _json[link_name] = (inputer, now_time, delete_time, link)
        writejson(_json, self.save_file)

    @commands.command()
    @commands.has_any_role(*COGS_CONFIG.getlist('save_link', 'allowed_roles'))
    async def save_link(self, ctx, link, name, days_to_hold: int = None):
        if ctx.channel.name in self.allowed_channels:
            _days = 7 if days_to_hold is None else days_to_hold
            _now = datetime.now()
            _delete_time = _now + timedelta(days=_days)

            _inputer = str(ctx.author)
            link = urlparse(link, scheme='https').geturl().replace('///', '//')
            if link not in FORBIDDEN_LINKS:
                await self.save_to_json(_inputer, name, _now.isoformat(timespec='seconds'), _delete_time.isoformat(timespec='seconds'), link)
                _post = f"from: **{ctx.author.name}**\navailable until: **{_delete_time.isoformat(timespec='seconds')}**\n\nlink: **{name}**\n{link}"
                await ctx.send(_post, delete_after=_days * 86400)

    def channel_from_id(self, _id):
        return self.bot.get_channel(_id)


def setup(bot):
    bot.add_cog(SaveLink(bot))
