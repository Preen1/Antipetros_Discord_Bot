# region [Module_Docstring]

"""
Main module, starts the Antistasi Discord Bot.
On the Cli use: antipetrosbot run [-t token file] [-save]

"""
# endregion [Module_Docstring]


# region [Imports]

import os
import logging
from time import sleep
from datetime import datetime
import click
import discord
from dotenv import find_dotenv, load_dotenv
import gidlogger as glog
from antipetros_discordbot import MAIN_DIR
from antipetros_discordbot.utility.misc import check_if_int
from antipetros_discordbot.utility.crypt import decrypt_db, encrypt_db
from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot
from antipetros_discordbot.utility.gidtools_functions import writeit, pathmaker, writejson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper

# endregion[Imports]

# region [TODO]


# endregion [TODO]


# region [Constants]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
# endregion [Constants]

# region [Logging]


def configure_logger():
    """
    Configures the logger from the base_config.ini file.
    When logging to file, the file rotates every new run and also when it reaches a size of 10mb.
    Mainly to either log to stdout and a file or only a file and how many files it should keep.
    """
    # TODO: way to convoluted, make it simpler look into better loggign frameworks.

    def from_config(key, attr_name):
        """
        Helper func to get values from the config, without having to type the section repetedly.

        Args:
            key (str): option name in the config
            attr_name (str): attribute to use to retrieve the value, i.e.: getboolean, get, getint

        Returns:
            [Any]: the desired value with, type is dictated by the attribute that is used to retrieve it (attr_name)
        """

        return getattr(BASE_CONFIG, attr_name)('logging', key)
    log_stdout = 'both' if from_config('log_also_to_stdout', 'getboolean') is True else 'file'
    log_level = from_config('logging_level', 'get')
    _log_file = glog.log_folderer(__name__, APPDATA)
    in_back_up = from_config('amount_keep_old_logs', 'getint')
    use_logging = from_config('use_logging', 'getboolean')
    if os.getenv('IS_DEV') == 'true':
        log_stdout = 'both'

    _log = glog.main_logger(_log_file, log_level, other_logger_names=['asyncio', 'gidsql', 'gidfiles', "gidappdata"], log_to=log_stdout, in_back_up=in_back_up)
    _log.info(glog.NEWRUN())
    if use_logging is False:
        logging.disable(logging.CRITICAL)
    if os.getenv('IS_DEV') == 'yes':
        _log.warning('!!!!!!!!!!!!!!!!!!! IS DEV !!!!!!!!!!!!!!!!!!!')
        _log.warning('!!!!!!!!!!!!!!!!! DEBUG MODE !!!!!!!!!!!!!!!!!')
    return _log


log = configure_logger()
# endregion[Logging]


# region [Helper]


# endregion [Helper]

# region [Main_function]

@click.group()
def cli():
    """
    dummy function to initiate click group.

    """


@cli.command(name='create_alias_data')
def command_alias_run():
    """
    function and cli command to start up the bot, create aliases but not connect to discord.
    Creates 4 versions for each alias:
        - base version
        - version where _ are replaced with -
        - version where _ are replaced with .
        - version where _ are removed
    """
    _out = {}
    anti_petros_bot = AntiPetrosBot()
    for command in anti_petros_bot.walk_commands():
        _out[command.name] = list(map(lambda x: x.replace('_', '-'), command.aliases))
        _out[command.name] += [alias.replace('-', '').replace('_', '') for alias in command.aliases if alias != command.name and alias.replace('-', '').replace('_', '') not in _out[command.name]]
        _out[command.name] += [alias.replace('-', '.').replace('_', '.') for alias in command.aliases if alias != command.name and alias.replace('-', '.').replace('_', '.') not in _out[command.name]]
        if '_' in command.name and command.name.replace('_', '-') not in _out[command.name]:
            _out[command.name].append(command.name.replace('_', '-'))
        _out[command.name] = list(set(_out[command.name]))
    writejson(_out, APPDATA['command_aliases.json'])


