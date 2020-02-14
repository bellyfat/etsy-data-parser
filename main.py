#!/usr/bin/env python

import os
import sys
from functools import reduce
from parsers.StatementParser import StatementParser
from parsers.OrderItemsParser import OrderItemsParser
from models.Statement import Statement
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


def parseOrderItems(statementCollection=None, disableWarnings=False):
    filename = ETSY_DATA_FOLDER_ROOT + "/EtsySoldOrderItems2019.csv"

    orderItemsParser = OrderItemsParser()
    orderItemCollection = orderItemsParser.parseOrderItems(
        filename, statementCollection, disableWarnings=disableWarnings)

    return orderItemCollection


def main():
    statementCollection = parseAllStatements()
    orderItemCollection = parseOrderItems(
        statementCollection, disableWarnings=True)

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

    # NOTE - Start figuring out basket difference

    orderItemCollectionLessBaskets = orderItemCollection.filterOutLineItemsByName(
        itemNameContains="cotton rope")

    # Create a dummy statement to house our numbers less baskets
    dummyStatementLessBaskets = Statement(orderItemCollectionLessBaskets)

    print("\n---------------------------------------------------------------")
    print("\tNON BASKET NUMBERS\t")
    print("---------------------------------------------------------------\n")

    print(dummyStatementLessBaskets)

    print("TOTAL ETSY REVENUE:", dummyStatementLessBaskets.getAllRevenue())
    print("SALES REVENUE:", dummyStatementLessBaskets.getRevenueFromSales())
    print()
    print("SALES FEES:", dummyStatementLessBaskets.getFeesAndTaxesFromSales())
    print("SALES TAX COLLECTED:", dummyStatementLessBaskets.getSalesTaxCollected())
    print("SALES REVENUE LESS SALES FEES:",
          dummyStatementLessBaskets.getNetFromSales())
    print()
    print("ALL OTHER FEES:", dummyStatementLessBaskets.getAllFeesAndTaxes())
    print("\tSHIPPING LABEL BALANCE:",
          dummyStatementLessBaskets.getShippingLabelBalance())

    pass


if __name__ == "__main__":
    main()
