import os
import xml.etree.ElementTree as ET
import random

import CardListFactory as c
import ListFactory as b

XMLFile = os.path.join(os.path.curdir, "obj", "DataStore", "CardsList.xml")
XMLRoot = ET.Element("data")
XMLTree = ET.ElementTree(XMLRoot)

try:
    XMLTree = ET.parse(XMLFile)
    XMLRoot = XMLTree.getroot()

except:
    print("No XML data found for cards.")


def readList():
    """build from XML file"""

    global XMLTree
    # global XMLRoot

    for ri in XMLTree.iter("card"):

        userName = ""
        userID = 0
        cardChanged = False
        drawPrintable = False
        bingoItemListIndex = []  # just the indexes
        bingoItemList = []  # allBingoList objects

        for attr in ri:
            if attr.tag == "userName":
                userName = attr.text
            elif attr.tag == "userID":
                userID = attr.text
            elif attr.tag == "cardChanged":
                cardChanged = attr.text == "True"
            elif attr.tag == "drawPrintable":
                drawPrintable = attr.text == "True"

            elif attr.tag == "bingoItemList":

                for bi in attr:
                    bingoItemListIndex.append(bi.text)  # this adds just the index as an int, not the object.

                # turn the bingoItem index into an AllBingoItem object
                for bi in bingoItemListIndex:

                    biExists = False

                    # find and add if it exists
                    for ab in b.bingoList:
                        if bi == str(ab.index):
                            biExists = True
                            bingoItemList.append(ab)
                            break

                    # if the index doesn't exist, create a temp copy of allBingoList but with the items already
                    # on the card removed, and randomly select one from this.
                    if not biExists:
                        tempABList = b.bingoList[:]  # make a copy...

                        for abi in bingoItemListIndex:
                            for ab in tempABList:
                                if abi == ab.index:
                                    tempABList.remove(ab)

                        # select from the list of items that aren't already in the bingoItemList and append
                        bingoItemList.append(random.choice(tempABList))
                        cardChanged = True

        c.NewBingoCard(userName, userID, cardChanged, bingoItemList, drawPrintable=drawPrintable)


def writeList():
    """Write to XML"""

    global XMLRoot
    global XMLTree
    # because when there isn't anything in the file it can skip the parsing, so need to do it again here.
    # deleting the existing records
    # global XMLTree
    try:
        for rootItem in XMLRoot.findall("*"):
            XMLRoot.remove(rootItem)
            XMLTree.write(XMLFile)
    except:
        XMLRoot = ET.Element("data")
        XMLTree = ET.ElementTree(XMLRoot)

    # add each object in b.BingoCardList to XML
    for item in c.bingoCardList:
        if item.userName == "":
            print("blank userName")

        noo = ET.Element("card")
        userName = ET.SubElement(noo, "userName")
        userName.text = item.userName
        userID = ET.SubElement(noo, "userID")
        userID.text = str(item.userID)
        cardChanged = ET.SubElement(noo, "cardChanged")
        cardChanged.text = str(item.cardChanged)
        drawPrintable = ET.SubElement(noo, "drawPrintable")
        drawPrintable.text = str(item.drawPrintable)

        bl = ET.SubElement(noo, "bingoItemList")

        for bingoItem in item.bingoItemList:
            bi = ET.SubElement(bl, "bingoItem")
            bi.text = str(bingoItem.index)

        XMLRoot.append(noo)

    # print ("bingoCardList len:"+str(len(c.bingoCardList)))
    ET.indent(XMLRoot, "    ")
    XMLTree.write(XMLFile)
