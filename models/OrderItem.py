import os
import sys
from const.STATEMENT_ITEM_TYPES import STATEMENT_ITEM_TYPES


class OrderItem():
    saleDate = None
    itemName = None
    quantity = None
    price = None
    couponCode = None
    couponDetails = None
    discountAmount = None
    shippingDiscount = None
    orderShipping = None
    orderSalesTax = None
    itemTotal = None

    # Important Fields
    transactionId = None
    listingId = None
    orderId = None

    # NOTE - OrderItems should have direct links to their unique lineItems
    statementLineItems = None

    def __init__(
            self,
            saleDate=None,
            itemName=None,
            quantity=None,
            price=None,
            couponCode=None,
            couponDetails=None,
            discountAmount=None,
            shippingDiscount=None,
            orderShipping=None,
            orderSalesTax=None,
            itemTotal=None,
            transactionId=None,
            listingId=None,
            orderId=None):
        self.saleDate = saleDate
        self.itemName = itemName
        self.quantity = quantity
        self.price = price
        self.couponCode = couponCode
        self.couponDetails = couponDetails
        self.discountAmount = discountAmount
        self.shippingDiscount = shippingDiscount
        self.orderShipping = orderShipping
        self.orderSalesTax = orderSalesTax
        self.itemTotal = itemTotal
        self.transactionId = transactionId
        self.listingId = listingId
        self.orderId = orderId

    def hasListingFeeLineItem(self):
        if(self.statementLineItems is None or len(self.statementLineItems) == 0):
            return False

        for lineItem in self.statementLineItems:
            if lineItem.statementType == STATEMENT_ITEM_TYPES.LISTING.value:
                return True

        return False

    def hasMultiQuantityListingFeeLineItem(self):
        if(self.statementLineItems is None or len(self.statementLineItems) == 0):
            return False

        for lineItem in self.statementLineItems:
            # LISTING item types WITH transactionId are multi-quantity Listing Fees
            if lineItem.statementType == STATEMENT_ITEM_TYPES.LISTING.value and lineItem.transactionId != None:
                return True

        return False

    def hasOnlyMultiQuantityListFee(self):
        if(self.statementLineItems is None or len(self.statementLineItems) == 0):
            return False

        for lineItem in self.statementLineItems:
            # LISTING item types WITHOUT transactionId are NOT multi-quantity Listing Fees
            if lineItem.statementType == STATEMENT_ITEM_TYPES.LISTING.value and lineItem.transactionId == None:
                return False

        return True

    def addStatementLineItem(self, lineItem):
        if self.statementLineItems == None:
            self.statementLineItems = []

        self.statementLineItems.append(lineItem)
