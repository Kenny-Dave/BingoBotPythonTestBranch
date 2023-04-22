#from mySettingsModule import mySettingsClass as s

bingoCardList=[]

def NewBingoCard(userName, userID, cardChanged, bingoItemList, drawPrintable):
    
    #create item
    bingoCardItem = bingoCardItemClass(userName, userID, cardChanged, bingoItemList, drawPrintable)

    #add to list, unless...
    if userName !="": bingoCardList.append(bingoCardItem)

    return bingoCardList

class bingoCardItemClass():

    userName = ""
    userID=0
    bingoItemList = []
    cardChanged = False
    drawPrintable = False
    
    def __init__(self,userName, userID, cardChanged, bingoItemList, drawPrintable):

        self.userName = userName
        self.bingoItemList = bingoItemList
        self.cardChanged = cardChanged
        self.userID = userID
        self.drawPrintable = drawPrintable

