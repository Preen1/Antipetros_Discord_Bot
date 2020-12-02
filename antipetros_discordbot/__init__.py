"""
A Discord Bot for the Antistasi (ArmA 3) Community Discord Server
"""
__version__ = "0.1"

# * Standard Library Imports -->

# * Third Party Imports -->
from dotenv import load_dotenv

load_dotenv()
# os.environ['PYTHONASYNCIODEBUG'] = '1'


def last_updated(as_datetime=False):
    import os
    import re
    from datetime import datetime
    from functools import partial
    collected_times = []
    this_file_dir = os.path.abspath(os.path.dirname(__file__))
    last_updated_regex = re.compile(r"(?P<updatetime>(?<=__updated__ \= ').*(?='))")
    for dirname, folderlist, filelist in os.walk(this_file_dir):
        for file in filelist:
            if file.endswith('.py'):
                with open(os.path.join(dirname, file), 'r') as pyfile:
                    regex_result = last_updated_regex.search(pyfile.read())
                    if regex_result:
                        collected_times.append(regex_result.groupdict()['updatetime'])

    collected_times = list(map(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"), collected_times))
    latest_time = max(collected_times)
    if as_datetime is True:
        return latest_time
    return latest_time.strftime("%Y-%m-%d %H:%M:%S")


__stmt = "Last Updated: " + str(last_updated())
print('~' * (52 + len(__stmt)))
print('~' * 25 + ' ' + __stmt + ' ' + '~' * 25)
print('~' * (52 + len(__stmt)))
