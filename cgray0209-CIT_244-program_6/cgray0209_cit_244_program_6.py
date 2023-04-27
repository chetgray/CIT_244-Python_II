"""CIT 244: Python II - Program 6: Bootstrap

Our last program will inject proper styling and navigation to our web
apps. We want to also query a database.

- The sqlite3 database is named payroll.db, here's the link:
  `payroll.zip`_
- Two tables: one named ``employees``, and it has these fields:
  ``emp_id``, ``department``, ``name``, ``wage``
- There are 26 employees divided into 4 departments
- The second table is named ``pay_data``, with these fields: ``p_id``,
  ``emp_id`` (which is a foreign key), ``hrs_worked``, ``pay_period``
- We want to be able to view weekly pay calculations for employees
  filtered by department
- We also want to be able to edit or update the hours worked for a given
  employee

The relationship between tables is one-to-many, not many-to-many. So
don't use the movie lens example or the courses example (many students
put in many classes). Look for examples in the one-to-many category.
Here is a video overview of how the program should go.

Py2 program 6 overview transcript:

    this is uh an overview of the last program program six programming
    assignment for python 2. we have a database that has a named
    ``payroll.db``. we have two tables. one is called ``employees``. it
    has an auto incrementing integer for ``emp_id``. it has a
    ``department``. there are four departments "shipping" "maintenance"
    "environment" and "advertising". there's an employee `name` and
    these are just the employees from the lost wages example a while
    back so there's 26 of them and then each employee has an hourly
    ``wage`` embedded in this page. now there's a second table
    ``pay_data``. it has just a ``p_id``, which we don't really need. it
    has the ``emp_id`` as a foreign key which allows us to link the two
    tables. "alita", which is employee number 1, if you remember, her
    name was alita,  we've not entered any hours for her yet this week
    and we're going to assume it's the same pay period for everybody so
    other people's hours have been in in already updated into the
    database. so employee number 7, whose name i forget, has 44 hours,
    and then back in the employees table we have the information on the
    hourly ``wage``, so between the two we can calculate the weekly pay.
    now what we'd like to be able to do in our app is to first view all
    the employees by department with their weekly pay calculated
    including any computation for overtime, and we'd also like to be
    able to update the employees hours work so that we can actually
    calculate the pay. so in our home page, the page where we land, it
    just says "you have already been properly validated and logged in",
    so we don't want to complicate this with a validating login, we
    don't want to use hashed passwords, we don't want to use maintaining
    state and cookies with this. those things are important, but we
    don't want this last program to be so complex that everybody just
    gives up, so this this should still be pretty manageable. i have
    only two routes for this. the first one, *view by department*, if i
    click this link here in the nav bar, because now bootstrap is making
    this look good and we've got some consistent navigation menu there
    at the top, so we click *view by department* and we get an html form
    that allows us to pick the department.  let me pick "maintenance"
    first and then click submit. i get only those employees whose whose
    department was maintenance. we've calculated their pay, as in this
    case. in the case of "pablo", $20.25 times 44 hours, so he gets four
    hours of overtime, gives him that. now if we go back we click view
    by department again and pick "shipping", we get only the shipping
    department people, of which alita is one, and notice that we've got
    no hours worked so we haven't calculated her pay this week. so we
    want to be able to view by the employees by department with their
    weekly pay calculated, and we'd like to be able to update the the
    user's hourly wage so that they can get paid. so let's say we need
    to enter alita's hourly wage. so we'll enter her employee id which
    is 1 and maybe alita is 30, is part-time, just to pick a different
    number, so we'll say she worked 32 hours. when i click this we need
    to update the hours worked for elita in the ``pay_data`` table, and
    we'd we'd like to be able to get a notice to say that that worked,
    to make sure that what we did was the right thing. so if i click
    submit here in my result page, my status page i get a message
    "insert successful at employee id one name elita department
    shipping". and if i go back to *view by department*, and i go back to
    the shipping, i should be able to see that alita now has 32 hours
    worked, and in fact it should show up in the database. if i go back
    to alita here in the pay data, sure enough it's been updated in the
    database at 32 hours. so this is what we intend to do. i will give
    you one of the routes, or at least my code for it, and you don't
    have to use my exact code but but this should give you a good start.


    .. code-block:: python

        @route('/getDepartment', method=['GET', 'POST'])  # display employees by department
        def department():

            if request.method == 'GET':
                return template('dept_form')
            else:  # assumes method = post
                dept = request.forms.get("dept")
                conn = sqlite3.connect("payroll.db")  # create database connection and cursor
                c = conn.cursor()

                sql = '''SELECT pay_data.emp_id, emp_name, wage, hrs_worked FROM employees
                       JOIN pay_data
                       WHERE pay_data.emp_id = employees.emp_id AND employees.department = ?'''
                cur.execute(sql, (dept,))

                rows = cur.fetchall()
                cur.close()
                hrs = 0
                wage = 0

                if rows:

                    dataList = []
                    for row in rows:
                        eid, name, wage, hrs = row  # unpack tuple
                        if hrs <= 40:
                            payout = wage * hrs
                        else:
                            ot_pay = (hrs - 40) * 1.5 * wage
                            payout = (wage * 40) + ot_pay

                        emp = (eid, name, wage, hrs, payout)
                        dataList.append(emp)

                    data = {'rows': dataList, 'dept': dept}
                    return template('show_department', data=data)

            else:
                msg = 'no such username'

    so when the for the get by
    department one we need to the first is a get request for the for the
    form the html form that has the drop down list that tells you uh
    because i can do both get and posts for this particular route the
    form that allows you the drop down list with the different
    departments and the submit button that's what uh that's what this
    form does and then because that's a form and it will be posted then
    we post if it posts back to the same route if it's not a get then
    else must mean it was a post and we're assuming those are the only
    two verbs http verbs we have to worry about so when we post it back
    it should have the department of uh from the drop-down list whether
    it was shipping or maintenance or whatever and then we'd like to get
    the information from this particular employee to make sure we got it
    right we could uh well anyway that's what we want to do so we get
    the department we connect to our database payroll.db we get a cursor
    and then we select because we'd like to see the all the information
    on all the employees we select pay underscore data employee id
    employee name wage hours worked from the employees table join pay
    underscore data where the pay underscore data id is equal to
    employee employee id and at the same time the employee department
    and this is the key part is equal to this question mark and we're
    going to substitute in the department we retrieved from the drop
    down list so that we get that list the group of employee will get a
    list of tuples representing the employee as employees for a
    particular department so rows is equal to fetch all remember rows is
    a list of tuples each each tuple is represents one record in the
    table we close the cursor just so in case something goes wrong it's
    closed we set up variables for hours and and wage so we can multiply
    the pay and the reason i'm showing this to you is i want to this
    part may be kind of a tricky part that holds you up and we don't
    have a whole ton of time left in the semester so so if we got a
    bunch of rows meaning that we found a depart a department with
    people in it we're going to set up a new list we're going to take
    this list of tuples and we're going to create a new one because we
    have to add in addition to what we got here we have to add the
    weekly pay to it before we send it to the template so we got a new
    list we say for row and rows so each one of these is a tuple first
    we unpack the tuple we unpack the row we get the employee id the
    name the wage and the hours and if the hours is less than or equal
    to 40 we just calculate the weekly pay payout here as hours times
    wage and if it's not less than or equal to 40 then they get time and
    a half for the hours over 40. so the overtime pay is hours minus 40
    so this will give us the number of hours over 40 times 1.5 times
    wage and so we just say the payout now is the wage times 40 hours
    plus whatever we get for the overtime i'll leave you to figure that
    out you know how to you know how to calculate overtime and so payout
    then is the new uh item that needs to go in the row that will show
    up in the table so now we create a new tuple for this employee we
    get their id which we got up here when we did the unpacking the name
    the wage the hours and then we add this payout variable so now we're
    sending one two three four five things to the template and then you
    take we take this employee and we append to this new list we got
    because we're creating a we're modifying the list of tuples that
    we're sending to the template and then after we've gone through all
    of that after gone through all the employees in the department we
    set up the the rows is equal to our data list and the department is
    equal to the department that we got up here at the top there and we
    send it to a template and that's what shows up as this so we whoops
    as this so we can we got the employee id the name the wage the hours
    worked and then we've added the calculate pay so that the template
    that looks at this is called ``show_department``.

    .. code-block:: html+mako

        % rebase('layout.tpl', title='department')

        <h3>Department: {{dept}}</h3>

        <p>
        <table class='table'>
        <tr><th>Emp ID</th><th>Name</th><th>Wage</th><th>Hrs Worked</th><th>Weekly Pay</th></tr>
        %for row in rows:
            <tr align="center">
            %for col in row:
                <td>{{col}}</td>
            %end
            </tr>
        %end
        </table>
        </p>
        <br>

    so it's just we just display the department at the top here we'd
    like to know that we got the right employees so that goes up here
    where to go right there so we display the department there and then
    the rest of this is just building a table like we built over and
    over and over again this in the last four weeks so i'm going to stop
    here this should be give you a good hint i think you'll if you don't
    wait till the last possible nanosecond i think you'll find this is
    this is a fun thing to do and it'll look a lot nicer and less
    primitive than what we've been doing and i think if you get it
    working you'll kind of this you'll kind of feel good about the
    semester we'll go hey we've done a lot of good stuff this semester
    uh so start early please start early and if you have questions or
    get stuck then please email me and we'll see if we can straighten it
    out

Clicking the *Edit Employee Data* link should show a page similar to the
following which allows entering the employee ID and hours worked.
Submitting this posts the information to a route that does an SQL
``UPDATE`` for the employee hours worked.

*second template*::

    Our Website    Home    View by Department    Edit Employee Data
    ---------------------------------------------------------------

    # WXYZ Corp

    ## Enter emp_id and Hours Worked

    [                ] employee ID
    [                ] Enter hrs worked

    [Submit Query]

    ---------------------------------------------------------------
    We know what we're doing

The update will overwrite a 0 or whatever value was used in the hours
worked column before for that employee.

For full credit, you must:

- you need a working Bootstrap nav bar in a main layout template that
  allows substituting in sub templates. The nav-bar should have 3
  working links.
- the default page associated with the nav-bar *Home* link should just
  say something like "You have successfully logged in."
- when you update the hours worked for a student you need to notify your
  user that the operation was successful.
- you must display all the employees from a given department and their
  weekly pay when the *View by Department* link is clicked.
- your code must allow updating any of the employee's hours worked when
  the *Edit Employee Data* link is clicked.
- your code must work with my database, so don't rename anything.

You **do not** need to have your program maintain state or log in.

.. _`payroll.zip`: https://elearning.kctcs.edu/bbcswebdav/pid-47334905-dt-content-rid-349590091_2/courses/JFC_4226_CIT_244_55Z1_83606/JFC_4226_CIT_244_55Z1_83606_ImportedContent_20221205032009/programs/payroll.zip

"""  # noqa: E501

