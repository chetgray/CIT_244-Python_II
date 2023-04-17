"""CIT 244: Python II - Program 5: hitting the bottle.py with sqlite

.. role:: python(code)
   :language: python

.. role:: sql(code)
    :language: sql

This program is about very basic web site navigation as well as having
the browser and web server interact with a simple database. Before doing
anything else, please view this video overview of how things should
work. It contains valuable code info as well.

    in this program we're going to take a quick look at how uh python 2
    program assignment 5 should go should work this is uh well i'll run
    it here in a minute but we're going to have a login from a database
    then i'll see if i can open that database real quick we have two
    tables in the database one is to give us the users and their
    passwords the other is uh a a list of trips we'll look at this real
    quick here so here's our ``members`` there's three of them they have
    a a unique uh they have a role but we're not using that and then we
    have an unencrypted password we're not using uh hashing passwords or
    cookies on this one so they just need to be able to when they enter
    the username and password we just need to find a match in this table
    called ``members`` the second table has a list of trips these are
    business trips so these are company people they expect to be
    reimbursed for their trips and their technicians maybe they drive to
    distant cities and fix stuff or calibrate things who knows but they
    make a round-trip uh trip and they write down their miles and
    gallons and eventually they'll be reimbursed for this so jay smith
    uh made a trip on the 2nd of uh january and also the 8th 9th and
    10th of january and a garcia made a trip on the 6th the 7th so on so
    eventually they're going to want to see their own trip the list of
    their trips so they know what to expect so they're supposed to log
    in they're able to then filter this uh this table this ``trips``
    table for their trips to see which trips are theirs and then they
    need to be able to add a trip when they get back from a trip they
    need to be able to add it to the database so that's where this is
    headed so let me run this okay even we're closed that's not what i
    want my uh i need to use port 8081 you probably don't but you might
    so this opens a login page let me get it more centered and i'm going
    to use jay smith since that's the one i remember j smith had the
    password of password we're not worried much about the security here
    and then we're expecting to find a match if for a successful login
    it takes us to this sort of menu page where we have the option to
    enter a new trip or to see all of the trips but on the other hand if
    we enter somebody who's uh don't whose credentials are not in the
    table if we click that we get it there's this we have a status
    template and then in this case the message sent to the template was
    that it failed so we need we need to be able to tell whether the
    person's credentials are proper all right so let me go back to j
    smith if i want to see if i'm j smith and i want to see my trips i
    click the bottom link i enter my name username i click submit and
    this gives me that there are 29 or 30 trips total these are this is
    this is just j smith strips trip id 1 3 7 and so on the trip id is a
    it's an auto incrementing integer now if i go back to my menus i can
    also enter a new trip so i can enter my username of jsmith i can
    pick a date in february and to be honest since we don't use the date
    for anything uh this this particular information only needs to be
    recognizable so let me go to orlando i don't know i'm just guessing
    how many round-trip miles and i'm just making up a number there and
    we'll if orlando shows up on our table uh it says trip insertion was
    successful this is our same status page that told us the the login
    was successful so now if we go back and we will improve on the
    navigation uh soon here but let's uh let's see if our if our orlando
    trip is there and sure enough there we are so this is the sequence
    of events i have uh this is my login route i'll give you a head
    start here the default route just sends a login page template so the
    person can enter their name and uh password and then when that is
    posted it is posted to this login route which gets the user
    information from the text boxes it opens the database creates a
    cursor we select all from ``members`` where their username we're
    using this username here we should also we should also make sure the
    password is there right now we're just simplifying things and
    remember that when you actually execute the sql this with these
    question mark things you need a tuple that is there's no we have
    only a single variable here user but if you put user in parentheses
    it's not a tuple so you have to add this com if there's only one
    thing you have to add this comma here then fetch one unlike fetch
    all fetch all returns a list of tuples where each tuple is a row in
    the database if you do fetch one and this we're only looking for a
    single person here uh it returns just a tuple so it would uh for
    jsmith it would return uh jsmith tech and and then his password his
    or her password and then we close it and so if we got a result
    result is the tuple that came back in this case if we get a result
    then we send uh send them that menu page where they get the pick
    between entering a trip and uh viewing the trips and if we if it's a
    bogus if it didn't work if it was the wrong credentials we're going
    to return a status template with a message and the message that the
    uh from in my case the message is the variable and the message and
    this in this case would that would be sent is that the law again
    failed now on the other hand if i want to enter the trip i need to
    be able to insert values and remember that we need the user the date
    the destination miles and gallons and that this none as i want you
    to remember is the takes the place of the auto incrementing id so i
    have one two three four five six things to to insert and so i need
    one two three four five six question marks here and data then is
    there is already in a tuple this is already a tuple and so on so i'm
    going to stop here so this doesn't get too long but i have uh i have
    a these templates you may go about you don't have to go about it
    this way or name them this way but when they log in when they first
    go to the default site they're given a page that allows them to log
    in if they log in it posts to a route which then shows them the menu
    the two links to make a choice between entering and viewing a trip
    and then depending on which one they pick if they pick one it takes
    them to a route where we're able to uh they are sent a template
    where they can add a trip or alternatively a or sorry yeah add a
    trip or view trips and then there's a a do-it-all status one that
    takes care of any errors that might be i'm going to stop here you're
    welcome to ask questions on this i so i would not wait till the last
    minute this is our first bottle program it'll take you a little
    while to get oriented and i think you'll find it's fun if you start
    early enough but anyway if you have questions let me know

You don't have to use any of the code shown; you are welcome to write
your own code as you please.

The database is named ``travel_expenses.db``, and there are two tables:
``members`` and ``trips``. Although you can add trips to the ``trips``
table, you must leave the other data and its structure intact. That is,
your code must work with my copy of the database.

A link to the database is given here: `travel_expenses.zip.`_

.. _`travel_expenses.zip.`: https://elearning.kctcs.edu/bbcswebdav/pid-47334903-dt-content-rid-349590090_2/courses/JFC_4226_CIT_244_55Z1_83606/JFC_4226_CIT_244_55Z1_83606_ImportedContent_20221205032009/programs/travel_expenses.zip

Here is a look at the `members` table and the first trips given in the
``trips`` table. ``trip_id`` is an auto-incrementing :sql:`integer`,
``miles`` is an :sql:`integer`, ``gallons`` is a :sql:`float`.
``username``, ``data``, and ``destination`` are of type :sql:`text`.

``members``:

============ ======== ============
``username`` ``role`` ``password``
============ ======== ============
jsmith       tech     password
agarcia      tech     superwoman
dwilson      tech     12345
============ ======== ============

``trips``:

=========== ============ ======== =============== ========= ===========
``trip_id`` ``username`` ``date`` ``destination`` ``miles`` ``gallons``
=========== ============ ======== =============== ========= ===========
1           jsmith       1/2/2014 chicago         663       20.7
2           agarcia      1/3/2014 indianapolis    226       8.7
3           jsmith       1/4/2014 nashville       409       16.4
4           dwilson      1/5/2014 indianapolis    243       8.4
5           agarcia      1/6/2014 st. louis       560       18.1
6           agarcia      1/7/2014 cincinnati      237       6.6
7           jsmith       1/8/2014 chicago         681       17.9
=========== ============ ======== =============== ========= ===========

Here's an example template. Remember templates have a ``.tpl`` file
extension. You do not have to use the same route names that I have used.

_add trip_:

.. code-block:: html+mako

    <html>
    <head><title>Data Entry Page</title></head>
    <body>

    Please spell destinations lower case:<br><br>
    <form action= '/enterTrip' method = 'POST'>
      <input type='text' name='user'> Username <br><br>
      <input type='text' name='date'> Date <br><br>
      <input type='text' name='dest'> Destination <br><br>
      <input type='text' name='miles'> Miles <br><br>
      <input type='text' name='gallons'> Gallons Used <br><br>
      <input type = "submit">
    </form>
    </body></html>

For full credit.

- use proper templates and put them in the views folder.
- you should make sure both the username and password the user enters
  match a record in the members table upon login. Otherwise, you should
  display a message that the login failed.
- if a user enters a trip, all values should be properly inserted into
  the trips table.
- you should display only the trips taken by a given user. No user
  should see the other user's trips.
- our html is not pretty, but information displayed should be readable.

Here are some things you don't have to do.

- we trust our employees to enter a valid employee id and data. you
  don't have to validate the data for this assignment
- since this is our first Bottle program you do not have to maintain
  state or use cookies for this program
"""  # noqa: E501

