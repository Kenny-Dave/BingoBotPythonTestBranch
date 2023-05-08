# cardGen
import os
import io
import discord
import random
from PIL import Image, ImageDraw
from pilmoji import Pilmoji

import Settings as s
import ListFactory as b
import CardListFactory as c

import XMLCardList


def checkCardPrint(cardsActive):
    replyContent = ""
    if not cardsActive:
        replyContent = "Bingo card issue is not presently active. Please speak to a mod if you require " \
                       "further information, read up the thread, or wait patiently :)"
    elif s.arrayX ** 2 > len(b.bingoList):
        replyContent = "There are not enough items in the bingo list to generate a card. Add more options or " \
                       "reduce the size of the card. " + str(len(b.bingoList)) + " items, card settings is " \
                       + str(s.arrayX) + " squared."

    return replyContent


def genCard(userName, userID, drawPrintable, bingoDate, v):
    """Generates a bingo card"""

    bingoItemList = []
    addCardToList = True

    if s.idempotentCardRequest:
        # check if the card already exists in the db and pick up the bingoList if so
        for ec in c.bingoCardList:
            if ec.userID == userID:
                bingoItemList = ec.bingoItemList
                addCardToList = False

                # change the card changed flag to false, as it's getting resent to user.
                ec.cardChanged = False
                ec.drawPrintable = drawPrintable
                break

    if not s.idempotentCardRequest:
        # remove the existing card for the user, before building a new one.
        for ec in c.bingoCardList:
            if ec.userName == userName:
                c.bingoCardList.remove(ec)
                break

    # if new request, generate bingoList
    if len(bingoItemList) == 0:
        bingoItemList = TextGen()
    # generate graphics
    bingoCard, bingoCardFileName = ImageGen(userName, bingoItemList, bingoDate, v, drawPrintable)

    # construct file reference for sending to user
    arr = io.BytesIO()
    bingoCard.save(arr, format='png', quality="keep")
    arr.seek(0)
    bingoCardIO = discord.File(fp=arr, filename=bingoCardFileName)

    # add card to list if a new request
    # print ("Add cards to list: "+str(addCardToList))
    if addCardToList:
        c.NewBingoCard(userName=userName, userID=userID, cardChanged=False,
                       bingoItemList=bingoItemList, drawPrintable=drawPrintable)
    XMLCardList.writeList()

    return bingoCardIO, bingoCardFileName


def TextGen():
    # returns the users generated text list
    # free square options are handled at printing, ignoring the relevant item in this list.

    bingoList = random.sample(b.bingoList, s.arrayX ** 2)

    return bingoList


def ImageGen(userName, bingoList, bingoDate, v, drawPrintable):
    # dropping the elements onto the background image, and drawing the lines and text entries.

    bingoDateStr = bingoDate.strftime("%d %b %y")
    backgroundPath = os.path.join(os.path.curdir, "obj", "GeneratedBackGrounds")

    # opening correct template
    if drawPrintable:
        im = Image.open(os.path.join(backgroundPath, "TemplatePrintable.png"))
        fontColor = "black"
    else:
        im = Image.open(os.path.join(backgroundPath, "Template.png"))
        fontColor = s.fontColor

    with im:

        draw = ImageDraw.Draw(im)

        # bingo elements text
        for i in range(s.arrayX):  # x boxes across
            for j in range(s.arrayX):  # y boxes down

                bingoListItem = bingoList[(i * s.arrayX) + j]
                # selecting the correct text from the list
                text = bingoListItem.rawText

                # set the text to "free" if it's the freeSquare element
                if s.freeSquare and (i * s.arrayX) + j == s.freeSquareElement:
                    text = s.freeSquareText

                # don't print text if the word is "Free" unless it's the printable version of the card
                if text == s.freeSquareText and not drawPrintable:
                    continue

                # reduce the text to fit, based on longest word then the string
                # fontWordResized = TextWrap.longWord(text=text)
                # textPrint, fontText = TextWrap.text_box(text=text, font=fontWordResized)
                textPrint, fontText = bingoListItem.formattedText, bingoListItem.fontSize

                # draw the text on the image, now you've calculated the wrapped string and font size.

                # centre of each box
                textPrintPos = (s.borderSize + ((i + 0.5) * s.boxSize), s.headerHeight + ((j + 0.5) * s.boxSize))
                # mm puts the anchor in the center, align centers the image around the anchor
                draw.text(xy=textPrintPos, text=textPrint, font=fontText, anchor="mm",
                          fill=fontColor, align="center")

        # print name, date, version
        # name position
        # height of text, as the anchor has to be at the top with pilmoji so can't use the center anchor.
        h = s.fontFooter.getsize("ABC")[1]
        # print("Height of footer text", str(h))
        namePrintPos = (s.borderSize + s.footerIndent,
                        s.headerHeight + (s.arrayX * s.boxSize) + int(0.5 * (s.borderSize - h)))

        # Date and version position
        dateVer = ""
        dateVerPos = (s.borderSize + (s.arrayX * s.boxSize) - s.footerIndent,
                      s.headerHeight + (s.arrayX * s.boxSize) + int(0.5 * (s.borderSize - h)))

        if s.drawDate:
            dateVer = bingoDateStr
        if s.drawVersion:
            dateVer = dateVer + " v" + str(v)

        if s.drawName:
            Pilmoji(im).text(xy=namePrintPos, text=userName, font=s.fontFooter, anchor="lt",
                             fill=s.fontFooterColor, align="left", emoji_position_offset=s.footerEmojiOffset)

        # date and version
        # no if check as it's blank if the elements aren't enabled.
        draw.text(xy=dateVerPos, text=dateVer, font=s.fontFooter, anchor="rt",
                  fill=s.fontFooterColor, align="right")

        # write card to file; create folder if it doesn't exist.
        if s.saveCards:
            saveFolder = os.path.join(os.path.curdir, "obj", "Cards", bingoDateStr, " v", str(v))
            checkFolder = os.path.isdir(saveFolder)

            if not checkFolder:
                os.makedirs(saveFolder)

            saveStr = os.path.join(saveFolder, str(userName) + ".png")
            im.save(saveStr, "PNG")

        bingoCardFileName = " ".join(["Bingo Card", userName, dateVer, ]) + ".png"

        # return the imageFile to the initializer
        return im, bingoCardFileName
