"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
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

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


def user_not_blacklisted(bot, logger):
    async def predicate(ctx):
        if bot.is_blacklisted(ctx.author):
            logger.warning('Tried invocation by blacklisted user: "%s", id: "%s"', ctx.author.name, str(ctx.author.id))
            await bot.command_call_blocked(ctx)

            return False

        return True
    return bot.add_check(predicate)


# region[Main_Exec]
if __name__ == '__main__':
    pass

# endregion[Main_Exec]
