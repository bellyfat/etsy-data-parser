import os
import sys


class StatementItem:
    def __init__(self, date, statementType, title, info, currency, amount, feesAndTaxes, net):
        self.date = date
        self.statementType = statementType
        self.title = title
        self.info = info
        self.currency = currency
        self.amount = amount
        self.feesAndTaxes = feesAndTaxes
        self.net = net
