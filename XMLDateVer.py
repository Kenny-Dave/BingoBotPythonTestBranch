import os
import xml.etree.ElementTree as ET
from datetime import datetime

XMLFile = os.path.join(os.path.curdir, "obj", "DataStore", "DateVer.xml")

try:
    XMLTree = ET.parse(XMLFile)
    XMLRoot = XMLTree.getroot()

except:
    print("No date and version found. Reverting to default.")


def readDateVer():
    bingoDateStr = "01 Jan 00"
    bingoDate = datetime.strptime(bingoDateStr, "%d %b %y")
    v = 1
    global XMLTree

    try:
        for ri in XMLTree.iter("*"):

            if ri.tag == "bingoDateStr":
                bingoDateStr = ri.text
                bingoDate = datetime.strptime(bingoDateStr, "%d %b %y")
            if ri.tag == "v":
                v = int(ri.text)
    except:
        # print("No date and version found. Reverting to default.")
        WriteDateVer(bingoDateStr, v)

    return bingoDate, v


def WriteDateVer(bingoDateStr, v):
    # because when there isn't anything in the file it can skip the parsing, so need to do it again here.
    global XMLTree
    global XMLRoot
    try:
        for rootItem in XMLRoot.findall("*"):
            XMLRoot.remove(rootItem)
            XMLTree.write(XMLFile)
    except:
        XMLRoot = ET.Element("Root")

        XMLTree = ET.ElementTree(XMLRoot)

    # write the bingoDateStr to XML
    bD = ET.Element("bingoDateStr")
    bD.text = bingoDateStr
    XMLRoot.append(bD)

    # write the version to XML
    vV = ET.Element("v")
    vV.text = str(v)
    XMLRoot.append(vV)

    # save new XML
    ET.indent(XMLRoot, "    ")
    XMLTree.write(XMLFile)
