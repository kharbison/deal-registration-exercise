import os
import sys
import argparse
import csv
import re
from datetime import datetime

from deal_reg_row import DealRegRow
from deal_reg_db import updateDealRegTableWithRows

#region Variables
#endregion

#region Define Arg Parser
def parse_args():
    argParser = argparse.ArgumentParser(description='Insert/Update Data Registration Table database with given .csv files.')
    argParser.add_argument('csvFiles', nargs='+', type=str, help='csv file(s) to update or add to a database')
    receivedArgs = argParser.parse_args()
    return receivedArgs
#endregion

#region Funtions
def verifyPNFormat(partNumber):
    """Part number should look something like SWPT000001
    Throw error if it does not match this format to keep
    row from being added to database"""

    if not type(partNumber) is str:
        raise TypeError(f'{partNumber} should be a string but is not.')

    result = re.fullmatch("^[A-Z]+PT[0-9]+$", partNumber)

    if result == None:
        raise ValueError(f'PartNumber does not fit the specified format of *PT#: {partNumber}')


def verifyDealRegGroup(regGroup):
    """There is no common pattern to the Deal Registration Groups
    so verify that it has a value that is not an empty string.
    Throw an error if it is '' so the row does not get added to the database"""

    if not type(regGroup) is str:
        raise TypeError(f'{regGroup} should be a string but is not.')

    if regGroup == '':
        raise ValueError(f'Deal Registration Group cannot be empty.')


def parseDate(dateName, dateToParse):
    """Check that the date given matches one of the excepted formats.
    Other formats will not be accepted at this time to reduce parsing confusion.
    If no formats match, throw and error to keep the row from being added to the database.
    Return: parsed datetime object"""

    if not type(dateToParse) is str:
        raise TypeError(f'{dateToParse} should be a string but is not.')

    for dtFmt in ("%m/%d/%Y %I:%M:%S %p","%m/%d/%y %I:%M:%S %p", "%Y-%m-%d-%H.%M.%S.%f", "%m/%d/%y", "%m/%d/%Y"):
        try:
            return datetime.strptime(dateToParse, dtFmt)
        except ValueError:
            pass

    raise ValueError(f'Unable to parse {dateName} into dateTime value: {dateToParse}')


def parseActiveFlag(activeFlag):
    """Verify that flag value given is either Y or N.
    Throw and error if it is not to keep the row from being added
    to the database.
    Return: case corrected Flag value"""

    if not type(activeFlag) is str:
        raise TypeError(f'{activeFlag} should be a string but is not.')

    #Case does not matter so change the flag value to upper case before verifying
    flag = activeFlag.upper()

    if not flag == 'Y' and not flag == 'N':
        raise ValueError(f'Active Flag value is not in the correct format of Y or N: {activeFlag}')
    else:
        return flag


def verifyAndParseRow(rowToParse):
    """Verify each row and stored the correctly parsed value
    of each column into a new dictionary. We don't want to modify
    the row from the csv file and we want to fix any case differences
    with the header values between tables.
    Return: the newly parsed row"""

    parsedRow = {}
    #verify each column value for the given row
    for column, value in rowToParse.items():
        columnName = column.upper()

        if columnName == 'PART_NUM':
            # Verify part number starts with prefix and has PT# afterwards
            verifyPNFormat(value)
            parsedRow[columnName] = value
            #print(f'{column} is valid')

        elif columnName == 'DEAL_REG_GROUP':
            verifyDealRegGroup(value)
            parsedRow[columnName] = value
            #print(f'{column} is valid')

        elif 'DATE' in columnName:
            # Abreviated year 99 from 9999 will be interpreted as 1999 instead of 9999.
            if columnName == 'END_DATE' and '99' in value and not '9999' in value:
                if 'ACTIVE_FLAG' in parsedRow:
                    if parsedRow['ACTIVE_FLAG'] == 'Y':
                        value = str.replace(value, '99', '9999')
                else:
                    value = str.replace(value, '99', '9999')

            # Attempt Date Time Parse
            parsedRow[columnName] = parseDate(column, value)
            #print(f'{column} is valid and parsed to {parsedRow[columnName]}')

        elif columnName == "ACTIVE_FLAG":
            parsedRow[columnName] = parseActiveFlag(value)
            #print(f'{column} is valid and parsed to {parsedRow[columnName]}')

        else:
            pass

    # Compare dates to check validity of the dates given
    start = parsedRow['START_DATE']
    end = parsedRow['END_DATE']
    if start > end:
        raise ValueError(f'The start date was determined to be greater than the end date. This format is invalid. Start Date: {start}  End Date: {end}')

    add = parsedRow['ADD_DATE']
    mod = parsedRow['MODIFIED_DATE']
    if  add > mod:
        raise ValueError(f'The add date was determined to be greater than the modified date. This format is invalid. Add Date: {add}  Modified Date: {mod}')

    # Row is valid and can be returned to be added.
    return parsedRow


