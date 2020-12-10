# region [Imports]

# * Standard Library Imports -->
import os

# * Third Party Imports -->
from gidconfig import ConfigHandler

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from antipetros_discordbot.utility.gidtools_functions import pathmaker


# endregion[Imports]


# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
glog.import_notification(log, __name__)

# endregion[Logging]

# region [Constants]

CONFIG_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_CONFIG = ConfigHandler(pathmaker(CONFIG_DIR, "base_config.ini"), interpolation=None)
COGS_CONFIG = ConfigHandler(pathmaker(CONFIG_DIR, 'cogs_config.ini'), interpolation=None)
# endregion[Constants]


# region[Main_Exec]

if __name__ == '__main__':
    pass

# endregion[Main_Exec]
