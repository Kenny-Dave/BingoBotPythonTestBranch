import xml.etree.ElementTree as ET
import pathlib

import AllBingoListFactoryModule as b
from AllBingoListFactoryModule import AllBingoItemClass

parentPathStr = str(pathlib.Path(__file__).parent.resolve())
XMLPath = parentPathStr+"\\obj\\DataStore\\"
XMLFile = XMLPath+"ItemsList.xml"

XMLTree=ET.parse(XMLFile)
XMLRoot=XMLTree.getroot()

#build allBingoList from XML file

allBingoList=[]

rawText=""
formattedText =""
fontSize=0

#print("XML instance pops on boot") #It does. 

def readList():
    #reads allBingoList from XML
    rawText=""
    index=0
    #formattedText=""
    #fontSize=0
    
    for ri in XMLTree.iter("bingoItem"):

        for attr in ri:
            if attr.tag=="rawText":
                rawText=attr.text
            elif attr.tag=="index":
                index =attr.text

        b.NewAllBingoItem(rawText,index)

def writeList():
    #writes allBingoList to XML

    #removes all the existing items. 
    for rootItem in XMLRoot.findall("*"):
        XMLRoot.remove(rootItem)

    XMLTree.write(XMLFile)

    #add each object in b.allBingo list to XML
    for item in b.allBingoList:
            if item.rawText=="": print("blank rawText")

            noo = ET.Element("bingoItem")
            rt = ET.SubElement(noo,"rawText")
            rt.text=item.rawText
            it = ET.SubElement(noo,"index")
            it.text=str(item.index)

            XMLRoot.append(noo)
    
    ET.indent(XMLRoot,"    ")
    XMLTree.write(XMLFile)