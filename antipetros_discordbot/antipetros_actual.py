
# region [Imports]
from pprint import pprint
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from antipetros_discordbot.utility.exceptions import TokenError
from gidtools.gidconfig import ConfigHandler, Get
import configparser
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG
# endregion[Imports]


try:
    HELP_COMMAND = BASE_CONFIG.get('general_settings', 'help_command')
except configparser.NoOptionError as error:
    print(error)
    HELP_COMMAND = None
TOKEN = None


def dynamic_command_prefix():
    try:
        _out = BASE_CONFIG.get('general_settings', 'command_prefix')
    except configparser.NoOptionError as error:
        print(error)
        _out = '$$'
    return _out


def get_help_command():
    try:
        _out = BASE_CONFIG.get('general_settings', 'help_command')
    except configparser.NoOptionError as error:
        print(error)
        _out = 'antipetros_help'
    return _out


def get_token():
    load_dotenv()
    _temp_token = os.getenv('DISCORD_TOKEN')
    if _temp_token not in [None, '', 'xxxx']:
        return _temp_token
    else:
        raise TokenError('token loaded from enviroment is empty or not set')


def create_bot():
    return commands.Bot(command_prefix=commands.when_mentioned_or(dynamic_command_prefix()), HELP_COMMAND=get_help_command())


def get_initial_extensions():
    _base_location = BASE_CONFIG.get('general_settings', 'cogs_location')
    for _extension in BASE_CONFIG.options('extensions'):
        if BASE_CONFIG.getboolean('extensions', _extension) is True:
            yield _base_location + '.' + _extension


ANTI_PETROS_BOT = create_bot()

# loading all cogs
if __name__ == '__main__':
    for extension in get_initial_extensions():
        print(f"{extension.split('.')[-1]}.py loaded")
        ANTI_PETROS_BOT.load_extension(extension)

# setting bot activity and presence and logging connection.


@ANTI_PETROS_BOT.event
async def on_ready():
    print('trying to log on as {0}!'.format(ANTI_PETROS_BOT.user.name))
    channel = ANTI_PETROS_BOT.get_channel(645930607683174401)
    print(f'{ANTI_PETROS_BOT.user.name} has connected to Discord!')
    # await channel.send('I have awoken! Muhahahahhaha')
# running the bot

ANTI_PETROS_BOT.run(get_token(), bot=True, reconnect=True)
