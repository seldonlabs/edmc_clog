import re
from monitor import monitor

APP_NAME = "EDMC Clog"
APP_VER = "0.3.0"

# response flags
IS_CL_BOT = 1
IS_CL_REDDIT = 2
IS_CL_RINZLER = 3
IS_NOT_CL = 4

# err flags
NO_RESULTS = 5
IS_ERR = 6
IS_UNK_ERR = 7

REDDIT_PATTERN = '(https?://.*)\)'


def is_mode():
    return monitor.mode.lower() == 'open'


def is_target_locked(entry):
    return entry['event'] == 'ShipTargeted' and entry['TargetLocked']


def is_target_unlocked(entry):
    return not entry['event'] == 'ShipTargeted' and entry['TargetLocked']


def is_scanned(entry):
    return "ScanStage" in entry and entry['ScanStage'] > 1


def is_cmdr(pilot_name):
    return pilot_name[0] == "$cmdr_decorate"


def is_text_cmd(entry):
    return entry['event'] == 'SendText' and entry['Message'].strip().startswith('/clog')


def is_clog(res):
    try:
        if res['DBdata']:
            if res['DBdata']['CombatLogger_bot'] != "":
                return IS_CL_BOT, res['DBdata']['CombatLogger_bot']

            elif res['DBdata']['CombatLogger_reddit'] != "":
                return IS_CL_REDDIT, re.search(REDDIT_PATTERN, res['DBdata']['CombatLogger_reddit']).group(1)

            elif res['DBdata']['CombatLogger_rinzler'] != "":
                return IS_CL_RINZLER, res['DBdata']['CombatLogger_rinzler']

            else:
                return IS_NOT_CL, ""
        else:
            return NO_RESULTS, ""

    except AttributeError:
        return IS_ERR, "Regex Err"
