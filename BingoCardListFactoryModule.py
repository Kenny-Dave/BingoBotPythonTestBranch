#from mySettingsModule import mySettingsClass as s

bingoCardList=[]

def NewBingoCard(userName,bingoItemList, XMLAppend):
    
    #create item
    bingoCardItem = bingoCardItemClass(userName,bingoItemList)

    #add to list, unless...
    if userName !="": bingoCardList.append(bingoCardItem)

    #add to XML, not built yet.
    if XMLAppend == True:
        pass

    return bingoCardList



class bingoCardItemClass():

    userName = ""
    bingoItemList = []
    
    def __init__(self,userName, bingoItemList):

        self.userName = userName
        self.bingoItemList = bingoItemList