__author__ = "Chet Gray <cgray0209@kctcs.edu>"
__copyright__ = "Copyright (c) 2023 Chet Gray"
__license__ = "UNLICENSED"
__version__ = "0.1.0"

import sqlite3
from contextlib import ExitStack, closing
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union, cast

from bottle import Bottle, request, template  # type: ignore

DB_PATH = Path("payroll.db")

app = Bottle()


@dataclass
class EmployeePayrollViewModel:
    """Employee payroll data."""

    emp_id: int
    emp_name: str
    department: str
    wage: float
    hrs_worked: float

    @property
    def gross_pay(self) -> float:
        return (
            min(self.hrs_worked, 40) * self.wage
            + max(0, self.hrs_worked - 40) * self.wage * 1.5
        )


def employee_payroll_factory(cursor: sqlite3.Cursor, row: Union[tuple, sqlite3.Row]):
    fields: list[str] = [col[0] for col in cursor.description]
    return EmployeePayrollViewModel(**dict(zip(fields, row)))


@app.get("/")  # type: ignore
def index() -> str:
    """Display the welcome page."""
    return template("welcome", active_page="home")


@app.get("/view-by-department")  # type: ignore
def list_by_department() -> str:
    """Display the form to enter the department."""
    departments: list[str] = []
    with ExitStack() as db_stack:
        # auto-close connection, auto-commit/rollback transaction, auto-close cursor
        con = db_stack.enter_context(closing(sqlite3.connect(DB_PATH)))
        db_stack.enter_context(con)
        cur = db_stack.enter_context(closing(con.cursor()))
        cur.execute("""
            SELECT DISTINCT department
            FROM employees
            ORDER BY department
            """)
        departments = [row[0] for row in cur.fetchall()]
    return template(
        "view-by-department-form", active_page="view-by-department", departments=departments
    )


