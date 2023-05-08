import io
import BotModuleUtils as utils
import ListFactory as b
import ListItemRemoved
import ListItemReplaced
import Settings as s
import TextWrap

from discord import File

import CardListItemRemoved
import XMLList


def listItems(messageList, message, fileByte):
    """Functions for manipulating the item list."""
    replyContent = "Input error for list. Type \"!bingo ?\" for a list of valid commands."
    replyFile = None
    command = messageList[2]

    match command:

        case "add":  # add an item to the list
            replyContent = addItem(message, messageList)
        case "remove":
            replyContent = remove(messageList)
        case "replace":
            replyContent = replace(message, messageList)
        case "view":
            replyContent = view()
        case "output":
            replyContent, replyFile = viewOutput()
        case "sort":
            replyContent = sort()
        case "addlist":  # add a list of items
            replyContent = replaceList(message, fileByte, replaceBool=False)
        case "replacelist":  # replace the list with a new list
            replyContent = replaceList(message, fileByte, replaceBool=True)
        case _:
            replyContent = "Input error for list. Type \"!bingo ?\" for a list of valid commands."

    return replyContent, replyFile


def addItem(message, messageList):
    if len(messageList) > 3:
        inputStr = message.content.lstrip("!bingo list add ")

        if not inputStr.startswith("\"") or not inputStr.endswith("\""):
            replyContent = "Could not resolve string to add. Format should be \"!bingo list add \"example text\"\"."

        else:
            inputStr = inputStr.lstrip("\"").rstrip("\"")
            itemExists = False

            for sel in b.bingoList:
                if inputStr == sel.rawText:
                    itemExists = True
                    replyContent = "Item is already in the list,", str(sel.index), ". Not added."
                    return replyContent

            if not itemExists:
                b.NewBingoItem(inputStr, 0)
                XMLList.writeList()

            replyContent = "Bingo list item \"" + inputStr + "\" added. There are now " + str(
                len(b.bingoList)) + " items in the bingo items list."

    else:
        # message thread
        replyContent = "Could not resolve string to add. Format should be \"!bingo list add \"example text\"\"."

    return replyContent


def remove(messageList):
    # removes the selected item in allBingoList
    # remove a list item, selected by index
    selIndex = int(messageList[3])
    selItem = utils.selBingItem(selIndex)

    if selItem is None:
        replyContent = "Index not found. Type \"!bingo list view\" to see the list with valid indices."
    else:

        bingoItemsChanged = [selIndex]
        replyContent = "Item " + str(selIndex) + ". \"" + selItem.rawText + "\" removed."

        # amend existing cards, for if they have the item on their list
        # if idempotency is on
        if s.idempotentCardRequest:
            userChangedString = ListItemRemoved.bingoItemRemoved(bingoItemsChanged)
            replyContent += ("\nUsers with changed bingocards: " + userChangedString + ".")
            # check that message length is not >2000 characters.

        # delete the entry from the list. Need the python index, not the humanised index.
        del b.bingoList[b.bingoList.index(selItem)]

        XMLList.writeList()

    return replyContent


def replace(message, messageList):
    # changes the raw text of the selected item in allBingoList
    selItem = None
    # try:
    selIndex = int(messageList[3])
    selItem = utils.selBingItem(selIndex)
    # print (selItem.rawText)
    if selItem is None:
        replyContent = "Index not found."
    else:
        # stripping the control from the message, to leave only what the new message is in. Inside ""s.
        newRawText = message.content.lstrip("!bingo list replace " + str(selIndex) + " \"").rstrip("\"")
        # cleaning based on various requirements.
        newRawText = utils.clean(newRawText)

        # Setting rawText and formattedText for the new string
        selItem.rawText = newRawText
        fontWordResized = TextWrap.longWord(text=selItem.rawText)
        selItem.formattedText, selItem.fontSize = TextWrap.text_box(selItem.rawText, font=fontWordResized)

        replyContent = "Text change for item " + str(selItem.index) + " to: " + str(selItem.rawText)

        if s.idempotentCardRequest:
            userChangedString = ListItemReplaced.ListItemReplacedFt(selIndex)
            replyContent += ("\nUsers with changed bingocards: " + userChangedString + ".")

        XMLList.writeList()

    return replyContent


