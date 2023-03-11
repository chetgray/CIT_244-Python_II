#!/usr/bin/env python3
"""CIT 244: Python II (4226_55Z1) - Program 2: Graphical User Interface

This assignment is to use wxPython to make a shipping calculator. The
total cost will vary with package weight, shipping speed, and any extras
the user might request.
"""

__author__ = "Chet Gray <cgray0209@kctcs.edu>"
__copyright__ = "Copyright (c) 2023 Chet Gray"
__license__ = "MIT"

from typing import Optional

import wx


class ShippingCalculator(wx.Frame):
    """A shipping calculator GUI."""

    def __init__(self, parent: Optional[wx.Window], title: str = "Shipping Calculator"):
        super().__init__(parent, title=title, size=(1500, 1500))

        self.panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_label = wx.StaticText(self.panel, -1, "Name")
        self.name_input = wx.TextCtrl(self.panel, -1)
        name_sizer.Add(name_label, 2, wx.RIGHT | wx.ALIGN_CENTER, 30)
        name_sizer.Add(self.name_input, 10, wx.EXPAND)
        sizer.Add(name_sizer, 0, wx.ALL | wx.EXPAND, 30)

        address_sizer = wx.BoxSizer(wx.HORIZONTAL)
        address_label = wx.StaticText(self.panel, -1, "Address")
        self.address_input = wx.TextCtrl(self.panel, -1, size=(500, -1))
        address_sizer.Add(address_label, 2, wx.RIGHT | wx.ALIGN_CENTER, 30)
        address_sizer.Add(self.address_input, 10, wx.EXPAND)
        sizer.Add(address_sizer, 0, wx.ALL | wx.EXPAND, 30)

        city_state_zip_sizer = wx.BoxSizer(wx.HORIZONTAL)
        city_state_zip_label = wx.StaticText(self.panel, -1, "City, State, and Zip")
        self.city_state_zip_input = wx.TextCtrl(self.panel, -1, size=(500, -1))
        city_state_zip_sizer.Add(city_state_zip_label, 2, wx.RIGHT | wx.ALIGN_CENTER, 30)
        city_state_zip_sizer.Add(self.city_state_zip_input, 10, wx.EXPAND)
        sizer.Add(city_state_zip_sizer, 0, wx.ALL | wx.EXPAND, 30)

        weight_speed_options_sizer = wx.BoxSizer(wx.HORIZONTAL)

        weight_sizer = wx.BoxSizer(wx.VERTICAL)
        weight_label = wx.StaticText(self.panel, -1, "Weight")
        self.w1 = wx.RadioButton(self.panel, -1, "0 - 1.9 lbs. $5.00", style=wx.RB_GROUP)
        self.w2 = wx.RadioButton(self.panel, -1, "2 - 4.9 lbs. $8.00")
        self.w3 = wx.RadioButton(self.panel, -1, "5 - 10 lbs. $12.25")
        weight_sizer.Add(weight_label, 0, wx.ALL | wx.ALIGN_CENTER, 50)
        weight_sizer.Add(self.w1, 0, wx.ALIGN_LEFT)
        weight_sizer.Add(self.w2, 0, wx.ALIGN_LEFT)
        weight_sizer.Add(self.w3, 0, wx.ALIGN_LEFT)
        weight_speed_options_sizer.Add(weight_sizer, 1, wx.ALL | wx.EXPAND, 30)

        speed_sizer = wx.BoxSizer(wx.VERTICAL)
        speed_label = wx.StaticText(self.panel, -1, "Speed")
        self.s1 = wx.RadioButton(self.panel, -1, "Overland $2.75", style=wx.RB_GROUP)
        self.s2 = wx.RadioButton(self.panel, -1, "3-day Air $6.15")
        self.s3 = wx.RadioButton(self.panel, -1, "2-day Air $10.70")
        self.s4 = wx.RadioButton(self.panel, -1, "Overnight $15.50")
        speed_sizer.Add(speed_label, 0, wx.ALL | wx.ALIGN_CENTER, 30)
        speed_sizer.Add(self.s1, 0, wx.ALIGN_LEFT)
        speed_sizer.Add(self.s2, 0, wx.ALIGN_LEFT)
        speed_sizer.Add(self.s3, 0, wx.ALIGN_LEFT)
        speed_sizer.Add(self.s4, 0, wx.ALIGN_LEFT)
        weight_speed_options_sizer.Add(speed_sizer, 1, wx.ALL | wx.EXPAND, 30)

        options_sizer = wx.BoxSizer(wx.VERTICAL)
        self.options_label = wx.StaticText(self.panel, -1, "Options")
        self.o1 = wx.CheckBox(self.panel, -1, "Extra Padding $4")
        self.o2 = wx.CheckBox(self.panel, -1, "Gift Wrapping $6")
        options_sizer.Add(self.options_label, wx.ALL | wx.ALIGN_CENTER, 30)
        options_sizer.Add(self.o1, 0, wx.ALIGN_LEFT)
        options_sizer.Add(self.o2, 0, wx.ALIGN_LEFT)
        weight_speed_options_sizer.Add(options_sizer, 1, wx.ALL | wx.EXPAND, 30)

        sizer.Add(weight_speed_options_sizer, 0, wx.ALL | wx.EXPAND, 30)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.calculate = wx.Button(self.panel, -1, "Calculate Total")
        self.clear = wx.Button(self.panel, -1, "Clear Form")
        button_sizer.Add(self.calculate)
        button_sizer.Add(self.clear)
        sizer.Add(button_sizer, 0, wx.ALL | wx.EXPAND, 30)

        self.calculate.Bind(wx.EVT_BUTTON, self.calculate_total)
        self.clear.Bind(wx.EVT_BUTTON, self.clear_form)

        summary_sizer = wx.BoxSizer(wx.VERTICAL)
        summary_label = wx.StaticText(self.panel, -1, "Shipping Summary")
        self.summary = wx.StaticText(self.panel, -1, "")
        summary_sizer.Add(summary_label)
        summary_sizer.Add(self.summary)
        sizer.Add(summary_sizer, 0, wx.ALL | wx.EXPAND, 30)

        self.panel.SetSizerAndFit(sizer)

    def calculate_total(self, event: wx.Event):
        """Calculates the total shipping cost and display it in the summary."""
        name = self.name_input.GetValue()
        address = self.address_input.GetValue()
        city_state_zip = self.city_state_zip_input.GetValue()

        weight_cost = 0.0
        if self.w1.GetValue():
            weight_cost = 5.00
        elif self.w2.GetValue():
            weight_cost = 8.00
        elif self.w3.GetValue():
            weight_cost = 12.25

        speed_cost = 0.0
        if self.s1.GetValue():
            speed_cost = 2.75
        elif self.s2.GetValue():
            speed_cost = 6.15
        elif self.s3.GetValue():
            speed_cost = 10.70
        elif self.s4.GetValue():
            speed_cost = 15.50

        options_cost = 0.0
        if self.o1.GetValue():
            options_cost += 4.00
        elif self.o2.GetValue():
            options_cost = 6.00

        total_cost = weight_cost + speed_cost + options_cost

        summary_text = f"""
        {name}
        {address}
        {city_state_zip}
        $ {total_cost:.2f}
        """

        self.summary.SetLabel(summary_text)

    def clear_form(self, event: wx.Event):
        """Resets the form to its initial state."""
        self.name_input.Clear()
        self.address_input.Clear()
        self.city_state_zip_input.Clear()
        self.w1.SetValue(False)
        self.w2.SetValue(False)
        self.w3.SetValue(False)
        self.s1.SetValue(False)
        self.s2.SetValue(False)
        self.s3.SetValue(False)
        self.s4.SetValue(False)
        self.o1.SetValue(False)
        self.o2.SetValue(False)
        self.summary.SetLabel("")


def _main():
    app = wx.App()
    frame = ShippingCalculator(None)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    _main()
