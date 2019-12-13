#!/usr/bin/env python

import os
import sys
from functools import reduce
from parsers.StatementParser import StatementParser
from models.StatementCollection import StatementCollection
from const.STATEMENT_ITEM_TYPES import STATEMENT_ITEM_TYPES
from const.MONTHS import MONTHS


def parseAllStatements():
    etsyDataRoot = 'etsy-data'
    fileNames = filter(lambda filename: 'lock' not in filename,
                       os.listdir('./etsy-data/statements'))
    fileNamesWithPath = list(map(
        lambda filename: etsyDataRoot + "/statements/" + filename, fileNames))

    statementParser = StatementParser()
    statementCollection = statementParser.parseStatements(fileNamesWithPath)

    return statementCollection


def main():
    statementCollection = parseAllStatements()

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


if __name__ == "__main__":
    main()
