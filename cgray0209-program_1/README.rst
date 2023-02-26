CIT 244: Python II (4226_55Z1) - Program 1. Classes
===================================================

We're going to write a program that manages the email address of our
contacts. Your program must contain a class named contact that has 3
attributes (instance variables): last name, first name, and email. Your
class should also have a method to return the full name and email
address for printing when requested. You may add other methods to the
class if you like.

Please start early in the week that this program is due; this gives you
plenty of time to ponder how is should work. Moreover, there will be
more to ponder as the course progresses. I am glad to help troubleshoot
programs, but I go to bed reasonably early and am unlikely to stay up
until midnight of the due date.

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

There are several examples of this kind of menu program scattered
throughout the lecture notes for the first several weeks of the
semester. The example most relevant to this assignment comes as the end
of the notes on Classes.

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
