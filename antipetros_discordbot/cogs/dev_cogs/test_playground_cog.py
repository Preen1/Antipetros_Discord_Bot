# * Standard Library Imports -->
import os
import asyncio
import platform
import subprocess
from io import BytesIO, StringIO
from datetime import datetime
from tempfile import TemporaryDirectory
from functools import partial
from pprint import pformat
# * Third Party Imports -->
import discord
from PIL import Image, ImageDraw, ImageFont
from pytz import timezone
from pyfiglet import Figlet
from fuzzywuzzy import fuzz, process as fuzzprocess
from discord.ext import commands
from googletrans import LANGUAGES, Translator
from discord.ext.commands import Greedy
from antistasi_template_checker.engine.antistasi_template_parser import run as template_checker_run
from discord.utils import parse_time
# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.cogs import get_aliases
from antipetros_discordbot.utility.misc import save_commands, datetime_isoformat_to_discord_format
from antipetros_discordbot.utility.checks import has_attachments, in_allowed_channels, allowed_channel_and_allowed_role, log_invoker
from antipetros_discordbot.utility.converters import FlagArg, DateOnlyConverter
from antipetros_discordbot.utility.gidtools_functions import loadjson, pathmaker
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.discord_markdown_helper.the_dragon import THE_DRAGON
from antipetros_discordbot.utility.discord_markdown_helper.special_characters import ZERO_WIDTH

# region [Logging]

log = glog.aux_logger(__name__)
glog.import_notification(log, __name__)

# endregion[Logging]


APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

HELP_TEST_DATA = loadjson(APPDATA["command_help.json"])
CONFIG_NAME = "test_playground"

FAQ_THING = """**FAQ No 17**
_How to become a server member?_
_Read the channel description on teamspeak or below_

_**Becoming a member:**_
```
Joining our ranks is simple: play with us and participate in this community! If the members like you you may be granted trial membership by an admin upon recommendation.

Your contribution and participation to this community will determine how long the trial period will be, and whether or not it results in full membership. As a trial member, you will receive in-game membership and a [trial] tag on these forums which assures you an invite to all events including official member meetings. Do note that only full members are entitled to vote on issues at meetings.
```"""


