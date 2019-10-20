import Tkinter as tk

from theme import theme

import edmc_clog_utils as l_utils

ED_ORANGE = "#ff7100"

STATUS_INIT_TXT = "Initialized"
STATUS_INACTIVE_TXT = "Inactive (hardpoints deployed)"
STATUS_ACTIVE_TXT = "Active"
STATUS_CHECKING_TXT = "Checking..."

RES_INIT_TXT = "Waiting..."


class Gui(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, name="clog_container", *args, **kwargs)
        self.pack(anchor=tk.NW)
        theme.register(self)

        title = tk.Label(self, text="Combat Log Checks v{}".format(l_utils.APP_VER), fg="white")
        title.pack(anchor=tk.W)

        self.cmdr = None
        self.err_msg = None
        self.result = l_utils.NO_RESULTS

        self.status_label = tk.Label(self, text=STATUS_INIT_TXT)
        self.status_label.pack(anchor=tk.W)

        self.res_txt = RES_INIT_TXT
        self.res_col = ED_ORANGE
        self.res_label = tk.Label(self, text=self.res_txt)
        self.res_label.pack(anchor=tk.W)

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
        if self.result == l_utils.IS_CL:
            self.status_label['text'] = STATUS_ACTIVE_TXT
            self.res_label['text'] = "{} was reported".format(self.cmdr)
            self.res_label['fg'] = "red"

        elif self.result == l_utils.IS_NOT_CL:
            self.status_label['text'] = STATUS_ACTIVE_TXT
            self.res_label['text'] = "{} is clean".format(self.cmdr)
            self.res_label['fg'] = "green"

        elif self.result == l_utils.NO_RESULTS:
            self.status_label['text'] = STATUS_ACTIVE_TXT
            self.res_label['text'] = "{} not found".format(self.cmdr)
            self.res_label['fg'] = ED_ORANGE

        elif self.result == l_utils.IS_ERR:
            self.status_label['text'] = STATUS_ACTIVE_TXT
            self.res_label['text'] = self.err_msg
            self.res_label['fg'] = "red"

        else:
            self.status_label['text'] = STATUS_ACTIVE_TXT
            self.res_label['text'] = "Unknown Error"
            self.res_label['fg'] = "red"
