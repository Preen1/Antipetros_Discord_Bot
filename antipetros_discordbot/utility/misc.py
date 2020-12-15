from functools import wraps, partial
from asyncio import get_event_loop
from concurrent.futures import ThreadPoolExecutor
import os
from antipetros_discordbot.utility.gidtools_functions import pathmaker, loadjson, writejson, readit, readbin, writeit, work_in, writebin
import gidlogger as glog
log = glog.aux_logger(__name__)
glog.import_notification(log, __name__)

SECOND_FACTOR = 1
MINUTE_FACTOR = SECOND_FACTOR * 60
HOUR_FACTOR = MINUTE_FACTOR * 60

DAY_FACTOR = HOUR_FACTOR * 24
WEEK_FACTOR = DAY_FACTOR * 7
MONTH_FACTOR = DAY_FACTOR * 30
YEAR_FACTOR = DAY_FACTOR * 365

FACTORS = {'years': YEAR_FACTOR, 'months': MONTH_FACTOR, 'weeks': WEEK_FACTOR, 'days': DAY_FACTOR, 'hours': HOUR_FACTOR, 'minutes': MINUTE_FACTOR, 'seconds': SECOND_FACTOR}
EXECUTOR = ThreadPoolExecutor(thread_name_prefix='Thread', max_workers=4)
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


def seconds_to_pretty(seconds: int):
    out_string = ''
    rest = seconds
    for name, factor in FACTORS.items():
        sub_result, rest = divmod(rest, factor)
        if sub_result != 0:
            out_string += f"**{name.title()}:** {str(sub_result)} | "
    return out_string


def sync_to_async(_func):
    @wraps(_func)
    def wrapped(*args, **kwargs):
        loop = get_event_loop()
        func = partial(_func, *args, **kwargs)
        return loop.run_in_executor(executor=EXECUTOR, func=func)
    return wrapped


def save_commands(cog):
    command_json_file = pathmaker('../docs/commands.json')
    command_json = loadjson(command_json_file)
    command_json[str(cog)] = {'file_path': pathmaker(os.path.abspath(__file__)),
                              'description': __doc__,
                              'commands': {(com.name + ' ' + com.signature).replace('<ctx>', '').replace('  ', ' ').strip(): com.help for com in cog.get_commands()}}
    writejson(command_json, command_json_file, indent=4)
    log.debug("commands for %s saved to %s", cog, command_json_file)
