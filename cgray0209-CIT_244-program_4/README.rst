CIT 244: Python II (4226_55Z1) - Program 4: more on wx.python, web
services, & databases
========================================================================

.. role:: python(code)
   :language: python

.. role:: sql(code)
    :language: sql

We start with an sqlite3 database named ``tech_stocks.db``. The database
has a table named ``dow_stocks``, which contains data on 9 of the 30
stocks that make up the Dow Jones Industrial Average. The table contains
a primary key named ``sid``, and columns for the company name, the
exchange the stock trades on, the stock symbol, the number of shares
purchased, and the price paid when the individual shares of that stock
were purchased. Do not change these column names: ``sid``, ``company``,
``exchange``, ``symbol``, ``shares``, ``purchase_price``. Note the stock
symbol for Apple is AAPL. In fact, make no modifications to this
database.

An image is shown below.

.. image:: https://elearning.kctcs.edu/bbcswebdav/pid-47334899-dt-content-rid-349590081_2/courses/JFC_4226_CIT_244_55Z1_83606/JFC_4226_CIT_244_55Z1_83606_ImportedContent_20221205032009/programs/dow_stocks_table.png

You may download a zipped copy of the database with this link: ⇒
`tech_stocks.zip`_

.. _`tech_stocks.zip`: https://elearning.kctcs.edu/bbcswebdav/pid-47334899-dt-content-rid-349590081_2/courses/JFC_4226_CIT_244_55Z1_83606/JFC_4226_CIT_244_55Z1_83606_ImportedContent_20221205032009/programs/tech_stocks.zip

In a real application you would have code that allows updating or
inserting new values as stocks are bought and sold. A column holding
dates would also probably be handy. There might likely be other tables
as well. But here we are not trying to make the perfect app. We just
want to develop code to get current info and compare it to saved data.

What we would like to do is make a daily query of a web service that
offers free stock quotes, and have our program compare the current price
for each stock with our original purchase price. Then, using the number
of shares purchased, we calculate and display the current profit or loss
for each stock. We also want to know the net profit or loss after
looking the results of all 9 of the individual stock values to see our
overall gains or losses. There are a very large number of web services
dealing with financial and stock market issues. We will use a free
service named finnhub.io.

The Details
-----------

We will make a desktop app using wxPython that queries a web service
named finnhub.io for data. We will combine this data with some of the
data in our tech_stocks database. In order to make Ajax/JSON requests to
finnhub.io and receive data, we first need to do a couple of things.

1. go to finnhub.io, click the button that says "Get free API key".
2. get your API key (or, sometimes it is called an access token). Store
   it somewhere easy to find.

This key will be attached to any requests you make for data. Free access
to Finnhub data is allowed as long as you don't make any more than 30
API requests per second. The key is mainly used by finnhub to ensure you
do not exceed this limit. We will have no trouble making less than 30
request per second. Here is the default page for finnhub. Note the green
buttons at the bottom of the image shown. Get your access key.

.. image:: https://elearning.kctcs.edu/bbcswebdav/pid-47334899-dt-content-rid-349590081_2/courses/JFC_4226_CIT_244_55Z1_83606/JFC_4226_CIT_244_55Z1_83606_ImportedContent_20221205032009/programs/finnhub.io-1.PNG

If you click the API Documentation button, you'll find a ton of info on
the services offered by finnhub. But we are mainly interested in getting
an up-to-date quote for each of our 9 stocks. The section is named
Quote. The information on how to do that is given a little more than
half way down the documentation page, and in fall of 2020 this info
looks like this next image. The page may have changed some, they may not
show the example code as given below, but they will show an example
response. The response, after being deserialized from JSON, is a python
dictionary of stock values. Keys of `c`, `h`, `l`, `o`, `pc`, and `t`,
as shown in the image below. Here these keys have values of closing
price (`c`), high for the day (`h`), low for the day(`l`, lower case L),
the opening value of the stock (`o`), and the previous close (`pc`).
They use Apple in this example.

.. image:: https://elearning.kctcs.edu/bbcswebdav/pid-47334899-dt-content-rid-349590081_2/courses/JFC_4226_CIT_244_55Z1_83606/JFC_4226_CIT_244_55Z1_83606_ImportedContent_20221205032009/programs/Quote.png

In the JSON response you may also have a `d` key (change), or a `dp` key
(percent change). Sometimes these keys are there, sometimes not.

