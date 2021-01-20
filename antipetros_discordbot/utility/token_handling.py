"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import shutil
from contextlib import contextmanager

# * Third Party Imports --------------------------------------------------------------------------------->
from dotenv import load_dotenv

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.utility.gidtools_functions import pathmaker
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper

# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]


# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)


# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')

TOKEN_TO_CLEAR = ['GITHUB_TOKEN', 'DISCORD_TOKEN']

# endregion[Constants]


def store_token_file(token_file):
    _new_path = pathmaker(APPDATA['user_env_files'], 'token.env')
    if os.path.isfile(_new_path) is True:
        os.remove(_new_path)
    shutil.copy(pathmaker(os.path.abspath(token_file)), _new_path)


@contextmanager
def load_tokenfile(file):
    load_dotenv(file)
    yield
    for token_name in TOKEN_TO_CLEAR:
        if token_name in os.environ:
            os.environ[token_name] = "xxxxxxxxxxxxx"


# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
