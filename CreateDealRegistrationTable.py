import os
import sys
import argparse
import csv
import datetime
from dateutil.parser import parse

#region Variables

#endregion

#region Define Arg Parser
def parse_args():
  argParser = argparse.ArgumentParser(description='Insert/Update Data Registration Table database with give .csv files.')
  argParser.add_argument('csvFiles', nargs='+', type=str, help='csv file(s) to update or add to a database')
  receivedArgs = argParser.parse_args()
  return receivedArgs
#endregion

#region Funtions
def parseDate(dateToParse):
  try:
    dt = parse(dateToParse)
    return dt
  except:
    dt = datetime.datetime.strptime(dateToParse, "%Y-%m-%d-%H.%M.%S.%f")
    return dt

def parseRow(rowToParse):
  parsedRow = dict.copy(rowToParse)
  for column, value in parsedRow.items():
    if 'DATE' in column:
      # Abreviated year 99 from 9999 will be interpreted as 1999 instead of 9999.
      # Verify that Start date comes after 1999 to ensure 9999 would be correct date.
      if column == 'END_DATE' and '99' in value and not '9999' in value:
        if type(parsedRow['START_DATE']) is datetime.datetime and parsedRow["START_DATE"].year > 1999:
          value = str.replace(value, '99', '9999')
        # Todo: Handle instance when start time as not been parsed yet. Will not happen with current csv file format.
      try:
        parsedRow[column] = parseDate(value)
      except ValueError:
        raise(ValueError(f'Unable to parse date into dateTime value: {value}'))
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
      parsedRow = parseRow(row)
      print(parsedRow)
      print(parsedRow['START_DATE'])
      print(parsedRow['END_DATE'])
      index = index + 1
      #Don't want to go through all lines in file right now so break after 10 lines
      if index > 9 :
        break

#endregion
