import os
import sys
from functools import reduce
from models.Statement import Statement


class StatementCollection:
    statements = None

    def __init__(self, statements):
        self.statements = statements

    def getStatementByMonth(self, month=None):
        if(month == None):
            raise "You need to provide a month!"
        return [l for l in self.statements if l.month == month][0]

    def filterByType(self, filterType=None):
        itemsToReturn = []
        if(filterType == None):
            raise "You need to provide a statementItem type!"
        for statement in self.statements:
            for statementItem in statement.statementItems:
                if(statementItem.statementType == filterType):
                    itemsToReturn.append(statementItem)

        return Statement(itemsToReturn)

    # TODO - might be wrong, need to account for refunds
    def getAllRevenue(self):
        return reduce(lambda prev, statement: prev + statement.getAllRevenue(), self.statements, 0)

    def getAllFeesAndTaxes(self):
        return reduce(lambda prev, statement: prev + statement.getAllFeesAndTaxes(), self.statements, 0)

    def getShippingLabelBalance(self):
        return reduce(lambda prev, statement: prev + statement.getShippingLabelBalance(), self.statements, 0)

    def getSalesTaxCollected(self):
        return reduce(lambda prev, statement: prev + statement.getSalesTaxCollected(), self.statements, 0)

    def getRevenueFromSales(self):
        return reduce(lambda prev, statement: prev + statement.getRevenueFromSales(), self.statements, 0)

    def getFeesAndTaxesFromSales(self):
        return reduce(lambda prev, statement: prev + statement.getFeesAndTaxesFromSales(), self.statements, 0)

    def getNetFromSales(self):
        return reduce(lambda prev, statement: prev + statement.getNetFromSales(), self.statements, 0)

    def getNetFromSalesLessTotalFees(self):
        return self.getNetFromSales() + self.getAllFeesAndTaxes()