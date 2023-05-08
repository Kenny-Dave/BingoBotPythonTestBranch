import Settings as s
import CardListFactory as c
import XMLDateVer as XDV
import XMLCardList as XBC
import XMLList
import ListFactory as b

import shutil
import os


def clearCardDB(delDate, delV, newDate, newV):
    """does a few things that need doing when the card list is reset. Removes the cards if they exist, resets the
    database, resorts and indexes the allBingoList, and writes all that to XML."""
    # delete the card pics, if they exist
    if s.saveCards:
        delCards(delDate, delV)

    # Write new date and ver to XML
    XDV.WriteDateVer(newDate, newV)

    # reset the cardList
    c.bingoCardList.clear()
    XBC.writeList()

    # Sort the allBingoList, reset the indexes. And write to XML.
    sortBingo()
    XMLList.writeList()


def delCards(delDate, v, *userName):
    """deletes the printed card. Either all if no userNames passed, or the userNames if they are."""

    saveFolder = os.path.join(s.parentPathStr, "obj", "Cards", delDate, " v", str(v))

    # if no userNames passed, delete the folder
    if len(userName) == 0:
        try:
            # saveFolder = s.parentPathStr + "\\obj\\Cards\\" + delDate + " v" + str(v) + "\\"
            print("Folder deleted: " + saveFolder)
            shutil.rmtree(saveFolder, ignore_errors=False)
        except:
            print("Could not delete card folder.")

    # if userNames passed, delete em all and leave the folder
    else:
        for uN in userName:
            if s.saveCards:
                try:
                    # saveFolder = s.parentPathStr + "\\obj\\Cards\\" + delDate + " v" + str(v) + "\\"
                    delFile = os.path.join(saveFolder, uN + ".png")
                    os.remove(delFile)
                except:
                    pass


def sortBingo():
    """sorts the bingo list and resets the artificial index to the list index+1"""
    b.bingoList.sort(key=lambda x: x.rawText)

    for it in b.bingoList:
        it.index = b.bingoList.index(it) + 1
