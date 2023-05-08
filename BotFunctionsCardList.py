from discord import File
import io

import XMLCardList
import Settings as s
import CardListFactory as c
import CardListItemRemoved
import CardGen


async def CardListItems(messageList, bingoDate, bingoDateStr, v, guild):
    """Functions for manipulating the card list"""
    replyFile = None
    replyContent = "Input error for card list. Type \"!bingo ?\" for a list of valid commands."
    try:
        command = messageList[2]
        match command:
            case "view":  # view the list of users that have requested cards
                replyContent, replyFile = view(attachFile=False)
            case "viewlist":  # Output file of the list of users that have requested cards
                replyContent, replyFile = view(attachFile=True)
            case "reset":  # delete the cards generated, either all or a specific item on the list
                replyContent = reset(bingoDateStr, messageList, v)
            case "reissue":  # sends all the amended cards to the users via DM
                replyContent = await reissue(bingoDate, guild, v)
            case _:
                replyContent = "Error processing cardList command. Type \"!bingo ? cardlist \" for a list of valid " \
                       "commands."
    except:
        pass
    return replyContent, replyFile


async def reissue(bingoDate, guild, v):
    """sends all the amended cards to the users via DM"""

    if not s.idempotentCardRequest:
        replyContent = "This option is disabled with the options selected by the server owner. "

    else:
        for card in c.bingoCardList:
            if card.cardChanged:
                userName = card.userName
                userID = card.userID
                bingoCardIO, bingoCardFileName = CardGen.genCard(
                    userName, userID, card.drawPrintable, bingoDate, v)

                # global guild
                member = await guild.fetch_member(userID)
                await member.send("Your bingo card has been amended.", file=bingoCardIO)
                print(bingoCardFileName + " sent to user.")

        replyContent = "All amended cards sent to users via DM."

    return replyContent


def reset(bingoDateStr, messageList, v):
    """delete the cards generated, either all or a specific item on the list"""
    delItem = messageList[3]
    if delItem == "all":
        # remove all cards
        c.bingoCardList.clear()
        if s.saveCards:
            CardListItemRemoved.delCards(bingoDateStr, v)
        replyContent = "All bingo cards deleted from the database."

    elif delItem.isdigit():
        # delete a specific users card
        delObj = c.bingoCardList.pop(int(delItem))
        if s.saveCards:
            CardListItemRemoved.delCards(bingoDateStr, v, delObj.userName)
        replyContent = "Card for " + delObj.userName + " deleted from the database."
    else:
        replyContent = "card reset failed. Index must be an integer in the list, or \"all\"."
    XMLCardList.writeList()

    return replyContent


def view(attachFile):
    """view the list of users that have requested cards"""
    userList = ["Cards active:"]
    replyFile = None
    replyContent = None
    for idu, u in enumerate(c.bingoCardList):
        if u.cardChanged:
            userList.append(str(idu) + ". " + u.userName + " [changed since issue]")
        else:
            userList.append(str(idu) + ". " + u.userName)

    if len(userList) == 1:
        userList.append("None")
    if attachFile:
        replyContent = "Cards active list attached."
        arr = "\n ".join(userList)
        arrIO = io.StringIO(arr)
        replyFile = File(fp=arrIO, filename="OutputCardList.txt")
    elif not attachFile:
        replyContent = "\n ".join(userList)

    return replyContent, replyFile
