import os
import sys
from enum import Enum


class STATEMENT_ITEM_TYPES(Enum):
    SALE = "Sale"
    PAYMENT = "Payment"
    DEPOSIT = "Deposit"
    TRANSACTION = "Transaction"
    LISTING = "Listing"
    MARKETING = "Marketing"
    SHIPPING_LABEL = "Shipping Label"
    REFUND = "Refund"
