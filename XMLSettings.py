import xml.etree.ElementTree as ET
import pathlib
from datetime import datetime

#import AllBingoListFactoryModule as b
#from AllBingoListFactoryModule import AllBingoItemClass

parentPathStr = str(pathlib.Path(__file__).parent.resolve())
XMLPath = parentPathStr+"\\obj\\DataStore\\"
XMLFile = XMLPath+"Settings.xml"

try:
    global XMLTree
    XMLTree=ET.parse(XMLFile)
    XMLRoot=XMLTree.getroot()

except: 
    print("No cardsActive value found")

def ReadCardsActive():
    
    cardsActive=True

    try:
        for ri in XMLTree.iter("*"):
        
            if ri.tag == "cardsActive":
                cardsActive = ri.text == "True"
    except:
        #print("No date and version found. Reverting to default.")
        WriteCardsActive(cardsActive)

    return cardsActive

def WriteCardsActive(cardsActive):

    #because when there isn't anything in the file it can skip the parsing, so need to do it again here. 
    global XMLTree
    try:
        for rootItem in XMLRoot.findall("*"):
            XMLRoot.remove(rootItem)
            XMLTree.write(XMLFile)
    except: 
        XMLRoot=ET.Element("Root")
        
        XMLTree=ET.ElementTree(XMLRoot)

    #write the cardsActive to XML
    cA = ET.Element("cardsActive")
    cA.text=str(cardsActive)
    XMLRoot.append(cA)

    #save new XML
    ET.indent(XMLRoot,"    ")
    XMLTree.write(XMLFile)