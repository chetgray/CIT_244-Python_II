CIT 244: Python II (4226_55Z1) - Program 3: Python & databases - sqlite3
and the wx.ListCtrl
========================================================================

.. role:: python(code)
   :language: python

.. role:: sql(code)
    :language: sql

You need to do 2 things to make this program work.

1. Create a sqlite3 database named ``speeding_tickes.db``, create a
   table within that database named tickets, then take the CSV file in
   this link and import that data into the tickets table. `tickets.csv`_
2. Write a program that reads the data from the table and inserts it
   into a :python:`wx.ListCtrl`. The program also uses a dialog box to
   allow adding new records to the table.

For me to run and grade your program using my database, our two database
need the have the same db name, same column names, and the same column
data types. So, please follow the given instructions carefully.

    The table holds real data for the first 49 speeding tickets issued
    during the early hours of July 4th, 2014, in or sort of near St.
    Paul, Minnesota.

Database name: ``speeding_tickets.db``

| Table name: ``tickets``
| column names: ``tid``, ``stop_data``, ``stop_time``, ``actual_speed``,
  ``posted_speed``, ``miles_over``, ``age``, ``violator_sex``
| ``tid``, the :sql:`INTEGER PRIMARY KEY`, is *not* auto-incrementing.
  Here's a possible SQL statement to create the table. Note column names
  and data types:

.. code-block:: sql

    CREATE TABLE tickets (
       tid INTEGER NOT NULL,
       stop_date TEXT NOT NULL,
       stop_time TEXT NOT NULL,
       actual_speed INTEGER NOT NULL,
       posted_speed INTEGER NOT NULL,
       miles_over INTEGER NOT NULL,
       age INTEGER NOT NULL,
       violator_sex TEXT NOT NULL,
       PRIMARY KEY (
          tid
       )
    );

And here's a glimpse of the first few records, starting at 11 minutes
into the morning of July 4th, 2014, as seen in SqliteStudio.

===== ========= ========= ============ ============ ========== === ============
tid   stop_date stop_time actual_speed posted_speed miles_over age violator_sex
===== ========= ========= ============ ============ ========== === ============
20124 7/4/2014  0:11:00   95           70           25         20  Female
20125 7/4/2014  0:36:00   95           70           25         25  Male
20126 7/4/2014  1:02:00   76           55           21         25  Male
20127 7/4/2014  1:02:00   77           60           17         27  Male
20128 7/4/2014  1:15:00   83           70           13         51  Female
20129 7/4/2014  1:28:00   88           55           33         25  Male
20130 7/4/2014  1:33:00   97           70           27         29  Male
20131 7/4/2014  1:52:00   74           30           44         35  Male
20132 7/4/2014  3:42:00   66           55           11         19  Male
20133 7/4/2014  3:51:00   50           40           10         25  Male
20134 7/4/2014  6:23:00   87           65           22         45  Male
20135 7/4/2014  6:27:00   85           70           15         32  Female
===== ========= ========= ============ ============ ========== === ============

The Program Assignment
----------------------

There is an example program in the lecture notes that is pretty similar
in structure to this assignment. Studying that example and watching the
associated video before starting this program will save you time in the
long run. Just sayin'.

Write a program that reads table data from the database into a
:Python:`wx.ListCtrl`. The database will be named ``speeding_tickets``
and the table is to be named ``tickets``. The CSV file contains a row of
8 heading and then 49 rows of records.

Your interface will need a :python:`wx.Frame` and a
:python:`wx.ListCtrl` and 3 buttons. A "Display" button loads all of the
ticket data into the list control. An "Insert Citation" button will open
a :python:`wx.Dialog` that allows the user to enter the 8 data items
used for a single record. When the user closes the dialog the new record
will be SQL :sql:`INSERT`ed to the tickets table and the list control
re-populated so as to display the inserted record. You also need a
"Close" button to close the program.

A possible interface might look like this; you may design your own
layout as long is it works like that shown. The list control should be
wide enough that you don't need a horizontal scroll bar. A vertical
scroll bar is fine.

.. image:: https://alt-5beddfe10b70f.blackboard.com/bbcswebdav/pid-47334894-dt-content-rid-349590076_2/courses/JFC_4226_CIT_244_55Z1_83606/JFC_4226_CIT_244_55Z1_83606_ImportedContent_20221205032009/programs/p3_tickets_table.PNG

Clicking the "Insert Citation" button should open a dialog box that
allows adding a new record to the table. You do not necessarily need to
have the dialog widgets in 2 columns as shown, a single column would
work just as well.

.. image:: https://alt-5beddfe10b70f.blackboard.com/bbcswebdav/pid-47334894-dt-content-rid-349590076_2/courses/JFC_4226_CIT_244_55Z1_83606/JFC_4226_CIT_244_55Z1_83606_ImportedContent_20221205032009/programs/p3_tickets_dialog.PNG

After entering data for a new record, clicking the "OK" button in the
dialog box should insert the record into the tickets table. Your code
should then repopulate the list control so as to include the new record.

If you missed it, once more here's a link to the tickets CSV file.

    `tickets.csv`_

.. _`tickets.csv`: https://alt-5beddfe10b70f.blackboard.com/bbcswebdav/pid-47334894-dt-content-rid-349590076_2/courses/JFC_4226_CIT_244_55Z1_83606/JFC_4226_CIT_244_55Z1_83606_ImportedContent_20221205032009/programs/tickets.csv

Here's what you need to do to get 100% on this one.

- create a sqlite3 database named ``speeding_tickets`` and create a
  table named ``tickets`` with the field names spelled exactly like
  those given in the CSV file. I recommend using the SQliteStudio, but
  you may use whatever program or method you want. There is a video on
  using Sqlite Studio in the lecture notes. You'll need to import the
  CSV file into SqliteStudio (or whatever) to generate the database.
- Your program should work with my database. For simplicity, as you
  write your program keep your database file in the same folder as your
  program so that we don't have any path issues.
- import the CSV file into the students table with the exact field names
  as given in the file. You should have 49 records.
- your program should properly connect to the database you created using
  techniques from the lecture notes.
- the ID field should be an :sql:`INTEGER PRIMARY KEY`. it does not need
  to be auto-incrementing.
- ``actual_speed``, ``posted_speed``, ``miles_over``, and ``age`` should
  all be :sql:`INTEGER`s.
- ``stop_date``, ``stop_time``, and ``violator_sex`` should be of type
  :sql:`TEXT`.
- the "Display" button should load the whole table into the list control
- the "Insert Citation" button should open a custom dialog that allows
  entering a new, complete record
- when the dialog is closed the new record is added to the tickets table
  using an SQL :sql:`INSERT`` statement and the updated table should
  then be re-displayed in the list control
- the "Close" button closes the program.
- you may use sizers or absolute positioning, your choice, but all
  widgets need to be visible to the user without having to resize the
  window.
