"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import traceback
from datetime import datetime

# * Third Party Imports --------------------------------------------------------------------------------->
from discord import Embed, ChannelType
from fuzzywuzzy import fuzz
from fuzzywuzzy import process as fuzzprocess
from discord.ext import commands

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.utility.misc import async_split_camel_case_string
from antipetros_discordbot.utility.exceptions import MissingAttachmentError
from antipetros_discordbot.utility.gidtools_functions import loadjson
from antipetros_discordbot.abstracts.subsupport_abstract import SubSupportBase
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.discord_markdown_helper.special_characters import ZERO_WIDTH
from typing import TYPE_CHECKING

# endregion[Imports]

# region [TODO]

# TODO: rebuild whole error handling system
# TODO: make it so that creating the embed also sends it, with more optional args

# endregion [TODO]

# region [AppUserData]


# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)


# endregion[Logging]

# region [Constants]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
EMBED_SYMBOLS = loadjson(APPDATA["embed_symbols.json"])
# endregion[Constants]


class ErrorHandler(SubSupportBase):

    def __init__(self, bot, support):
        self.bot = bot
        self.support = support
        self.loop = self.bot.loop
        self.is_debug = self.bot.is_debug
        self.error_handle_table = {commands.MaxConcurrencyReached: self._handle_max_concurrency,
                                   commands.CommandOnCooldown: self._handle_command_on_cooldown,
                                   commands.errors.BadArgument: self._handle_bad_argument,
                                   MissingAttachmentError: self._handle_missing_attachment,
                                   commands.CheckFailure: self._handle_check_failure}
        self.default_delete_after_seconds = 120
        glog.class_init_notification(log, self)

    async def handle_errors(self, ctx, error):
        error_traceback = '\n'.join(traceback.format_exception(error, value=error, tb=None))
        await self.error_handle_table.get(type(error), self._default_handle_error)(ctx, error, error_traceback)
        if ctx.channel.type is ChannelType.text:
            await ctx.message.delete()
            log.error("Error '%s' was caused by '%s' on the command '%s' with args '%s' and traceback '%s'", error.__class__.__name__, ctx.author.name, ctx.command.name, ctx.args, error_traceback)

    async def _default_handle_error(self, ctx, error, error_traceback):
        log.error('Ignoring exception in command {}:'.format(ctx.command))
        log.exception(error, exc_info=True, stack_info=False)
        if ctx.channel.type is ChannelType.text:
            await self.bot.message_creator(embed=await self.error_reply_embed(ctx, error, 'Error With No Special Handling Occured', msg=str(error), error_traceback=error_traceback))

    async def _handle_check_failure(self, ctx, error, error_traceback):
        if self.bot.is_blacklisted(ctx.author) is False:
            await ctx.channel.send(delete_after=self.default_delete_after_seconds, embed=await self.error_reply_embed(ctx,
                                                                                                                      error,
                                                                                                                      'Missing Permission',
                                                                                                                      f'{ctx.author.mention}\n{ZERO_WIDTH}\n **You dont_have Permission to call this Command**\n{ZERO_WIDTH}'))

    async def _handle_missing_attachment(self, ctx, error, error_traceback):
        await ctx.channel.send(delete_after=self.default_delete_after_seconds, embed=await self.error_reply_embed(ctx,
                                                                                                                  error,
                                                                                                                  'Missing Attachments',
                                                                                                                  f'{ctx.author.mention}\n{ZERO_WIDTH}\n **{str(error)}**\n{ZERO_WIDTH}'))

    async def _handle_bad_argument(self, ctx, error, error_traceback):
        await ctx.channel.send(delete_after=self.default_delete_after_seconds, embed=await self.error_reply_embed(ctx,
                                                                                                                  error,
                                                                                                                  'Wrong Argument',
                                                                                                                  f'{ctx.author.mention}\n{ZERO_WIDTH}\n **You tried to invoke `{ctx.command.name}` with an wrong argument**\n{ZERO_WIDTH}\n```shell\n{ctx.command.name} {ctx.command.signature}\n```',
                                                                                                                  error_traceback=None))

    async def _handle_command_on_cooldown(self, ctx, error, error_traceback):
        await ctx.channel.send(embed=await self.error_reply_embed(ctx, error, 'STOP SPAMMING!', f'{ctx.author.mention}\n{ZERO_WIDTH}\n **Your mother was a hamster and your father smelt of elderberries!**', error_traceback=error_traceback), delete_after=self.default_delete_after_seconds)
        await ctx.message.delete()
        await ctx.send(embed=await self.error_message_embed(ctx, error))
        log.error("Error '%s' was caused by '%s' on the command '%s' with args '%s'", error.__class__.__name__, ctx.author.name, ctx.command.name, ctx.args)

    async def _handle_max_concurrency(self, ctx, error, error_traceback):
        await ctx.channel.send(embed=await self.error_reply_embed(ctx, error, 'STOP SPAMMING!', f'{ctx.author.mention}\n{ZERO_WIDTH}\n **Your mother was a hamster and your father smelt of elderberries!**', error_traceback=error_traceback), delete_after=self.default_delete_after_seconds)
        await ctx.message.delete()

        log.error("Error '%s' was caused by '%s' on the command '%s' with args '%s'", error.__class__.__name__, ctx.author.name, ctx.command.name, ctx.args)

    async def error_reply_embed(self, ctx, error, title, msg, error_traceback=None):
        embed = Embed(title=title, description=f"{ZERO_WIDTH}\n{msg}\n{ZERO_WIDTH}", color=self.support.color('red').int, timestamp=datetime.utcnow())
        embed.set_thumbnail(url=EMBED_SYMBOLS.get('warning'))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        if error_traceback is not None:
            embed.add_field(name='Traceback', value=str(error_traceback)[0:500])
        if ctx.command is not None:
            embed.set_footer(text=f"Command: `{ctx.command.name}`\n{ZERO_WIDTH}\n By User: `{ctx.author.name}`\n{ZERO_WIDTH}\n Error: `{await async_split_camel_case_string(error.__class__.__name__)}`\n{ZERO_WIDTH}\n{ZERO_WIDTH}")
        else:
            embed.set_footer(text=f"text: {ctx.message.content}\n{ZERO_WIDTH}\n By User: `{ctx.author.name}`\n{ZERO_WIDTH}\n Error: `{await async_split_camel_case_string(error.__class__.__name__)}`\n{ZERO_WIDTH}\n{ZERO_WIDTH}")

        return embed

    async def error_message_embed(self, ctx, error, msg=ZERO_WIDTH):
        embed = Embed(title='ERROR', color=self.support.color('orange').int, timestamp=datetime.utcnow(), description=ZERO_WIDTH + '\n' + msg + '\n' + ZERO_WIDTH)
        embed.set_thumbnail(url=EMBED_SYMBOLS.get('warning'))
        try:
            embed.add_field(name=await async_split_camel_case_string(error.__class__.__name__), value=f"error occured with command: {ctx.command.name} and arguments: {str(ctx.args)}")
        except AttributeError:
            embed.add_field(name=await async_split_camel_case_string(error.__class__.__name__), value="command not found\n" + ZERO_WIDTH + '\n', inline=False)
            corrections = fuzzprocess.extract(ctx.message.content.split(' ')[1], [command.name for command in self.bot.commands], scorer=fuzz.token_set_ratio, limit=3)
            if corrections is not None:
                embed.add_field(name='did you mean:', value=ZERO_WIDTH + '\n' + f'\n{ZERO_WIDTH}\n'.join(correction[0] for correction in corrections), inline=False)
            embed.set_footer(text=f'to get a list of all commands use:\n@AntiPetros {self.bot.help_invocation}\n{ZERO_WIDTH}\n{ZERO_WIDTH}')

        return embed

    async def if_ready(self):
        log.debug("'%s' sub_support is READY", str(self))

    async def update(self):
        log.debug("'%s' sub_support was UPDATED", str(self))

    def retire(self):
        log.debug("'%s' sub_support was RETIRED", str(self))


def get_class():
    return ErrorHandler
# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
