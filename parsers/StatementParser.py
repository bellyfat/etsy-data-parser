import os
import sys
import csv
from datetime import datetime
from models.Statement import Statement
from models.StatementItem import StatementItem
from models.StatementCollection import StatementCollection


class StatementParser:

    def parseStatements(self, filePathList):
        statements = []
        for filePath in filePathList:
            month = self._extractMonth(filePath)
            year = self._extractYear(filePath)
            statementItems = self._parseStatement(filePath)
            statement = Statement(statementItems, month, year)
            statements.append(statement)
        return StatementCollection(statements)

    def _extractMonth(self, filePath):
        pathItems = filePath.split('/')
        filename = pathItems[len(pathItems)-1]
        filenameSplit = filename.split('.')[0].split('_')
        month = filenameSplit[len(filenameSplit) - 1]
        return int(month)

    def _extractYear(self, filePath):
        pathItems = filePath.split('/')
        filename = pathItems[len(pathItems)-1]
        filenameSplit = filename.split('.')[0].split('_')
        year = filenameSplit[len(filenameSplit) - 2]
        return int(year)

    def _parseStatement(self, filePath):
        statementItems = []
        with open(filePath) as csvFile:
            csvReader = csv.reader(csvFile)
            next(csvReader)  # skip the first line of headers
            for row in csvReader:

                recordDate = datetime.strptime(
                    row[0], "%B %d, %Y").date()

                statementItems.append(StatementItem(
                    date=recordDate,
                    statementType=row[1],
                    title=row[2],
                    info=row[3],
                    currency=row[4],
                    amount=float(row[5].replace('$', '')
                                 ) if row[5] != "--" else 0,
                    feesAndTaxes=float(row[6].replace(
                        '$', '')) if row[6] != "--" else 0,
                    net=float(row[7].replace('$', '')) if row[5] != "--" else 0))
        return statementItems
