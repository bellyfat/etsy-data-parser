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

        # PROBLEM - Etsy is not giving us the correct tax calculation within the "Taxes & Fees" section
        # To solve this, calculate: taxCollected = (revenueAmount - fee&tax) - net
        self.collectedSalesTax = (amount + feesAndTaxes) - net
        self.net = net

    def _printerFormat(self, variable):
        return ("     {}                       ".format(str(variable)[:20]))[:20]

    def __str__(self):
        return "{}{}{}{}{}{}{}{}{}".format(self._printerFormat(self.date), self._printerFormat(self.statementType), self._printerFormat(self.title), self._printerFormat(self.info), self._printerFormat(self.currency), self._printerFormat(self.amount), self._printerFormat(self.feesAndTaxes), self._printerFormat(self.collectedSalesTax), self._printerFormat(self.net))
