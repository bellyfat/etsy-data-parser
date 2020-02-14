import os
import sys
import csv
from datetime import datetime
from const.ORDER_ITEM_COLUMN_MAPPING import ORDER_ITEM_COLUMN_MAPPING
from models.OrderItemCollection import OrderItemCollection
from models.OrderItem import OrderItem


class OrderItemsParser():

    def parseOrderItems(self, filePath, statementCollection=None, disableWarnings=False):
        if(statementCollection == None):
            raise "You must provide a statementCollection before you can parse orderItems (needed for linking orderItems)"

        orderItems = []

        with open(filePath) as csvFile:
            csvReader = csv.reader(csvFile)

            next(csvReader)  # skip first row of headers

            for row in csvReader:
                saleDate = datetime.strptime(
                    row[ORDER_ITEM_COLUMN_MAPPING.SALE_DATE.value], "%m/%d/%y").date()
                itemName = row[ORDER_ITEM_COLUMN_MAPPING.ITEM_NAME.value]
                quantity = int(row[ORDER_ITEM_COLUMN_MAPPING.QUANTITY.value])
                price = float(row[ORDER_ITEM_COLUMN_MAPPING.PRICE.value])
                couponCode = row[ORDER_ITEM_COLUMN_MAPPING.COUPON_CODE.value]
                couponDetails = row[ORDER_ITEM_COLUMN_MAPPING.COUPON_DETAILS.value]
                discountAmount = float(
                    row[ORDER_ITEM_COLUMN_MAPPING.DISCOUNT_AMOUNT.value])
                shippingDiscount = float(
                    row[ORDER_ITEM_COLUMN_MAPPING.SHIPPING_DISCOUNT.value])
                orderShipping = float(
                    row[ORDER_ITEM_COLUMN_MAPPING.ORDER_SHIPPING.value])
                orderSalesTax = float(
                    row[ORDER_ITEM_COLUMN_MAPPING.ORDER_SALES_TAX.value])
                itemTotal = float(
                    row[ORDER_ITEM_COLUMN_MAPPING.ITEM_TOTAL.value])
                transactionId = row[ORDER_ITEM_COLUMN_MAPPING.TRANSACTION_ID.value]
                listingId = row[ORDER_ITEM_COLUMN_MAPPING.LISTING_ID.value]
                orderId = row[ORDER_ITEM_COLUMN_MAPPING.ORDER_ID.value]

                orderItems.append(OrderItem(
                    saleDate=saleDate,
                    itemName=itemName,
                    quantity=quantity,
                    price=price,
                    couponCode=couponCode,
                    couponDetails=couponDetails,
                    discountAmount=discountAmount,
                    shippingDiscount=shippingDiscount,
                    orderShipping=orderShipping,
                    orderSalesTax=orderSalesTax,
                    itemTotal=itemTotal,
                    transactionId=transactionId,
                    listingId=listingId,
                    orderId=orderId
                ))

        return OrderItemCollection(orderItems, statementCollection.getAllLineItems(), disableWarnings=disableWarnings)