__author__ = "Chet Gray <cgray0209@kctcs.edu>"
__copyright__ = "Copyright (c) 2023 Chet Gray"
__license__ = "UNLICENSED"
__version__ = "0.1.0"

import sqlite3
from contextlib import ExitStack
from pathlib import Path

from bottle import Bottle, request, template

DB_PATH = Path("travel_expenses.db")

app = Bottle()


@app.get("/")  # type: ignore
def login():
    """Display the login page."""
    return template("login_form.tpl")


@app.post("/")  # type: ignore
def do_login():
    """Login the user."""
    # pylint: disable-next=no-member
    username: str = request.forms.get("username")  # type: ignore
    # pylint: disable-next=no-member
    password: str = request.forms.get("password")  # type: ignore
    if not is_valid_login(username, password):
        return template(
            "login_form.tpl", alert_context="warning", alert_message="Invalid login"
        )
    return template("user_menu.tpl", username=username)


def is_valid_login(username: str, password: str) -> bool:
    """Check if the user is valid."""
    is_valid = False
    with ExitStack() as db_stack:
        # auto-close
        con = db_stack.enter_context(sqlite3.connect(DB_PATH))
        # auto-commit/rollback
        db_stack.enter_context(con)
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM members WHERE username = ? AND password = ?", (username, password)
        )
        is_valid = cur.fetchone() is not None
    return is_valid


