from CardListFactory import bingoCardList
import ListFactory as b
import XMLCardList

import random


def bingoItemRemoved(bingoItemsRemoved):
    """Code to run to amend cards if a bingo item is removed with the list remove or list replace command.
    bingoItemsRemoved is a list of indexes."""
    usersChangedList = []

    # make a copy of the list to select the replacement bingo item from, which excludes the items already selected
    # for the card
    tempABListCtrl = b.bingoList[:]

    # removing the killed items from the pool of potential replacement items
    for ab in b.bingoList:
        for bi in bingoItemsRemoved:
            if bi == ab.index:
                try:
                    tempABListCtrl.remove(ab)
                except:
                    print("Could not remove item bi." + str(bi) + " " + str(ab.index))

    # remove the items already on a card from the pool for that card, so there aren't duplicates
    for card in bingoCardList:

        itemsToChangeList = []
        tempABList = tempABListCtrl[:]

        for selItem in card.bingoItemList:

            for itemRemoved in bingoItemsRemoved:  # find all changed items on this card
                if itemRemoved == selItem.index:
                    itemsToChangeList.append(itemRemoved)

        if len(itemsToChangeList) != 0:  # if there are changed items on the card
            usersChangedList.append(card.userName)
            card.cardChanged = True

            for cardItem in card.bingoItemList:
                for ab in b.bingoList:  # removing the items on the card from the pool of new items
                    if ab.index == cardItem.index:
                        try:
                            tempABList.remove(ab)
                        except:
                            pass
                        continue

            replaceList = random.sample(tempABList, len(itemsToChangeList))  # select the replacement bingoItems

            n = 0
            for itemToChange in itemsToChangeList:  # apply changes to card

                for cardItem in card.bingoItemList:
                    if itemToChange == cardItem.index:
                        replaceIndex = card.bingoItemList.index(cardItem)
                        card.bingoItemList.remove(cardItem)
                        card.bingoItemList.insert(replaceIndex, replaceList[n])
                        n += 1
                        break

    if len(usersChangedList) == 0:
        usersChangedList.append("None")
    else:
        XMLCardList.writeList()

    usersChangedString = ", ".join(usersChangedList)

    return usersChangedString
