from mySettingsModule import mySettingsClass as s

allBingoList=[]

def NewAllBingoItem(rawText,index):
        
    #create item
    allBingoListItem = AllBingoItemClass(rawText,index)

    #add to list, unnless blank or equal to freesquare text
    if allBingoListItem.rawText !="" and allBingoListItem.rawText !=s.freeSquareText:
        allBingoList.append(allBingoListItem)

    return allBingoList

class AllBingoItemClass():

    rawText=""
    formattedText=""
    fontSize=0
    index=0

    def __init__(self,rawText=rawText,index=index):

        #Read XML for the raw text of each item
        self.rawText=rawText.rstrip("\n")
        #Read XML for the index of each item
        self.index=int(str(index).rstrip("\n"))

        #calculate index if not sent
        if self.index==0:
            maxIndex=0
            for item in allBingoList:
                if item.index>maxIndex:
                    maxIndex= item.index
            
            #print(maxIndex)
            self.index = maxIndex+1        