@cli.command(name='only_command_info')
def command_info_run():
    """
    Function and cli command to start up the bot, collect bot-commands extended info, but not connect to discord.

    collected as json in /docs

    """
    anti_petros_bot = AntiPetrosBot()
    _commands = {}
    for cog_name, cog_object in anti_petros_bot.cogs.items():
        for command in cog_object.get_commands():
            clean_params = {}
            for name, parameter in command.clean_params.items():

                clean_params[name] = {'annotation': str(parameter.annotation).replace("<class '", '').replace("'>", '').strip() if parameter.annotation is not parameter.empty else None,
                                      'default': check_if_int(parameter.default) if parameter.default is not parameter.empty else None,
                                      'kind': parameter.kind.description}

            _commands[command.name] = {'cog_name': command.cog_name,
                                       'aliases': command.aliases,
                                       'brief': command.brief,
                                       'clean_params': clean_params,
                                       'description': command.description,
                                       'enabled': command.enabled,
                                       'help': command.help,
                                       'hidden': command.hidden,
                                       'short_doc': command.short_doc,
                                       'signature': command.signature,
                                       'usage': command.usage,
                                       'require_var_positional': command.require_var_positional}
    writejson(_commands, pathmaker(APPDATA['documentation'], 'command_data.json'), sort_keys=True)


@cli.command(name="clean")
def clean_user_data():
    if os.environ['IS_DEV'].casefold() in ['true', 'yes', '1'] or APPDATA.dev is True:
        raise RuntimeError("Cleaning not possible in Dev Mode")
    APPDATA.clean(APPDATA.AllFolder)


@cli.command(name='only_info')
def info_run():
    """
    Function and cli command to start up the bot, collect bot-commands basic info, but not connect to discord.
    used to auto build the readme
    """
    os.environ['INFO_RUN'] = "1"
    command_json_file = pathmaker(os.getenv('TOPLEVELMODULE'), '../docs/commands.json')
    writejson({}, command_json_file)
    anti_petros_bot = AntiPetrosBot()


@cli.command(name='stop')
def stop():
    """
    Cli way of autostoping the bot.
    creates and file in a specific folder that acts like a shutdown trigger (bot watches the folder)
    afterwards deletes the file. Used as redundant way to shut down if other methods fail, if this fails, the server has to be restarted.

    """
    shutdown_trigger_path = pathmaker(APPDATA['shutdown_trigger'], 'shutdown.trigger')
    writeit(shutdown_trigger_path, 'shutdown')
    sleep(10)
    if os.path.isfile(shutdown_trigger_path) is True:
        os.remove(shutdown_trigger_path)
    print(f'AntiPetrosBot was shut down at {datetime.utcnow().strftime("%H:%M:%S on the %Y.%m.%d")}')


@cli.command(name='run')
@click.option('--token', '-t')
@click.option('--db-key', '-dbk')
def run(token, db_key):
    """
    Standard way to start the bot and connect it to discord.
    takes the token as string and the key to decrypt the db also as string.
    calls the actual main() function.

    Args:
        token_file ([str]): discord token
        save_token_file ([str]): key to decrypt the db's
    """
    os.environ['INFO_RUN'] = "0"
    main(token=token, db_key=db_key)


def main(token: str, db_key: str):
    """
    Starts the Antistasi Discord Bot 'AntiPetros'.

    creates the bot, loads the extensions and starts the bot with the Token.
    is extra function so the bot can be started via cli but also from within vscode.

    Args:
        token_file ([str]): discord token
        save_token_file ([str]): key to decrypt the db's
    """
    os.environ['INFO_RUN'] = "0"
    decrypt_db(db_key)
    anti_petros_bot = AntiPetrosBot(token=token, db_key=db_key)
    _out = {}

    for command in anti_petros_bot.walk_commands():
        _out[command.name] = list(map(lambda x: x.replace('_', '-'), command.aliases))
        _out[command.name] += [alias.replace('-', '').replace('_', '') for alias in command.aliases if alias != command.name and alias.replace('-', '').replace('_', '') not in _out[command.name]]
        _out[command.name] += [alias.replace('-', '.').replace('_', '.') for alias in command.aliases if alias != command.name and alias.replace('-', '.').replace('_', '.') not in _out[command.name]]
        if '_' in command.name and command.name.replace('_', '-') not in _out[command.name]:
            _out[command.name].append(command.name.replace('_', '-'))
        _out[command.name] = list(set(_out[command.name]))
    writejson(_out, APPDATA['command_aliases.json'])

    try:
        anti_petros_bot.run()
    finally:
        encrypt_db(db_key)


# endregion [Main_function]
# region [Main_Exec]
if __name__ == '__main__':
    if os.getenv('IS_DEV') == 'true':
        load_dotenv('token.env')

        main(token=os.getenv('ANTIDEVTROS_TOKEN'), db_key=os.getenv('DB_KEY'))
    else:
        main()


# endregion[Main_Exec]
