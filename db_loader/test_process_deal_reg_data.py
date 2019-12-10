import pytest
from datetime import datetime
from collections import OrderedDict

import process_deal_reg_data
import deal_reg_row
from deal_reg_row import DealRegRow


#region test verifyPNFormat()
def test_verifyPNFormatPass():
    pn = 'SWPT001234'
    # Exception will be thrown if unexpected error occurrs
    process_deal_reg_data.verifyPNFormat(pn)


def test_verifyPNFormatFailAllNum():
    pn = '0123456'
    with pytest.raises(ValueError):
        process_deal_reg_data.verifyPNFormat(pn)


def test_verifyPNFormatFailNoNum():
    pn = 'SWPTABCDEF'
    with pytest.raises(ValueError):
        process_deal_reg_data.verifyPNFormat(pn)


def test_verifyPNFormatFailInvalidDataType():
    pn = 123456
    with pytest.raises(TypeError):
        process_deal_reg_data.verifyPNFormat(pn)
#endregion

#region test verifyDealRegGroup()
def test_verifyDealRegGroupPass():
    regGroup = 'Access Management'
    # Exception will be thrown if unexpected error occurrs
    process_deal_reg_data.verifyDealRegGroup(regGroup)


def test_verifyDealRegGroupValueFail():
    regGroup = ''
    with pytest.raises(ValueError):
        process_deal_reg_data.verifyDealRegGroup(regGroup)


def test_verifyDealRegGroupTypeFail():
    regGroup = 123456
    with pytest.raises(TypeError):
        process_deal_reg_data.verifyDealRegGroup(regGroup)
#endregion

#region test parseDate()
def test_parseDatePassFormat1():
    date = '10/12/2019'
    assert process_deal_reg_data.parseDate('Date', date) == datetime(2019, 10, 12)


def test_parseDatePassFormat2():
    date = '10/12/19'
    assert process_deal_reg_data.parseDate('Date', date) == datetime(2019, 10, 12)


def test_parseDatePassFormat3():
    date = '10/12/2019 12:30:00 AM'
    assert process_deal_reg_data.parseDate('Date', date) == datetime(2019, 10, 12, 0, 30, 0)


def test_parseDatePassFormat4():
    date = '10/12/19 12:30:00 AM'
    assert process_deal_reg_data.parseDate('Date', date) == datetime(2019, 10, 12, 0, 30, 00)


def test_parseDatePassFormat5():
    date = '2019-10-12-0.30.0.000000'
    assert process_deal_reg_data.parseDate('Date', date) == datetime(2019, 10, 12, 0, 30, 00)


def test_parseDateValueFail():
    date = 'This is a string Not a Date'
    with pytest.raises(ValueError):
        process_deal_reg_data.parseDate('Date', date)


def test_parseDateTypeFail():
    date = 101219
    with pytest.raises(TypeError):
        process_deal_reg_data.parseDate('Date', date)
#endregion

#region test parseActiveFlag()
def test_parseActiveFlagPassY():
    flag = 'y'
    assert process_deal_reg_data.parseActiveFlag(flag) == 'Y'


def test_parseActiveFlagPassN():
    flag = 'N'
    assert process_deal_reg_data.parseActiveFlag(flag) == 'N'


def test_parseActiveFlagValueFail():
    flag = 'A'
    with pytest.raises(ValueError):
        process_deal_reg_data.parseActiveFlag(flag)


def test_parseActiveFlagTypeFail():
    flag = 2
    with pytest.raises(TypeError):
        process_deal_reg_data.parseActiveFlag(flag)
#endregion

