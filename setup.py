from setuptools import setup, find_packages
import os


# region[Constants]
ANTIPETROSDISCORDBOT_AUTHOR = ['Giddius']
ANTIPETROSDISCORDBOT_SHORT_DESCRIPTION = 'WiP'
ANTIPETROSDISCORDBOT_LONG_DESCRIPTION_FILE = 'README.md'
ANTIPETROSDISCORDBOT_VERSION = "0.1.0"
ANTIPETROSDISCORDBOT_LICENSE = 'MIT'
ANTIPETROSDISCORDBOT_ENTRY_POINTS = {}
ANTIPETROSDISCORDBOT_URL = ''
ANTIPETROSDISCORDBOT_REQUIREMENTS_FILE = 'requirements.txt'
# endregion[Constants]


def get_dependencies():
    # sourcery skip: inline-immediately-returned-variable, list-comprehension
    _out = []
    if os.path.isfile(ANTIPETROSDISCORDBOT_REQUIREMENTS_FILE) is True:
        with open(ANTIPETROSDISCORDBOT_REQUIREMENTS_FILE, 'r', errors='replace') as fileobject:
            _temp_list = fileobject.read().splitlines()

        for line in _temp_list:
            if line != '' and line.startswith('#') is False:
                _out.append(line)
    return _out


def get_long_description_type():
    _type_dict = {
        'md': 'text/markdown',
        'rst': 'text/x-rst',
        'txt': 'text/plain'
    }
    _ext = ANTIPETROSDISCORDBOT_LONG_DESCRIPTION_FILE.split('.')[-1]
    return _type_dict.get(_ext, 'text/plain')


def get_version():
    return ANTIPETROSDISCORDBOT_VERSION


def get_short_description():
    return ANTIPETROSDISCORDBOT_SHORT_DESCRIPTION


def get_long_description():
    with open(ANTIPETROSDISCORDBOT_LONG_DESCRIPTION_FILE, 'r', errors='replace') as fileobject:
        _out = fileobject.read()
    return _out


def get_url():
    return ANTIPETROSDISCORDBOT_URL


def get_author():
    with open('LICENSE', 'r') as lic_file:
        _first_line = lic_file.readline()
    if 'MIT' in _first_line:
        return 'MIT'
    else:
        return ANTIPETROSDISCORDBOT_AUTHOR


def get_license():
    return ANTIPETROSDISCORDBOT_LICENSE


def get_entry_points():
    return ANTIPETROSDISCORDBOT_ENTRY_POINTS


setup(name='antipetros_discordbot',
      version=get_version(),
      description=get_short_description(),
      long_description=get_long_description(),
      long_description_content_type=get_long_description_type(),
      url=get_url(),
      author=get_author(),
      license=get_license(),
      packages=find_packages(),
      install_requires=get_dependencies(),
      include_package_data=True,
      entry_points=get_entry_points(),
      options={"bdist_wheel": {"universal": True}}
      )
