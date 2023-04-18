# bot.py

from ast import Delete, Try

import io
import os

import discord
from discord import File #, Member, Attachment

import XML
import XMLBingoCards
import XMLDateVer
import XMLSettings

import pathlib
from datetime import datetime
from dotenv import load_dotenv
from CardGenModule import CardGenClass
from mySettingsModule import mySettingsClass as s
import AllBingoListFactoryModule as b
import BingoCardListFactoryModule as c
import allBingoItemRemovedModule

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#print(TOKEN)

intents=discord.Intents.default()
intents.message_content=True

client = discord.Client(intents=intents)

parentPathStr = str(pathlib.Path(__file__).parent.resolve())

XML.readList()
#print ("Len allBingoList: "+str(len(b.allBingoList)))
XMLBingoCards.readList()
#print ("Len card list: "+str(len(c.bingoCardList)))

global bingoDate

bingoDate, v = XMLDateVer.readDateVer()
global cardsActive
cardsActive = XMLSettings.ReadCardsActive()
print (cardsActive)
global bingoDateStr
bingoDateStr = bingoDate.strftime("%d/%m/%y")

#This selects the item in allBingo list based on the text given it. 
#Used when replacing text, etc. 
def selBingItem(selIndex):
                        
    #selItem=None
    for sel in b.allBingoList:
        if sel.index == selIndex:
            selItem = sel
            return selItem
        else:
            selItem = None

    return selItem

def sortBingo():
    #sorts the bingo list and resets the artificial index to the list index+1
    b.allBingoList.sort(key=lambda x: x.rawText)

    for it in b.allBingoList:
        #print(it.rawText)
        it.index = b.allBingoList.index(it)+1

def clean(rawText):

    #removing or changing characters that will confuse XML.
    for char in rawText:
        if char == "<": char ="["
        elif char ==">": char = "]"
        elif char =="\"": char = ""
        elif char =="\'": char = ""
            
    #Text "Free" needs to be reserved as there is logic attached to it for the freesquare. It won't print when appropriate, we don't want it in the list. 
    if rawText =="Free": rawText ="Free square"
    rawSplit = rawText.split(".")
    
    #remove the leading number and dot, which could be there if it's a list from generated data. 
    if len(rawSplit)>1:
        if rawSplit[0].isdigit:
            rawText = rawText.lstrip(rawSplit[0]+". ")

    return rawText

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    for guild in client.guilds:
        print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )

    print("Bingo list entries: "+str(len(b.allBingoList)))

