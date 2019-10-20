from monitor import monitor

APP_NAME = "EDMC Clog"
APP_VER = "0.1.0"

IS_CL = 1
IS_NOT_CL = 2
NO_RESULTS = 3
IS_ERR = 4
IS_UNK_ERR = 5

def is_mode():
    """
    Check for open mode
    :return:
    """
    return monitor.mode.lower() == 'open'


def is_target_locked(entry):
    """
    Check if an event is a ShipTargeted and a TargetLocked is true
    :param entry:
    :return:
    """
    return entry['event'] == 'ShipTargeted' and entry['TargetLocked']


def is_target_unlocked(entry):
    """
    Check if an event is a ShipTargeted and a TargetLocked is false
    :param entry:
    :return:
    """
    return not entry['event'] == 'ShipTargeted' and entry['TargetLocked']


def is_scanned(entry):
    """
    Check for a scan stage, 2 for scanning, 3 for scanned
    :param entry:
    :return:
    """
    return entry['ScanStage'] == 3


def notify(msg):
    """
    log message
    :param msg:
    :return:
    """
    print(u"{}: {}".format(APP_NAME, msg))


def warn(msg):
    """
    warning log message
    :param msg:
    :return:
    """
    print(u"{}: [WARNING] {}".format(APP_NAME, msg))


def format_bool(v):
    return 'Y' if v else 'N'


def is_clog(res):
    if res['DBdata']:
        if res['DBdata']['CombatLogger_bot'] != "" or \
                res['DBdata']['CombatLogger_reddit'] != "" or \
                res['DBdata']['CombatLogger_rinzler'] != "":
            return IS_CL
        else:
            return IS_NOT_CL
    else:
        return NO_RESULTS
