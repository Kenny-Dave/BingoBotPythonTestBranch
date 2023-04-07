import xml.etree.ElementTree as ET
import pathlib
from datetime import datetime

import AllBingoListFactoryModule as b
from AllBingoListFactoryModule import AllBingoItemClass

parentPathStr = str(pathlib.Path(__file__).parent.resolve())
XMLPath = parentPathStr+"\\obj\\DataStore\\"
XMLFile = XMLPath+"DateVer.xml"

try:
    global XMLTree
    XMLTree=ET.parse(XMLFile)
    XMLRoot=XMLTree.getroot()

except: 
    print("No date and version found. Reverting to default.")

def readDateVer():
    
    bingoDateStr="01/01/00"
    bingoDate = datetime.strptime(bingoDateStr, '%d/%m/%y')
    v=1

    try:
        for ri in XMLTree.iter("*"):
        
            if ri.tag == "bingoDateStr":
                bingoDateStr = ri.text
                bingoDate = datetime.strptime(bingoDateStr, '%d/%m/%y')
            if ri.tag == "v":
                v =int(ri.text)
    except:
        #print("No date and version found. Reverting to default.")
        writeDateVer(bingoDateStr, v)

    return bingoDate, v

def writeDateVer(bingoDateStr, v):

    #because when there isn't anything in the file it can skip the parsing, so need to do it again here. 
    global XMLTree
    try:
        for rootItem in XMLRoot.findall("*"):
            XMLRoot.remove(rootItem)
            XMLTree.write(XMLFile)
    except: 
        XMLRoot=ET.Element("Root")
        
        XMLTree=ET.ElementTree(XMLRoot)

    #write the bingoDateStr
    bD = ET.Element("bingoDateStr")
    bD.text=bingoDateStr
    XMLRoot.append(bD)

    #write the version
    vV = ET.Element("v")
    vV.text=str(v)
    XMLRoot.append(vV)

    #save new
    ET.indent(XMLRoot,"    ")
    XMLTree.write(XMLFile)