def view():
    # prints a list of the allBingoList elements in the thread. Index + ". " + rawText
    replyContent = ""
    for el in b.bingoList:
        replyContent = replyContent + str(el.index) + ". " + el.rawText + "\n"

    return replyContent


def viewOutput():
    # prints a list of the allBingoList elements to a text file and attaches it. Index + ". " + rawText
    # content is one string, many lines, of allBingoList. In human-readable form.
    listContent = ""
    for el in b.bingoList:
        listContent = listContent + str(el.index) + ". " + el.rawText + "\n"
    # turn the variable content into a file to attach in message
    arrIO = io.StringIO(listContent)
    file = File(fp=arrIO, filename="OutputList.txt")
    replyContent = "Bingo list attached."
    return replyContent, file
    # await message.channel.send("Bingo list attached.",
    #                            file=File(fp=arrIO, filename="OutputList.txt"))


def replaceList(message, fileByte, replaceBool):
    if len(message.attachments) != 1:
        replyContent = "There must be exactly one attachment when using this command. " \
                       + str(len(message.attachments)) + " detected."
    else:

        # for updating existing cards, and message in thread.
        bingoItemsRemoved = []

        # turn bytes object into a (messy) string object
        fileReplacex = io.TextIOWrapper(fileByte, encoding='utf-8')

        # input is TextIOWrapper, output is a cleaned list

        # list of items on the replaceList
        fileReplaceList = cleanFile(fileReplacex)

        # These are counters for the message to user as to what has changed.
        sameCount = 0
        addCount = 0
        delCount = 0

        # for iterating across allBingoList, removing items without messing the iteration up.
        # allBingoList is then set to this afterwards.
        allBingoListIter = []
        if replaceBool:
            # Check if an allBingoList item exists in replace list and delete if not
            for sel in b.bingoList:

                itemExists = False

                for item in fileReplaceList:

                    if sel.rawText == item:
                        itemExists = True
                        allBingoListIter.append(sel)
                        break

                if not itemExists:
                    delCount += 1
                    bingoItemsRemoved.append(sel.index)

            # just the ones that made it through, because they're also on the replaceList.
            b.allBingoList = allBingoListIter

        # check if an item in the replaceList is in the allBingoList and add if not.
        for item in fileReplaceList:

            itemExists = False

            # Check if item exists in allBingoList
            for sel in b.bingoList:
                if item == sel.rawText:
                    itemExists = True
                    sameCount += 1
                    break

            # add it if it doesn't.
            if not itemExists:
                addCount += 1
                b.NewBingoItem(item, 0)

        if replaceBool:
            print("Replace list run; ", str(sameCount), "items were already in the list, ", str(addCount),
                  "items added, ", str(delCount), "items removed.")

            replyContent = "List replaced successfully. " + str(sameCount) + " items were already in the list, " + \
                           str(addCount) + " items attempted to add, " + str(delCount) + " items removed." + \
                           " There are now " + str(len(b.bingoList)) + " items in the bingo items list."
        if not replaceBool:
            print("Add list run; ", str(sameCount), "items were already in the list, ", str(addCount),
                  "items added.")
            replyContent = "File added successfully. " + str(sameCount) + " lines are the same, " + \
                           str(addCount) + " items attempted to add. There are now " + str(len(b.bingoList)) +\
                           " items in the bingo items list."

        # amend existing cards, for if they have the item on their list
        if s.idempotentCardRequest and replaceBool is True:
            userChangedString = ListItemRemoved.bingoItemRemoved(bingoItemsRemoved)
            replyContent += "\nUsers with changed bingo cards: " + userChangedString + "."

        # serialise
        XMLList.writeList()

    return replyContent


def sort():
    if s.idempotentCardRequest:
        replyContent = "This option is disabled with the option for consistent cards enabled." \
                       + "List will be sorted when the date or version is changed, when the " \
                         "cards database is reset."
    else:
        # Sort the allBingoList, reset the indexes. And write to XML.
        CardListItemRemoved.sortBingo()
        replyContent = "List sorted and reindexed."
        XMLList.writeList()

    return replyContent


def cleanFile(fileReplacex):
    """A util function, for cleaning *files* incoming. """
    fileReplaceClean = []

    for line in fileReplacex:

        # clean the line
        line = line.rstrip("\r\n")
        line = line.rstrip("\n")
        line = utils.clean(line)
        if line == "":
            continue
        fileReplaceClean.append(line)

    return fileReplaceClean
