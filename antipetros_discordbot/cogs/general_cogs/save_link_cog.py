"""
An extension Cog to let users temporary save links.

Saved links get posted to a certain channel and deleted after the specified time period from that channel (default in config).
Deleted links are kept in the bots database and can always be retrieved by fuzzy matched name.

Checks against a blacklist of urls and a blacklist of words, to not store malicious links.

cogs_config.ini section: 'save_link'

currently implemented config options:

    - 'allowed_roles' --> comma-seperated-list of role names
    (eg: Dev_helper, Admin) !names have to match completely and are case-sensitive!

    - 'allowed_channels' --> comma-seperated-list of channel names
    (eg: bot-development-and-testing, general-dev-stuff) !names have to match completely and are case-sensitive!

    - 'link_channel' --> channel id for the channel that is used as 'storage', where the bot posts the saved links for the time period
    (eg: 645930607683174401)

    - 'delete_all_allowed_roles' --> comma-seperated-list of role names that are allowed to clear the link Database, all links will be lost.
    will propably be turned into user id list

    - bad_link_answer_image --> file_path or appdata file name to an image to use when answering to an forbidden link (None means no image)
    ! not fully implented !

    - default_storage_days --> integer of days to default to if user does not specifiy amount of time to keep link
    (eg: 7)

    - member_to_notifiy_bad_link --> comma-seperated-list of user_ids of users that should be notified per DM when an bad link is posted.

    - notify_with_link --> boolean if the notification DM should include the bad link
"""

__updated__ = '2020-11-24 07:33:55'
# region [Imports]

# * Standard Library Imports -->
import os
from datetime import datetime, timedelta
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

# * Third Party Imports -->
import aiohttp
import discord
from discord.ext import commands

import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.utility.enums import RequestStatus
from antipetros_discordbot.utility.locations import find_path
from antipetros_discordbot.utility.named_tuples import LINK_DATA_ITEM
from antipetros_discordbot.utility.sqldata_storager import LinkDataStorageSQLite
from antipetros_discordbot.utility.gidtools_functions import writeit, loadjson, pathmaker, writejson
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG, COGS_CONFIG

# endregion [Imports]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# location of this file, does not work if app gets compiled to exe with pyinstaller
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


# endregion [Constants]

# region [TODO]

# TODO: Implement "delete_link" commands

# TODO: Implement background task to pull a fresh blacklist and create a fresh forbidden_link_list every day

# TODO: implement getting bad image path from config, getting bad image name from path and checking if None, sending no image if none

# TODO: refractor channel_from_id into utilities

# TODO: refractor 'get_forbidden_list' to not use temp directory but send as filestream or so

# TODO: need help figuring out how to best check bad link or how to format/normalize it


# endregion [TODO]


class SaveLink(commands.Cog):
    """
    Actual Cog Class for SaveLink features.

    available_commands:
        -
    """

    # url to blacklist for forbidden_link_list
    blocklist_hostfile_url = "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn/hosts"

# region [Init]

    def __init__(self, bot):
        self.bot = bot
        self.is_debug = BASE_CONFIG.getboolean('general_settings', 'is_debug')
        # composition to make data storage modular, currently set up for an sqlite Database
        self.data_storage_handler = LinkDataStorageSQLite()

        self.allowed_channels = set(COGS_CONFIG.getlist('save_link', 'allowed_channels'))
        self.forbidden_links = set(loadjson(pathmaker(THIS_FILE_DIR, r'..\..\data\data_storage\json_data\forbidden_link_list.json')))  # read previously saved blacklist, because extra_setup method does not run when the cog is only reloaded
        self.forbidden_url_words = set(map(lambda x: str(x).casefold(), loadjson(pathmaker(THIS_FILE_DIR, r'..\..\data\data_storage\json_data\forbidden_url_words.json'))))
        self.link_channel = None  # weird setup because again, the extra setup does not execute when only reloaded.
        try:
            self.link_channel = self.channel_from_id(COGS_CONFIG.getint('save_link', 'link_channel'))
        except AttributeError as error:
            log.error('link_channel had error: %s', str(error))

        # will be removed soon and values will be gathered from config
        self.bad_link_image = (pathmaker(THIS_FILE_DIR, r"..\..\data\fixed_data\bertha.png"), 'bertha.png')

# endregion [Init]