@client.event
async def on_message(message, *args, **kwargs):

    #generates a card image to return to the user
    #this function has to be here as it uses message, so needs the on_message to be initialized.
    def printCard(drawPrintable):
        userName=message.author.name
        CardGenClassInstance = CardGenClass(userName, drawPrintable)
        
        bingoItemList = []
        addCardToList = True

        if s.idempotentCardRequest == True:
            #check if the card already exists in the db and pick up the bingoList if so
            for ec in c.bingoCardList:
                if ec.userName==userName:
                    bingoItemList=ec.bingoItemList
                    addCardToList = False
                    break

        if s.idempotentCardRequest == False:
            #remove the existing card for the user, before building a new one.
            for ec in c.bingoCardList:
                if ec.userName==userName:
                    c.bingoCardList.remove(ec)
                    break

        #if new request, generate bingoList
        #print ("Len bingo item list: "+str(len(bingoItemList)))
        if len(bingoItemList) ==0: bingoItemList = CardGenClassInstance.TextGen()
        #generate graphics
        bingoCard, bingoCardFileName = CardGenClassInstance.ImageGen(bingoItemList, bingoDate, v)
        
        #construct file reference for sending to user
        arr = io.BytesIO()
        bingoCard.save(arr, format='png',quality="keep")
        arr.seek(0)
        bingoCardIO = discord.File(fp=arr, filename=bingoCardFileName)

        #add card to list if a new request
        #print ("Add cards to list: "+str(addCardToList))
        if addCardToList == True: c.NewBingoCard(userName,bingoItemList, True)
        
        #should change this to an append function
        #print("To XML cards in printcard")
        XMLBingoCards.writeList()

        return bingoCardIO, bingoCardFileName

    #exits if message is from self, to avoid loops
    if message.author == client.user:
        return
    
    #splits the message by spaces to evaluate each option. 
    #note that this is complicated by the list items containing spaces, a solution is done for that locally. 
    messageList=message.content.split()

    if message.content.startswith("!bingo"):

            replyContent =""
            global cardsActive

        #try:
            #draws standard bingo card
            if len(messageList)==1: 



                if s.arrayX**2>len(b.allBingoList):
                    replyContent = "There are not enough items in the bingo list to generate a card. " \
                        +str(len(b.allBingoList)+" items, card settings is "+s.arrayX+" squared.")
                    await message.channel.send(replyContent)
                elif cardsActive == False:
                    replyContent = "Bingo card issue is not presently active. Please speak to a mod if you require further information, read up the thread, or wait patiently :)"
                    await message.channel.send(replyContent)

                else:
                    
                    drawPrintable=False
            
                    bingoCardIO, bingoCardFileName=printCard(drawPrintable)

                    if s.messageChannel==True: 
                        await message.channel.send(file=bingoCardIO)
                        print(bingoCardFileName+" sent to thread.")
                    if s.messageUser==True:
                        await message.author.send(file=bingoCardIO)
                        print(bingoCardFileName+" sent to user.")

            #draws low ink bingo card
            elif messageList[1]=="printable":
            
                if s.arrayX**2>len(b.allBingoList):
                    replyContent = "There are not enough items in the bingo list to generate a card. "+str(len(b.allBingoList)+ \
                        " items, card settings is "+s.arrayX+" squared.")
                    await message.channel.send(replyContent)
                elif cardsActive == False:
                    replyContent = "Bingo card issue is not presently active. Please speak to a mod if you require further information, read up the thread, or wait patiently :)"
                    await message.channel.send(replyContent)
                else:
                    drawPrintable=True

                    bingoCardIO, bingoCardFileName=printCard(drawPrintable)

                    if s.messageChannel==True: 
                        await message.channel.send(file=bingoCardIO)
                        print(bingoCardFileName+" sent to thread.")
                    if s.messageUser==True:
                        await message.author.send(file=bingoCardIO)
                        print(bingoCardFileName+" sent to user.")
            
            #returns standard about message
            elif messageList[1]=="about":
                replyContent = "Discord bingoBot version "+s.fileVersion+" \nWritten by Kenny Dave."
                await message.channel.send(replyContent)

            #Prints the contents of the helpfile to the thread
            elif messageList[1]=="?":

                #user commands help file
                if len(messageList)==2:
                    helpfile =parentPathStr+"\\obj\\HelpStrings\HelpText.txt"

                #flexible addition for end owner. Will print any file in the folder if the input matches the file name.
                #add text to help file if this is done. 
                else: 
                    helpfile =parentPathStr+"\\obj\\HelpStrings\\"+messageList[2]+".txt"

                with open(helpfile,"r") as f:
                    replyContent = "".join(f.readlines())
                    await message.channel.send(replyContent)
                f.close

            #commands beyond this point are restricted to moderators only, for amending lists etc.
            #currently causes failure for DMs. Need to set it to check the modmin permission for the attached guild.
            elif message.author.guild_permissions.moderate_members==False:
                await message.channel.send("Only moderators have permission to access mod commands, and you do not seem to.")

            #make card issue active or inactive
            elif messageList[1]=="toggleactive":
                if cardsActive == True:
                    cardsActive = False 
                    replyContent = "Card issue is now inactive. Users will not be able to request a card."
                    XMLSettings.WriteCardsActive(cardsActive)
                else:
                    cardsActive = True 
                    replyContent = "Card issue is now active. Users will be able to request a card."
                    XMLSettings.WriteCardsActive(cardsActive)
                await message.channel.send(replyContent)

            #change the selected date. 
            elif messageList[1]=="date":

                global bingoDate
                global v

                if len(messageList)==2:
                    
                    await message.channel.send("Currently set date is: "+bingoDate.strftime("%d %b %y")+" Version is v"+str(v)+".")
                else:
                    #stripping the control from the message, to leave only new date.
                    global bingoDateStr
                    bingoDateStr = message.content.lstrip("!bingo date \"").rstrip("\"")
                
                    #Setting. 
                    try:

                        bingoDate = datetime.strptime(bingoDateStr, '%d/%m/%y')

                        v = 1
                    
                        #Write new date and ver to XML
                        XMLDateVer.WriteDateVer(bingoDateStr,str(v),cardsActive)

                        #reset the cardList
                        c.bingoCardList.clear()
                        XMLBingoCards.writeList()

                        #Sort the allBingoList, reset the indexes. And write to XML.
                        sortBingo()
                        XML.writeList()

                        await message.channel.send("bingoDate changed to "+bingoDate.strftime("%d %b %Y")+ \
                                                   ". Version reset to 1. Bingo List sorted and reindexed.")
                
                    except:
                        await message.channel.send("Could not read new date correctly. Please ensure it is in the format dd/mm/yy, e.g. 25/03/23.")

            elif messageList[1]=="version":
                #increments or changes the version, while keeping the date the same. If more than one bingo game for a date. 

                try:
                    #if nothing after version, just increment by 1. 
                    if len(messageList)==2:
                        v +=1
                    #or if there is, change the version to that. 
                    elif messageList[2].isdigit()==True:
                        v=messageList[2]

                    #Write new date and ver to XML
                    XMLDateVer.WriteDateVer(bingoDateStr,str(v),cardsActive)

                    #reset the cardList
                    c.bingoCardList.clear()
                    XMLBingoCards.writeList()

                    #Sort the allBingoList, reset the indexes. And write to XML.
                    sortBingo()
                    XML.writeList()

                    #message channel
                    await message.channel.send("Version changed to "+str(v)+". Date remains "+bingoDate.strftime("%d %b %Y")+". Bingo List sorted and reindexed.")
                except: 
                    await message.channel.send("Could not read new version. Must be an integer.")

                #Need to also recalc the indexes and delete the old user info. 
                
            elif messageList[1]=="list":

                #replace the list with a new list
                if messageList[2]=="replacelist":

                    if len(message.attachments) !=1:
                        await message.channel.send("There must be exactly one attachment when using this command. " \
                                                   +str(len(message.attachments))+" detected.")
                        
                    else:
                        
                        #for updating existing cards, and message in thread. 
                        bingoItemsRemoved =[]

                        #turn the attachment into a readable byte object
                        att = message.attachments[0]
                        fileByte = io.BytesIO()
                        await att.save(fp=fileByte)

                        #turn bytes object into a (messy) string object
                        fileReplacex=io.TextIOWrapper(fileByte,encoding ='utf-8')

                        #input is TextIOWrapper, output is a cleaned list
                        def cleanfile(TextIOWrapper=fileReplacex):
                            
                            fileReplaceClean=[]

                            for line in fileReplacex:
                            
                                #clean the line
                                line = line.rstrip("\r\n")
                                line = clean(line)
                                if line == "": continue
                                fileReplaceClean.append(line)
                                
                            return fileReplaceClean

                        #list of items on the replacelist
                        fileReplaceList = cleanfile(fileReplacex)

                        #These are counters for the message to user as to what has changed. 
                        sameCount = 0
                        addCount = 0 
                        delCount = 0

                        #for iterating across allBingoList, removing items without messing the iteration up. allBingoList is then set to this afterwards. 
                        allBingoListIter = []

                        #Check if an allBingoList item exists in replace list and delete if not
                        for sel in b.allBingoList:
                            
                            itemExists = False

                            for item in fileReplaceList:

                                if sel.rawText==item:
                                    itemExists=True
                                    allBingoListIter.append(sel)
                                    break
                            
                            if itemExists == False:
                                delCount +=1
                                bingoItemsRemoved.append(sel.index)

                                
                        #just the ones that made it through, because they're also on the replace list.
                        b.allBingoList = allBingoListIter

                        #check if an item in the replace list is in the allBingoList and add if not.
                        for item in fileReplaceList:

                            itemExists=False

                            #Check if item exists in allBingoList    
                            for sel in b.allBingoList:
                                if item == sel.rawText:
                                    itemExists=True
                                    sameCount += 1
                                    break
                            
                            #add it if it doesn't. 
                            if itemExists == False:
                                addCount +=1
                                b.NewAllBingoItem(item,0)

                        #print to shell
                        print ("Replacelist run; ",str(sameCount),"items were already in the list, ",str(addCount), "items added, ",\
                        str(delCount),"items removed.")

                        replyContent = "Replacelist run; "+str(sameCount)+" items were already in the list, "+str(addCount)+ \
                        " items attempted to add, "+str(delCount)+" items removed." + " There are now "+str(len(b.allBingoList))+ \
                        " items in the bingo items list."
                        
                        #amend existing cards, for if they have the item on their list
                        if s.idempotentCardRequest == True:
                            userChangedString = allBingoItemRemovedModule.allBingoItemRemoved(bingoItemsRemoved)
                            replyContent += "\nUsers with changed bingocards: "+userChangedString+"."

                        #message thread
                        await message.channel.send(replyContent)
                            
                        #serialise
                        XML.writeList()

                #add an item to the list
                elif messageList[2]=="add":

                    if len(messageList)>3:
                        input = message.content.lstrip("!bingo list add ")

                        #If it can't find the " at the start and end of what is stripped, message and exit. 
                        if not input.startswith("\"") or not input.endswith("\""):
                            await message.channel.send("Could not resolve string to add. Format should be \"!bingo list add \"example text\"\".")
                            
                        else:
                            #remove the " from the front and back
                            input = input.lstrip("\"").rstrip("\"")                            
                            
                            #itemExists measures whether the item in the addList is already in allBingoList. If not, add it. 
                            itemExists=False

                            #Check if item exists in allBingoList    
                            for sel in b.allBingoList:
                                
                                if input == sel.rawText:
                                    itemExists=True
                                    await message.channel.send("Item is already in the list,",str(sel.index),". Not added.")
                                    break
                            
                            #add it if it doesn't
                            if itemExists == False:
                                b.NewAllBingoItem(input,0)
                                XML.writeList()

                            #message thread
                            await message.channel.send("Bingo list item \""+input+"\" added. There are now "+str(len(b.allBingoList))+" items in the bingo items list.")
                            
                    else:
                        #message thread
                        await message.channel.send("Could not resolve string to add. Format should be \"!bingo list add \"example text\"\".")

                #add a list of items to the list using an attachment
                elif messageList[2]=="addlist":

                    if len(message.attachments) !=1:
                        await message.channel.send("There must be exactly one attachment when using this command. " \
                                                   +str(len(message.attachments))+" detected.")
                        
                    else:
                        #turn the attachment into a readable byte object
                        att = message.attachments[0]
                        fileByte = io.BytesIO()
                        await att.save(fp=fileByte)

                        #turn bytes object into a (messy) string object
                        file=io.TextIOWrapper(fileByte,encoding ='utf-8')

                        sameCount = 0
                        addCount = 0 

                        for linex in file:
                            
                            #clean the line
                            line = linex.rstrip("\r\n")
                            line = clean(line)

                            #itemExists measures whether the item in the addList is already in allBingoList. If not, add it. 
                            itemExists=False

                            #Check if item exists in allBingoList    
                            for sel in b.allBingoList:
                                if line == sel.rawText:
                                    itemExists=True
                                    sameCount += 1
                                    break
                            
                            #add it if it doesn't
                            if itemExists == False and line !="":
                                addCount +=1
                                b.NewAllBingoItem(line,0)

                        print ("Addlist run; ",str(sameCount),"items were already in the list, ",str(addCount), "items added.")

                        #message thread
                        await message.channel.send("File added successfully. "+str(sameCount)+" lines are the same, "+str(addCount)+" items attempted to add, " + \
                                                    " There are now "+str(len(b.allBingoList))+" items in the bingo items list.")
                            
                        #serialise
                        XML.writeList()
                        
                elif messageList[2]=="remove":
                    #removes the selected item in allBingoList
                    
                    #remove a list item, selected by index
                    selIndex = int(messageList[3])
                    selItem=selBingItem(selIndex)

                    if selItem== None: 
                        await message.channel.send("Index not found.")
                    else:
                        
                        bingoItemsRemoved =[]
                        bingoItemsRemoved.append(selIndex)

                        replyContent = "Item "+str(selIndex)+". \""+selItem.rawText+"\" removed."

                        #amend existing cards, for if they have the item on their list
                        #if idepotency is on
                        if s.idempotentCardRequest == True:
                            userChangedString = allBingoItemRemovedModule.allBingoItemRemoved(bingoItemsRemoved)
                            replyContent += ("\nUsers with changed bingocards: "+userChangedString+".")
                            #check that message length is not >2000 characters. 

                        #delete the entry from the list. Need the python index, not the humanised index. 
                        del b.allBingoList[b.allBingoList.index(selItem)]

                        await message.channel.send(replyContent)

                        XML.writeList()

                elif messageList[2]=="change":
                    #changes the raw text of the selected item in allBingoList
                    
                    selItem=None

                    #try:
                    selIndex = int(messageList[3])

                    selItem=selBingItem(selIndex)
                    #print (selItem.rawText)

                    if selItem== None: 
                        await message.channel.send("Index not found.")
                    else:
                        #stripping the control from the message, to leave only what the new message is in. Inside ""s.                         
                        newRawText = message.content.lstrip("!bingo list change "+str(selIndex)+" \"").rstrip("\"")
                        #cleaning based on various requirements. 
                        newRawText = clean(newRawText)
                        #Setting. 
                        selItem.rawText = newRawText

                        #print(selItem.rawText)
                        replyContent = "Text change for item "+str(selItem.index)+" to: "+str(selItem.rawText)
                        await message.channel.send(replyContent)
                        XML.writeList()

                    #except Exception as e: 
                    #     await message.channel.send("Command not recognised. Type \"!bingo ?\" for a list of commands. \n"+str(e))

                #print the list of elements in bingoList
                elif messageList[2]=="view":
                    #prints a list of the allBingoList elements in the thread. Index + ". " + rawText

                    replyContent =""
                    for el in b.allBingoList:
                        replyContent = replyContent+str(el.index) + ". "+el.rawText+"\n"

                    await message.channel.send(replyContent)

                elif messageList[2]=="output":
                    #prints a list of the allBingoList elements to a text file and attaches it. Index + ". " + rawText

                    #content is one string, many lines, of allBingoList. In human readable form.
                    replyContent =""
                    for el in b.allBingoList:
                        replyContent = replyContent+str(el.index) + ". "+el.rawText+"\n"

                    #turn the variable content into a file to attach in message
                    arr = io.StringIO(replyContent)

                    #send message
                    await message.channel.send(replyContent = "Bingo list attached.", file=File(fp=arr,filename="OutputList.txt"))

                elif messageList[2]=="sort":

                    if s.idempotentCardRequest == True:
                        await message.channel.send("This option is disabled with the option for consistent cards enabled. " /
                        +"List will be sorted when the date or version is changed, when the cards database is reset.")
                    else:
                        #Sort the allBingoList, reset the indexes. And write to XML.
                        sortBingo()
                        await message.channel.send("List sorted and reindexed.")
                        XML.writeList()

                else:
                    await message.channel.send("Input error for list. Type \"!bingo ?\" for a list of valid commands.")

            elif messageList[1]=="cardlist":

                try:
                    replyContent=""
                    #view the list of users that have requested cards
                    if messageList[2]=="view":
                    
                        userList= ["Cards active:"]
                        for idu, u in enumerate(c.bingoCardList):
                            userList.append(str(idu)+". "+u.userName)

                        replyContent = "\n ".join(userList)
                        #print cardDB entries
                        #need the index in there; list index is fine. 
                
                    #delete the entry
                    elif messageList[2]=="reset":
                    
                    
                        delItem = messageList[3]
                        print("delItem: "+str(delItem))
                        print(delItem.isdigit())
                        print("1".isdigit())

                        if delItem == "all":
                            #remove all entries
                            c.bingoCardList.clear()
                            replyContent = "All bingo cards deleted from the database."
                            pass
                        elif delItem.isdigit() == True:
                            delObj = c.bingoCardList.pop(int(delItem))
                            replyContent = "Card for "+delObj.userName+" deleted from the database."
                        else:
                            replyContent = "card reset failed. Index must be an integer in the list, or \"all\"."
                        
                        #XML
                        XMLBingoCards.writeList()

                except:
                    replyContent = "Error processing cardList command. Type \"!bingo ? cardlist \" for a list of valid commands."

                #check that message length is not >2000 characters. 
                await message.channel.send(replyContent)

            else:
                await message.channel.send("Command not recognised. Type \"!bingo ?\" for a list of valid commands")

                #we should have this in a try catch as well I think. That will deal with it not having sufficient members. 
        #except Exception as e:
            #print("Command not recognised. Type \"!bingo ?\" for a list of commands (error)")
        #    await message.channel.send(str(e)+" exception")
        

client.run(str(TOKEN))