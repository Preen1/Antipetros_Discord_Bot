# region [Module_Docstring]

"""
Main module, starts the Antistasi Discord Bot.
On the Cli use: antipetrosbot run [-t token file] [-save]

"""
# endregion [Module_Docstring]


# region [Imports]
UV_LOOP_IMPORTED = False
# * Standard Library Imports -->
import os
import logging
from time import sleep
from datetime import datetime

# * Third Party Imports -->
import click
import discord
from dotenv import load_dotenv, find_dotenv

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot import MAIN_DIR
from antipetros_discordbot.utility.misc import check_if_int
from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot
from antipetros_discordbot.utility.gidtools_functions import writeit, pathmaker, writejson
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.crypt import encrypt_db, decrypt_db
# endregion[Imports]

# region [TODO]

# TODO: create prompt for token, with save option


# endregion [TODO]


# region [Constants]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
# endregion [Constants]

# region [Logging]


def configure_logger():
    """
    [summary]

    [extended_summary]
    """
    def from_config(key, attr_name):

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
    [summary]

    [extended_summary]
    """
    pass


@cli.command(name='create_alias_data')
def command_alias_run():
    """
    [summary]

    [extended_summary]
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
    [summary]

    [extended_summary]
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


@cli.command(name='only_info')
def info_run():
    """
    [summary]

    [extended_summary]
    """
    os.environ['INFO_RUN'] = "1"
    anti_petros_bot = AntiPetrosBot()


@cli.command(name='stop')
def stop():
    """
    [summary]

    [extended_summary]
    """
    shutdown_trigger_path = pathmaker(APPDATA['shutdown_trigger'], 'shutdown.trigger')
    writeit(shutdown_trigger_path, 'shutdown')
    sleep(10)
    if os.path.isfile(shutdown_trigger_path) is True:
        os.remove(shutdown_trigger_path)
    print(f'AntiPetrosBot was shut down at {datetime.utcnow().strftime("%H:%M:%S on the %Y.%m.%d")}')


@cli.command(name='run')
@click.option('--token', '-t', default=None)
@click.option('--db-key', '-dbk', default=None)
def run(token, db_key):
    """
    [summary]

    [extended_summary]

    Args:
        token_file ([type]): [description]
        save_token_file ([type]): [description]
    """
    os.environ['INFO_RUN'] = "0"
    main(token=token, db_key=db_key)


def main(token=None, db_key=None):
    """
    Starts the Antistasi Discord Bot 'AntiPetros'.

    creates the bot, loads the extensions and starts the bot with the Token.
    """
    os.environ['INFO_RUN'] = "0"
    decrypt_db(db_key)
    anti_petros_bot = AntiPetrosBot(token=token, db_key=db_key)

    try:
        anti_petros_bot.run()
    finally:
        encrypt_db(db_key)


# endregion [Main_function]
# region [Main_Exec]
if __name__ == '__main__':
    print(f"{os.getenv('IS_DEV')=}")
    if os.getenv('IS_DEV') == 'true':
        load_dotenv('token.env')
        main(token=os.getenv('DISCORD_TOKEN'), db_key=os.getenv('DB_KEY'))
    else:
        main()


# endregion[Main_Exec]
