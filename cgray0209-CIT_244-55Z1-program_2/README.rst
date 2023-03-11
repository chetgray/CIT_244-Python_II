####################################################################
CIT 244: Python II (4226_55Z1) - Program 2: Graphical User Interface
####################################################################

.. role:: python(code)
   :language: python

This assignment is to use wxPython to make a shipping calculator. The
total cost will vary with package weight, shipping speed, and any extras
the user might request. The layout should look something like this.

This is the default state of the interface (first radio of each radio
button selected, everything else clear). Nothing has been calculated or
else the Clear Form button has just been clicked.

The prices for various weights and shipping speeds are shown. (0 - 1.9
lbs add $5, 3-day air shipping add 6.15, etc.).

    Weight

    - 0 - 1.9 lbs. $5.00
    - 2 - 4.9 lbs. $8.00
    - 5 - 10 lbs. $12.25

    Speed

    - Overland $2.75
    - 3-day Air $6.15
    - 2-day Air $10.70
    - Overnight $15.50

    Options

    - Extra Padding $4
    - Gift Wrapping $6

For full credit: your layout does not have to look exactly like this,
but the prices must be the same, and it should contain the widgets
shown, and it should be sensible so someone using it can easily tell
what is happening when a button is clicked. You also need to write this
yourself and not turn in some else's work.

You'll need these wxPython widgets.

- 3 TextCtrl widgets; one for name, one for address, and one for
  city-state-zip
- 7 radio buttons total, with a group of 3 for package weight, and a
  group of 4 for package delivery speed
- 2 check boxes for selecting options
- 2 buttons, one to trigger calculating the total, the other to reset
  the form in its default position.
- a number of StaticText widgets to make sure everything is labeled
  clearly
- a label at the bottom of the frame where the results will be printed.
  Since the form has been cleared in the image above you cannot see the
  summary label until something is actually calculated. (see the image
  later on this page)

Please start early in the week that this program is due; this gives you
plenty of time to ponder how is should work. Moreover, there will be
more to ponder as the course progresses. I am glad to help troubleshoot
programs, but I go to bed reasonably early and am unlikely to stay up
until midnight of the due date.

Shown next is an example calculation for a gift-wrapped 3 lb. package
shipped 3-day air. Note the 4-line summary printed at the bottom of the
form which includes the content of all three TextCtrl widgets plus the
calculated total shipping cost. This summary was printed in a single
StaticText widget designated for displaying the results when the
Calculate Total button was clicked.

    :Name:
        Mr Ralph Cramden
    :Address:
        12101 Studebaker Drive
    :City, State, and Zip:
        Grayhound, TX 20002
    :Weight:
        2 - 4.9 lbs. $8.00
    :Speed:
        3-day Air $6.15
    :Options:
        - Gift Wrapping $6

    Shipping Summary

    Mr Ralph Cramden
    12101 Studebaker Drive
    Grayhound, TX 20002
    $ 20.15

You may benefit from the following hints.

Recall that to define a group of radio buttons the first radio button of
each group must be designated by a :python:`style=wx.RB_GROUP` property.
The following 5 buttons form 2 groups. The first 2 radios form a group,
and the last 3 radios form a different group. This means you can select
one radio from each group.

.. code-block:: python

    self.a1 = wx.RadioButton(self.panel, -1, 'just 1', pos=(23, 100), style = wx.RB_GROUP)
    self.a2 = wx.RadioButton(self.panel, -1, 'just 2', pos=(23, 100))

    self.r = wx.RadioButton(self.panel, -1, 'red', pos=(23, 100), style = wx.RB_GROUP)
    self.g = wx.RadioButton(self.panel, -1, 'green', pos=(23, 100))
    self.b = wx.RadioButton(self.panel, -1, 'blue', pos=(23, 100))

By default the first button in each group will be selected.

And generally, for both radio buttons and checkboxes, you can set the
state of the button using the following.

.. code-block:: python

    self.btn.SetValue(False)   # False unchecks a button, True would select it.

And, you can make a label print things multi-line if you set a size of
both a height and a width, and you concatenate the strings to be printed
with "\\n", which is the new line character. So this would print "The
cat in the hat." on one line.

.. code-block:: python

    txt = "The cat" + " in the hat."
    self.label.SetValue(txt)

But this would print "The cat" on one line, and "in the hat." on the
next line.

.. code-block:: python

    txt = "The cat" + "\n" + "in the hat."
    self.label.SetValue(txt)

And finally, when setting the size property of a widget, if you set one
of the dimensions as -1 that dimension will display as the default
value. For example, the following would be a TextCtrl with a width of
220 pixels, but a height set at the default (which is big enough for any
letters)

.. code-block:: python

    self.name = wx.TextCtrl(self.panel, -1, pos=(90, 30), size=(220, -1))
