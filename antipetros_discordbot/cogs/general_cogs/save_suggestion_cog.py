
__updated__ = '2020-12-02 02:15:12'

# region [Imports]

# * Standard Library Imports -->
import os
import re
import sqlite3 as sqlite
import unicodedata
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
# * Third Party Imports -->
import discord
from discord.ext import commands
from async_property import async_property

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.utility.named_tuples import SUGGESTION_DATA_ITEM
from antipetros_discordbot.utility.sqldata_storager import SuggestionDataStorageSQLite
from antipetros_discordbot.utility.gidtools_functions import loadjson, writejson, pathmaker
from antipetros_discordbot.data.config.config_singleton import COGS_CONFIG

# endregion[Imports]

# region [Logging]

log = glog.aux_logger(__name__)
log.debug(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# location of this file, does not work if app gets compiled to exe with pyinstaller
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


# endregion [Constants]

# region [TODO]


# TODO: create get_my_data and remove_my_suggestion and delete_all_my_data method for the user

# TODO: create report generator in different formats, at least json and Html, probably also as embeds and Markdown

# endregion[TODO]

class SaveSuggestion(commands.Cog):
    suggestion_name_regex = re.compile(r"(?P<name>(?<=#).*)")
    config_name = 'save_suggestions'
    executor = ThreadPoolExecutor(3)
# region [Init]

    def __init__(self, bot):
        self.bot = bot
        self.data_storage_handler = SuggestionDataStorageSQLite()
        log.debug(glog.class_initiated(self))

# endregion [Init]

# region [Setup]


# endregion [Setup]

# region [Properties]


    @property
    def command_emojis(self):
        if self.bot.is_debug:
            COGS_CONFIG.read()
        return {'save': COGS_CONFIG.get(self.config_name, 'save_emoji'),
                'upvote': COGS_CONFIG.get(self.config_name, 'upvote_emoji'),
                'downvote': COGS_CONFIG.get(self.config_name, 'downvote_emoji')}

    @property
    def categories(self):
        _out = self.data_storage_handler.category_emojis
        if self.bot.is_debug:
            log.debug(_out)
        return _out

    @property
    def allowed_channels(self):
        if self.bot.is_debug:
            COGS_CONFIG.read()
        return set(COGS_CONFIG.getlist(self.config_name, 'allowed_channels'))

    @property
    def messages_to_watch(self):
        return self.data_storage_handler.get_all_non_discussed_message_ids()

    @property
    def saved_messages(self):
        return self.data_storage_handler.get_all_message_ids()

    @property
    def loop(self):
        return asyncio.get_running_loop()

# endregion [Properties]

# region [Listener]

    @commands.Cog.listener(name='on_ready')
    async def extra_cog_setup(self):
        log.info(f"{self} Cog ----> nothing to set up")

    async def new_suggestion(self, channel, message, guild_id, reaction_user):
        if message.id in self.saved_messages:
            await channel.send(embed=await self.make_already_saved_embed())
            return

        message_member = await self.bot.retrieve_member(guild_id, message.author.id)
        reaction_member = await self.bot.retrieve_member(guild_id, reaction_user.id)
        now_time = datetime.utcnow()
        name = await self.collect_title(message.content)
        extra_data = (message.attachments[0].filename, await message.attachments[0].read()) if len(message.attachments) != 0 else None

        suggestion_item = SUGGESTION_DATA_ITEM(name, message_member, reaction_member, message, now_time)

        was_saved, suggestion_item = await self.add_suggestion(suggestion_item, extra_data)
        log.info("saved new suggestion, suggestion name: '%s', suggestion author: '%s', saved by: '%s', suggestion has extra data: '%s'",
                 name,
                 message_member.name,
                 reaction_member.name,
                 'yes' if extra_data is not None else 'no')

        if was_saved is True:
            await channel.send(embed=await self.make_add_success_embed(suggestion_item))

    async def change_category(self, channel, message, emoji_name):
        category = self.categories.get(emoji_name)
        if category:
            success = await self.set_category(category, message.id)
            if success:
                await channel.send(embed=await self.make_changed_category_embed(message, category))
                log.info("updated category for suggestion (id: %s) to category '%s'", message.id, category)
                for reaction_emoji in self.categories:
                    if reaction_emoji is not None and reaction_emoji != emoji_name:
                        other_reaction = await self.specifc_reaction_from_message(message, reaction_emoji)
                        if other_reaction is not None:
                            await other_reaction.clear()

    async def change_votes(self, message, emoji_name):
        reaction = await self.specifc_reaction_from_message(message, emoji_name)
        _count = reaction.count
        self.data_storage_handler.update_votes(emoji_name, _count, message.id)
        log.info("updated votecount for suggestion (id: %s) for type: '%s' to count: %s", message.id, emoji_name, _count)

    @ commands.Cog.listener()
    @ commands.has_any_role(*COGS_CONFIG.getlist('save_suggestions', 'allowed_roles'))
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        if channel.name not in self.allowed_channels:
            return
        reaction_user = await self.bot.fetch_user(payload.user_id)
        if reaction_user.bot is True or reaction_user.id in self.bot.blacklist_user:
            return
        message = await channel.fetch_message(payload.message_id)
        emoji_name = unicodedata.name(payload.emoji.name)

        if emoji_name == self.command_emojis['save']:
            await self.new_suggestion(channel, message, payload.guild_id, reaction_user)

        elif emoji_name in self.categories and message.id in self.saved_messages:
            await self.change_category(channel, message, emoji_name)

        elif emoji_name in [self.command_emojis['upvote'], self.command_emojis['downvote']] and message.id in self.saved_messages:
            await self.change_votes(message, emoji_name)


# endregion [Listener]

# region [Commands]


    @ commands.command()
    @ commands.has_any_role(*COGS_CONFIG.getlist('save_suggestions', 'allowed_roles'))
    async def clear_all_suggestions(self, ctx, sure=False):
        if ctx.channel.name not in self.allowed_channels:
            return
        if sure is False:
            await ctx.send("Do you really want to delete all saved suggestions?\n\nANSWER **YES** in the next __30 SECONDS__")
            user = ctx.author
            channel = ctx.channel

            def check(m):
                return m.author.name == user.name and m.channel.name == channel.name
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                await self._clear_suggestions(ctx, msg.content)
            except asyncio.TimeoutError:
                await ctx.send('No answer received, canceling request to delete Database, nothing was deleted')
        else:
            await self._clear_suggestions(ctx, 'yes')

    @ commands.command()
    @ commands.has_any_role(*COGS_CONFIG.getlist('save_suggestions', 'allowed_roles'))
    async def retrieve_all(self, ctx):
        _txt = ''
        x = loadjson(self.save_file)
        if x != {}:
            for key, value in x.items():
                _txt += '**' + key + '**\n'
                for _time, _msg in value:
                    _txt += '- ' + _time + ' ----> ' + _msg + '\n\n'
                _txt += '-----------\n\n'
        else:
            _txt = 'no saved entries found'
        await ctx.send(_txt)

    @ commands.command()
    @ commands.has_any_role(*COGS_CONFIG.getlist('save_suggestions', 'allowed_roles'))
    async def request_my_data(self, ctx):
        user = ctx.author
        _json = loadjson(self.save_file)
        _data = _json.get(str(user), None)
        if _data is None:
            await user.send('we have nothing saved from you')
        else:
            _out = ''
            for time, _save_content in _data:
                _out += f'**At {time} we saved this message from you:**\n```{_save_content}```\n\n'
            await user.send(_out)

# endregion [Commands]

# region [DataStorage]

    async def add_suggestion(self, suggestion_item: SUGGESTION_DATA_ITEM, extra_data=None):
        if extra_data is not None:
            _path = pathmaker(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\antipetros_discordbot\data\data_storage\images\suggestion_extra_data", extra_data[0])
            with open(_path, 'wb') as extra_data_file:
                extra_data_file.write(extra_data[1])
            suggestion_item = suggestion_item._replace(extra_data=(extra_data[0], _path))
        try:
            self.data_storage_handler.add_suggestion(suggestion_item)
            return True, suggestion_item
        except sqlite.Error as error:
            log.error(error)
            return False, suggestion_item

    async def set_category(self, category, message_id):
        try:
            self.data_storage_handler.update_category(category, message_id)
            return True
        except sqlite.Error as error:
            log.error(error)
            return False

    async def _clear_suggestions(self, ctx, answer):
        if answer.casefold() == 'yes':
            await ctx.send('deleting Database')
            await self.loop.run_in_executor(self.executor, self.data_storage_handler.clear)
            await ctx.send('Database was cleared, ready for input again')

        elif answer.casefold() == 'no':
            await ctx.send('canceling request to delete Database, nothing was deleted')


# endregion [DataStorage]

# region [Embeds]


    async def make_add_success_embed(self, suggestion_item: SUGGESTION_DATA_ITEM):
        _filtered_content = []
        if suggestion_item.name is not None:
            for line in suggestion_item.message.content.splitlines():
                if suggestion_item.name.casefold() not in line.casefold():
                    _filtered_content.append(line)
            _filtered_content = '\n'.join(_filtered_content)
        else:
            _filtered_content = suggestion_item.message.content
        _filtered_content = f"```\n{_filtered_content.strip()}\n```"

        embed = discord.Embed(title="**Suggestion was Saved!**", description="Your suggestion was saved for the Dev Team.\n\n", color=0xf2ea48)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Media-floppy.svg/2000px-Media-floppy.svg.png")
        embed.add_field(name="Title:", value=f"__{suggestion_item.name}__", inline=False)
        if COGS_CONFIG.getboolean(self.config_name, 'add_success_embed_verbose') is True:
            embed.add_field(name="Author:", value=f"*{suggestion_item.message_author.name}*", inline=True)
            embed.add_field(name="Content:", value=_filtered_content, inline=True)
            embed.add_field(name='Saved Timestamp:', value=suggestion_item.time.isoformat(timespec='seconds'), inline=False)

        extra_data_value = ['No attachments detected'] if suggestion_item.extra_data is None else suggestion_item.extra_data[0]
        embed.add_field(name='Attachments', value=f"`{extra_data_value}`")

        return embed

    async def make_changed_category_embed(self, message, category):
        embed = discord.Embed(title="**Updated Suggestion Category**", description="I updated the category an Suggestion\n\n", color=0xf2a44a)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Update-manager-icon.svg/500px-Update-manager-icon.svg.png")
        embed.add_field(name="New Category:", value=category, inline=False)
        embed.add_field(name="Suggestion:", value=message.jump_url, inline=False)
        return embed

    async def make_already_saved_embed(self):
        embed = discord.Embed(title="**This Suggestion was already saved!**", description="I did not save the Suggestion as I have it already saved", color=0xe04d7e)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Dialog-error.svg/2000px-Dialog-error.svg.png")
        return embed


# endregion [Embeds]

# region [Helper]

    async def collect_title(self, content):
        name_result = self.suggestion_name_regex.search(content)
        if name_result:
            name = name_result.group('name')
            name = None if len(name) > 100 else name.strip().title()
        else:
            name = None
        return name

    async def specifc_reaction_from_message(self, message, target_reaction):
        for reaction in message.reactions:
            if unicodedata.name(reaction.emoji) == target_reaction:
                return reaction


# endregion [Helper]

# region [DunderMethods]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.user.name})"

    def __str__(self):
        return self.__class__.__name__

# endregion [DunderMethods]


def setup(bot):
    bot.add_cog(SaveSuggestion(bot))
