import pytest
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

os.environ['DEAL_REG_DB_URL'] = 'postgresql://postgres@localhost:5432/TestDB'

import deal_reg_db
from deal_reg_row import DealRegRow

def test_updateDealRegTableWithRowsFail_NoRowsGiven():
    """Index Error should be thrown when empty data is passed in"""
    with pytest.raises(IndexError):
        deal_reg_db.updateDealRegTableWithRows([])


def test_updateDealRegTableWithRowsFail_InvalidRowData():
    """Value Error should be thrown if invalid part number is passed in"""

    newRow = DealRegRow({'PART_NUM': '000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ADD_DATE': datetime(2019, 12, 5, 21, 30, 21), 'MODIFIED_DATE': datetime(2019, 12, 5, 21, 30, 21)})

    with pytest.raises(ValueError):
        deal_reg_db.updateDealRegTableWithRows([newRow])


def test_updateDealRegTableWithRowsFail_InvalidDatabase():
    """Exception should be thrown if invalid connections is set in environment"""

    # Set up deal_reg_db file globals
    os.environ['DEAL_REG_DB_URL'] = 'postgresql://postgres@localhost:5000/TestDB'
    deal_reg_db.engine = create_engine(os.getenv('DEAL_REG_DB_URL'))
    deal_reg_db.Session = sessionmaker(bind=deal_reg_db.engine)

    newRow = DealRegRow({'PART_NUM': 'SWPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ADD_DATE': datetime(2019, 12, 5, 21, 30, 21), 'MODIFIED_DATE': datetime(2019, 12, 5, 21, 30, 21)})

    with pytest.raises(Exception):
        deal_reg_db.updateDealRegTableWithRows([newRow])


def test_updateDealRegTableWithRowsPass_EmptyTblRowAdd():
    """New Row Should be added to empty/missing table"""

    # Set up deal_reg_db file globals
    os.environ['DEAL_REG_DB_URL'] = 'postgresql://postgres@localhost:5432/TestDB'
    deal_reg_db.engine = create_engine(os.getenv('DEAL_REG_DB_URL'))
    deal_reg_db.Session = sessionmaker(bind=deal_reg_db.engine)

    # Create Local session info
    testEngine = create_engine(os.getenv('DEAL_REG_DB_URL'))
    testSession = sessionmaker(bind=testEngine)

    # Access DB and drop table if it exists
    if not database_exists(testEngine.url):
        create_database(testEngine.url)

    activeSession = testSession()

    # Drop table if there
    testEngine.execute('DROP TABLE IF EXISTS tbl_deal_reg;')

    activeSession.commit()
    activeSession.close()

    newRow = DealRegRow({'PART_NUM': 'SWPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ADD_DATE': datetime(2019, 12, 5, 21, 30, 21), 'MODIFIED_DATE': datetime(2019, 12, 5, 21, 30, 21)})

    # Add tble and row to database
    deal_reg_db.updateDealRegTableWithRows([newRow])

    # Verify new row exists
    activeSession = testSession()

    result = activeSession.query(deal_reg_db.DealRegTable) \
                            .filter(deal_reg_db.DealRegTable.part_num == 'SWPT000796').all()

    assert not result == []

    activeSession.commit()
    activeSession.close()


def test_updateDealRegTableWithRowsPass_ExistingTblRowAdd():
    """Existing rows with same part number prefix should be deleted
    and new row should be added to table"""

    # Set up deal_reg_db file globals
    os.environ['DEAL_REG_DB_URL'] = 'postgresql://postgres@localhost:5432/TestDB'
    deal_reg_db.engine = create_engine(os.getenv('DEAL_REG_DB_URL'))
    deal_reg_db.Session = sessionmaker(bind=deal_reg_db.engine)

    # Create Local session info
    testEngine = create_engine(os.getenv('DEAL_REG_DB_URL'))
    testSession = sessionmaker(bind=testEngine)

    # Access DB and drop table if it exists
    if not database_exists(testEngine.url):
        create_database(testEngine.url)

    # Drop table if there
    testEngine.execute('DROP TABLE IF EXISTS tbl_deal_reg;')

    # Add tbl back and start session
    deal_reg_db.Base.metadata.create_all(testEngine)

    activeSession = testSession()

    # Create existing row to be deleted by function
    initialRow = DealRegRow({'PART_NUM': 'SWPT000795', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ADD_DATE': datetime(2019, 12, 5, 21, 30, 21), 'MODIFIED_DATE': datetime(2019, 12, 5, 21, 30, 21)})

    activeSession.add(deal_reg_db.DealRegTable(initialRow))

    initialRowsFound = activeSession.query(deal_reg_db.DealRegTable) \
                               .filter(deal_reg_db.DealRegTable.part_num == 'SWPT000795') \
                               .all()

    if initialRowsFound == []:
        activeSession.commit()
        activeSession.close()
        raise Exception('Error: Setup failed. Inital row could not be added to table')

    activeSession.commit()
    activeSession.close()

    newRow = DealRegRow({'PART_NUM': 'SWPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ADD_DATE': datetime(2019, 12, 5, 21, 30, 21), 'MODIFIED_DATE': datetime(2019, 12, 5, 21, 30, 21)})

    # Add tble and row to database
    deal_reg_db.updateDealRegTableWithRows([newRow])

    # Verify new row exists
    activeSession = testSession()

    add_result = activeSession.query(deal_reg_db.DealRegTable) \
                            .filter(deal_reg_db.DealRegTable.part_num == 'SWPT000796') \
                            .all()

    delete_result = activeSession.query(deal_reg_db.DealRegTable) \
                                 .filter(deal_reg_db.DealRegTable.part_num == 'SWPT000795') \
                                 .all()
    assert not add_result == [] and delete_result == []

    activeSession.commit()
    activeSession.close()