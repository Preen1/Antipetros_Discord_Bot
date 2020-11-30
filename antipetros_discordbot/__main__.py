# region [Module_Docstring]

"""
Main module, starts the Antistasi Discord Bot.

"""
# endregion [Module_Docstring]

__updated__ = '2020-11-30 20:31:16'


# region [Imports]

# * Standard Library Imports -->
import os
import logging
import configparser

# * Third Party Imports -->
from dotenv import load_dotenv
from discord.ext import commands

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.utility.exceptions import TokenError
from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG

# endregion[Imports]

# region [Logging]

_log_file = glog.log_folderer(__name__)
log = glog.main_logger(_log_file, BASE_CONFIG.get('logging', 'logging_level'))
formatter = logging.Formatter('%(asctime)s | %(levelname)s | (%(lineno)s) | %(module)s | %(funcName)s | --> %(message)s <--')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
log.info(glog.NEWRUN())
if BASE_CONFIG.getboolean('logging', 'use_logging') is False:
    logging.disable(logging.CRITICAL)

# endregion[Logging]

# region [Constants]

# import location of the Admin Cog as it is not loaded dynamically
ADMIN_COG = "antipetros_discordbot.cogs.admin_cog"

# endregion [Constants]

# region [Helper_Functions]


def dynamic_command_prefix():
    """
    loads command prefix settings from the Base Config, if not found sets it to '$$'

    Returns:
        either string or if 'invoke_by_mention' is set to True, retrurns 'commands.when_mentioned_or' callable
    """
    try:
        prefix = BASE_CONFIG.get('general_settings', 'command_prefix')
    except configparser.NoOptionError as error:
        log.error(error)
        prefix = '$$'
    if BASE_CONFIG.getboolean('general_settings', 'invoke_by_mention') is True:
        prefix = commands.when_mentioned_or(prefix)
    return prefix


def get_help_command():
    """
    loads help command from config, if not found sets it to 'antipetros_help"

    Returns:
        str: help_command
    """
    try:
        _out = BASE_CONFIG.get('general_settings', 'help_command')
    except configparser.NoOptionError as error:
        log.error(error)
        _out = 'antipetros_help'
    return _out


# TODO: Deal wit the tripple or quadrouple redundancy in regards to the env file
def get_token():
    """
    Reloads env file then reads and returns the Token.

    Args:
        envfile (str, optional): path to env file. Defaults to None.

    Raises:
        TokenError: raised if Token is not set in the env or set to nothing or set to 'xxxx'

    Returns:
        str: Token
    """

    load_dotenv()
    _temp_token = os.getenv('DISCORD_TOKEN')
    if _temp_token not in [None, '', 'xxxx']:
        return _temp_token
    else:
        raise TokenError('token loaded from enviroment is empty or not set')


def get_initial_extensions():
    """
    Reads extensions to load from the config.

    Cogs should be specified in the config as [folder].[cog_name without '.py'] = [boolean]

    Relies on 'cog_location' under 'general_settings' in the BaseConfig, for the base cog folder.

    Yields:
        str: the full cog import path if the cog is set to load
    """
    _base_location = BASE_CONFIG.get('general_settings', 'cogs_location')
    for _extension in BASE_CONFIG.options('extensions'):
        if BASE_CONFIG.getboolean('extensions', _extension) is True:
            yield _base_location + '.' + _extension

# endregion [Helper_Functions]

# region [Main_function]


def main():
    """
    Starts the Antistasi Discord Bot 'AntiPetros'.

    creates the bot, loads the extensions and starts the bot with the Token.
    """

    ANTI_PETROS_BOT = AntiPetrosBot(command_prefix=dynamic_command_prefix(), HELP_COMMAND=get_help_command(), self_bot=False)

    ANTI_PETROS_BOT.load_extension(ADMIN_COG)
    for extension in get_initial_extensions():
        log.info("%s.py loaded", extension.split('.')[-1])
        ANTI_PETROS_BOT.load_extension(extension)

    @ANTI_PETROS_BOT.event
    async def on_ready():
        log.info('trying to log on as %s!', ANTI_PETROS_BOT.user.name)

        log.info('%s has connected to Discord!', ANTI_PETROS_BOT.user.name)
        channel = ANTI_PETROS_BOT.get_channel(BASE_CONFIG.getint('startup_message', 'channel'))
        if BASE_CONFIG.getboolean('startup_message', 'use_startup_message') is True:
            await channel.send(BASE_CONFIG.get('startup_message', 'message'))

    ANTI_PETROS_BOT.run(get_token(), bot=True, reconnect=True)

# endregion [Main_function]


if __name__ == '__main__':
    main()
