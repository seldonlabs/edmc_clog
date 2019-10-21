import plug

import edmc_clog_utils as l_utils
import edmc_clog_net as l_net
import edmc_clog_gui as l_gui

_flag_status = 0
_hardpoints_deployed = False
_gui = None


def plugin_start():
    print "Starting {} v{}".format(l_utils.APP_NAME, l_utils.APP_VER)
    return l_utils.APP_NAME


def plugin_app(parent):
    global _gui
    _gui = l_gui.Gui(parent)

    return _gui


def dashboard_entry(cmdr, is_beta, entry):
    global _gui
    global _hardpoints_deployed
    global _flag_status

    if not is_beta:
        flags = entry['Flags']
        _is_in_SC = flags & plug.FlagsSupercruise

        # not in SC
        if not _is_in_SC:
            _hardpoints_deployed = flags & plug.FlagsHardpointsDeployed
            if _hardpoints_deployed:
                if _flag_status + 64 == flags:
                    _gui.set_status_inactive()
                _flag_status = flags
            else:
                if _flag_status - 64 == flags:
                    _gui.set_status_active()
                _flag_status = flags


def journal_entry(cmdr, is_beta, system, station, entry, state):
    global _gui
    global _hardpoints_deployed

    if not is_beta:
        if l_utils.is_mode() and not _hardpoints_deployed:
            if l_utils.is_scanned(entry):
                coded_pilot_name = entry['PilotName'].split(':')

                if coded_pilot_name[0] == "$cmdr_decorate":
                    search_name = coded_pilot_name[1][6:-1]
                    pilot_name_localised = entry['PilotName_Localised']

                    _gui.set_status_checking()
                    res = l_net.call_service(search_name)

                    if type(res) is str:
                        _gui.result = l_utils.IS_ERR
                        _gui.err_msg = res
                    elif type(res) is dict:
                        _gui.cmdr = pilot_name_localised
                        t = l_utils.is_clog(res)
                        _gui.result = t[0]
                        _gui.report_url = t[1]
                    else:
                        _gui.result = l_utils.IS_UNK_ERR

                    _gui.after(500, _gui.set_response_label)


def plugin_stop():
    print "Stopping {}".format(l_utils.APP_NAME)
