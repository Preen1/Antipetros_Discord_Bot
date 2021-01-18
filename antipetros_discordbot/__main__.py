# region [Module_Docstring]

"""
Main module, starts the Antistasi Discord Bot.

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

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot import MAIN_DIR
from antipetros_discordbot.utility.misc import check_if_int
from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot
from antipetros_discordbot.utility.token_handling import load_tokenfile, store_token_file
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

_log_file = glog.log_folderer(__name__, APPDATA)
log_stdout = 'both' if BASE_CONFIG.getboolean('logging', 'log_also_to_stdout') is True else 'file'
if os.getenv('IS_DEV') == 'true':
    log_stdout = 'both'
log = glog.main_logger(_log_file, BASE_CONFIG.get('logging', 'logging_level'), other_logger_names=['asyncio', 'gidsql', 'gidfiles', "gidappdata"], log_to=log_stdout, in_back_up=BASE_CONFIG.getint('logging', 'amount_keep_old_logs'))
log.info(glog.NEWRUN())
if BASE_CONFIG.getboolean('logging', 'use_logging') is False:
    logging.disable(logging.CRITICAL)
if os.getenv('IS_DEV') == 'yes':
    log.warning('!!!!!!!!!!!!!!!!!!! IS DEV !!!!!!!!!!!!!!!!!!!')
    log.warning('!!!!!!!!!!!!!!!!! DEBUG MODE !!!!!!!!!!!!!!!!!')
# endregion[Logging]


# region [Helper]


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


# endregion [Helper]

# region [Main_function]

@click.group()
def cli():
    pass


@cli.command(name='create_alias_data')
def command_alias_run():
    _out = {}
    anti_petros_bot = AntiPetrosBot(command_prefix='$$', self_bot=False, activity=AntiPetrosBot.activity_from_config(), intents=get_intents())
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
    anti_petros_bot = AntiPetrosBot(command_prefix='$$', self_bot=False, activity=AntiPetrosBot.activity_from_config(), intents=get_intents())
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
    os.environ['INFO_RUN'] = "1"
    anti_petros_bot = AntiPetrosBot(command_prefix='$$', self_bot=False, activity=AntiPetrosBot.activity_from_config(), intents=get_intents())


@cli.command(name='stop')
def stop():
    shutdown_trigger_path = pathmaker(APPDATA['shutdown_trigger'], 'shutdown.trigger')
    writeit(shutdown_trigger_path, 'shutdown')
    sleep(10)
    if os.path.isfile(shutdown_trigger_path) is True:
        os.remove(shutdown_trigger_path)
    print(f'AntiPetrosBot was shut down at {datetime.utcnow().strftime("%H:%M:%S on the %Y.%m.%d")}')


@cli.command(name='run')
@click.option('--token_file', '-t', default=None)
@click.option('--save-token-file/--dont-save-token-file', '-save/-nosave', default=False)
def run(token_file, save_token_file):
    os.environ['INFO_RUN'] = "0"
    main(token_file, save_token_file)


def main(token_file=None, save_token_file=False):
    """
    Starts the Antistasi Discord Bot 'AntiPetros'.

    creates the bot, loads the extensions and starts the bot with the Token.
    """
    os.environ['INFO_RUN'] = "0"
    if token_file is not None and save_token_file is True:
        store_token_file(token_file)

    token_file = pathmaker(APPDATA["user_env_files"], 'token.env') if token_file is None else pathmaker(token_file)
    with load_tokenfile(token_file):
        discord_token = os.getenv('DISCORD_TOKEN')
        decrypt_db()

    anti_petros_bot = AntiPetrosBot(command_prefix='$$', self_bot=False, activity=AntiPetrosBot.activity_from_config(), intents=get_intents())

    try:
        anti_petros_bot.run(discord_token, bot=True, reconnect=True)
    finally:
        discord_token = 'xxxxxxxxxxxxxxxx'
        encrypt_db()


# endregion [Main_function]
# region [Main_Exec]
if __name__ == '__main__':
    if os.getenv('IS_DEV') == 'true':
        main(pathmaker(MAIN_DIR, 'token.env'))
    else:
        main()


# endregion[Main_Exec]
