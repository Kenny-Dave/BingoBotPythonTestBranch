import XMLSettings
import copy
from datetime import datetime
import os

import CardListItemRemoved
import Settings as s
import ListFactory as b
import CardListFactory as c


def toggleActive(cardsActive):

    if cardsActive:
        cardsActive = False
        replyContent = "Card issue is now inactive. Users will not be able to request a card."
        XMLSettings.WriteCardsActive(cardsActive)

    else:
        cardsActive = True
        replyContent = "Card issue is now active. Users will be able to request a card."
        XMLSettings.WriteCardsActive(cardsActive)

    return replyContent, cardsActive


def date(bingoDate, v, message, messageList):

    bingoDateStr = bingoDate.strftime("%d %b %y")

    if len(messageList) == 2:
        replyContent = "Currently set date is: " + bingoDateStr + ", Version is v" + \
                       str(v) + "."
    else:
        # stripping the control from the message, to leave only new date.

        try:
            bingoDateStrOld = copy.copy(bingoDateStr)
            vOld = copy.copy(v)

            # done like this, so we don't assign junk to bingoDateStr, and it errors before reassigning
            # variables if it's junk.
            bingoDateStrTry = message.content.lstrip("!bingo date \"").rstrip("\"")
            try:
                bingoDate = datetime.strptime(bingoDateStrTry, "%d %b %y")
            except:
                bingoDate = datetime.strptime(bingoDateStrTry, "%d/%m/%y")
            bingoDateStr = bingoDate.strftime("%d %b %y")
            v = 1

            CardListItemRemoved.clearCardDB(bingoDateStrOld, vOld, bingoDateStr, v)

            replyContent = "bingoDate changed to " + bingoDateStr + \
                           ". Version reset to 1. Bingo List sorted and reindexed."

        except:
            replyContent = "Could not read new date correctly. Please ensure it is in the format dd mmm " \
                           "yy, e.g. \"25 Apr 23\"."
    return replyContent, bingoDate, v


def helpText(messageList):
    if len(messageList) == 2:
        helpfile = os.path.join(s.parentPathStr, "obj", "HelpStrings", "HelpText.txt")

    # flexible addition for end owner. Will print any file in the folder if the input matches the file name.
    # add text to help file if this is done.
    else:
        # helpfile = s.parentPathStr + "/obj/HelpStrings/" + messageList[2] + ".txt"
        helpfile = os.path.join(s.parentPathStr, "obj", "HelpStrings", messageList[2] + ".txt")

    with open(helpfile, "r") as f:
        replyContent = "".join(f.readlines())
        # await message.channel.send(replyContent)

    return replyContent


def status(bingoDate, v, cardsActive):
    replyContent = "Bingo card status:\n" + \
                   "Currently set date is: " + bingoDate.strftime("%d %b %y") + ", Version is v" + str(v) + \
                   ".\nThere are " + str(len(b.bingoList)) + " items in the bingo list, and " + \
                   str(len(c.bingoCardList)) + " active cards.\n" + \
                   "Card issue is currently "
    if not cardsActive:
        replyContent += "in"
    replyContent += "active."

    return replyContent


def version(bingoDateStr, v, messageList):
    """Increments or changes the version, while keeping the date the same. If more than one bingo game for a date."""
    bingoDateStrOld = copy.copy(bingoDateStr)
    vOld = copy.copy(v)

    try:
        # if nothing after version, just increment by 1.
        if len(messageList) == 2:
            v += 1
        # or if there is, change the version to that.
        elif messageList[2].isdigit():
            v = messageList[2]

        if v != vOld:
            CardListItemRemoved.clearCardDB(bingoDateStrOld, vOld, bingoDateStr, v)
            replyContent = "Version changed to " + str(
                v) + ". Date remains " + bingoDateStr + ". Bingo List sorted and reindexed."

        else:
            replyContent = "Could not read new version number. Must be an integer, or blank to increment."

    except:
        replyContent = "Could not read new version. Must be an integer, or blank to increment."


    return replyContent, v
