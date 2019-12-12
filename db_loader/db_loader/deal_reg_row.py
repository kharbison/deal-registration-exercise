class DealRegRow:

    def __init__(self, verifiedRow):
        self.partNum = verifiedRow['PART_NUM']
        self.dealRegGroup = verifiedRow['DEAL_REG_GROUP']
        self.startDate = verifiedRow['START_DATE']
        self.endDate = verifiedRow['END_DATE']
        self.addDate = verifiedRow['ADD_DATE']
        self.modDate = verifiedRow['MODIFIED_DATE']
        self.activeFlag = 'N/A'
        self.partType = 'Unknown'

        if 'ACTIVE_FLAG' in verifiedRow:
            self.activeFlag = verifiedRow['ACTIVE_FLAG']

        if 'SWPT' in self.partNum.upper():
            self.partType = 'SW'
        elif 'SAPT' in self.partNum.upper():
            self.partType = 'SaaS'

    def areEqual(self, rowToCompare):
        return (self.partNum == rowToCompare.partNum and
                self.dealRegGroup == rowToCompare.dealRegGroup and
                self.startDate == rowToCompare.startDate and
                self.endDate == rowToCompare.endDate and
                self.addDate == rowToCompare.addDate and
                self.modDate == rowToCompare.modDate and
                self.activeFlag == rowToCompare.activeFlag)
