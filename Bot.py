# Bot.py

import io
import os

import discord

from dotenv import load_dotenv

import XMLList
import XMLCardList
import XMLDateVer
import XMLSettings

# from CardGenModule import CardGenClass
import Settings as s
import ListFactory as b
import CardListFactory as c
import CardTemplateGen
import CardGen

import BotFunctionsGen as bFG
import BotFunctionsList as bFL
import BotFunctionsCardList as bFCL

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# print(TOKEN)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

XMLList.readList()
XMLCardList.readList()
bingoDate, v = XMLDateVer.readDateVer()
cardsActive = XMLSettings.ReadCardsActive()
bingoDateStr = bingoDate.strftime("%d %b %y")


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    global guild
    guild = client.guilds[0]
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    print(
        "Bingo list count: " + str(len(b.bingoList)) + "\n"
        "Active card count: " + str(len(c.bingoCardList)) + "\n"
        "Working directory: " + s.currDirPrint + "\n"
        "Selected date and version: " + bingoDateStr + " v" + str(v) + "\n"
        "Card print active: " + str(cardsActive))

    # regenerating the background files based on any changes to the settings.
    CardTemplateGen.TemplateGen()
    CardTemplateGen.TemplatePrintableGen()


@client.event
async def on_message(message):

    # exits if message is from self, to avoid loops
    if message.author == client.user:
        return

    messageContentLower = message.content.lower()

    if messageContentLower.startswith("!bingo"):

        fileByte = None
        replyContent = ""
        replyFile = None
        replyBool = True
        global cardsActive
        global guild

        if len(message.attachments) > 0:
            # turn the first attachment into a readable byte object
            att = message.attachments[0]
            fileByte = io.BytesIO()
            await att.save(fp=fileByte)

        # member is the message.author but the property of the guild.
        # used to pull the nickname on the server, if there is one. Defaults to discord name if None.

        member = await guild.fetch_member(message.author.id)

        userName = member.nick
        if userName is None:
            userName = message.author.name
        userID = message.author.id

        global bingoDate
        global bingoDateStr
        global v

        # splits the message by spaces to evaluate each option. 
        # note that this is complicated by the list items containing spaces, a solution is done for that locally. 
        messageList = messageContentLower.split()

        # check if user has mod permissions on any of the linked guild. If they do, they can do mod commands here. 
        memberHasModPermission = False
        if member.guild_permissions.moderate_members:
            memberHasModPermission = True

        drawPrintable = False
        if len(messageList) == 1:
            command = "nonPrintable"
        elif messageList[1] == "printable":
            drawPrintable = True
            command = "printable"
        else:
            command = messageList[1]

        match command:

            case "printable" | "nonPrintable":  # Prints a bingo card
                replyContent = CardGen.checkCardPrint(cardsActive)
                if replyContent == "":
                    bingoCardIO, bingoCardFileName = CardGen.genCard(userName, userID, drawPrintable, bingoDate, v)

                    if s.messageChannel:
                        await message.channel.send(file=bingoCardIO)
                        print(bingoCardFileName + " sent to thread.")
                    if s.messageUser:
                        await message.author.send(file=bingoCardIO)
                        print(bingoCardFileName + " sent to user.")
                    replyBool = False

            case "about":  # returns standard about message
                replyContent = "Discord bingoBot version " + s.fileVersion + " \nWritten by Kenny Dave."
            case "?" | "help" | "h":
                """Prints the contents of the helpFile to the thread"""
                replyContent = bFG.helpText(messageList)
            case "status":
                replyContent = bFG.status(bingoDate, v, cardsActive)
            case _:
                pass

        # commands beyond this point are restricted to moderators only, for amending lists etc.
        # currently causes failure for DMs. Need to set it to check the modMin permission for the attached guild.
        if not memberHasModPermission:
            replyContent = s.notModText
        else:
            match command:
                case "toggleactive":  # make card issue active or inactive
                    replyContent, cardsActive = bFG.toggleActive(cardsActive)
                case "date":  # change the selected date.
                    replyContent, bingoDate, v = bFG.date(bingoDate, v, message, messageList)
                case "version":  # change the selected version
                    replyContent, v = bFG.version(bingoDateStr, v, messageList)
                case "list":  # list functions
                    replyContent, replyFile = bFL.listItems(messageList, message, fileByte)
                case "cardlist":  # cardList functions
                    replyContent, replyFile = await bFCL.CardListItems(messageList, bingoDate, bingoDateStr, v, guild)

        if replyBool is True:
            if replyContent != "" or replyFile is not None:
                await message.channel.send(replyContent, file=replyFile)
            else:
                await message.channel.send("Command not recognised. Type \"!bingo ?\" for a list of valid commands")

            # we should have this in a try catch as well I think. That will deal with it not having sufficient members. 
    # except Exception as e:
    # print("Command not recognised. Type \"!bingo ?\" for a list of commands (error)")
    #    await message.channel.send(str(e)+" exception")


client.run(str(TOKEN))
