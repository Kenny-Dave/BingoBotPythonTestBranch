import os
import xml.etree.ElementTree as ET

import ListFactory as b

"""
parentPathStr = str(pathlib.Path(__file__).parent.resolve())
XMLPath = parentPathStr + "/obj/DataStore/"
XMLFile = XMLPath + "ItemsList.xml"
"""

XMLFile = os.path.join(os.path.curdir, "obj", "DataStore", "ItemsList.xml")

XMLTree = ET.parse(XMLFile)
XMLRoot = XMLTree.getroot()

# build allBingoList from XML file

allBingoList = []

rawText = ""
formattedText = ""
fontSize = 0


# print("XML instance pops on boot") #It does.

def readList():
    # reads allBingoList from XML
    rawText = ""
    index = 0

    for ri in XMLTree.iter("bingoItem"):

        for attr in ri:
            if attr.tag == "rawText":
                rawText = attr.text
            elif attr.tag == "index":
                index = attr.text

        b.NewBingoItem(rawText, index)


def writeList():
    # writes allBingoList to XML

    # removes all the existing items.
    for rootItem in XMLRoot.findall("*"):
        XMLRoot.remove(rootItem)

    XMLTree.write(XMLFile)

    # add each object in b.allBingo list to XML
    for item in b.bingoList:
        if item.rawText == "":
            print("blank rawText")

        noo = ET.Element("bingoItem")
        rt = ET.SubElement(noo, "rawText")
        rt.text = item.rawText
        it = ET.SubElement(noo, "index")
        it.text = str(item.index)

        XMLRoot.append(noo)

    ET.indent(XMLRoot, "    ")
    XMLTree.write(XMLFile)
