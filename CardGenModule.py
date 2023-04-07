#cardGen

import os

import random
import pathlib
from PIL import Image, ImageDraw, ImageFont

import TextWrap
from mySettingsModule import mySettingsClass as s
import AllBingoListFactoryModule as b

class CardGenClass():

    """Generates a bingo card using the settings from mySettingsModule and the username from Discord API. All settings changed in mySettings module"""

    userName="userName defined in CardGenClass" #you need to define it here, otherwise it says not defined. It's overwritten in the constructor.
    drawPrintable="False"

    boxBackground=Image.new("RGB",(1,1))

    def TextGen(self):
        #returns the users generated text list
        #free square options are handled at printing, ignoring the relevant item in this list. 

        bingoList = random.sample(b.allBingoList,s.arrayX**2)

        return bingoList

    def ImageGen(self,bingoList, bingoDate, v):
        #dropping the elements onto the background image, and drawing the lines and text entries.

        bingoDateStr=bingoDate.strftime("%d %b %Y")

        #path to picture elements. 
        parentPathStr = str(pathlib.Path(__file__).parent.resolve())
        elementsPath = parentPathStr+"\\obj\\Picture Elements\\"

        #calculate correct size for background image
        Wcorrect = (s.borderSize*2)+(s.arrayX*s.boxSize)
        Hcorrect = (s.borderSize)+(s.arrayX*s.boxSize)+s.headerHeight
        sizeCorrect=(Wcorrect,Hcorrect)
        
        #background image to draw everything on. Must be the correct size, as determined by marginSize, boxSize, headerHeight. Code will resize as needed
        #but result quality may vary. 
        if self.drawPrintable: #we make a a blank image, white color
            im = Image.new(mode="RGB",size = sizeCorrect,color="white")
            #image=elementsPath+"BlankBackground.png"
        else:
            image = elementsPath+"Background.png"
            im = Image.open(image)

        #im is the background image, which the elements are drawn onto. 
        with im:

            #check background size is correct
            W,H = im.size

            if W == Wcorrect and H == Hcorrect:
                pass
            elif W>=Wcorrect and H>=Hcorrect:
                im = im.crop(0,0,sizeCorrect)
                print("Background image not the correct size for the settings. Cropped. Image should be "+str(sizeCorrect)+".")
            else:
                im = im.resize(sizeCorrect,Image.Resampling.LANCZOS)
                print("Background image too small for the settings. Scaled. Image should be "+str(sizeCorrect)+".")

            draw = ImageDraw.Draw(im)

            #draw title
            titleBoxSize=((s.borderSize*2)+(s.boxSize*s.arrayX),s.headerHeight)    

            #Plain text title
            if self.drawPrintable:
                self.fontColor="black"
                self.fontFooterColor="black"

                titleFont= ImageFont.truetype(self.fontPath,self.titleFontSize)

                draw.text(xy=(titleBoxSize[0]/2,titleBoxSize[1]/2),text=self.titleStr,font=titleFont,anchor="mm", \
                        fill=self.fontColor,align="center")
            
            #picture for title 
            else:
                self.fontColor=s.fontColor
                self.fontFooterColor=s.fontFooterColor

                titleImage =Image.open(elementsPath+"Title.png")

                #check that the Title image is not bigger than the space it's going in. Scale if it is. 
                #This will make it look awful if it isn't the right shape.
                W, H = titleBoxSize #space
                w,h = titleImage.size #pic

                if w > W:
                    titleImage = titleImage.resize((W,int(h*W/w)),Image.Resampling.LANCZOS)
                    print("Title picture too wide. Scaling down. Space is "+str(W)+" * "+str(H))
                    w,h = titleImage.size #recalculate the new h for checking that...
            
                if h > H:
                    titleImage = titleImage.resize((int(w*H/h),H),Image.Resampling.LANCZOS)
                    print("Title picture too tall. Scaling down. Space is "+str(W)+" * "+str(H))
                    w,h = titleImage.size
                
                # Once it fits, draw it in the middle.
                titleDrawPos = (W-w)//2,(H-h)//2 #has to be an integer
                im.paste(titleImage,titleDrawPos,mask=titleImage)

            #draws the semi opaque white box behind the boxes.
            if self.drawPrintable:
                pass
            else:
                #solid color, same size as image. 
                boxBackground = Image.new(mode="RGB", size=im.size,color=s.boxBackgroundColor)

                #mask determines where it is drawn, and how opaque it is. 
                with Image.new(mode="L", size=im.size,color=0) as imMask:
                    drawMask=ImageDraw.Draw(imMask)
                    maskRectangle = s.borderSize, s.headerHeight ,s.borderSize+(s.arrayX*s.boxSize), s.headerHeight+(s.arrayX*s.boxSize)
                    drawMask.rectangle(maskRectangle,fill=s.boxBackgroundOpacity)

                    #remove free square
                    if s.freeSquare == True:
                        maskRectangle = s.borderSize+(s.boxSize*(s.arrayX//2)), s.headerHeight+(s.boxSize*(s.arrayX//2)) \
                            ,s.borderSize+(s.boxSize*(1+s.arrayX//2)), s.headerHeight+(s.boxSize*(1+(s.arrayX//2)))
                        drawMask.rectangle(maskRectangle,fill=0)
                    
                    im.paste(boxBackground,(0,0),imMask)

                #draw freesquare background        
                if s.freeSquare==True:

                    #color
                    FSBackground = Image.new(mode="RGB", size=im.size,color=s.FSBackgroundColor)
                    #position and size
                    FSRectangle = s.borderSize+(s.boxSize*(s.arrayX//2)), s.headerHeight+(s.boxSize*(s.arrayX//2)) \
                        ,s.borderSize+(s.boxSize*(1+s.arrayX//2)), s.headerHeight+(s.boxSize*(1+(s.arrayX//2)))

                    #mask over freesquare
                    with Image.new(mode="L", size=im.size,color=0) as imFSMask:
                        drawMask=ImageDraw.Draw(imFSMask)
                        drawMask.rectangle(FSRectangle,fill=s.FSBackgroundOpacity)
                    
                    #draw
                    im.paste(FSBackground,(0,0),imFSMask)

                    #open the freesquare image
                    FSImage =Image.open(elementsPath+"FreeSquare.png")

                    #check that the FS image is 100*100, scale if not. This will make it look awful if it isn't at least square. 
                    size = s.boxSize,s.boxSize
                    width,height = FSImage.size
                    if width !=s.boxSize or height !=s.boxSize:
                        FSImage = FSImage.resize(size,Image.Resampling.LANCZOS)
                        print("Resizing freesquare image; should be "+str(s.boxSize[0])+" * "+str(s.boxSize[1])+".")

                    #draw
                    im.paste(FSImage,FSRectangle, mask=FSImage)

            #box lines
            for i in range(s.arrayX+1):

                #vertical
                line= [s.borderSize+(i*s.boxSize), s.headerHeight, \
                    s.borderSize+(i*s.boxSize), s.headerHeight+(s.arrayX*s.boxSize)]
                draw.line(line, fill=s.lineColor, width=s.lineWidth)
                #horizontal
                line= [s.borderSize, s.headerHeight+(i*s.boxSize), \
                    s.borderSize+(s.arrayX*s.boxSize), s.headerHeight+(i*s.boxSize)]
                draw.line(line, fill=s.lineColor, width=s.lineWidth)

            #bingo elements text
            for i in range(s.arrayX): #x boxes across
                for j in range(s.arrayX): #y boxes down

                    #selecting the correct text from the list
                    self.text=bingoList[(i*s.arrayX)+j].rawText
                    
                    #set the text to "free" if it's the freeSquare element
                    if s.freeSquare==True and (i*s.arrayX)+j==s.freeSquareElement:
                        self.text = s.freeSquareText

                    #don't print text if the word is "Free" unless it's the printable version of the card
                    if self.text == s.freeSquareText and self.drawPrintable==False: continue 

                    #reduce the text to fit, based on longest word then the string
                    self.fontWordResized = TextWrap.longWord(text=self.text)
                    textPrint, s.fontText = TextWrap.text_box(text=self.text,font=self.fontWordResized)
                    
                    # draw the text on the image, now you've calculated the wrapped string and font size. 

                    #centre of each box
                    textPrintPos = (s.borderSize+((i+0.5)*s.boxSize),s.headerHeight+((j+0.5)*s.boxSize))
                    #draw. mm puts the anchor in the center, align centers the image around the anchor
                    draw.text(xy=textPrintPos,text=textPrint,font=s.fontText,anchor="mm", \
                        fill=self.fontColor,align="center")

            #print name, date, version
            #name position
            namePrintPos=(s.borderSize+s.footerIndent,s.headerHeight+(s.arrayX*s.boxSize)+int((0.5*s.borderSize)))
            
            #Date and version position
            dateVer=""
            dateVerPos=(s.borderSize+((s.arrayX*s.boxSize))-s.footerIndent, \
                s.headerHeight+(s.arrayX*s.boxSize)+int((0.5*s.borderSize)))

            if s.drawDate == True:
                dateVer = bingoDateStr
            if s.drawVersion == True:
                dateVer = dateVer +" v"+str(v)
            
            #solid color
            boxBackground = Image.new(mode="RGB", size=im.size,color=self.fontFooterColor)

            #mask determines where the solid color is drawn, which is just the text, and how opaque it is from settings. 
            with Image.new(mode="L", size=im.size,color=0) as imMask:
                drawMask=ImageDraw.Draw(imMask)
                
                #mask name
                if s.drawName == True:
                    drawMask.text(xy=namePrintPos,text=self.userName,font=s.fontFooter,anchor="lm", \
                    fill=s.footerOpacity,align="left")
                
                #mask date and version
                drawMask.text(xy=dateVerPos,text=dateVer,font=s.fontFooter,anchor="rm", \
                fill=s.footerOpacity,align="right")
                    
                im.paste(boxBackground,(0,0),imMask)#prints only where the text is. 

            # write card to file; create folder if it doesn't exist. 
            if s.saveCards == True:
                saveFolder = parentPathStr+"\\obj\\Cards\\"+bingoDateStr+" v"+str(v)+"\\"
                checkFolder= os.path.isdir(saveFolder)

                if not checkFolder:
                    os.makedirs(saveFolder)

                saveStr = saveFolder+str(self.userName)+".png"
                im.save(saveStr, "PNG")

            bingoCardFileName = " ".join(["Bingo Card",self.userName,dateVer,])+".png"

            #return the imagefile to the initializer
            return im, bingoCardFileName

    def __init__(self,userName = userName, drawPrintable = drawPrintable):

        self.userName = userName
        self.drawPrintable = drawPrintable