def checkNewRowNeeded(oldRow, newRow):
    """Compare duplicate row values to see which one should be kept.
    Return: True (replace old value with new one)
            False (keep old value and do not add new one)"""

    if not oldRow.endDate == newRow.endDate:
        return oldRow.endDate < newRow.endDate
    else:
        if not oldRow.addDate == newRow.addDate:
            return oldRow.addDate < newRow.addDate
        else:
            if oldRow.activeFlag == newRow.activeFlag:
                if not oldRow.modDate == newRow.modDate:
                    return oldRow.modDate < newRow.modDate
                else:
                    raise ValueError(f'Unable to determine validity of duplicate row for part number {newRow.partNum}. Both rows only differ in the Deal Reg Group they are assigned to.')
            else:
                return oldRow.activeFlag == 'N' and newRow.activeFlag == 'Y'


def addNewRow(validRow, allRows):
    """Create new DealRegRow object from valid row, check to see if
    a duplicate already exists, determine which row to keep if it does or
    add the new row if it doesn't"""

    newRow = DealRegRow(validRow)

    # If a duplicate exists only one should be found because this check is preformed each time
    # a new row needs to be added
    duplicateRow = next((item for item in allRows if item.partNum == newRow.partNum), None)

    if duplicateRow == None:
        allRows.append(newRow)
    else:
        if duplicateRow.areEqual(newRow):
            # New row does not need to be added because an exact match already exists
            pass
        else:
            newRowNeeded = checkNewRowNeeded(duplicateRow, newRow)

            if newRowNeeded:
                #Remove old Row first then add new one
                allRows.remove(duplicateRow)
                allRows.append(newRow)
            else:
                # New row is not needed and old row needs to stay
                pass


def main():
    #Check received args first
    args = parse_args()
    #print(args)

    for fileName in args.csvFiles:
        tableRows = []
        with open(fileName, "r", encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for index, row in enumerate(reader):
                try:
                    parsedRow = verifyAndParseRow(row)
                    addNewRow(parsedRow, tableRows)
                except ValueError as ex:
                    print(f'\n\nError Found: Row {index} of {fileName} is not valid and will not be added to the database.\n')
                    print(ex)
                except TypeError as ex:
                    print(f'\n\nError Found: Row {index} of {fileName} has a column value that is not of the correct type.\n'
                    + 'This row will not be added to the database.')
                    print(ex)
                except Exception as ex:
                    print('Unexpected Error Found: Error found while parsing row.')
                    print(ex)
                #Don't want to go through all lines in file right now so break after 10 lines
                #print(row)
                #print(parsedRow)
                #if index > 10 :
                    #break

        #for singleRow in tableRows:
           # attrs = vars(singleRow)
           # print('\n')
           # print(', '.join("%s: %s" % item for item in attrs.items()))
        try:
            updateDealRegTableWithRows(tableRows)
        except Exception as ex:
            print('\nError updating database with table data:\n')
            print(ex)




#endregion

#region Main
if __name__ == "__main__":
    main()
else:
     pass
#endregion
