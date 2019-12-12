import re
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy_utils import database_exists, create_database

#region Global
if not 'DEAL_REG_DB_URL' in os.environ:
    print('Error: Environment variable DEAL_REG_DB_URL does not exist. \n'
           + 'Set this variable to the PostgreSQL DB path so this program can modify the database.')
    sys.exit()
elif os.getenv('DEAL_REG_DB_URL') == '':
    print('Error: Environment Variable DEAL_REG_DB_URL cannot be an empty string.\n'
          + 'Set this variable to the PostgresSQL DB path so this program can modify the database.')
    sys.exit()

engine = create_engine(os.getenv('DEAL_REG_DB_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()
#endregion

#region DB Table Schema

class DealRegTable(Base):
    __tablename__ = 'tbl_deal_reg'
    id = Column(Integer, primary_key = True)
    part_num = Column(String)
    deal_reg_group = Column(String)
    active_flag = Column(String)
    end_date = Column(DateTime)
    part_type = Column(String)

    def __init__ (self, rowToAdd):
        self.part_num = rowToAdd.partNum
        self.deal_reg_group = rowToAdd.dealRegGroup
        self.active_flag = rowToAdd.activeFlag
        self.end_date = rowToAdd.endDate
        self.part_type = rowToAdd.partType
#endregion

#region functions
def closeSession(activeSession):
    print('Closing Session')
    activeSession.commit()
    activeSession.close()


def updateDealRegTableWithRows(allTableRows):
    global engine
    global Session
    global Base

    if not database_exists(engine.url):
        print('Creating Database')
        create_database(engine.url)

    print('database is active, creating session and schema for the table.')

    # Generate Schema for Deal Registration Table
    Base.metadata.create_all(engine)

    # Create Session to interact with table
    session = Session()

    try:
        # allTableRows shouldn't be empty, throw error if it is
        if len(allTableRows) == 0:
            raise IndexError('Error: Input does not contain any rows to modify the database with.')

        #Get part number type prefix to determine if any already exist in the table
        queryPrefix = re.match( "^[A-Z]+PT", allTableRows[0].partNum)


        if queryPrefix != None:
            # Get prefix string from regex match and create empty list
            # for generated table rows to go
            prefixString = queryPrefix.group(0)
            newTableRows = []

            # Attempt to generate all rows before any table manipulation is done.
            # We don't want to manipulate the database with bad data
            for row in allTableRows:
                newTableRows.append(DealRegTable(row))

            # if rows were generated and no error thrown update/add the new rows
            if len(newTableRows) > 0:

                # Delete all parts currently in the database that have the same prefix.
                # To make sure all data is up to date we want to completely blow away the
                # current table data of the matching type so the new data can be inserted.
                # This will help insure that all rows in the database are correct.
                itemsDeleted = session.query(DealRegTable) \
                                      .filter(DealRegTable.part_num.contains(prefixString)) \
                                      .delete(synchronize_session = False)

                print(f'{itemsDeleted} parts deleted from the Deal Registration table containing the {prefixString} prefix')

                # Aftrer any necessary deletes were made. Bulk add all of the new rows to the database.
                session.add_all(newTableRows)

                print(f'{len(newTableRows)} added to the Deal Registration table.')

            else:
                # It is unlikely that this exception will be thrown but it is here just in case
                raise ValueError('Unable to add updated part numbers to Deal registration '
                                + 'table because no new rows were able to be created.\n\n'
                                + 'No modifications were done to the database.')

        else:
            # The likelyhood of the row data received not matching to the prefix regex is extremely unlikely but
            # we shouldn't try to modify the table if bad data is received
            raise ValueError('Invalid table data trying to be added to the Deal Registration database table.')
    except Exception as ex:
        # Simply pass exception along
        raise ex
    finally:
        # Ensure session is closed before exiting the function
        closeSession(session)

#endregion