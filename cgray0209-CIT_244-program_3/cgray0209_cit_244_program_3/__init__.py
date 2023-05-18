"""CIT 244: Python II (4226_55Z1) - Program 3: Python & databases - sqlite3 and the wx.ListCtrl
"""

import dataclasses
import sqlite3
from contextlib import ExitStack, closing
from dataclasses import dataclass
from multiprocessing.resource_sharer import stop
from pathlib import Path
from typing import Optional

import wx

# Column = namedtuple("Column", ["name", "heading", "format", "width"])


@dataclass
class Column:
    """Information for storing and displaying a column of data"""

    name: str
    heading: str
    format: Optional[int]
    width: int
    type_: str


_columns = [
    Column("tid", "ID", None, 50, "INTEGER PRIMARY KEY"),
    Column("stop_date", "Stop Date", None, 100, "TEXT"),
    Column("stop_time", "Stop Time", None, 100, "TEXT"),
    Column("actual_speed", "Actual Speed", None, 100, "INTEGER"),
    Column("posted_speed", "Posted Speed", None, 100, "INTEGER"),
    Column("miles_over", "Miles Over", None, 100, "INTEGER"),
    Column("age", "Violator Age", None, 100, "INTEGER"),
    Column("violator_sex", "Violator Sex", None, 100, "TEXT"),
]


_db_path = Path("speeding_tickes.db")


@dataclass
class Ticket:
    """A speeding ticket"""

    tid: int
    stop_date: str
    stop_time: str
    actual_speed: int
    posted_speed: int
    miles_over: int
    age: int
    violator_sex: str