# region [Setup]

    async def _process_raw_blocklist_content(self, raw_content):
        """
        Process downloaded Blacklist to a list of raw urls.

        Returns:
            set: forbidden_link_list as set for quick contain checks
        """

        _out = []
        if self.is_debug is True:
            raw_content += '\n\n0 www.stackoverflow.com'  # added for Testing
        for line in raw_content.splitlines():
            if line.startswith('0') and line not in ['', '0.0.0.0 0.0.0.0']:
                line = line.split('#')[0].strip()
                _, forbidden_url = line.split(' ')
                _out.append(forbidden_url.strip())
        return set(_out)

    async def _create_forbidden_link_list(self):
        """
        Downloads Blacklist and saves it to json, after processing (-->_process_raw_blocklist_content)
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(self.blocklist_hostfile_url) as _response:
                if RequestStatus(_response.status) is RequestStatus.Ok:
                    _content = await _response.read()
                    _content = _content.decode('utf-8', errors='ignore')
                    self.forbidden_links = await self._process_raw_blocklist_content(_content)
                    self.forbidden_links = set(map(lambda x: urlparse('https://' + x).netloc.replace('www.', ''), self.forbidden_links))
                    _path = pathmaker(THIS_FILE_DIR, r'..\..\data\data_storage\json_data\forbidden_link_list.json')
                    writejson(list(map(lambda x: urlparse('https://' + x).netloc.replace('www.', ''), self.forbidden_links)), _path)  # converting to list as set is not json serializable

# endregion [Setup]

# region [Listener]

    @commands.Cog.listener(name='on_ready')
    async def _extra_cog_setup(self):
        """
        Setup methods that run if the Bot Connects successfully.

        Currently it:
            - creates a fresh forbidden_link_list json
            - retrieves the channel to save the links to from the config

        ! DOES NOT EXECUTE WHEN COG IS RELOADED !
        """

        await self._create_forbidden_link_list()
        self.link_channel = self.channel_from_id(COGS_CONFIG.getint('save_link', 'link_channel'))
        log.info(f"{self} Cog ----> finished extra setup")

# endregion [Listener]

# region [Commands]

    @commands.command()
    @commands.has_any_role(*COGS_CONFIG.getlist('save_link', 'delete_all_allowed_roles'))
    async def delete_all_links(self, ctx):
        """
        Delete all saved links.

        Implementation is hhandled by DataStorage, but usually involves deleting the storage file (eg: sqlite, deletes db and reinitializes it)

        Args:
            ctx (discord.context): mandatory command argument
        """
        log.debug("command was triggered in %s", ctx.channel.name)
        if ctx.channel.name not in self.allowed_channels:
            log.debug("channel not is 'allowed channel'")
            return
        self.data_storage_handler.delete_all()
        await ctx.send("cleared all saved links")
        log.info("all links were deleted from the DataStorage by request of '%s'", ctx.author.name)

    @commands.command()
    @commands.has_any_role(*COGS_CONFIG.getlist('save_link', 'allowed_roles'))
    async def get_link(self, ctx, name):
        """
        Get a link as normal answer message, by link name.

        actual matching is implemented and handled by the DataStorage

        Args:
            ctx (discord.context): mandatory command argument
            name (str): link name
        """
        log.debug("command was triggered in %s", ctx.channel.name)
        if ctx.channel.name not in self.allowed_channels:
            log.debug("channel not is 'allowed channel'")
            return
        log.info("Link with Link name '%s' was requested", name)
        _link = self.data_storage_handler.get_link(name)
        await ctx.send(_link)
        log.info("retrieve link '%s'", _link)

    @commands.command()
    @commands.has_any_role(*COGS_CONFIG.getlist('save_link', 'allowed_roles'))
    async def get_all_links(self, ctx, in_format='plain'):
        """
        Get a list of all saved links, as a file.

        Args:
            ctx (discord.context): mandatory command argument
            in_format (str, optional): output format, currently possible: 'json', 'plain' is txt. Defaults to 'plain'.
        """
        log.debug("command was triggered in %s", ctx.channel.name)
        if ctx.channel.name not in self.allowed_channels:
            log.debug("channel not is 'allowed channel'")
            return
        with TemporaryDirectory() as tempdir:
            if in_format == 'json':
                _link_dict = self.data_storage_handler.get_all_links('json')
                _name = 'all_links.json'
                _path = pathmaker(tempdir, _name)
                if len(_link_dict) == 0:
                    await ctx.send('no saved links')
                    return
                writejson(_link_dict, _path)

            else:
                _link_list = self.data_storage_handler.get_all_links('plain')
                _name = 'all_links.txt'
                _path = pathmaker(tempdir, _name)
                if len(_link_list) == 0:
                    await ctx.send('no saved links')
                    return
                writeit(_path, '\n'.join(_link_list))

            _file = discord.File(_path, _name)
            await ctx.send(file=_file)

    @commands.command()
    @commands.has_any_role(*COGS_CONFIG.getlist('save_link', 'allowed_roles'))
    async def save_link(self, ctx, link: str, link_name: str = None, days_to_hold: int = None):
        """
        Main Command of the SaveLink Cog.
        Save a link to the DataStorage and posts it for a certain time to an storage channel.

        [extended_summary]

        Args:
            ctx (discord.context): mandatory command argument
            link (str): link to save
            link_name (str, optional): name to save the link as, if not given will be generated from url. Defaults to None.
            days_to_hold (int, optional): time befor the link will be deleted from storage channel in days, if not give will be retrieved from config. Defaults to None.
        """
        log.debug("command was triggered in %s", ctx.channel.name)
        if ctx.channel.name not in self.allowed_channels:
            log.debug("channel not is 'allowed channel'")
            return

        # check if it is a forbidden link, before computing all that expansive shit
        to_check_link = await self._make_check_link(link)
        log.debug("link transformed to  check link: '%s'", to_check_link)
        parsed_link = urlparse(link, scheme='https').geturl().replace('///', '//')
        date_and_time = datetime.utcnow()
        if all(to_check_link != forbidden_link for forbidden_link in self.forbidden_links) and all(forbidden_word not in to_check_link for forbidden_word in self.forbidden_url_words):
            log.debug("'%s' NOT in forbidden link list and does not contain a forbidden word", parsed_link)
            # create link name if none was supplied
            if link_name is None:
                log.debug("No Link name provided")
                link_name = await self._make_link_name(link)
            link_name = link_name.upper()

            # check if link name is already occupied
            if await self._check_link_name_existing(link_name) is True:
                log.error("link name '%s' already in DataStorage", link_name)
                await ctx.send(f"The link_name '{link_name}', is already taken, please choose a different Name.")
                return None

            # calculate or retrieve all other needed values
            days = COGS_CONFIG.getint('save_link', 'default_storage_days') if days_to_hold is None else days_to_hold
            delete_date_and_time = date_and_time + timedelta(days=days)
            author = ctx.author

            # create the link item and save it
            link_item = LINK_DATA_ITEM(author, link_name, date_and_time, delete_date_and_time, parsed_link)
            log.info("new link --> author: '%s', link_name: '%s', delete_date_time: '%s', days_until_delete: '%s', parsed_link: '%s'",
                     author.name,
                     link_name,
                     delete_date_and_time.isoformat(timespec='seconds'),
                     str(days),
                     parsed_link)
            await self.save(link_item)

            # if this is a debug run, delete the answer message after 30 seconds else delete after specified time (86400 is the number of seconds in a day)
            delete_answer = days * 86400 if self.is_debug is False else 30

            # post the link as embed to the specified save link channel
            await self.link_channel.send(embed=await self._answer_embed(link_item), delete_after=delete_answer)

            # post an success message to the channel from where the command was invoked. Delete after 60 seconds.
            await ctx.send('✅ Link was successfully saved', delete_after=60)

        else:
            log.warning("link '%s' matched against a forbidden link or contained a forbidden word", parsed_link)
            delete_answer = None if self.is_debug is False else 30

            # send warning for forbidden link infraction
            await ctx.send(embed=await self._bad_link_embed(), file=await self._get_bad_link_image(), delete_after=delete_answer)
            if ctx.channel.permissions_for(ctx.me).manage_messages:
                # if channel permissions for bot allows it, because it has an forbidden link in it and should most likely be deleted from the discord
                await ctx.message.delete(delay=None)
                log.debug("was able to delete the offending link")
                was_deleted = True
            else:
                log.error("was NOT able to delete the offending link")
                was_deleted = False

            # notify users specified in the config of the attempt at saving an forbidden link
            notify_embed = await self._notify_dm_embed(was_deleted=was_deleted,
                                                       author=ctx.author,
                                                       date_time=date_and_time,
                                                       channel=ctx.channel.name,
                                                       link=parsed_link,
                                                       matches_link=await self.get_matched_forbidden_link(to_check_link),
                                                       matches_word=await self.get_matched_forbidden_word(to_check_link))

            for user_id in COGS_CONFIG.getlist('save_link', 'member_to_notifiy_bad_link'):
                user = self.bot.get_user(int(user_id))
                await user.send(embed=notify_embed, delete_after=delete_answer)
                log.debug("notified '%s' about the offending link", user.name)

    @commands.command()
    @commands.has_any_role(*COGS_CONFIG.getlist('save_link', 'allowed_roles'))
    async def get_forbidden_list(self, ctx, file_format='json'):
        """
        command to get the forbidden link list as an file.

        Mostly debug related. Should be turned into an DM Command.

        Args:

            file_format (str, optional): format the list file should have(currently possible: 'json'). Defaults to 'json'.
        """
        log.debug("command was triggered in %s", ctx.channel.name)
        if ctx.channel.name not in self.allowed_channels:
            log.debug("channel not is 'allowed channel'")
            return
        if file_format == 'json':
            with TemporaryDirectory() as tempdir:
                _name = 'forbidden_links.json'
                _path = pathmaker(tempdir, _name)
                writejson(list(self.forbidden_links), _path, indent=2)
                _file = discord.File(_path, filename=_name)
                await ctx.send(file=_file, delete_after=60)
                log.info("send forbidden link list to '%s'", ctx.author.name)


# endregion [Commands]

# region [DataStorage]

    async def link_name_list(self):
        """
        Retrieves all saved link names from the DataStorage.

        async wrapper for access to the modular data storage (currently sqlite Db)

        Returns:
            set: set of all link names
        """

        return self.data_storage_handler.all_link_names

    async def save(self, link_item: LINK_DATA_ITEM):
        """
        Adds new link to the DataStorage

        async wrapper for access to the modular data storage (currently sqlite Db)

        Args:
            link_item (LINK_DATA_ITEM): namedtuple to contain link data see 'antipetros_discordbot.utility.named_tuples --> LINK_DATA_ITEM'
        """

        self.data_storage_handler.add_data(link_item)

# endregion [DataStorage]

# region [Embeds]

    async def _answer_embed(self, link_item):
        """
        creates the stored link embed for an saved link.

        Is extra function to make it more readable. No customization currently.

        Returns:
            discord.Embed: link storage embed.
        """

        _rel_time = link_item.delete_date_time - link_item.date_time
        _embed = discord.Embed(title="Saved Link", description="Temporary Stored Link", color=0x4fe70e)
        _embed.set_thumbnail(url="https://images.emojiterra.com/twitter/v13.0/512px/1f517.png")
        _embed.add_field(name="from:", value=link_item.author.name, inline=True)
        _embed.add_field(name=link_item.link_name + ':', value=link_item.link, inline=False)
        _embed.add_field(name="available until:", value=link_item.delete_date_time.strftime("%Y/%m/%d, %H:%M:%S") + f" ({str(_rel_time).split(',')[0].strip()})", inline=False)
        _embed.add_field(name="retrieve command:", value=f"`get_link {link_item.link_name}`", inline=True)
        _embed.add_field(name="retrieve all command", value="`get_all_links`", inline=True)
        _embed.set_footer(text='This link will be deleted after the date specified in "available until", afterwards it can still be retrieved by the retrieve commands')
        return _embed

    async def _bad_link_embed(self):
        """
        creates the answer embed for an answer to an forbidden link.

        Is extra function to make it more readable. No customization currently.

        Returns:
            discord.Embed: Bad link answer embed
        """

        embed = discord.Embed(title="FORBIDDEN LINK", description="You tried to save a link that is either in my forbidden_link-list or contains a forbidden word.", color=0x7c0303)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Forbidden_Symbol_Transparent.svg/1200px-Forbidden_Symbol_Transparent.svg.png")
        embed.add_field(name="🚫 The link has NOT been saved! 🚫", value="-", inline=False)
        embed.add_field(name="⚠️ DO NOT TRY THIS AGAIN ⚠️", value="-", inline=False)
        embed.set_footer(text="! This has been Logged !")
        return embed

    async def _notify_dm_embed(self, was_deleted: bool, author, date_time: datetime, channel: str, link: str, matches_link: list, matches_word: list):
        """
        creates the notify embed for DM notifications when an forbidden link was tried to be saved forbidden link.

        Is extra function to make it more readable. No customization currently.

        Returns:
            discord.Embed: notify dm embed
        """

        _description = ('The message has been successfully deleted and warning was posted!' if was_deleted else "I was not able to delete the message, but posted the warning")

        embed = discord.Embed(title='ATTEMPT AT SAVING FORBIDDEN LINK', description=_description, color=0xdf0005)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Warning.svg/1200px-Warning.svg.png")
        embed.add_field(name="User", value=f"__**{author.name}**__", inline=False)
        embed.add_field(name="User Display Name", value=f"*{author.display_name}*", inline=False)
        embed.add_field(name="User ID", value=f"**{author.id}**", inline=False)
        embed.add_field(name="Channel", value=f"**{channel}**", inline=False)
        embed.add_field(name="Date", value=date_time.date().isoformat(), inline=True)
        embed.add_field(name="Time", value=f"{date_time.time().isoformat(timespec='seconds')} UTC", inline=True)
        if COGS_CONFIG.getboolean('save_link', 'notify_with_link') is True:
            embed.add_field(name="Offending Link", value=f"***{link}***", inline=False)
            if matches_link != []:
                print(matches_link)
                embed.add_field(name="forbidden link matches", value='\n'.join(matches_link), inline=False)
            if matches_word != []:
                print(matches_word)
                embed.add_field(name="forbidden word matches", value='\n'.join(matches_word), inline=False)
        embed.set_footer(text="You have been notified, because your discord user id has been registered in my config, to be notified in such events.")
        return embed


# endregion [Embeds]

    async def _get_bad_link_image(self):
        """
        Wraps the bad_link_image in and discord File object.
        has to be created each time, can't be stored in attribute as discord File object.

        Returns:
            discord.File: discord File containing the image
        """

        # image_path = COGS_CONFIG.get('save_link', 'bad_link_answer_image')
        # if image_path.casefold() == 'none':
        #     return None
        # image_name = os.path.basename(image_path)
        # return discord.File(image_path, image_name)
        return discord.File(self.bad_link_image[0], self.bad_link_image[1])

# region [Helper]

    def channel_from_id(self, _id):
        """
        helper to get an channel from an channel id.
        | Will be refractored into utilities |

        Args:
            _id (int): channel id (can be found by right clicking the channel after enabling, dev mode in discord)

        Returns:
            channel_object: the channel as discord object
        """

        _channel = self.bot.get_channel(_id)
        print("save_link_channel is " + str(_channel.name))
        return _channel

    async def _make_check_link(self, url):
        """
        Helper to normalize the link url, so it can easily be compared to the forbidden links (normalized link in each forbidden link)

        Args:
            url (str): link url

        Returns:
            str: normalized link url
        """

        temp_url = 'https://' + url if not url.startswith('http') else url
        check_link = urlparse(temp_url).netloc.replace('www.', '')
        return check_link.casefold()

    async def _make_link_name(self, url):
        """
        Helper to create an link name from the url if none was give by the command.

        Args:
            url (str): link url

        Returns:
            str: link name
        """
        temp_url = 'https://' + url if not url.startswith('http') else url
        link_name = urlparse(temp_url).netloc.replace('www.', '')
        link_name = link_name.split('.')
        return link_name[0]

    async def _check_link_name_existing(self, name):
        """
        Helper to check if link_name is already occupied.

        Args:
            name (str): link name

        Returns:
            [bool]: bool (True if already occupied)
        """

        _name_list = await self.link_name_list()
        return name in _name_list

    async def get_matched_forbidden_link(self, check_link):
        """
        get all unique matches between the input link and the forbidden link list, as list.

        Args:
            check_link (str): modified check url

        Returns:
            (list): all matches as list, if no matches, returns empty list
        """

        _out = [link for link in self.forbidden_links if check_link == link]
        return list(set(_out))

    async def get_matched_forbidden_word(self, url):
        """
        get all unique matches between the input link and the forbidden word list, as list.

        Args:
            check_link (str): modified check url

        Returns:
            (list): all matches as list, if no matches, returns empty list
        """

        _out = [word for word in self.forbidden_url_words if word in url]
        return list(set(_out))


# endregion [Helper]

# region [DunderMethods]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.user.name})"

    def __str__(self):
        return self.__class__.__name__

# endregion [DunderMethods]


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(SaveLink(bot))