#region test verifyAndParseRow()
def test_verifyAndParseRowPass():
    inputRow = [('PART_NUM', 'SAPT000797'), ('DEAL_REG_GROUP', 'Service Action'),
                ('start_date', '10/9/18'), ('END_DATE', '12/31/99'),
                ('ACTIVE_FLAG', 'y'),
                ('ADD_DATE', '2018-12-27-21.30.21.000000'),
                ('MODIFIED_DATE', '2018-12-27-21.30.21.000000')]
    inputRow = OrderedDict(inputRow)

    result = {'PART_NUM': 'SAPT000797', 'DEAL_REG_GROUP': 'Service Action',
              'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
              'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21),
              'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)}

    assert process_deal_reg_data.verifyAndParseRow(inputRow) == result


def test_verifyAndParseRowTimeVerifyFail1():
    """Vallue Error exception should be thrown if the end date
    comes before the start date."""

    inputRow = [('PART_NUM', 'SAPT000797'), ('DEAL_REG_GROUP', 'Service Action'),
                ('start_date', '10/9/18'), ('END_DATE', '10/8/18'),
                ('ACTIVE_FLAG', 'y'),
                ('ADD_DATE', '2018-12-27-21.30.21.000000'),
                ('MODIFIED_DATE', '2018-12-27-21.30.21.000000')]
    inputRow = OrderedDict(inputRow)

    with pytest.raises(ValueError):
        process_deal_reg_data.verifyAndParseRow(inputRow)


def test_verifyAndParseRowTimeVerifyFail2():
    """Vallue Error exception should be thrown if the modified date
    comes before the add date."""

    inputRow = [('PART_NUM', 'SAPT000797'), ('DEAL_REG_GROUP', 'Service Action'),
                ('start_date', '10/9/18'), ('END_DATE', '12/31/99'),
                ('ACTIVE_FLAG', 'y'),
                ('ADD_DATE', '2018-12-27-21.30.21.000000'),
                ('MODIFIED_DATE', '2018-12-25-21.30.21.000000')]
    inputRow = OrderedDict(inputRow)

    with pytest.raises(ValueError):
        process_deal_reg_data.verifyAndParseRow(inputRow)
#endregion

#region test checkNewRowNeeded()
def test_checkNewRowNeededPass_useEndDate():
    """Verify that the function returns false because the old row
    has and end date that comes after the new row."""

    oldRow = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    newRow = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(2019, 10, 31, 0, 0),
                          'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2019, 10, 27, 21, 30, 21)})

    assert process_deal_reg_data.checkNewRowNeeded(oldRow, newRow) == False


def test_checkNewRowNeededPass_useAddDate():
    """Verify that the function returns true because both rows
    have the same end date but the new row has an added date that
    comes after the old row."""

    oldRow = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    newRow = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ADD_DATE': datetime(2019, 12, 5, 21, 30, 21), 'MODIFIED_DATE': datetime(2019, 12, 5, 21, 30, 21)})

    assert process_deal_reg_data.checkNewRowNeeded(oldRow, newRow) == True


def test_checkNewRowNeededPass_useModifiedDate():
    """Verify that the function returns false because both rows
    have the same end date, add date, and active flag (N/A) but
    the old row has a modified date that comes after the new row."""

    oldRow = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2019, 12, 5, 21, 30, 21)})

    newRow = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    assert process_deal_reg_data.checkNewRowNeeded(oldRow, newRow) == False


def test_checkNewRowNeededPass_useActiveFlag():
    """Verify that the function returns true because both rows
    have the same end date and add date but the new row has an
    active flag of Y while the old one has N."""

    oldRow = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ACTIVE_FLAG': 'N', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    newRow = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    assert process_deal_reg_data.checkNewRowNeeded(oldRow, newRow) == True


def test_checkNewRowNeededFail():
    """Verify and exception is thrown because both rows have all
    the same values except for the Deal Registration Group"""

    oldRow = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'IBM Brand',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    newRow = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    with pytest.raises(ValueError):
        process_deal_reg_data.checkNewRowNeeded(oldRow, newRow)
#endregion

#region test addNewRow()
def test_addNewRowPass_RowsSame():
    """Verify that the existing list of items isn't modified because
    the new duplicate row is exactly the same as the old."""

    row1 = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    row2 = DealRegRow({'PART_NUM': 'SAPT000797', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    row3 = {'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
            'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
            'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)}

    allRows = [row1, row2]

    process_deal_reg_data.addNewRow(row3, allRows)

    assert allRows == [row1, row2]

def test_addNewRowPass_RowsDiffKeep():
    """Verify that the existing list of items isn't modified because
    the duplicate row has an end date greater than that of the new row."""

    row1 = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    row2 = DealRegRow({'PART_NUM': 'SAPT000797', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    row3 = {'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
            'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(2019, 12, 9, 0, 0),
            'ACTIVE_FLAG': 'N', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2019, 12, 5, 21, 30, 21)}

    allRows = [row1, row2]

    process_deal_reg_data.addNewRow(row3, allRows)

    assert allRows == [row1, row2]

def test_addNewRowPass_RowsDiffReplace():
    """Verify that the old row is deleted from the list
    and the new row is added to the end because the duplicate
    row has an end date that comes before the new one."""

    row1 = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(2019, 12, 9, 0, 0),
                          'ACTIVE_FLAG': 'N', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    row2 = DealRegRow({'PART_NUM': 'SAPT000797', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    row3 = {'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
            'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
            'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)}

    allRows = [row1, row2]

    process_deal_reg_data.addNewRow(row3, allRows)

    assert row2.areEqual(allRows[0]) and DealRegRow(row3).areEqual(allRows[1])

def test_addNewRowPass_addNew():
    """Verify that the new row is added to the list
    because no duplicate rows were found."""

    row1 = DealRegRow({'PART_NUM': 'SAPT000796', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(2019, 12, 9, 0, 0),
                          'ACTIVE_FLAG': 'N', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    row2 = DealRegRow({'PART_NUM': 'SAPT000797', 'DEAL_REG_GROUP': 'Service Action',
                          'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
                          'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)})

    row3 = {'PART_NUM': 'SAPT000798', 'DEAL_REG_GROUP': 'Service Action',
            'START_DATE': datetime(2018, 10, 9, 0, 0), 'END_DATE': datetime(9999, 12, 31, 0, 0),
            'ACTIVE_FLAG': 'Y', 'ADD_DATE': datetime(2018, 12, 27, 21, 30, 21), 'MODIFIED_DATE': datetime(2018, 12, 27, 21, 30, 21)}

    allRows = [row1, row2]

    process_deal_reg_data.addNewRow(row3, allRows)

    assert allRows[0] == row1 and allRows[1] == row2 and DealRegRow(row3).areEqual(allRows[2])
#endregion