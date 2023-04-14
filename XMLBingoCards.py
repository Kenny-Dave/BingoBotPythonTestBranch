import xml.etree.ElementTree as ET
import pathlib
import random

import BingoCardListFactoryModule as c
import AllBingoListFactoryModule as b



#from bingoCardListFactoryModule import bingoCardItemClass
parentPathStr = str(pathlib.Path(__file__).parent.resolve())
#print (parentPathStr)

XMLPath = parentPathStr+"\\obj\\DataStore\\"
XMLFile = XMLPath+"CardsList.xml"

global XMLTree
XMLRoot=ET.Element("data")
XMLTree=ET.ElementTree(XMLRoot)

try:
    XMLTree=ET.parse(XMLFile)
    XMLRoot=XMLTree.getroot()

except: 
    print("No XML data found for cards.")

#build from XML file

def readList():
    
    for ri in XMLTree.iter("card"):

        userName=""
        bingoItemListIndex=[] #just the indexes
        bingoItemList = [] #allBingoList objects

        for attr in ri:
            if attr.tag=="userName":
                userName=attr.text
            
            elif attr.tag=="bingoItemList":

                
                for bi in attr:
                
                    bingoItemListIndex.append (bi.text) #this adds just the index as an int, not the object. 
                    
                #turn the bingoItem index into an AllBingoItem object
                for bi in bingoItemListIndex:
                        
                    biExists=False

                    #find and add if it exists
                    for ab in b.allBingoList:
                        if bi == str(ab.index): 
                            biExists=True
                            bingoItemList.append(ab)
                            break

                    #if the index doesn't exist, create a temp copy of allBingoList but with the items already on the card removed,
                    # and randomly select one from this. 

                    #Need to dupe this functionality for when the allBingoList changes so that a sensible card is still printed rather than complete regen.
                    #at the moment, it still prints deleted items, until a restart when this logic runs so replaces the removed items. 
                    #it's fine on change, as it's changing the existing object. 
                    #removing items or replacing the list only removes the objects from the list, so it still prints the existing item. 
                    if biExists == False:
                        tempABList = b.allBingoList[:] #make a copy...

                        for abi in bingoItemListIndex:
                            for ab in tempABList:
                                if abi==ab.index:
                                    tempABList.remove(ab)

                        bingoItemList.append(random.choice(tempABList))

        c.NewBingoCard(userName,bingoItemList, XMLAppend = False)

def writeList():
    #write to XML

    #because when there isn't anything in the file it can skip the parsing, so need to do it again here. 
    #deleting the existing records
    #global XMLTree
    try:
        for rootItem in XMLRoot.findall("*"):
            XMLRoot.remove(rootItem)
            XMLTree.write(XMLFile)
    except: 
        XMLRoot=ET.Element("data")
        XMLTree=ET.ElementTree(XMLRoot)

    #add each object in b.BingoCardList to XML
    for item in c.bingoCardList:
            if item.userName=="": print("blank userName")


            noo = ET.Element("card")
            rt = ET.SubElement(noo,"userName")
            rt.text=item.userName

            bl = ET.SubElement(noo,"bingoItemList")

            for bingoItem in item.bingoItemList:

                bi = ET.SubElement(bl,"bingoItem")
                bi.text=str(bingoItem.index)

            XMLRoot.append(noo)

    print ("bingoCardList len:"+str(len(c.bingoCardList)))
    print ("XMLCard written.")
    ET.indent(XMLRoot,"    ")
    XMLTree.write(XMLFile)