"""CIT 244: Python II - Program 6: Bootstrap
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
