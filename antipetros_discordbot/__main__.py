# region [Module_Docstring]

"""
Main module, starts the Antistasi Discord Bot.

"""
# endregion [Module_Docstring]


# region [Imports]
UV_LOOP_IMPORTED = False
# * Standard Library Imports -->
import os
import sys
import platform
import logging
import configparser
import shutil
from pprint import pprint, pformat
import inspect
import asyncio
from contextlib import contextmanager
# * Third Party Imports -->
import discord
from dotenv import load_dotenv
from discord.ext import commands
from watchgod import awatch
if platform.system() == 'Linux':
    try:
        import uvloop
        UV_LOOP_IMPORTED = True
    except ImportError as error:
        print(error)
import click

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.init_userdata.user_data_setup import SupportKeeper
from antipetros_discordbot.utility.exceptions import TokenError
from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot

from antipetros_discordbot.utility.gidtools_functions import writejson, writeit, pathmaker, loadjson, readit
from antipetros_discordbot.utility.embed_helpers import make_basic_embed
# endregion[Imports]

# region [Constants]

APPDATA = SupportKeeper.get_appdata()
BASE_CONFIG = SupportKeeper.get_config('base_config')
COGS_CONFIG = SupportKeeper.get_config('cogs_config')
# endregion [Constants]

# region [Logging]

_log_file = glog.log_folderer(__name__, APPDATA)
log_stdout = 'both' if BASE_CONFIG.getboolean('logging', 'log_also_to_stdout') is True else 'file'
log = glog.main_logger(_log_file, BASE_CONFIG.get('logging', 'logging_level'), other_logger_names=['asyncio', 'gidsql', 'gidfiles', "gidappdata"], log_to=log_stdout)
log.info(glog.NEWRUN())
if BASE_CONFIG.getboolean('logging', 'use_logging') is False:
    logging.disable(logging.CRITICAL)
if os.getenv('IS_DEV') == 'yes':
    log.warning('!!!!!!!!!!!!!!!!!IS DEV!!!!!!!!!!!!!!!!!')
# endregion[Logging]


# region [Helper_Functions]

def find_env_files():
    env_files = {}
    if os.getenv('IS_DEV').casefold() in ['yes', 'true', 1, 'y']:
        env_files['.env'] = pathmaker(os.path.abspath('.env'))
    else:
        for env_folder in [APPDATA['env_files'], APPDATA['user_env_files']]:
            for env_file in os.scandir(env_folder):
                if os.path.isfile(env_file.path) is True:
                    env_files[env_file.name] = pathmaker(env_file.path)
    return env_files


@contextmanager
def load_env_files():
    env_files = find_env_files()
    excludes = BASE_CONFIG.getlist('env_files', 'auto_load_excluded')
    for key, value in env_files.items():
        if all(key.casefold() != excl_filename.casefold() for excl_filename in excludes):
            load_dotenv(value)
    yield
    os.environ['DISCORD_TOKEN'] = 'xxxxxxxxxxxxx'


def get_intents():
    if BASE_CONFIG.get('intents', 'convenience_setting') == 'all':
        intents = discord.Intents.all()
    elif BASE_CONFIG.get('intents', 'convenience_setting') == 'default':
        intents = discord.Intents.default()
    else:
        intents = discord.Intents.none()
        for sub_intent in BASE_CONFIG.options('intents'):
            if sub_intent != "convenience_setting":
                setattr(intents, sub_intent, BASE_CONFIG.getboolean('intents', sub_intent))
    return intents


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
    # if BASE_CONFIG.getboolean('env_files', 'auto_load') is True:
    #     load_env_files()
    with load_env_files():
        _temp_token = os.getenv('DISCORD_TOKEN')
        if _temp_token not in [None, '', 'xxxx']:
            return _temp_token
        else:
            raise TokenError('token loaded from enviroment is empty or not set')


# endregion [Helper_Functions]

# region [Main_function]
@click.command()
def command_info_run():
    ANTI_PETROS_BOT = AntiPetrosBot(command_prefix='$$', self_bot=False, activity=AntiPetrosBot.activity_from_config(), intents=get_intents())
    _commands = {}
    for cog in ANTI_PETROS_BOT.cogs.items():
        for command in cog.get_commands():
            _commands[command.name] = {'cog_name': command.cog_name,
                                       'aliases': command.aliases,
                                       'brief': command.brief,
                                       'clean_params': command.clean_params,
                                       'description': command.description,
                                       'enabled': command.enabled,
                                       'help': command.help,
                                       'hidden': command.hidden,
                                       'short_doc': command.short_doc,
                                       'signature': command.signature,
                                       'usage': command.usage}
    writejson(_commands, pathmaker(APPDATA['docs'], 'command_data.json'))


@click.command()
def info_run():
    ANTI_PETROS_BOT = AntiPetrosBot(command_prefix='$$', self_bot=False, activity=AntiPetrosBot.activity_from_config(), intents=get_intents())


def main():
    """
    Starts the Antistasi Discord Bot 'AntiPetros'.

    creates the bot, loads the extensions and starts the bot with the Token.
    """

    ANTI_PETROS_BOT = AntiPetrosBot(command_prefix='$$', self_bot=False, activity=AntiPetrosBot.activity_from_config(), intents=get_intents())

    if len(sys.argv) == 1 or sys.argv[1] != 'get_info_run':
        log.info('trying to log on as %s!', str(ANTI_PETROS_BOT))
        if UV_LOOP_IMPORTED is True:
            uvloop.install()
        ANTI_PETROS_BOT.run(get_token(), bot=True, reconnect=True)


# endregion [Main_function]

# region [Main_Exec]

if __name__ == '__main__':
    try:
        main()
    except:
        log.exception(sys.exc_info()[0])
        raise

# endregion[Main_Exec]
