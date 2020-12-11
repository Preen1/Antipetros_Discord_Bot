from gidappdata import SupportKeeper
from gidappdata.cli.pack_and_bin_and_py_data import generate_user_data_binfile
from gidappdata.utility.extended_dotenv import find_dotenv_everywhere
import os
import checksumdir
import dotenv

dotenv.load_dotenv(find_dotenv_everywhere('project_meta_data.env'))

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(THIS_FILE_DIR, 'data_pack')
CONSTRUCTION_INFO_FILE = os.path.join(THIS_FILE_DIR, 'construction_info.env')
if os.path.isfile(os.path.join(THIS_FILE_DIR, "bin_data.py")) is True:
    from .bin_data import bin_archive_data


def has_new_data():
    _current_hash = os.getenv("CURRENT_DATA_DIR_HASH")
    _new_hash = checksumdir.dirhash(DATA_DIR)
    return _new_hash != _current_hash


if has_new_data():
    bin_archive_data = generate_user_data_binfile(THIS_FILE_DIR, os.getenv('PROJECT_NAME'), os.getenv('PROJECT_AUTHOR'))

if os.path.isfile(CONSTRUCTION_INFO_FILE):
    dotenv.load_dotenv(CONSTRUCTION_INFO_FILE)

if os.path.isfile('dev.trigger') is True:
    SupportKeeper.set_dev(True, DATA_DIR)
SupportKeeper.set_archive_data(bin_archive_data)
APPDATA = SupportKeeper.get_appdata()
