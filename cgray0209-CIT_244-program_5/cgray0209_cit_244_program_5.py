"""CIT 244: Python II - Program 5: hitting the bottle.py with sqlite
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
    app.run(host="localhost", port=8080, debug=True)


if __name__ == "__main__":
    _main()
