import webbrowser
import Tkinter as tk

from theme import theme

import edmc_clog_utils as l_utils

ED_ORANGE = "#ff7100"

STATUS_INIT_TXT = "Initialized"
STATUS_INACTIVE_TXT = "Inactive (hardpoints deployed)"
STATUS_ACTIVE_TXT = "Active"
STATUS_CHECKING_TXT = "Checking..."

CMDR_INIT_TXT = "No Cmdr"
RES_INIT_TXT = "No Report"


class ResBtn(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.grid(row=0, column=1)
        theme.register(self)
        self['bd'] = 0

    def set_is_cl(self):
        self['text'] = "Check Report"
        self['fg'] = "red"
        self['bd'] = 1
        self['state'] = tk.NORMAL

    def set_not_cl(self):
        self['text'] = "Clean"
        self['disabledforeground'] = "green"
        self['bd'] = 0
        self['state'] = tk.DISABLED

    def set_no_results(self):
        self['text'] = RES_INIT_TXT
        self['disabledforeground'] = ED_ORANGE
        self['bd'] = 0
        self['state'] = tk.DISABLED

    def set_err_msg(self, err_msg):
        self['text'] = err_msg
        self['disabledforeground'] = "red"
        self['bd'] = 0
        self['state'] = tk.DISABLED


class Gui(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, name="clog_container", *args, **kwargs)
        self.pack(anchor=tk.NW)
        theme.register(self)

        # state
        self.cmdr = CMDR_INIT_TXT
        self.err_msg = None
        self.result = l_utils.NO_RESULTS
        self.res_txt = RES_INIT_TXT
        self.res_col = ED_ORANGE
        self.report_url = "http://"

        # header
        header = tk.Frame(self)
        header.pack(anchor=tk.NW)

        tk.Label(header, text="CLogs v{}".format(l_utils.APP_VER)).grid(row=0, column=0)

        self.status_label = tk.Label(header, text=STATUS_INIT_TXT, fg=ED_ORANGE, bg="black")
        self.status_label.grid(row=0, column=1)

        # result
        result = tk.Frame(self)
        result.pack(anchor=tk.NW)

        self.cmdr_label = tk.Label(result, text=self.cmdr)
        self.cmdr_label.grid(row=0, column=0)

        self.res_btn = ResBtn(result, text=self.res_txt, state=tk.DISABLED, bg="black", command=self.__report_callback)
        self.res_btn.grid(row=0, column=1, padx=5, pady=5)

    def __report_callback(self):
        webbrowser.open_new_tab(self.report_url)

    def set_status_inactive(self):
        self.status_label['text'] = STATUS_INACTIVE_TXT
        self.status_label['fg'] = "red"

    def set_status_active(self):
        self.status_label['text'] = STATUS_ACTIVE_TXT
        self.status_label['fg'] = "green"

    def set_status_checking(self):
        self.status_label['text'] = STATUS_CHECKING_TXT
        self.status_label['fg'] = ED_ORANGE

    def set_response_label(self):
        self.set_status_active()
        self.cmdr_label['text'] = self.cmdr

        if self.result == l_utils.IS_CL_REDDIT:
            self.res_btn.set_is_cl()

        elif self.result == l_utils.IS_NOT_CL:
            self.res_btn.set_not_cl()

        elif self.result == l_utils.NO_RESULTS:
            self.res_btn.set_no_results()

        elif self.result == l_utils.IS_ERR:
            self.res_btn.set_err_msg(self.err_msg)

        else:
            self.res_btn.set_err_msg("Unknown Error")
