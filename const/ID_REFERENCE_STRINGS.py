import os
import sys
from enum import Enum


class ID_REFERENCE_STRINGS(Enum):
    TRANSACTION = 'transaction:'
    TRANSACTION_SHIPPING = 'order:'
    SALE = 'Payment for Order'
    LISTING = 'listing:'
