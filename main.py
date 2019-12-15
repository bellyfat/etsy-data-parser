#!/usr/bin/env python

import os
import sys
from functools import reduce
from parsers.StatementParser import StatementParser
from parsers.OrderItemsParser import OrderItemsParser
from models.StatementCollection import StatementCollection
from const.STATEMENT_ITEM_TYPES import STATEMENT_ITEM_TYPES
from const.MONTHS import MONTHS

ETSY_DATA_FOLDER_ROOT = 'etsy-data'


def parseAllStatements():
    fileNames = filter(lambda filename: 'lock' not in filename,
                       os.listdir('./etsy-data/statements'))
    fileNamesWithPath = list(map(
        lambda filename: ETSY_DATA_FOLDER_ROOT + "/statements/" + filename, fileNames))

    statementParser = StatementParser()
    statementCollection = statementParser.parseStatements(fileNamesWithPath)

    return statementCollection


def parseOrderItems(statementCollection=None):
    filename = ETSY_DATA_FOLDER_ROOT + "/EtsySoldOrderItems2019.csv"

    orderItemsParser = OrderItemsParser()
    orderItemCollection = orderItemsParser.parseOrderItems(
        filename, statementCollection)

    return orderItemCollection


def main():
    statementCollection = parseAllStatements()
    orderItemCollection = parseOrderItems(statementCollection)

    print(statementCollection)

    totalEtsyRevenue = statementCollection.getAllRevenue()
    etsySalesRevenue = statementCollection.getRevenueFromSales()

    etsySalesFees = statementCollection.getFeesAndTaxesFromSales()
    etsySalesTaxCollected = statementCollection.getSalesTaxCollected()
    revenueLessSalesFees = statementCollection.getNetFromSales()
    totalFees = statementCollection.getAllFeesAndTaxes()

    shippingLabelBalance = statementCollection.getShippingLabelBalance()

    print("TOTAL ETSY REVENUE:", totalEtsyRevenue)
    print("SALES REVENUE:", etsySalesRevenue)
    print()
    print("SALES FEES:", etsySalesFees)
    print("SALES TAX COLLECTED:", etsySalesTaxCollected)
    print("SALES REVENUE LESS SALES FEES:", revenueLessSalesFees)
    print()
    print("ALL OTHER FEES:", totalFees)
    print("\tSHIPPING LABEL BALANCE:", shippingLabelBalance)

    # Start temporary basket calculations
    # print("--------------------\nJUST BASKET NUMBERS\n--------------------")
    # print(statementCollection.getUniqueSalesItems())


if __name__ == "__main__":
    main()
