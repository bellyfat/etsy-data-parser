#!/usr/bin/env python

import os
import sys
from parsers.StatementParser import StatementParser


def main():
    etsyDataRoot = 'etsy-data'
    fileNames = filter(lambda filename: 'lock' not in filename,
                       os.listdir('./etsy-data/statements'))
    fileNamesWithPath = list(map(
        lambda filename: etsyDataRoot + "/statements/" + filename, fileNames))

    statementParser = StatementParser()
    allStatements = statementParser.parseStatements(fileNamesWithPath)

    return allStatements


if __name__ == "__main__":
    main()
