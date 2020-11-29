
__updated__ = '2020-11-29 03:38:55'

# region [Imports]

# * Standard Library Imports -->
import os
import re
import sqlite3 as sqlite
import unicodedata
from datetime import datetime

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

# TODO: make it so that changing an suggestion category removes all other category emojis

# TODO: create get_my_data and remove_my_suggestion and delete_all_my_data method for the user

# TODO: create report generator in different formats, at least json and Html, probably also as embeds and Markdown

# endregion[TODO]

class SaveSuggestion(commands.Cog):
    suggestion_name_regex = re.compile(r"(?P<name>(?<=#).*)")
    config_name = 'save_suggestions'
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
        return {'save': COGS_CONFIG.get(self.config_name, 'save_emoji'),
                'upvote': COGS_CONFIG.get(self.config_name, 'upvote_emoji'),
                'downvote': COGS_CONFIG.get(self.config_name, 'downvote_emoji')}

    @property
    def categories(self):
        return self.data_storage_handler.category_emojis

    @property
    def allowed_channels(self):
        return set(COGS_CONFIG.getlist(self.config_name, 'allowed_channels'))

    @property
    def messages_to_watch(self):
        return self.data_storage_handler.get_all_non_discussed_message_ids()

    @property
    def saved_messages(self):
        return self.data_storage_handler.get_all_message_ids()

# endregion [Properties]

# region [Listener]

    @commands.Cog.listener(name='on_ready')
    async def extra_cog_setup(self):
        log.info(f"{self} Cog ----> nothing to set up")

    @commands.Cog.listener()
    @commands.has_any_role(*COGS_CONFIG.getlist('save_suggestions', 'allowed_roles'))
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        if channel.name not in self.allowed_channels:
            return

        reaction_user = await self.bot.fetch_user(payload.user_id)
        if reaction_user.bot is True or reaction_user.id in self.bot.blacklist_user:
            return
        guild = self.bot.get_guild(payload.guild_id)
        reaction_member = await guild.fetch_member(reaction_user.id)

        message = await channel.fetch_message(payload.message_id)
        message_author = message.author
        message_member = await guild.fetch_member(message_author.id)
        attachments = message.attachments
        now_time = datetime.utcnow()

        if unicodedata.name(payload.emoji.name) == self.command_emojis['save']:
            if message.id in self.saved_messages:
                await channel.send("Suggestion was already saved!")
                return
            name = await self.collect_title(message.content)
            extra_data = (attachments[0].filename, await attachments[0].read()) if len(attachments) != 0 else None
            suggestion_item = SUGGESTION_DATA_ITEM(name, message_member, reaction_member, message, now_time)
            was_saved, suggestion_item = await self.add_suggestion(suggestion_item, extra_data)
            log.info("saved new suggestion, suggestion name: '%s', suggestion author: '%s', saved by: '%s', suggestion has extra data: '%s'",
                     name,
                     message_member.name,
                     reaction_member.name,
                     'yes' if extra_data is not None else 'no')
            if was_saved is True:
                await channel.send(embed=await self.make_add_success_embed(suggestion_item))
        elif unicodedata.name(payload.emoji.name) in self.categories and message.id in self.saved_messages:
            category = self.categories.get(unicodedata.name(payload.emoji.name), None)
            if category:
                success = await self.set_category(category, message.id)
                if success:
                    await channel.send(embed=await self.make_changed_category_embed(message, category))
                    log.info("updated category for suggestion (id: %s) to category '%s'", message.id, category)
        elif unicodedata.name(payload.emoji.name) in [self.command_emojis['upvote'], self.command_emojis['downvote']] and message.id in self.saved_messages:
            reaction = await self.specifc_reaction_from_message(message, unicodedata.name(payload.emoji.name))
            _count = reaction.count
            self.data_storage_handler.update_votes(unicodedata.name(payload.emoji.name), _count, message.id)
            log.info("updated votecount for suggestion (id: %s) for type: '%s' to count: %s", message.id, unicodedata.name(payload.emoji.name), _count)


# endregion [Listener]

# region [Commands]

    @ commands.command()
    @ commands.has_any_role(*COGS_CONFIG.getlist('save_suggestions', 'allowed_roles'))
    async def clear_all(self, ctx):
        if ctx.channel.name in self.allowed_channels:
            writejson({}, self.save_file)
            _msg = 'I have cleared the file'
        else:
            _msg = 'you dont have the permission for that'
        await ctx.send(_msg)

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