@app.post("/view-by-department")  # type: ignore
def do_list_by_department() -> str:
    """Display the employees in the department."""
    # pylint: disable-next=no-member
    department: Optional[str] = request.forms.get("department")  # type: ignore
    pay_period: str = ""
    employees: list[EmployeePayrollViewModel] = []
    with ExitStack() as db_stack:
        # auto-close connection, auto-commit/rollback transaction, auto-close cursor
        con = db_stack.enter_context(closing(sqlite3.connect(DB_PATH)))
        db_stack.enter_context(con)
        cur = db_stack.enter_context(closing(con.cursor()))
        cur.execute("""
            SELECT MAX(pay_period)
            FROM pay_data
            """)
        pay_period = cur.fetchone()[0]
        cur.row_factory = employee_payroll_factory
        cur.execute(
            f"""
            SELECT
                employees.emp_id
              , employees.emp_name
              , employees.department
              , employees.wage
              , pay_data.hrs_worked
            FROM employees
                JOIN pay_data
                    ON employees.emp_id = pay_data.emp_id
            WHERE pay_data.pay_period = ?
                {"AND employees.department = ?" if department else ""}
            """,
            (pay_period, department) if department else (pay_period,),
        )
        employees = cur.fetchall()
    return template(
        "list-employee-payroll.tpl",
        active_page="view-by-department",
        department=department,
        pay_period=pay_period,
        employees=employees,
    )