Test
----

As a preliminary test you should copy the following URL, replace the
last part with your actual access token, and paste it into your browser
address bar. Hit enter. You should get a JSON response back for
Caterpillar in JSON format.

    ``https://finnhub.io/api/v1/quote?symbol=CAT&token=youracccesstoken``

In our Python code we will need to use a URL like this with the requests
library. The structure of a request looks like this next code chunk when
using Python. This is an example python request which should print out
the returned information in a form that has been deserialized; it should
be a regular python dictionary, accessable using the methods we normally
use to manipulate dictionary data. The access token used here is a fake
and will not work, so either remove it our use your own key if you want
to test it out in the python shell or whatever IDE you use.

.. code-block:: python

    res = requests.get('https://finnhub.io/api/v1/quote?symbol=AAPL&token=youraccesstoken')
    res = res.json()     # convert response from JSON to Python

This part of the URL is the base.

    ``https://finnhub.io/api/v1/quote?``

And to that we need to attach, using the Apple stock symbol as an
example, the following

    ``symbol=AAPL``

and along with an ampersand, you would add the name=value pair for your
access token. The token below is fictional and will not work. Your api
key (or token) is usually a mix of 20 random-looking characters.

    ``&token=12g45amc0123``      # this is not a real access key, do not use

As we said, initially the response comes back in JSON format. As we
know, the following :python:`.json()` python method deserializes the
data in the variable named :python:`reqData` from the JSON format to a
regular python dictionary.

.. code-block:: python

    dictionary_data = reqData.json()

Of the response values, we only need the current value of the stock. But
shown below is a minimum number of lines of code that would make a
request (assumes you have pip installed requests at some point in the
past). In this case we want the IBM stock values. This was done in
October 2020. The API key has been blurred. As we said, the data comes
back to use as JSON by default.

We concatenate the stock symbol into the URL, a technique you should
find useful in this assignment.

.. code-block:: pycon

    >>> import requests
    >>> sym = 'IBM' # concatenate request url
    >>> url = 'https://finnhub.io/api/v1/quote?symbol=' + sym + '&token=youraccesstoken'
    >>> req = requests.get(url)
    >>> data = req.json() # convert json to dictionary
    >>> print(data)
    {'c': 115.74, 'h': 116.62, 'l': 115.53, 'o': 116.5, 'pc': 115.76, 't': 1603479130}
    >>> print("current Price: ", data['c'])
    current Price:  115.74
    >>> print("Previous Close: ", data['pc'])
    Previous Close:  115.76
    >>> print("Open: ", data['o'])
    Open:  116.5

Your Code
---------

When executed, your program needs to open a wx frame with the following
widgets. In this image no button has been clicked yet:

- two labels at the top, one will display the current date and one will
  display the net gain and loss calculated for all 9 stocks in the
  database table named `dow_stocks` when the button is clicked.
- a regular list control with 6 columns: "Company", "Symbol", "Purchase
  Price", "Current Price", "Shares", "Gain/Loss"
- a row of buttons. the "Display Data" button causes code to query the
  database and get the company, symbol, purchase price, and number of
  shares. That same code needs to make a request to finnhub to get the
  current price of each of the 9 stocks. Then using the number of
  shares, the purchase price, and the current price, calculate the gain
  or loss for each of the 9 stocks and display those values.
- the close button just closes the program.

This is the initial state when you first run the program.

.. image:: https://elearning.kctcs.edu/bbcswebdav/pid-47334899-dt-content-rid-349590081_2/courses/JFC_4226_CIT_244_55Z1_83606/JFC_4226_CIT_244_55Z1_83606_ImportedContent_20221205032009/programs/frame1.PNG

::

    +-------------------------------------------------------------------------------------+
    | My Stocks                                                              [🗕] [🗖] [🗙] |
    +-------------------------------------------------------------------------------------+
    |                            Today's Date                                             |
    |                            Total                                                    |
    |                                                                                     |
    | +------------------+--------+----------------+---------------+--------+-----------+ |
    | | Company          | Symbol | Purchase Price | Current Price | Shares | Gain/Loss | |
    | +------------------+--------+----------------+---------------+--------+-----------+ |
    | |                  |        |                |               |        |           | |
    | |                  |        |                |               |        |           | |
    | |                  |        |                |               |        |           | |
    | |                  |        |                |               |        |           | |
    | |                  |        |                |               |        |           | |
    | |                  |        |                |               |        |           | |
    | |                  |        |                |               |        |           | |
    | |                  |        |                |               |        |           | |
    | |                  |        |                |               |        |           | |
    | |                  |        |                |               |        |           | |
    | +------------------+--------+----------------+---------------+--------+-----------+ |
    |                                                                                     |
    |                          [ Display Data ] [    Cancel    ]                          |
    |                                                                                     |
    +-------------------------------------------------------------------------------------+

