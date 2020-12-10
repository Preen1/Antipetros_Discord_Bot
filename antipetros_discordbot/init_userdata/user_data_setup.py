from gidappdata import SupportKeeper
import os
from .bin_data import bin_archive_data

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


SupportKeeper.set_dev(True, os.path.join(THIS_FILE_DIR, 'data_pack'))
SupportKeeper.set_archive_data(bin_archive_data)
APPDATA = SupportKeeper.get_appdata()
