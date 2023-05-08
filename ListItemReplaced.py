from CardListFactory import bingoCardList
import XMLCardList


def ListItemReplacedFt(listItemReplaced):
    """Code to run to amend cards if a bingo item is removed with the list remove or list replace command.
    bingoItemsRemoved is a list of indexes."""
    usersChangedList = []

    for card in bingoCardList:

        for selItem in card.bingoItemList:
            # print("listItemReplaced: ", str(listItemReplaced), "selItem: ",selItem)
            if int(listItemReplaced) == int(selItem.index):
                usersChangedList.append(card.userName)
                card.cardChanged = True

    if len(usersChangedList) == 0:
        usersChangedList.append("None")
    else:
        XMLCardList.writeList()

    usersChangedString = ", ".join(usersChangedList)

    return usersChangedString
