import datetime
import locale
import sqlite3
import sys
from contextlib import ExitStack
from pathlib import Path
from typing import Optional

import requests
import wx

DEFAULT_API_KEY = "dEfAuLtApIkEy"
DEFAULT_DB_PATH = Path("tech_stocks.db")
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


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

    def __init__(self, parent: Optional[wx.Window], api_key: str, db_path: Path):
        self.api_key = api_key
        self.db_path = db_path
        wx.Frame.__init__(self, parent, title="My Stocks", size=(800, 600))

        panel = wx.Panel(self)

        # create Date and Net Gain/Loss labels
        datetime_label = wx.StaticText(panel, label="Last updated:", style=wx.ALIGN_RIGHT)
        self.datetime_value = wx.StaticText(panel, label="")
        net_gain_loss_label = wx.StaticText(panel, label="Net gain/loss:", style=wx.ALIGN_RIGHT)
        self.net_gain_loss_value = wx.StaticText(panel, label="")

        # create list control
        self.list_ctrl = wx.ListCtrl(
            panel,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN,
        )
        self.list_ctrl.InsertColumn(0, "Company", width=150)
        self.list_ctrl.InsertColumn(1, "Symbol", width=75)
        self.list_ctrl.InsertColumn(2, "Purchase Price", format=wx.LIST_FORMAT_RIGHT, width=125)
        self.list_ctrl.InsertColumn(3, "Current Price", format=wx.LIST_FORMAT_RIGHT, width=125)
        self.list_ctrl.InsertColumn(4, "Shares", format=wx.LIST_FORMAT_RIGHT, width=100)
        self.list_ctrl.InsertColumn(5, "Gain/Loss", format=wx.LIST_FORMAT_RIGHT, width=125)

        # create buttons
        display_data_button = wx.Button(panel, label="Display Data")
        cancel_button = wx.Button(panel, label="Cancel")

        # create sizers
        date_sizer = wx.BoxSizer(wx.HORIZONTAL)
        date_sizer.Add(datetime_label, 0, wx.ALL, 5)
        date_sizer.Add(self.datetime_value, 0, wx.ALL, 5)

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
        self.datetime_value.SetLabel(datetime.datetime.now().strftime("%A, %B %d, %Y %H:%M"))
        total_gain_loss = 0.0
        # connect to the db
        with ExitStack() as db_stack:
            # auto-close
            con = db_stack.enter_context(sqlite3.connect(self.db_path))
            # auto-commit/rollback
            db_stack.enter_context(con)
            cur = con.cursor()
            cur.row_factory = sqlite3.Row  # type: ignore
            cur.execute("SELECT * FROM dow_stocks")
            rows: list[sqlite3.Row] = cur.fetchall()
            for row in rows:
                current_price = get_current_price(self.api_key, row["symbol"])
                gain_loss: Optional[float] = (
                    (current_price - row["purchase_price"]) * row["shares"]
                    if current_price is not None
                    else None
                )
                total_gain_loss += gain_loss or 0.0
                self.list_ctrl.Append(
                    (
                        row["company"],
                        row["symbol"],
                        locale.currency(row["purchase_price"], grouping=True),
                        (
                            locale.currency(current_price, grouping=True)
                            if current_price is not None
                            else "unavailable"
                        ),
                        f"{row['shares']:,}",
                        (
                            locale.currency(gain_loss, grouping=True)
                            if gain_loss is not None
                            else "unavailable"
                        ),
                    )
                )
        self.net_gain_loss_value.SetLabel(locale.currency(total_gain_loss, grouping=True))

    def on_cancel(self, event: wx.CommandEvent) -> None:
        """Close the frame, terminating the application."""
        self.Close(True)


def get_current_price(api_key: str, symbol: str) -> Optional[float]:
    """Get current price of stock."""
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        return None
    try:
        return response.json()["c"]
    except (KeyError, TypeError):
        return None


class MyStocksApp(wx.App):
    def __init__(self, api_key: str, db_path: Path):
        self.api_key = api_key
        self.db_path = db_path
        wx.App.__init__(self)

    def OnInit(self) -> bool:
        frame = StockListFrame(None, api_key=self.api_key, db_path=self.db_path)
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
        default=DEFAULT_API_KEY,
    )
    parser.add_argument(
        "-d",
        "--db",
        dest="db_path",
        help="path to database",
        default=DEFAULT_DB_PATH,
        type=Path,
    )
    options = parser.parse_args(argv[1:])

    app = MyStocksApp(api_key=options.api_key, db_path=options.db_path)
    app.MainLoop()

    return 0


if __name__ == "__main__":
    try:
        rc = main(sys.argv)
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error: {e}", file=sys.stderr)
        rc = 1
    sys.exit(rc)
