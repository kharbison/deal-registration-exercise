# Deal Registration Exercise Design Document

This document is an overview of the design approach taken on this project. See the [Install Guide](https://github.com/kharbison/deal-registration-exercise/tree/master/README.md) for instructions on how to install and run the application.

## Requirements

Project overview and requirements can before found [here](https://github.com/CChastang/deal-registration-exercise/issues/1).

#### Special Considerations:
- The Database should be capable of being updated at any time with new CSV file(s).
- Part Numbers with an inactive status should not return a Deal Registration Group to the user.


## Application Design

This application consists of a parser that processes the given CSV files and stores them into a database, a frontend that allows the user to give a part number as input to get back a Deal Registration Group, and a backend that accepts the REST call with the requested part number and queries the database to return the associated Deal Registration Group.

#### Technologies Used:
- CSV parsing and data injection: Python
- Database: PostgreSQL
- Backend Server: Node.Js/Express
- Frontend web framework: Vue and Carbon
- Deployment: Docker

#### Component Interactions:

CSV Parser <----> PostgreSQL <----> Server <----> Web App

### Frontend Web App

The frontend web app can be accessed by going to http://localhost:8080. Here the user can get the Deal Registration Group of a part number by entering the part number into the text field and clicking the 'search' button. If a group is returned, the part number and associated group will be displayed in a table on the screen.

Successful searches will collect in the table with the most resent search always appearing at the top. This history data can be cleared at any time by clicking the 'clear history' button.

If an error is returned from the search, an alert will be displayed for the user with more specific details about why the error might have occured.

### Backend Server

The backend server accepts a GET request from the frontend with a part number included. Once this request is received a query with the part number is sent to database and the result of this query is examinded to determine the correct response needing to be sent to the frontend.

#### Query Responses w/ Actions Taken:
- An entry is found with the requested part number and the active flag is not N.
    * The Deal Registration Group is returned to the frontend.

- An entry is found with the requested part number but the active flag is N or the query does not return any results.
    * A 404 Error is returned with no entires or active entries found response.

- More than one result is returned.
    * A 500 Internal server error is returned because this, in theory, should never happen.

If the user does not give a valid part number to search, a 422 Unprocessable Entry is returned to the user with an explanation of what the part number should look like.

### CSV Parser

The CSV parser takes at least one csv file, verifies each row for syntactically correct data, handles identifying and eliminating duplicates, removes any old data existing in the database, and injects the new data into the database.

#### Data Verification

Because the data received may not always be completely clean, validation of each column is done on every row.

- #### Part Number
    * A part number is considered valid if it starts with letters indicating its type (Saas, SW, etc.) followed by the letters PT and any combination of numbers afterwards.
- #### Deal Registration Group
    * The group of each part number is checked for any content. A row with an empty group string will not be accepted as valid data.
- #### Date Strings (Start Date, End Date, Add Date, Modified Date)
    * There are 5 excepted formats for the date strings. Any rows that have date string that can not be parsed will not be added to the database
        * MM/dd/YY or MM/dd/YYYY
            * month and day can be formated as 1 or 01
        * MM/dd/YY hh:mm:ss AM/PM or MM/dd/YYYY hh:mm:ss AM/PM
        * YYYY-MM-dd-HH.mm.ss.f
    - A row is consided invalid if the End Date or Modified Date are earlier in time compared to their respective Start Date and Add Date.
- #### Active Flag
    * An active flag does not have to be defined for each row but if it is it must either be Y or N (case does not matter).
    * Each row in the database is stored with an active flag even if it was not supplied in the data given. All rows without a flag present will be stored with an active flag of N/A.

Due to design and development time constraints some assumptions were made about the level of cleanliness the data would be given in.

#### Assumptions:
1. Because new part types may be added at any time, it is assumed that if the part number is in the correct format string then it should be accepted as a valid part number.

2. Group names may contain any combination of words, numbers, and symbols so it is assumed that as long as a group name is given for the part it is valid.

3. There are so many different ways to format a date string that when the month and day numbers are in the lower range of values it can become confusing as to how to parse the string so it is assumed that the dates are formated into one of the five examples seen above.

4. Some date strings have the year 9999 represented as 99 and standard parsing sees this value as 1999 instead of 9999. It is assumed that if there is no active flag or the active flag is set to Y, then 99 should represent 9999.

#### Duplicate Data Handling

Once a row has been determined to have valid data, it is added to a temperary list to await database injection. Before being added to this list, the current items are searched to find out if an already validated row contains the same part number as the one trying to be added. If a duplicate part number is found, the two rows go through a check list to determine which row should be used.

In each case below, if the answer is no then the next question is considered otherwise the action underneath the question is taken.

1. Is ALL data in both rows the exact same?
    * Yes: Keep the existing row and get rid of the new one.
    * No: Move to question 2.

2. Are the end dates of the two rows different?
    * Yes: Keep the row with the end date that is farthest in the future.
    * No: Move to question 3.

3. Are the start dates of the two rows different?
    * Yes: Keep the row with the start date that is most recent.
    * No: Move to question 4.

4. Are the active flags of the two rows different? (i.e. Y N and not Y Y, N N, or N/A N/A)
    * Yes: Keep the row that has Y for the active flag.
        * Tables that do not contain an active flag will not have different values for this.
    * No: Move to question 5.

5. Are the modification dates of the two rows different?
    * Yes: Keep the row thas was most recently modified.
    * No: See below.

If all questions aboved are answered with a no, then an error is thrown and the user is notified that the validity of the duplicates could not be determined and the parser moves on to the next row keeping the old row in the database.

#### Data Injection into the Database

Because the database can be updated at any time while the user is able to request part number data from it, data from each given table is only inserted into the database once all valid rows have been collected and duplicate part numbers have been eliminated.

To insert the data, a bulk delete is first permformed on any matching part types(Saas, SW, etc.) that currently exist in the database. This ensures that all data in the database is fully up to date with the most current table received. Once any already existing data has be removed, a bulk insert is performed and all valid rows from the parsed table are added to the database.

Performing bulk deletes and inserts keeps data from being added to the database that is not valid.

If the database or table does not exist when the script wants to insert new data, they will be created before any attempt is made to insert into them.
