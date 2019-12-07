import os
import sys
import argparse
import csv
import re
from datetime import datetime
import DealRegRow

#region Variables
RowsToAdd = []
#endregion

#region Define Arg Parser
def parse_args():
  argParser = argparse.ArgumentParser(description='Insert/Update Data Registration Table database with give .csv files.')
  argParser.add_argument('csvFiles', nargs='+', type=str, help='csv file(s) to update or add to a database')
  receivedArgs = argParser.parse_args()
  return receivedArgs
#endregion

#region Funtions
def verifyPNFormat(partNumber):
  result = re.fullmatch("^[A-Z]+PT[0-9]+$", partNumber)
  if result == None:
    raise ValueError()

def verifyDelRegGroup(regGroup):
  if regGroup == '':
    raise ValueError()

def parseDate(dateToParse):
  for dtFmt in ("%m/%d/%Y %I:%M:%S %p","%m/%d/%y %I:%M:%S %p", "%Y-%m-%d-%H.%M.%S.%f", "%m/%d/%y", "%m/%d/%Y"):
    try:
      return datetime.strptime(dateToParse, dtFmt)
    except ValueError:
      pass

  raise ValueError()

def parseActiveFlag(activeFlag):
  flag = activeFlag.upper()
  if not flag == 'Y' and not flag == 'N':
    raise ValueError()
  else:
    return flag

def verifyAndParseRow(rowToParse):
  parsedRow = {}
  #verify each column value for the given row
  for column, value in rowToParse.items():
    columnName = column.upper()

    if columnName == 'PART_NUM':
      # Verify part number starts with prefix and has PT# afterwards
      try:
        verifyPNFormat(value)
        parsedRow[columnName] = value
        print(f'{column} is valid')
      except ValueError:
        raise ValueError(f'PartNumber does not fit the specified format of *PT#: {value}')

    elif columnName == 'DEAL_REG_GROUP':
      try:
        verifyDelRegGroup(value)
        parsedRow[columnName] = value
        print(f'{column} is valid')
      except ValueError:
        raise ValueError(f'Deal Registration Group cannot be empty.')

    elif 'DATE' in columnName:
      if 'END' in columnName:
        # Abreviated year 99 from 9999 will be interpreted as 1999 instead of 9999.
        if columnName == 'END_DATE' and '99' in value and not '9999' in value:
          if 'ACTIVE_FLAG' in parsedRow:
            if parsedRow['ACTIVE_FLAG'] == 'Y':
              value = str.replace(value, '99', '9999')
          else:
              value = str.replace(value, '99', '9999')

      # Attempt Date Time Parse
      try:
        parsedRow[columnName] = parseDate(value)
        print(f'{column} is valid and parsed to {parsedRow[columnName]}')
      except ValueError:
        raise ValueError(f'Unable to parse {column} into dateTime value: {value}')

    elif columnName == "ACTIVE_FLAG":
      try:
        parsedRow[columnName] = parseActiveFlag(value)
        print(f'{column} is valid and parsed to {parsedRow[columnName]}')
      except ValueError:
        raise ValueError(f'Active Flag value is not in the correct format of Y or N: {value}')

    else:
      pass

  return parsedRow


#endregion

#region Main
#Check received args first
args = parse_args()
print(args)

for fileName in args.csvFiles:
  with open(fileName, "r", encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    index = 0
    for row in reader:
      parsedRow = verifyAndParseRow(row)
      print(parsedRow)
      index = index + 1
      #Don't want to go through all lines in file right now so break after 10 lines
      if index > 9 :
        break

#endregion