@app.get("/edit-employee-data")  # type: ignore
def edit_employee_data() -> str:
    """Display the form to enter the employee ID and hours worked."""
    return template("edit-employee-data-form", active_page="edit-employee-data")


@app.post("/edit-employee-data")  # type: ignore
def do_edit_employee_data() -> str:
    """Update the employee's hours worked."""
    # pylint: disable-next=no-member
    emp_id = int(request.forms.get("emp_id"))  # type: ignore
    # pylint: disable-next=no-member
    hrs_worked = float(request.forms.get("hrs_worked"))  # type: ignore
    pay_period: str = ""
    employee: Optional[EmployeePayrollViewModel] = None
    try:
        with ExitStack() as db_stack:
            # auto-close connection, auto-commit/rollback transaction, auto-close cursor
            con = db_stack.enter_context(closing(sqlite3.connect(DB_PATH)))
            db_stack.enter_context(con)
            cur = db_stack.enter_context(closing(con.cursor()))
            cur.execute("""
                SELECT MAX(pay_period)
                FROM pay_data
                """)
            pay_period = cur.fetchone()[0]
            cur.execute(
                """
                UPDATE pay_data
                SET hrs_worked = ?
                WHERE emp_id = ?
                    AND pay_period = ?
                """,
                (hrs_worked, emp_id, pay_period),
            )
            cur.row_factory = employee_payroll_factory
            cur.execute(
                """
                SELECT
                    employees.emp_id
                  , employees.emp_name
                  , employees.department
                  , employees.wage
                  , pay_data.hrs_worked
                FROM employees
                    JOIN pay_data
                        ON employees.emp_id = pay_data.emp_id
                WHERE employees.emp_id = ?
                    AND pay_data.pay_period = ?
                """,
                (emp_id, pay_period),
            )
            employee = cur.fetchone()
            if not employee:
                raise sqlite3.Error(f"Employee ID {emp_id} not found.")
    except sqlite3.Error as err:
        return template(
            "edit-employee-data-form",
            active_page="edit-employee-data",
            alert_context="danger",
            alert_message=f"Could not update employee data: {err}",
        )
    employee = cast(EmployeePayrollViewModel, employee)
    return template(
        "list-employee-payroll",
        active_page="edit-employee-data",
        department=employee.department,
        pay_period=pay_period,
        employees=[employee],
        alert_context="success",
        alert_message="Successfully updated employee data.",
    )


def _main():
    """Main entry point for the bottle application."""
    app.run(host="localhost", port=8080, debug=True, reloader=True)


if __name__ == "__main__":
    _main()
