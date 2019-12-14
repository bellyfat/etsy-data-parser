import os
import sys
from functools import reduce
from models.StatementItem import StatementItem
from const.STATEMENT_ITEM_TYPES import STATEMENT_ITEM_TYPES


class Statement:
    statementItems = []
    month = None
    year = None

    def __init__(self, statementItems, month=None, year=None):
        self.statementItems = sorted(statementItems, key=lambda i: i.date)
        self.month = month
        self.year = year

    def filteredStatementByType(self, filterType=None):
        if(filterType == None):
            return self
        filteredItems = list(
            filter(lambda x: x.statementType == filterType, self.statementItems))
        return Statement(filteredItems)

    # TODO - might be wrong, need to account for refunds
    def getAllRevenue(self):
        return reduce(lambda prev, statementItem: statementItem.amount + prev, self.statementItems, 0)

    def getAllFeesAndTaxes(self):
        return reduce(lambda prev, statementItem: prev + statementItem.feesAndTaxes, self.statementItems, 0)

    def getShippingLabelBalance(self):
        filteredStatement = self.filteredStatementByType(
            filterType=STATEMENT_ITEM_TYPES.SHIPPING_LABEL.value)
        return reduce(lambda prev, item: item.feesAndTaxes + prev, filteredStatement.statementItems, 0)

    def getRevenueFromSales(self):
        filteredStatement = self.filteredStatementByType(
            filterType=STATEMENT_ITEM_TYPES.SALE.value)
        return reduce(lambda prev, saleItem: saleItem.amount + prev, filteredStatement.statementItems, 0)

    def getFeesAndTaxesFromSales(self):
        filteredStatement = self.filteredStatementByType(
            filterType=STATEMENT_ITEM_TYPES.SALE.value)
        return reduce(lambda prev, feeItem: feeItem.feesAndTaxes + prev, filteredStatement.statementItems, 0)

    def getSalesTaxCollected(self):
        filteredStatement = self.filteredStatementByType(
            filterType=STATEMENT_ITEM_TYPES.SALE.value)
        return reduce(lambda prev, item: item.collectedSalesTax + prev, filteredStatement.statementItems, 0)

    def getNetFromSales(self):
        filteredStatement = self.filteredStatementByType(
            filterType=STATEMENT_ITEM_TYPES.SALE.value)
        return reduce(lambda prev, netItem: netItem.net + prev, filteredStatement.statementItems, 0)

    def calculateMarketingCosts(self):
        items = list(filter(lambda item: (item.statementType ==
                                          STATEMENT_ITEM_TYPES.MARKETING.value), self.statementItems))
        return reduce(lambda prev, item: prev + item.feesAndTaxes, items, 0)

    def getRowCount(self):
        return len(self.statementItems)

    # TODO - also print month, year, + all headers
    def __str__(self):
        toReturn = ""
        for statementItem in self.statementItems:
            toReturn += str(statementItem) + "\n"
        return toReturn