class TicketListFrame(wx.Frame):
    """Main application window

    +---------------------------------------------------+
    | "Citation Data"                                   |
    +---------------------------------------------------+
    |                   {List Control}                  |
    |                                                   |
    +---------------------------------------------------+
    |        [Display] [Insert Citation] [Close]        |
    +---------------------------------------------------+
    """

    def __init__(self, parent: Optional[wx.Window]):
        wx.Frame.__init__(self, parent, title="Traffic Tickets", size=(800, 600))

        panel = wx.Panel(self)

        self.ticket_list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT)
        for col_idx, col in enumerate(_columns):
            self.ticket_list_ctrl.InsertColumn(col_idx, col.heading, width=col.width)

        display_button = wx.Button(panel, label="Display")
        insert_button = wx.Button(panel, label="Insert Citation")
        close_button = wx.Button(panel, label="Close")
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(display_button, proportion=0, flag=wx.ALL, border=5)
        button_sizer.Add(insert_button, proportion=0, flag=wx.ALL, border=5)
        button_sizer.Add(close_button, proportion=0, flag=wx.ALL, border=5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(
            wx.StaticText(panel, label="Citation Data"),
            proportion=0,
            flag=wx.ALIGN_LEFT | wx.ALL,
            border=5,
        )
        sizer.Add(wx.StaticLine(panel), proportion=0, flag=wx.EXPAND)
        sizer.Add(self.ticket_list_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(wx.StaticLine(panel), proportion=0, flag=wx.EXPAND)
        sizer.Add(button_sizer, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

        display_button.Bind(wx.EVT_BUTTON, self.on_display_button)
        insert_button.Bind(wx.EVT_BUTTON, self.on_insert_button)
        close_button.Bind(wx.EVT_BUTTON, self.on_close_button)

        panel.SetSizerAndFit(sizer)

    def on_display_button(self, event: wx.CommandEvent):
        try:
            self.load_data()
        except sqlite3.Error as ex:
            error_modal = wx.MessageDialog(
                self, str(ex), "Database Error", wx.OK | wx.ICON_ERROR
            )
            error_modal.ShowModal()

    def load_data(self):
        """Load data from the database into the list control"""

        self.ticket_list_ctrl.DeleteAllItems()
        with ExitStack() as db_stack:  # auto-close
            con = db_stack.enter_context(closing(sqlite3.connect(_db_path)))
            # auto-commit/rollback
            db_stack.enter_context(con)
            cur = con.cursor()
            cur.execute("SELECT * FROM tickets")
            tickets = cur.fetchall()
            for row in tickets:
                self.ticket_list_ctrl.Append(row)

    def on_insert_button(self, event: wx.CommandEvent):
        """Open the insert ticket dialog, insert the ticket if the user clicks OK, and reload
        the data"""

        dialog = InsertTicketDialog(None)
        try:
            if dialog.ShowModal() == wx.ID_OK:
                input = (
                    dialog.tid_ctrl.GetValue(),
                    dialog.stop_date_ctrl.GetValue(),
                    dialog.stop_time_ctrl.GetValue(),
                    dialog.actual_speed_ctrl.GetValue(),
                    dialog.posted_speed_ctrl.GetValue(),
                    dialog.miles_over_ctrl.GetValue(),
                    dialog.age_ctrl.GetValue(),
                    dialog.violator_sex_ctrl.GetValue(),
                )
                if not all(input):
                    raise ValueError("Please enter all fields")
                ticket = Ticket(
                    int(dialog.tid_ctrl.GetValue()),
                    dialog.stop_date_ctrl.GetValue(),
                    dialog.stop_time_ctrl.GetValue(),
                    int(dialog.actual_speed_ctrl.GetValue()),
                    int(dialog.posted_speed_ctrl.GetValue()),
                    int(dialog.miles_over_ctrl.GetValue()),
                    int(dialog.age_ctrl.GetValue()),
                    dialog.violator_sex_ctrl.GetValue(),
                )
                self.insert_ticket(ticket)
            self.load_data()
        except sqlite3.Error as ex:
            error_modal = wx.MessageDialog(
                self, str(ex), "Database Error", wx.OK | wx.ICON_ERROR
            )
            error_modal.ShowModal()
        except ValueError as ex:
            error_modal = wx.MessageDialog(self, str(ex), "Input Error", wx.OK | wx.ICON_ERROR)
            error_modal.ShowModal()
        finally:
            dialog.Destroy()

    def insert_ticket(
        self,
        ticket: Ticket,
    ):
        """Insert a ticket into the database"""

        with ExitStack() as db_stack:  # auto-close
            con = db_stack.enter_context(closing(sqlite3.connect(_db_path)))
            # auto-commit/rollback
            db_stack.enter_context(con)
            con.execute(
                (
                    f"INSERT INTO tickets ({', '.join(col.name for col in _columns)})"
                    " VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                ),
                dataclasses.astuple(ticket),
            )

    def on_close_button(self, event: wx.CommandEvent):
        self.Close()


class InsertTicketDialog(wx.Dialog):
    """Dialog for inserting a new ticket into the database

    +------------------------------------------------------+
    | "Insert Citation"                                    |
    +------------------------------------------------------+
    |    Ticket Id: [        ]            Date: [        ] |
    |         Time: [        ]    Actual Speed: [        ] |
    | Posted Speed: [        ]        MPH Over: [        ] |
    |          Age: [        ]             Sex: [        ] |
    |  [ Insert ] [ Cancel ]                               |
    +------------------------------------------------------+
    """

    def __init__(self, parent: Optional[wx.Window]):
        wx.Dialog.__init__(self, parent, title="Insert Citation", size=(600, 400))

        panel = wx.Panel(self)

        tid_label = wx.StaticText(panel, label="Ticket Id:")
        self.tid_ctrl = wx.TextCtrl(panel)
        stop_date_label = wx.StaticText(panel, label="Date:")
        self.stop_date_ctrl = wx.TextCtrl(panel)
        stop_time_label = wx.StaticText(panel, label="Time:")
        self.stop_time_ctrl = wx.TextCtrl(panel)
        actual_speed_label = wx.StaticText(panel, label="Actual Speed:")
        self.actual_speed_ctrl = wx.TextCtrl(panel)
        posted_speed_label = wx.StaticText(panel, label="Posted Speed:")
        self.posted_speed_ctrl = wx.TextCtrl(panel)
        miles_over_label = wx.StaticText(panel, label="MPH Over:")
        self.miles_over_ctrl = wx.TextCtrl(panel)
        age_label = wx.StaticText(panel, label="Age:")
        self.age_ctrl = wx.TextCtrl(panel)
        violator_sex_label = wx.StaticText(panel, label="Sex:")
        self.violator_sex_ctrl = wx.TextCtrl(panel)
        input_sizer = wx.FlexGridSizer(rows=4, cols=4, hgap=5, vgap=5)
        input_sizer.AddMany(
            [
                (tid_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
                (self.tid_ctrl, 0, wx.EXPAND),
                (stop_date_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
                (self.stop_date_ctrl, 0, wx.EXPAND),
                (stop_time_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
                (self.stop_time_ctrl, 0, wx.EXPAND),
                (actual_speed_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
                (self.actual_speed_ctrl, 0, wx.EXPAND),
                (posted_speed_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
                (self.posted_speed_ctrl, 0, wx.EXPAND),
                (miles_over_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
                (self.miles_over_ctrl, 0, wx.EXPAND),
                (age_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
                (self.age_ctrl, 0, wx.EXPAND),
                (violator_sex_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
                (self.violator_sex_ctrl, 0, wx.EXPAND),
            ]
        )

        apply_button = wx.Button(panel, id=wx.ID_OK, label="Insert")
        cancel_button = wx.Button(panel, id=wx.ID_CANCEL, label="Cancel")
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(apply_button, proportion=0, flag=wx.ALL, border=5)
        button_sizer.Add(cancel_button, proportion=0, flag=wx.ALL, border=5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(
            wx.StaticText(panel, label="Insert Citation"),
            proportion=0,
            flag=wx.ALIGN_LEFT | wx.ALL,
            border=5,
        )
        sizer.Add(wx.StaticLine(panel), proportion=0, flag=wx.EXPAND)
        sizer.Add(
            input_sizer,
            proportion=0,
            flag=wx.ALIGN_CENTER | wx.ALL,
            border=5,
        )
        sizer.Add(button_sizer, proportion=0, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

        panel.SetSizerAndFit(sizer)


def create_tables():
    """Create the database tables if they don't already exist"""

    with ExitStack() as db_stack:  # auto-close
        con = db_stack.enter_context(closing(sqlite3.connect(_db_path)))
        # auto-commit/rollback
        db_stack.enter_context(con)
        con.execute(
            f"CREATE TABLE IF NOT EXISTS tickets ({', '.join(f'{col.name} {col.type_}' for col in _columns)})"
        )


class TicektApp(wx.App):
    """Main application class"""

    def OnInit(self):
        """Called when the application is initialized"""

        create_tables()
        frame = TicketListFrame(None)
        self.SetTopWindow(frame)
        frame.Show()
        return True


def main():
    """Entry point for the application script"""
    app = TicektApp()
    app.MainLoop()


if __name__ == "__main__":
    main()
