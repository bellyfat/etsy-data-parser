import os
import sys
from functools import reduce
from models.Statement import Statement
from const.STATEMENT_ITEM_TYPES import STATEMENT_ITEM_TYPES


class StatementCollection:
    statements = None

    # TODO - Also sort by year
    def __init__(self, statements):
        self.statements = sorted(statements, key=lambda s: s.month)

    def getStatementByMonth(self, month=None):
        if(month == None):
            raise "You need to provide a month!"
        return [l for l in self.statements if l.month == month][0]

    def getAllLineItems(self):
        itemsToReturn = []
        for statement in self.statements:
            for statementItem in statement.statementItems:
                itemsToReturn.append(statementItem)
        return itemsToReturn

    # NOTE - parameter taks a list of line items. Method returns all stored lineItems in this object less the lineItems passed.
    def getLineItemsDifference(self, lineItemsToRemove=[]):
        # First, create a hashset of the passed lineItems for quick lookup
        lineItemDifference = []
        lineItemsToRemoveSet = set(lineItemsToRemove)

        for internalLineItem in self.getAllLineItems():
            if not internalLineItem in lineItemsToRemoveSet:
                lineItemDifference.append(internalLineItem)

        return lineItemDifference

    def filterByType(self, filterType=None):
        itemsToReturn = []
        if(filterType == None):
            raise "You need to provide a statementItem type!"
        for statement in self.statements:
            for statementItem in statement.statementItems:
                if(statementItem.statementType == filterType):
                    itemsToReturn.append(statementItem)

        return Statement(itemsToReturn)

    # Simply returns a string list of all unique sales items
    def getUniqueSalesItems(self):
        salesOnlyTransactions = self.filterByType(
            filterType=STATEMENT_ITEM_TYPES.SALE.value).statementItems

        titlesOnly = list(map(lambda tx: tx.title, salesOnlyTransactions))
        return titlesOnly

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

    def __str__(self):
        toReturn = ""
        for x in self.statements:
            toReturn += str(x)
        return toReturn
