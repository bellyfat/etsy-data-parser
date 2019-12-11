import os
import sys
import csv
from models.Statement import Statement
from models.StatementItem import StatementItem


class StatementParser:

    def parseStatements(self, filePathList):
        statements = []
        for filePath in filePathList:
            statementItems = self._parseStatement(filePath)
            statement = Statement(statementItems)
            statements.append(statement)
        return statements

    def _parseStatement(self, filePath):
        statementItems = []
        with open(filePath) as csvFile:
            csvReader = csv.reader(csvFile)
            next(csvReader)  # skip the first line of headers
            for row in csvReader:
                statementItems.append(StatementItem(
                    date=row[0], statementType=row[1], title=row[2], info=row[3], currency=row[4], amount=row[5], feesAndTaxes=row[6], net=row[7]))
        return statementItems
