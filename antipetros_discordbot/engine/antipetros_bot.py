# region [Imports]

# * Standard Library Imports -->

# * Third Party Imports -->
from discord.ext import commands

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG

# endregion[Imports]

__updated__ = '2020-11-27 00:25:50'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class AntiPetrosBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blacklist_user = BASE_CONFIG.getlist('blacklist', 'user')
        self.is_debug = BASE_CONFIG.getboolean('general_settings', 'is_debug')

    async def retrieve_member(self, guild_id, user_id):
        guild = self.get_guild(guild_id)
        return await guild.fetch_member(user_id)


# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
