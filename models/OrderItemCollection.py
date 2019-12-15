import os
import sys

"""
    NOTE: Needed to create some hash tables so we can reference orderItems by their 
    order, listing, and transaction IDs.
"""


class OrderItemCollection():
    orderItems = []

    """ Datastructs to map unique IDs to specific orders """

    orderIdToOrderDict = {}

    # EDGE CASE - one listing can have many orderItems - store a LIST of orderItems
    listingIdToOrderDict = {}

    transactionIdToOrderDict = {}

    def __init__(self, orderItems, allStatementLineItems=None):
        if(allStatementLineItems == None):
            raise "You must provide all line items for all statements, so orderItems can be linked to corresponding lineItems"
        self.orderItems = orderItems
        self._initHashtables()
        self._linkLineItemsToOrderItems(allStatementLineItems)

    def _initHashtables(self):
        self._initOrderIdHashTable()
        self._initListingIdHashTable()
        self._initTransactionIdHashTable()

    def _initOrderIdHashTable(self):
        for item in self.orderItems:
            self.orderIdToOrderDict[item.orderId] = item

    def _initListingIdHashTable(self):
        for item in self.orderItems:
            if(item.listingId not in self.listingIdToOrderDict):
                self.listingIdToOrderDict[item.listingId] = []
            self.listingIdToOrderDict[item.listingId].append(item)

    def _initTransactionIdHashTable(self):
        for item in self.orderItems:
            self.transactionIdToOrderDict[item.transactionId] = item

    def _linkLineItemsToOrderItems(self, statementLineItems):

        # Stores the Listing Items we could not link to an Order (These were most likely listing fees that got paid early on, but EVENTUALLY sold an order later)
        unlinkedListingItems = []

        for statementItem in statementLineItems:

            # Link by TransactionId
            if(statementItem.transactionId != None):
                if(statementItem.transactionId not in self.transactionIdToOrderDict):
                    print("WARNING: Couldn't find an orderItem which links to statementLineItem having transactionId: {}".format(
                        statementItem.transactionId))
                    print(statementItem)
                    print()
                    continue
                foundOrderObject = self.transactionIdToOrderDict[statementItem.transactionId]
                foundOrderObject.addStatementLineItem(statementItem)

            # Link by ListingId
            if(statementItem.listingId != None):
                if(statementItem.listingId not in self.listingIdToOrderDict):
                    # EDGE CASE - There are instances when products have been listed WITHOUT ever being purchased.
                    # In this case, there is NO order to link it to (because no one ever ordered this item, but listing charge still occurred).
                    # Simply skip over these statementItems
                    continue

                foundOrderObjects = self.listingIdToOrderDict[statementItem.listingId]

                # EDGE CASE - It is possible for the same product to be ordered again on the same day.
                # We don't want EVERY listing fee tied to order A, and nothing on order B for the same day.
                #
                # Solution: Each order object is allowed up to ONE regular listing fee and ONE multi-quantity listing fee.
                # If a listing fee slot is taken up for an order that day, push the fee to the NEXT order than day.

                didLinkListingFee = False

                for orderObj in foundOrderObjects:

                    # If the statementItem has a transactionID, that means this was a multi-quantity listing charge. Add that as well to the item
                    if orderObj.saleDate == statementItem.date:

                        """ conditions where a second listing fee can be added to a single orderItem """

                        # If the orderObj doesn't have any listing fee, we can add it
                        orderHasNoListingFee = not orderObj.hasListingFeeLineItem()

                        # OR, if the orderObj ONLY has multi-quantity listing fees, we can add a non-multi-quantity listing fee
                        canAddAsRegularListingFee = not statementItem.isMultiQuantityListingFee(
                        ) and orderObj.hasOnlyMultiQuantityListFee()

                        # OR, if the orderObj has NO multi-quantity listing fees, we can add a multi-quantity listing fee
                        canAddAsMultiQuantityListingFee = statementItem.isMultiQuantityListingFee(
                        ) and not orderObj.hasMultiQuantityListingFeeLineItem()

                        if orderHasNoListingFee or canAddAsRegularListingFee or canAddAsMultiQuantityListingFee:
                            orderObj.addStatementLineItem(statementItem)
                            didLinkListingFee = True
                            break

                if not didLinkListingFee:
                    # Try to resolve link errors later
                    unlinkedListingItems.append(statementItem)

            # Link by OrderId
            if(statementItem.orderId != None):
                if(statementItem.orderId not in self.orderIdToOrderDict):
                    print("WARNING: Couldn't find an orderItem which links to statementLineItem having orderId: {}".format(
                        statementItem.orderId))
                    print(statementItem)
                    print()
                    continue
                foundOrderObject = self.orderIdToOrderDict[statementItem.orderId]
                foundOrderObject.addStatementLineItem(statementItem)

        self._tryResolveListingItemLinkErrors(unlinkedListingItems)

    # Try to resolve Listing Item linking errors. If we cannot resolve, warn the user
    def _tryResolveListingItemLinkErrors(self, unlinkedListingItems):

        if(unlinkedListingItems == None or len(unlinkedListingItems) == 0):
            return

        for listingItem in unlinkedListingItems:
            # TODO - Add logic to supress errors. For now, just show errors.
            print(
                " WARNING: Unable to link a listingFeeLineItem to an orderItem. This can likely be ignored for Listing Fees of -0.2")
            print(listingItem)
            print()
