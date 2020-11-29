# region [Imports]

# * Standard Library Imports -->
from datetime import datetime
# * Third Party Imports -->
from discord.ext import commands
from async_property import async_property

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.data.config.config_singleton import BASE_CONFIG

# endregion[Imports]

__updated__ = '2020-11-29 03:00:10'

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
        self.start_time = datetime.utcnow()
        self.max_message_length = 2000

    @property
    def is_debug(self):
        return BASE_CONFIG.getboolean('general_settings', 'is_debug')

    @property
    def blacklist_user(self):
        return list(map(int, BASE_CONFIG.getlist('blacklist', 'user')))

    @property
    def contact_user(self):
        return BASE_CONFIG.get('blacklist', 'contact_user')

    async def retrieve_member(self, guild_id, user_id):
        guild = self.get_guild(guild_id)
        return await guild.fetch_member(user_id)

    async def split_to_messages(self, ctx, message, split_on='\n'):
        _out = ''
        print(len(message))
        chunks = message.split(split_on)
        max_index = len(chunks) - 1
        for chunk in chunks:
            if sum(map(len, _out)) < self.max_message_length:
                _out += chunk + split_on
            else:
                print(len(_out))
                await ctx.send(_out)
                _out = ''
        await ctx.send(_out)


# region[Main_Exec]
if __name__ == '__main__':
    pass

# endregion[Main_Exec]
