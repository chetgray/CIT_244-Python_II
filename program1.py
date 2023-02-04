#!/usr/bin/env python3.9
""" CIT 244: Python II (4226_55Z1) - Program 1. Classes

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
        return f"{self.last_name}, {self.first_name}\t\t\t{self.email}"


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

    while True:
        print(
            """Enter a menu selection:
[1] Display all contacts
[2] Create new contact
[3] Exit
"""
        )
        menuInput = input(">>> ").strip()
        print()
        if menuInput == "1":
            print("Name\t\t\t\tEmail")
            print("====\t\t\t\t=====")
            for contact in contacts:
                print(contact)
            print()
        elif menuInput == "2":
            pass
        elif menuInput == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")
            print()
            continue


if __name__ == "__main__":
    _main()
