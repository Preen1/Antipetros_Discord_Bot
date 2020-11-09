import discord
from discord.ext import commands
from github import Github, GithubException
from datetime import datetime, timedelta
from gidtools.gidfiles import writejson, loadjson, pathmaker
import os
import random
from collections import namedtuple
from pprint import pformat
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG, COGS_CONFIG
from antipetros_discordbot.utility.locations import find_path
from antipetros_discordbot.utility.misc import config_channels_convert
from PIL import Image, ImageFont, ImageDraw
from tempfile import TemporaryDirectory


THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


class TestPlayground(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.allowed_roles = ["Dev Helper", "Admin"]
        self.allowed_channels = ["bot-development-and-testing"]

    @commands.command()
    async def embed_test(self, ctx):
        author_roles = [_user_role.name for _user_role in ctx.author.roles]
        if any(_allowed_role in author_roles for _allowed_role in self.allowed_roles) and ctx.channel.name in self.allowed_channels:
            embed = discord.Embed(title='this is a test embed'.title(), description=f'it is posted in {ctx.channel.name}')
            embed.add_field(name='From', value=ctx.author.name)
            embed.set_footer(text='destroy all humans'.upper())
            await ctx.send(embed=embed)

    @commands.command(name='changesettings')
    async def change_setting_to(self, ctx, config, section, option, value):
        author_roles = [_user_role.name for _user_role in ctx.author.roles]
        if any(_allowed_role in author_roles for _allowed_role in self.allowed_roles) and ctx.channel.name in self.allowed_channels:
            if config.casefold() in ['base_config', 'cogs_config']:
                if config.casefold() == 'base_config':
                    _config = BASE_CONFIG
                elif config.casefold() == 'cogs_config':
                    _config = COGS_CONFIG

                if section in _config.sections():
                    _config.set(section, option, value)
                    _config.save()
                    await ctx.send(f"change the setting '{option}' in section '{section}' to '{value}'")
                else:
                    await ctx.send('no such section in the specified config')
            else:
                await ctx.send('config you specified does not exist!')

    @commands.command(name='die_antipetros_die')
    async def shutdown(self, ctx):
        author_roles = [_user_role.name for _user_role in ctx.author.roles]
        if any(_allowed_role in author_roles for _allowed_role in self.allowed_roles) and ctx.channel.name in self.allowed_channels:
            _a10_pic = "https://www.jetav8r.com/A10Gallery1/0090.jpg"
            await ctx.send(f'So long cruel world. As my last act I will gift you an A10 Bombing run\n{_a10_pic}')
            await self.bot.logout()

    @commands.command()
    async def roll_a_d(self, ctx, sides: int, amount: int = 1):
        _result = 0
        _dice = []
        for _ in range(amount):
            _rolled = random.randint(1, sides)
            _result += _rolled
            _dice.append(_rolled)
        await ctx.send(f"**you have rolled a total of:** {str(_result)}\n**dice result:** {', '.join(map(str,_dice))}")

    @commands.command()
    async def draw_me_a_picture(self, ctx):
        _name = ctx.author.name
        font = ImageFont.truetype("ariblk.ttf", 24)
        img = Image.new('RGB', (400, 400), color='green')
        draw = ImageDraw.Draw(img)
        draw.text((10, 200), f"Nobody likes you, {_name}", (0, 0, 0), font=font)
        with TemporaryDirectory() as tmpdirname:
            img.save(os.path.join(tmpdirname, "tmpimage.png"))
            with open(os.path.join(tmpdirname, "tmpimage.png"), 'rb') as timage:
                picture = discord.File(timage)
                await ctx.send(file=picture)


def setup(bot):
    bot.add_cog(TestPlayground(bot))