@app.get("/add")  # type: ignore
def add_trip():
    """Display the add trip page."""
    return template("add_trip_form.tpl")


@app.post("/add")  # type: ignore
def do_add_trip():
    """Add a trip to the database."""
    # pylint: disable-next=no-member
    username: str = request.forms.get("username")  # type: ignore
    # pylint: disable-next=no-member
    date: str = request.forms.get("date")  # type: ignore
    # pylint: disable-next=no-member
    destination: str = request.forms.get("destination")  # type: ignore
    # pylint: disable-next=no-member
    miles: str = request.forms.get("miles")  # type: ignore
    # pylint: disable-next=no-member
    gallons: str = request.forms.get("gallons")  # type: ignore
    try:
        with ExitStack() as db_stack:
            # auto-close
            con = db_stack.enter_context(sqlite3.connect(DB_PATH))
            # auto-commit/rollback
            db_stack.enter_context(con)
            cur = con.cursor()
            cur.execute(
                (
                    "INSERT INTO trips (username, date, destination, miles, gallons)"
                    " VALUES (?, ?, ?, ?, ?)"
                ),
                (username, date, destination, miles, gallons),
            )
    except sqlite3.Error as err:
        return template(
            "add_trip_form.tpl",
            alert_context="warning",
            alert_message=f"Error adding trip: {err}",
        )
    return template("add_trip_form.tpl", alert_context="success", alert_message="Trip added")


@app.get("/listByUser")  # type: ignore
def list_trips_by_user():
    """Display the list trips by user page."""
    return template("list_trips_by_user_form.tpl")


@app.post("/listByUser")  # type: ignore
def do_list_trips_by_user():
    """List trips by user."""
    # pylint: disable-next=no-member
    username: str = request.forms.get("username")  # type: ignore
    trips = []
    try:
        with ExitStack() as db_stack:
            # auto-close
            con = db_stack.enter_context(sqlite3.connect(DB_PATH))
            # auto-commit/rollback
            db_stack.enter_context(con)
            cur = con.cursor()
            cur.row_factory = sqlite3.Row  # type: ignore
            cur.execute(
                (
                    "SELECT trip_id, username, date, destination, miles, gallons,"
                    " miles / gallons AS mpg"
                    " FROM trips"
                    " WHERE username = ?"
                ),
                (username,),
            )
            trips = cur.fetchall()
    except sqlite3.Error as err:
        return template(
            "list_trips_by_user_form.tpl",
            alert_context="warning",
            alert_message=f"Error listing trips: {err}",
        )
    if not trips:
        return template(
            "list_trips_by_user_form.tpl",
            alert_context="warning",
            alert_message=f"No trips found for {username}",
        )
    return template(
        "list_trips.tpl",
        page_title="Trips by User",
        page_heading=f"Trips for {username}",
        trips=trips,
    )


def _main():
    """Main entry point for the bottle application."""
    app.run(host="localhost", port=8080, debug=True, reloader=True)


if __name__ == "__main__":
    _main()
