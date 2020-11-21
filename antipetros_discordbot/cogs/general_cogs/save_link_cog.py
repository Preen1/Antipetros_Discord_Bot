# region [Imports]
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from antipetros_discordbot.utility.gidtools_functions import writejson, loadjson, pathmaker, writeit
import os
from collections import namedtuple
from pprint import pformat
from urllib.parse import urlparse
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG, COGS_CONFIG
from antipetros_discordbot.utility.locations import find_path
from antipetros_discordbot.utility.misc import config_channels_convert
import aiohttp
from antipetros_discordbot.utility.enums import RequestStatus
from antipetros_discordbot.utility.named_tuples import LINK_DATA_ITEM
import asyncio
from tempfile import TemporaryDirectory
# endregion [Imports]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


# TODO: Implemenet "get_link", "get_all_links" and "delete_link" commands

# TODO: change permissions so he can delete messages.

# !TODO: Important! create data_storage_handlers

class SaveLink(commands.Cog):
    blocklist_hostfile_url = "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn/hosts"

    def __init__(self, bot):
        self.bot = bot
        self.data_storage_handler = None
        self.allowed_channels = set(COGS_CONFIG.getlist('save_link', 'allowed_channels'))
        self.forbidden_links = set(loadjson(pathmaker(THIS_FILE_DIR, r'..\..\data\data_storage\json_data\forbidden_link_list.json')))
        self.forbidden_url_words = loadjson(find_path('forbidden_url_words.json'))
        self.link_channel = None
        try:
            self.link_channel = self.channel_from_id(COGS_CONFIG.getint('save_link', 'link_channel'))
        except AttributeError as error:
            print('link_channel had error: ' + str(error))
        self.forbidden_links.add('www.stackoverflow.com')
        self.bad_link_image = discord.File(pathmaker(THIS_FILE_DIR, r"..\..\data\fixed_data\bertha.png"), 'bertha.png')

    @commands.Cog.listener(name='on_ready')
    async def extra_cog_setup(self):
        await self.create_forbidden_link_list()
        self.link_channel = self.channel_from_id(COGS_CONFIG.getint('save_link', 'link_channel'))
        print(f"\n{'-' * 30}\n{self.__class__.__name__} Cog ----> finished extra setup\n{'-' * 30}")

    async def process_raw_blocklist_content(self, raw_content):
        _out = []
        for line in raw_content.splitlines():
            if line.startswith('0') and line not in ['', '0.0.0.0 0.0.0.0']:
                line = line.split('#')[0].strip()
                _, forbidden_url = line.split(' ')
                _out.append(forbidden_url.strip())
        return set(_out)

    async def create_forbidden_link_list(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.blocklist_hostfile_url) as _response:
                if RequestStatus(_response.status) is RequestStatus.Ok:
                    _content = await _response.read()
                    _content = _content.decode('utf-8', errors='ignore')

                    self.forbidden_links = await self.process_raw_blocklist_content(_content)
                    _path = pathmaker(THIS_FILE_DIR, r'..\..\data\data_storage\json_data\forbidden_link_list.json')
                    print(_path)
                    writejson(list(self.forbidden_links), pathmaker(THIS_FILE_DIR, r'..\..\data\data_storage\json_data\forbidden_link_list.json'))

    async def save(self, link_item):
        pass

    @commands.command()
    @commands.has_any_role(*COGS_CONFIG.getlist('save_link', 'allowed_roles'))
    async def save_link(self, ctx, link, link_name=None, days_to_hold: int = None):
        if ctx.channel.name in self.allowed_channels:

            days = 7 if days_to_hold is None else days_to_hold
            date_and_time = datetime.utcnow()
            delete_date_and_time = date_and_time + timedelta(days=days)
            author = ctx.author
            link_name = link.split('.')[1] if link_name is None else link_name
            link_name = link_name.upper()
            link = urlparse(link, scheme='https').geturl().replace('///', '//')

            if all(forbidden_link.casefold() not in link.casefold() for forbidden_link in self.forbidden_links) and all(forbidden_word.casefold() not in link.casefold() for forbidden_word in self.forbidden_url_words):
                link_item = LINK_DATA_ITEM(author, link_name, date_and_time, delete_date_and_time, link)
                await self.save(link_item)
                _embed = await self.answer_embed(link_item)

                await self.link_channel.send(embed=_embed, delete_after=days * 86400)
                await ctx.send('✅ Link was successfully saved')
            else:
                await ctx.send('you tried to save a link that is either in my forbidden_link-list or contains a forbidden word. __Your Message Has been deleted!__\n\n🚫 **The link has NOT been saved!** 🚫\n\n⚠️ **__DO NOT TRY THIS AGAIN__** ⚠️\n\n _This has been Logged_!', file=self.bad_link_image)
                await ctx.message.delete()

    @commands.command()
    @commands.has_any_role(*COGS_CONFIG.getlist('save_link', 'allowed_roles'))
    async def get_forbidden_list(self, ctx, file_format='json'):
        if ctx.channel.name in self.allowed_channels:
            if file_format == 'json':
                with TemporaryDirectory() as tempdir:
                    _name = 'forbidden_links.json'
                    _path = pathmaker(tempdir, _name)
                    writejson(list(self.forbidden_links), _path, indent=2)
                    _file = discord.File(_path, filename=_name)
                    await ctx.send(file=_file, delete_after=60)

    def channel_from_id(self, _id):
        _channel = self.bot.get_channel(_id)
        print("save_link_channel is " + str(_channel.name))
        return _channel

    async def answer_embed(self, link_item):
        _rel_time = link_item.delete_date_time - link_item.date_time
        _embed = discord.Embed(title="Saved Link", description="Temporary Stored Link", color=0x4fe70e)
        _embed.set_thumbnail(url="https://images.emojiterra.com/twitter/v13.0/512px/1f517.png")
        _embed.add_field(name="from:", value=link_item.author.name, inline=True)
        _embed.add_field(name=link_item.link_name + ':', value=link_item.link, inline=False)
        _embed.add_field(name="available until:", value=link_item.delete_date_time.strftime("%Y/%M/%d, %H:%M:%S") + f" ({str(_rel_time).split(',')[0].strip()})", inline=False)
        _embed.add_field(name="retrieve command:", value=f"`get_link {link_item.link_name}`", inline=True)
        _embed.add_field(name="retrieve all command", value="`get_all_links`", inline=True)
        _embed.set_footer(text='This link will be deleted after the date specified in "available until", afterwards it can still be retrieved bythe retrieve commands')
        return _embed


def setup(bot):
    bot.add_cog(SaveLink(bot))