class TestPlaygroundCog(commands.Cog, command_attrs={'hidden': True, "name": "TestPlayground"}):
    config_name = "test_playground"
    language_dict = {value: key for key, value in LANGUAGES.items()}

    def __init__(self, bot):
        self.bot = bot
        self.support = self.bot.support
        self.allowed_channels = set(COGS_CONFIG.getlist('test_playground', 'allowed_channels'))
        self.translator = Translator()
        if os.environ.get('INFO_RUN', '') == "1":
            save_commands(self)
        glog.class_init_notification(log, self)

    @commands.command(aliases=get_aliases("make_figlet"))
    @ commands.has_any_role(*COGS_CONFIG.getlist("test_playground", 'allowed_roles'))
    @in_allowed_channels(set(COGS_CONFIG.getlist("test_playground", 'allowed_channels')))
    async def make_figlet(self, ctx, *, text: str):

        figlet = Figlet(font='gothic', width=300)
        new_text = figlet.renderText(text.upper())
        await ctx.send(f"```fix\n{new_text}\n```")

    async def get_text_dimensions(self, text_string, font_name, image_size):
        # https://stackoverflow.com/a/46220683/9263761
        font_size = 500
        buffer = 50
        image_width, image_height = image_size
        image_width = image_width - (buffer * 2)
        image_height = image_height - (buffer * 2)

        text_width = 99999999999
        text_height = 9999999999
        while text_width > image_width or text_height > image_height:
            font = ImageFont.truetype(font_name, font_size)
            ascent, descent = font.getmetrics()

            text_width = font.getmask(text_string).getbbox()[2]
            text_height = font.getmask(text_string).getbbox()[3] + descent
            font_size -= 1
        return font, text_width, text_height, font_size

    async def get_smalle_text_dimensions(self, text_string, font):
        # https://stackoverflow.com/a/46220683/9263761
        ascent, descent = font.getmetrics()

        text_width = font.getmask(text_string).getbbox()[2]
        text_height = font.getmask(text_string).getbbox()[3] + descent

        return (text_width, text_height)

    async def get_font_path(self, font_name):
        _font_dict = {}
        font_folder = pathmaker() if platform.system() == 'Windows' else None
        if font_folder is None:
            raise FileNotFoundError("could not locate font folder")
        for file in os.scandir(font_folder):
            if file.is_file() and file.name.endswith('.ttf'):
                _font_dict[os.path.splitext(file.name)[0].casefold()] = pathmaker(file.path)
        if font_name.casefold() in _font_dict:
            return _font_dict.get(font_name.casefold())
        new_font_name = fuzzprocess.extractOne(font_name.casefold(), _font_dict.keys())
        return _font_dict.get(new_font_name)

    @commands.command(aliases=get_aliases("text_to_image"))
    @ commands.has_any_role(*COGS_CONFIG.getlist("test_playground", 'allowed_roles'))
    @in_allowed_channels(set(COGS_CONFIG.getlist("test_playground", 'allowed_channels')))
    async def text_to_image(self, ctx, *, text: str):
        font_path = APPDATA['stencilla.ttf']
        image_path = APPDATA['armaimage.png']

        image = Image.open(APPDATA['armaimage.png'])
        font, text_width, text_height, font_size = await self.get_text_dimensions(text, font_path, image.size)
        second_font = ImageFont.truetype(font_path, size=font_size - (font_size // 35))
        second_width, second_height = await self.get_smalle_text_dimensions(text, second_font)
        draw_interface = ImageDraw.Draw(image, mode='RGBA')
        draw_interface.text((((image.size[0] - text_width) // 2), 50), text, fill=(1, 1, 1), font=font)
        draw_interface.text((((image.size[0] - second_width) // 2), 50 + 10), text, fill=(255, 226, 0), font=second_font, stroke_fill=(0, 176, 172), stroke_width=(font_size // 50))
        await self._send_image(ctx, image, 'test', 'TEST', 'PNG')

    async def _send_image(self, ctx, image, name, message_title, image_format=None, delete_after=None):
        image_format = 'png' if image_format is None else image_format
        with BytesIO() as image_binary:
            image.save(image_binary, image_format.upper(), optimize=True)
            image_binary.seek(0)
            out_file = discord.File(image_binary, filename=name + '.' + image_format)
            embed = discord.Embed(title=message_title)
            embed.set_image(url=f"attachment://{name.replace('_','')}.{image_format}")
            await ctx.send(embed=embed, file=out_file, delete_after=delete_after)

    @commands.command(aliases=get_aliases("check_date_converter"))
    @ commands.has_any_role(*COGS_CONFIG.getlist("test_playground", 'allowed_roles'))
    @in_allowed_channels(set(COGS_CONFIG.getlist("test_playground", 'allowed_channels')))
    async def check_date_converter(self, ctx, in_date: DateOnlyConverter):
        year = in_date.year
        month = in_date.month
        day = in_date.day
        hour = in_date.hour
        minute = in_date.minute
        second = in_date.second

        await ctx.send(f"__year:__ {year} | __month:__ {month} | __day:__ {day} || __hour:__ {hour} | __minute:__ {minute} | __second:__ {second}")

    async def correct_template(self, template_content, item_data):
        new_content = template_content
        for item in item_data:
            if item.has_error is True and item.is_case_error is True:
                new_content = new_content.replace(f'"{item.item}"', f'"{item.correction}"')
        return new_content

    @commands.command(aliases=get_aliases("check_template"))
    @ allowed_channel_and_allowed_role(CONFIG_NAME, True, allowed_in_dm_key='check_template_allowed_in_dm')
    @has_attachments(1)
    async def check_template(self, ctx, all_items_file=True, case_insensitive: bool = False):
        attachment = ctx.message.attachments[0]
        if attachment.filename.endswith('.sqf'):

            await ctx.send(await self.bot.get_antistasi_emoji("Salute"))

            async with ctx.typing():
                await asyncio.sleep(2)
                attachment_data = await attachment.read()
                attachment_data = attachment_data.decode('utf-8', errors='ignore')
                found_data = await self.bot.execute_in_thread(template_checker_run, attachment_data, case_insensitive)
                found_data_amount_errors = found_data.get('found_errors')
                found_data = found_data.get('items')
                description = "**__NO__** errors in this Template File"
                if found_data_amount_errors > 0:
                    if found_data_amount_errors > 1:
                        description = f"{found_data_amount_errors} errors in this file"
                    else:
                        description = f"{found_data_amount_errors} error in this file"

                embed = discord.Embed(title=f"Template Check: {attachment.filename}", description=description,
                                      color=self.support.color('OLIVE_DRAB_0x7'.casefold()).discord_color, timestamp=datetime.now(tz=timezone("Europe/Berlin")))
                embed.set_thumbnail(url="https://s3.amazonaws.com/files.enjin.com/1218665/site_logo/NEW%20LOGO%20BANNER.png")

                if found_data_amount_errors != 0:
                    embed.add_field(name="Corrected file", value="I have attached the corrected file", inline=False)
                    embed.add_field(name="Case Errors", value=f"\n{ZERO_WIDTH}I only corrected case errors", inline=False)
                    embed.add_field(name="Not corrected was:\n" + ZERO_WIDTH,
                                    value='\n'.join([error_item.item for error_item in found_data if error_item.has_error is True and (error_item.is_case_error is False or error_item.correction == "FILEPATH")]) + '\n' + ZERO_WIDTH, inline=False)
                    code_message = [f"{'#'*34}\n{'#'*10} FOUND ERRORS {'#'*10}\n{'#'*34}\n"]

                    sep_one = max(map(len, [item.item for item in found_data if item.has_error is True])) + 3
                    for index, error_item in enumerate(found_data):
                        if error_item.has_error:
                            case_error = 'Yes' if error_item.is_case_error is True else 'No'
                            possible_correction = '' if error_item.correction is None else f'| possible correction =      "{error_item.correction}"'
                            has_error = f' | error =    Yes   | is case error = {case_error}{" "*(6-len(case_error))} {possible_correction}'
                            start_sign = '++ '
                            code_message.append(start_sign + f'item =        "{error_item.item}"{" " * (sep_one - len(error_item.item))} | line number =    {str(error_item.line_number)} {" " * (6 - len(str(error_item.line_number)))} {has_error}\n')

                    await self.bot.split_to_messages(ctx, message='\n'.join(code_message + ['\n' + ZERO_WIDTH]), in_codeblock=True, syntax_highlighting='ml')

                    await asyncio.sleep(1)
                    new_content = await self.correct_template(attachment_data, found_data)
                    new_file_name = attachment.filename.replace('.sqf', '_CORRECTED.sqf')
                    with StringIO() as io_fp:
                        io_fp.write(new_content)
                        io_fp.seek(0)
                        _file = discord.File(io_fp, new_file_name)

                        await ctx.send(file=_file)
                else:
                    await ctx.reply(file=discord.File(APPDATA["Congratulations.mp3"], spoiler=True))
                await ctx.send(embed=embed)
                await asyncio.sleep(1)
                if all_items_file is True:
                    with StringIO() as io_fp:
                        io_fp.write(f"ALL ITEMS FROM FILE '{attachment.filename}'")
                        sorted_found_data = sorted(found_data, key=lambda x: (1 if x.has_error else 99, x.line_number))
                        for item in found_data:

                            case_error = 'yes' if item.is_case_error is True else 'no'
                            possible_correction = '' if item.correction is None else f'| possible correction: "{item.correction}"'
                            has_error = f' | error: yes | is case error: {case_error}{" "*(5-len(case_error))} {possible_correction}'

                            io_fp.write(
                                f'item: "{item.item}"{" "*(50-len(item.item))} | line number: {str(item.line_number)}{" "*(5-len(str(item.line_number)))} {has_error}\n')
                        io_fp.seek(0)
                        _all_item_file = discord.File(io_fp, attachment.filename.replace('.sqf', '_ALL_ITEMS.sqf'))

                        await ctx.send(file=_all_item_file)
                        await asyncio.sleep(5)

    @ commands.command(aliases=get_aliases("the_dragon"))
    @ allowed_channel_and_allowed_role("test_playground")
    async def the_dragon(self, ctx):
        await ctx.send(THE_DRAGON)

    @ commands.command(aliases=get_aliases("random_embed_color"))
    @ allowed_channel_and_allowed_role("test_playground")
    async def random_embed_color(self, ctx):
        color = self.bot.support.random_color
        embed = discord.Embed(title='test', description=color.name, color=color.int)
        await ctx.send(embed=embed)

    @ commands.command(aliases=get_aliases("send_all_colors_file"))
    @ allowed_channel_and_allowed_role("test_playground")
    async def send_all_colors_file(self, ctx):
        _file = discord.File(str(self.bot.support.all_colors_json_file), os.path.basename(str(self.bot.support.all_colors_json_file)))
        await ctx.send('here', file=_file)

    @ commands.command(aliases=get_aliases("check_flags"))
    @ allowed_channel_and_allowed_role("test_playground")
    async def check_flags(self, ctx, flags: Greedy[FlagArg(['make_embed', 'random_color'])], ending: str):
        print(flags)
        if 'make_embed' in flags:
            color = discord.Embed.Empty
            if 'random_color' in flags:
                color = self.bot.support.random_color.int
            embed = discord.Embed(title='check flags', description=ending, color=color)
            await ctx.send(embed=embed)
        else:
            await ctx.send(ending)

    @ commands.command(aliases=get_aliases("test_dyn_time"))
    @ allowed_channel_and_allowed_role("test_playground")
    async def test_dyn_time(self, ctx):
        embed = discord.Embed(title='testing dynamic timestamp', description='Could you please post under this message the time you see as timestamp of this Embed? (just copy paste)', timestamp=datetime.now(tz=timezone('Europe/Vienna')))
        await ctx.send(embed=embed)

    async def find_all_template_files(self, channel):
        async for message in channel.history(limit=None):
            if len(message.attachments) >= 1:
                attachment = message.attachments[0]
                if attachment.filename.endswith('.sqf'):
                    yield message

    @ commands.command(aliases=get_aliases("get_all_template_messages"))
    @ allowed_channel_and_allowed_role("test_playground")
    async def get_all_template_messages(self, ctx):

        channel = await self.bot.fetch_channel(785935400467824651)
        async for message in self.find_all_template_files(channel):
            await self.check_template_iter_file(ctx, message.attachments[0])
            await asyncio.sleep(5)

    async def check_template_iter_file(self, ctx, file, case_insensitive: bool = False):
        _file = file
        with ctx.typing():
            with TemporaryDirectory() as tempdir:
                tempfile_path = pathmaker(tempdir, _file.filename)
                await _file.save(tempfile_path)
                case = '--case-insensitive' if case_insensitive is True else '--case-sensitive'
                func = partial(subprocess.run, [APPDATA["antistasi_template_checker.exe"], 'from_file', '-np', case, tempfile_path], check=True, capture_output=True)
                cmd = await self.bot.execute_in_thread(func)
                _output = cmd.stdout.decode('utf-8', errors='replace')
                # await self.bot.split_to_messages(ctx, _output, in_codeblock=True)
                new_file_name = _file.filename.replace(os.path.splitext(_file.filename)[-1], '_CORRECTED' + os.path.splitext(_file.filename)[-1])
                new_file_path = pathmaker(tempdir, new_file_name)
                if os.path.isfile(new_file_path):
                    _new_file = discord.File(new_file_path, new_file_name)
                    await ctx.send('The Corrected File', file=_new_file)

    async def _translate(self, text, out_language, in_language=None):
        in_lang_code = self.language_dict.get(in_language.casefold()) if in_language is not None else 'auto'
        out_lang_code = self.language_dict.get(out_language.casefold())

        x = self.translator.translate(text=text, dest=out_lang_code, src=in_lang_code)
        return x.text

    @ commands.command(hidden=False, aliases=get_aliases("translate"))
    @ commands.has_any_role(*COGS_CONFIG.getlist('test_playground', 'allowed_roles'))
    @ in_allowed_channels(set(COGS_CONFIG.getlist("test_playground", 'allowed_channels')))
    async def translate(self, ctx, out_lang, *, text):
        log.info("command was initiated by '%s'", ctx.author.name)
        if out_lang.casefold() not in self.language_dict:
            await ctx.send('unknown language')
            return
        result = await self._translate(text, out_lang)
        await self.bot.split_to_messages(ctx, result)

    @commands.command(aliases=get_aliases('search_usernames'))
    @allowed_channel_and_allowed_role(CONFIG_NAME, in_dm_allowed=True, allowed_roles_key='roles_restricted_command', allowed_in_dm_key="search_usernames_dm_allowed")
    @log_invoker(log, 'critical')
    async def search_usernames(self, ctx, *, names: str):
        full_match = {}
        partial_match = {}
        similar_match = {}
        to_match_names = names.split(',')
        to_match_names = set(map(lambda x: x.strip().casefold(), to_match_names))
        user_list = self.bot.users
        for user in user_list:
            for name in to_match_names:
                if name not in full_match:
                    full_match[name] = []
                if name not in partial_match:
                    partial_match[name] = []
                if name == user.name.casefold():
                    full_match[name].append(user.name)
                elif name in user.name.casefold():
                    partial_match[name].append(user.name)
        # for match_name in to_match_names:
        #     fuzz_result = fuzzprocess.extract(match_name, [user.name for user in user_list])
        #     if fuzz_result:
        #         similar_match[match_name] = fuzz_result
        await ctx.reply("__**Full Matches**__")
        await self.bot.split_to_messages(ctx, pformat(full_match).replace('{', '').replace('}', ''))
        await ctx.reply("__**Partial Matches**__")
        await self.bot.split_to_messages(ctx, pformat(partial_match).replace('{', '').replace('}', ''))
        await ctx.reply("__**all user I can see**__")
        await self.bot.split_to_messages(ctx, '\n'.join([user.name for user in user_list]), in_codeblock=True)

    @commands.command()
    @allowed_channel_and_allowed_role(CONFIG_NAME)
    @log_invoker(log, 'debug')
    async def embed_experiment(self, ctx):

        await ctx.send(**await self.bot.make_generic_embed(author='bot_author', footer=))

# region [SpecialMethods]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.user.name})"

    def __str__(self):
        return self.qualified_name

# endregion [SpecialMethods]


def setup(bot):
    bot.add_cog(TestPlaygroundCog(bot))
