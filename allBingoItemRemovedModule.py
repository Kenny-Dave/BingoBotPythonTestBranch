from BingoCardListFactoryModule import bingoCardList 
import AllBingoListFactoryModule as b
import XMLBingoCards

import random

#code to run to ammend cards if a bingo item is removed with the list remove or list replace command.
#bingoItemsRemoved is a list of indexes.
def allBingoItemRemoved(bingoItemsRemoved):
    
    usersChangedList =[]

    #make a copy of the list to select the replacement bingo item from, which excludes the items already selected for the card
    tempABListCtrl = b.allBingoList [:]

    #removing the items being removed from the pool of new items, which is the same for all cards
    for ab in b.allBingoList:
        for bi in bingoItemsRemoved:
            if bi == ab.index:
                try: tempABListCtrl.remove(ab)
                except: print("Could not remove item bi." + str(bi)+" "+str(ab.index))

    #remove the items already a card from the pool for that card
    for card in bingoCardList:

        #print (card.userName)

        itemsToChangeList=[]
        tempABList = tempABListCtrl [:]

        for selItem in card.bingoItemList:

            #find all changed items on this card
            for itemRemoved in bingoItemsRemoved:
                if itemRemoved == selItem.index:
                    itemsToChangeList.append(itemRemoved)

        #print ("itemsToChangeList len: "+str(len(itemsToChangeList)))

        for item in itemsToChangeList: print("Item index to remove: "+str(item))
        #if there are changed items on the card
        if len(itemsToChangeList) !=0:
            
            usersChangedList.append(card.userName)
            card.cardChanged = True
            
            #print("User: "+card.userName+".\nCardChanged = True.")
            #print ("bingoItemList len: "+str(len(card.bingoItemList)))

            for cardItem in card.bingoItemList:
                
                #removing the items on the card from the pool of new items
                for ab in b.allBingoList:
                    #print ("cardItem and ab indexes: "+str(cardItem.index)+" "+str(ab.index))
                    if ab.index == cardItem.index:
                        #print (True)
                        try: tempABList.remove(ab)
                        except: pass #print("Could not remove item." + str(ab.index)+" "+str(cardItem.index))
                        continue

            #select the replacement bingoItems
            replaceList = random.sample(tempABList,len(itemsToChangeList))

            #print("replace list len, tempABList len: "+str(len(replaceList))+" "+str(len(tempABList)))
            #print("allBingoList len: "+str(len(b.allBingoList)))
            
            n=0
            for itemToChange in itemsToChangeList:
                
                for cardItem in card.bingoItemList:
                    if itemToChange == cardItem.index:
                        replaceIndex= card.bingoItemList.index(cardItem)
                        card.bingoItemList.remove(cardItem)
                        card.bingoItemList.insert(replaceIndex,replaceList[n])
                        n +=1
                        break
    
    if len(usersChangedList)==0: 
        usersChangedList.append("None")
    else: 
        XMLBingoCards.writeList()

    #for messaging the users with changed cards to channel.
    usersChangedString = ", ".join(usersChangedList)

    return usersChangedString