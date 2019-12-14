import os
import sys


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
    transactionId = None  # important
    listingId = None  # important
    orderId = None  # important

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

    def addStatementLineItem(self, lineItem):
        if self.statementLineItems == None:
            self.statementLineItems = []

        self.statementLineItems.append(lineItem)
