#!/usr/bin/env python3.9
"""CIT 244: Python II (4226_55Z1) - Program 1. Classes

We're going to write a program that manages the email address of our
contacts. Your program must contain a class named contact that has 3
attributes (instance variables): last name, first name, and email. Your
class should also have a method to return the full name and email
address for printing when requested. You may add other methods to the
class if you like.

Each contact should use a single instance of your contact class. You
should use either a list or a dictionary to act as a container of the
contact instances.

Also, the program should have a menu that allows the user to interact
with your collection of contacts: displaying contacts or adding new
contacts as long as the user wishes, then saying goodbye when finished.
The menu should offer these options.

.. code:: pycon

   Program Options.
      1.) Display all contacts
      2.) Create new contact
      3.) Exit
   >>> option = input("Enter 1, 2, or 3: ")

For full credit.

- use a python class to represent the contact info and at least one
  method to print that info.
- collect each new contact instance in a list or dictionary.
- please format printed output so all column data lines up.

Here is a possible print-out, where we display some pre-existing
contacts, add a new contact, then re-display the list to see that our
contact has been added. Again, you are not required to save to disk
before exiting.

.. code:: console

     Program Options.
        1.) Display all contacts
        2.) Create new contact
        3.) Save and exit

    Enter 1, 2, or 3: 1

    Name            Email
    smith, sue      ssmith@wer.com
    Dean, hugh      hrdean@abc.com
    green, sam      sgreen@rty.com

     Program Options.
        1.) Display all contacts
        2.) Create new contact
        3.) Save and exit

    Enter 1, 2, or 3: 2

    Enter contact's first name: mac
    Enter contact's last name: davis
    Enter contact email: mdavis@asd.com

     Program Options.
        1.) Display all contacts
        2.) Create new contact
        3.) Save and exit

    Enter 1, 2, or 3: 1

    Name            Email
    smith, sue      ssmith@wer.com
    Dean, hugh      hrdean@abc.com
    green, sam      sgreen@rty.com
    davis, mac      mdavis@asd.com

     Program Options.
        1.) Display all contacts
        2.) Create new contact
        3.) Save and exit

    Enter 1, 2, or 3:
"""

__author__ = "Chet Gray <cgray0209@kctcs.edu>"
__copyright__ = "Copyright  2023 Chet Gray"
__license__ = "MIT"


from dataclasses import dataclass
from typing import Iterable


class Contact:
    """A contact has a last name, first name, and email address.

    Your program must contain a class named contact that has 3 attributes (instance variables):
    last name, first name, and email. Your class should also have a method to return the full
    name and email address for printing when requested.
    """

    def __init__(self, last_name: str, first_name: str, email: str) -> None:
        """Initialize a new contact.

        Parameters
        ----------
        last_name : str
            The contact's last name.
        first_name : str
            The contact's first name.
        email : str
            The contact's email address.
        """
        self.last_name = last_name
        self.first_name = first_name
        self.email = email

    def __str__(self) -> str:
        """Return the full name and email address for printing.

        Returns
        -------
        str
            The full name and email address for printing.
        """
        return f'"{self.last_name}, {self.first_name}" <{self.email}>'


@dataclass
class Column:
    """A column in a table.

    Parameters
    ----------
    header : str
        The column header.
    attr : str
        The attribute of the contact to display in this column.
    width : int, default=0
        The width of the column, by default 0
    """

    header: str
    attr: str
    width: int = 0


def print_table(records: Iterable[object], columns: Iterable[Column]) -> None:
    """Print a table of records.

    Parameters
    ----------
    records : Iterable[object]
        The list of records to print.
    columns : Iterable[Column]
        The columns of attributes from those records to print.
    """
    # Determine the necessary column widths, and print accordingly.
    for column in columns:
        column.width = len(column.header)
        for record in records:
            column.width = max(column.width, len(getattr(record, column.attr)))
    print("  ".join(column.header.ljust(column.width) for column in columns))
    print("  ".join("=" * column.width for column in columns))
    for record in records:
        print("  ".join(getattr(record, column.attr).ljust(column.width) for column in columns))


def _main() -> None:
    """The main entry point of the program.

    Also, the program should have a menu that allows the user to interact with your collection
    of contacts: displaying contacts or adding new contacts as long as the user wishes, then
    saying goodbye when finished. The menu should offer these options.
    """
    contacts: list[Contact] = [
        Contact("Marquardt", "Eda", "emarquardt@example.com"),
        Contact("Hartman", "Earl", "ehartman@example.com"),
        Contact("Muller", "Lester", "lmuller@example.com"),
    ]
    columns = [
        Column("Last Name", "last_name"),
        Column("First Name", "first_name"),
        Column("Email", "email"),
    ]

    while True:
        print(
            "Enter a menu selection:\n"
            "[1] Display all contacts\n"
            "[2] Create new contact\n"
            "[3] Exit\n"
        )
        menuInput = input(">>> ").strip()
        print()
        if menuInput == "1":  # Display all contacts
            print_table(contacts, columns)
            print()
        elif menuInput == "2":  # Create new contact
            first_name = input("Enter contact's first name: ").strip()
            last_name = input("Enter contact's last name: ").strip()
            email = input("Enter contact email: ").strip()
            print()
            new_contact = Contact(last_name, first_name, email)
            contacts.append(new_contact)
            print(f"Successfully created contact: {new_contact}")
            print()
        elif menuInput == "3":  # Exit
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")
            print()
            continue


if __name__ == "__main__":
    _main()
