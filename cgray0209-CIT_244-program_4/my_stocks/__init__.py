import array
import datetime
import sqlite3
import sys
from typing import Optional

import requests
import wx

DEFAULT_API_KEY = "dEfAuLtApIkEy"


# main frame
class StockListFrame(wx.Frame):
    """Main frame for the application.

    ::

        +-------------------------------------------------------------------------------------+
        | My Stocks                                                              [🗕] [🗖] [🗙] |
        +-------------------------------------------------------------------------------------+
        |                            Date: { today's date and time }                          |
        |                            Net gain/loss: { total }                                 |
        |                                                                                     |
        | +------------------+--------+----------------+---------------+--------+-----------+ |
        | | Company          | Symbol | Purchase Price | Current Price | Shares | Gain/Loss | |
        | +------------------+--------+----------------+---------------+--------+-----------+ |
        | | 3M               | MMM    |         157.50 |        169.26 |    100 |   1176.00 | |
        | | Apple Inc.       | AAPL   |         102.40 |        115.00 |    100 |   1260.00 | |
        | | Boeing           | BA     |         157.20 |        167.22 |    200 |   2004.00 | |
        | | Caterpillar Inc. | CAT    |         162.35 |        167.96 |    200 |   1122.00 | |
        | | Cisco Systems    | CSCO   |          35.75 |         38.82 |    100 |    307.00 | |
        | | Honeywell        | HON    |         180.25 |        174.56 |    100 |   -569.00 | |
        | | IBM              | IBM    |         111.45 |        115.96 |    300 |   1353.00 | |
        | | Intel            | INTC   |          66.10 |         48.08 |    200 |  -3604.00 | |
        | | Microsoft        | MSFT   |         177.80 |        215.35 |    100 |   3755.00 | |
        | |                  |        |                |               |        |           | |
        | +------------------+--------+----------------+---------------+--------+-----------+ |
        |                                                                                     |
        |                          [ Display Data ] [    Cancel    ]                          |
        |                                                                                     |
        +-------------------------------------------------------------------------------------+

        - two labels at the top, one will display the current date and one will display the net
          gain and loss calculated for all 9 stocks in the database table named `dow_stocks`
          when the button is clicked.
        - a regular list control with 6 columns: "Company", "Symbol", "Purchase Price", "Current
          Price", "Shares", "Gain/Loss"
        - a row of buttons. the "Display Data" button causes code to query the database and get
          the company, symbol, purchase price, and number of shares. That same code needs to
          make a request to finnhub to get the current price of each of the 9 stocks. Then using
          the number of shares, the purchase price, and the current price, calculate the gain or
          loss for each of the 9 stocks and display those values.
    """

    def __init__(self, parent: Optional[wx.Window], api_key: str):
        wx.Frame.__init__(self, parent, title="My Stocks", size=(800, 600))
        self.api_key = api_key

        panel = wx.Panel(self)

        # create Date and Net Gain/Loss labels
        date_label = wx.StaticText(panel, label="Date:", style=wx.ALIGN_RIGHT)
        self.date_value = wx.StaticText(panel, label="")
        net_gain_loss_label = wx.StaticText(panel, label="Net gain/loss:", style=wx.ALIGN_RIGHT)
        self.net_gain_loss_value = wx.StaticText(panel, label="")

        # create list control
        self.list_ctrl = wx.ListCtrl(
            panel,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN,
        )
        self.list_ctrl.InsertColumn(0, "Company", width=150)
        self.list_ctrl.InsertColumn(1, "Symbol", width=75)
        self.list_ctrl.InsertColumn(2, "Purchase Price", width=100)
        self.list_ctrl.InsertColumn(3, "Current Price", width=100)
        self.list_ctrl.InsertColumn(4, "Shares", width=75)
        self.list_ctrl.InsertColumn(5, "Gain/Loss", width=100)

        # create buttons
        display_data_button = wx.Button(panel, label="Display Data")
        cancel_button = wx.Button(panel, label="Cancel")

        # create sizers
        date_sizer = wx.BoxSizer(wx.HORIZONTAL)
        date_sizer.Add(date_label, 0, wx.ALL, 5)
        date_sizer.Add(self.date_value, 0, wx.ALL, 5)

        net_gain_loss_sizer = wx.BoxSizer(wx.HORIZONTAL)
        net_gain_loss_sizer.Add(net_gain_loss_label, 0, wx.ALL, 5)
        net_gain_loss_sizer.Add(self.net_gain_loss_value, 0, wx.ALL, 5)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(display_data_button, 0, wx.ALL, 5)
        button_sizer.Add(cancel_button, 0, wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(date_sizer, 0, wx.ALL, 5)
        main_sizer.Add(net_gain_loss_sizer, 0, wx.ALL, 5)
        main_sizer.Add(self.list_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # bind events
        display_data_button.Bind(wx.EVT_BUTTON, self.on_display_data)
        cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

        # main_sizer.SetSizeHints(panel)
        panel.SetSizer(main_sizer)

    def on_display_data(self, event: wx.CommandEvent) -> None:
        """Display data in list control."""
        self.list_ctrl.DeleteAllItems()
        self.date_value.SetLabel(datetime.datetime.now().strftime("%Y-%m-%d"))
        self.net_gain_loss_value.SetLabel("0.00")

    def on_cancel(self, event: wx.CommandEvent) -> None:
        """Close the frame, terminating the application."""
        self.Close(True)


class MyStocksApp(wx.App):
    def __init__(self, api_key: str):
        self.api_key = api_key
        super().__init__()

    def OnInit(self) -> bool:
        frame = StockListFrame(None, api_key=self.api_key)
        self.SetTopWindow(frame)
        frame.Show()
        return True


def main(argv: Optional[list[str]] = None) -> int:
    import argparse  # pylint: disable=import-outside-toplevel

    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser()
    # get api key from command line
    parser.add_argument(
        "-k",
        "--key",
        dest="api_key",
        help="finnhub API key",
        required=True,
        default=DEFAULT_API_KEY,
    )
    options = parser.parse_args(argv[1:])

    app = MyStocksApp(api_key=options.api_key)
    app.MainLoop()

    return 0


if __name__ == "__main__":
    try:
        rc = main(sys.argv)
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error: {e}", file=sys.stderr)
        rc = 1
    sys.exit(rc)
