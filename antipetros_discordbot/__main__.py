
# region [Imports]
from pprint import pprint
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from antipetros_discordbot.utility.exceptions import TokenError
import configparser
import argparse
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG
# endregion[Imports]

# region [Constants]

# -------------------
DEV = False
# -------------------

ADMIN_COG = "antipetros_discordbot.cogs.admin_cog"
try:
    HELP_COMMAND = BASE_CONFIG.get('general_settings', 'help_command')
except configparser.NoOptionError as error:
    print(error)
    HELP_COMMAND = None


# endregion [Constants]


def dynamic_command_prefix():
    try:
        prefix = BASE_CONFIG.get('general_settings', 'command_prefix')
    except configparser.NoOptionError as error:
        print(error)
        prefix = '$$'
    if BASE_CONFIG.getboolean('general_settings', 'invoke_by_mention') is True:
        prefix = commands.when_mentioned_or(prefix)
    return prefix


def get_help_command():
    try:
        _out = BASE_CONFIG.get('general_settings', 'help_command')
    except configparser.NoOptionError as error:
        print(error)
        _out = 'antipetros_help'
    return _out


# TODO: Deal wit the tripple or quadrouple redundancy in regards to the env file
def get_token(envfile=None):
    _file = '.env' if envfile is None else envfile
    load_dotenv(_file)
    _temp_token = os.getenv('DISCORD_TOKEN')
    if _temp_token not in [None, '', 'xxxx']:
        return _temp_token
    else:
        raise TokenError('token loaded from enviroment is empty or not set')


def get_initial_extensions():
    _base_location = BASE_CONFIG.get('general_settings', 'cogs_location')
    for _extension in BASE_CONFIG.options('extensions'):
        if BASE_CONFIG.getboolean('extensions', _extension) is True:
            yield _base_location + '.' + _extension


def main():

    _envfile = None

    ANTI_PETROS_BOT = commands.Bot(command_prefix=dynamic_command_prefix(), HELP_COMMAND=get_help_command(), self_bot=False)

    ANTI_PETROS_BOT.load_extension(ADMIN_COG)
    for extension in get_initial_extensions():
        print(f"{extension.split('.')[-1]}.py loaded")
        ANTI_PETROS_BOT.load_extension(extension)

    @ANTI_PETROS_BOT.event
    async def on_ready():
        print(f'trying to log on as {ANTI_PETROS_BOT.user.name}!')

        print(f'{ANTI_PETROS_BOT.user.name} has connected to Discord!')
        if BASE_CONFIG.getboolean('general_settings', 'use_startup_message') is True:
            channel = ANTI_PETROS_BOT.get_channel(BASE_CONFIG.getint('startup_message', 'channel'))
            await channel.send(BASE_CONFIG.get('startup_message', 'message'))

    ANTI_PETROS_BOT.run(get_token(_envfile), bot=True, reconnect=True)


if __name__ == '__main__':
    main()