This next image is what it looked like when I clicked the "Display Data"
button on Oct 23, 2020. As an example calculation, we can see that we
originally bought 100 shares of 3M for $157.50 per share, which is
stored in our database. We queried finnhub on Oct 23 and got a current
price 169.26. The overall gain or loss for this stock would be 100
shares times (current price - purchase price). This calculation will be
negative (a loss) if current price is less than purchase price. gain =
100(169.26 - 157.5) = 1176.

.. image:: https://elearning.kctcs.edu/bbcswebdav/pid-47334899-dt-content-rid-349590081_2/courses/JFC_4226_CIT_244_55Z1_83606/JFC_4226_CIT_244_55Z1_83606_ImportedContent_20221205032009/programs/frame2.PNG

::

    +-------------------------------------------------------------------------------------+
    | My Stocks                                                              [🗕] [🗖] [🗙] |
    +-------------------------------------------------------------------------------------+
    |                            Friday, October 23, 2020 13:23                           |
    |                            Net gain/loss: $ 6804.00                                 |
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

Generally, you need to query the database table to get the original
data. Then you're gonna need a loop to make the 9 finnhub queries that
get the returned current prices, then make the proper calculations and
add up the 9 gain/loss values to get the Net gain/loss. This loop is
where most of the calculations would likely be performed. Be careful not
to make an infinite loop. You only get 30 requests per second. After
looping, then display the results in the GUI for your user.

Prerequesite: If you have not already installed the requests library in
an earlier lesson, then before running any code open the command prompt
and install requests. If you did the examples in from the lecture notes
you may already have installed requests.

.. code-block:: shell

    pip install requests

You're gonna need to import wx, sqlite3, requests, and we need to be
able to get the date, which is not included in the finnhub data set, so
you will also need to import datetime

.. code-block:: python

    import wx
    import sqlite3
    import requests
    import datetime

We've not done much with Python dates, but the Internet is full of
examples. Here's a code hint. We need to import datetime, as shown
above, and if so the first line below gets the information for NOW, that
is, the current date and time. The second line formats the date as
day-of-the-week, month, day, year, hours (on the 24 hr clock), and
minutes.

.. code-block:: python

    x = datetime.datetime.now() # date and time
    date = x.strftime("%A %B %d, %Y : %H:%M")

For full credit
---------------

- Use either sizers or absolute positioning; you're choice. your layout
  does not need to look exactly like mine, but it does need the same
  widgets and they need to be visible when the window opens. the list
  control needs to be large enough to display the columns without a
  horizontal scroll bar showing up.
- the values are dollars, so round any calculations to no more than 2
  decimal places so there are no numbers that look like
  345.3333222211123344
- you need a loop to send the 9 stock requests. in order to have a loop
  send your requests to finnhub, you will need an API key. if you don't
  want me to see your api key, you can type wxyz in for the access token
  before sending me your code, but leave the rest of the code intact so
  I only have to substitute my key in place of yours. and don't lose
  your access key.
- to make this work your code will have to query the database and
  retrieve the company, symbol, purchase price, and number of shares in
  order to display this data along with the finnhub values. Do not hard
  code the ``dow_stocks`` information in your program.
- your code will need to work with my copy of the database.
- Start early. As usual, there is an example in the lecture notes that
  should give you a good start. Let me know if there are quesitons.

Hint: You need a loop, a loop that reads a line of data in from the
database, makes a request to the web service for the current price of
that stock, uses that stock price to calculate profit and loss, then
puts everything in the list control for that row. There are other things
to do as well. Here's kind of an outline.

.. code-block:: python

    #connect to stocks db, fetch the rows of data

        #loop thru the rows.
        # get the stock symbol for the stock in this row
        # concatenate the request to the web service for that stock
        # get the current price for the stock
        # calculate profit or loss
        # append info to the list control
