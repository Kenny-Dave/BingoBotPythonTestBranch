# cardGen
import os
from PIL import Image, ImageDraw, ImageFont

import Settings as s

"""Generates a bingo card template using the settings from mySettingsModule. 
All settings changed in mySettings module"""

# you need to define it here, otherwise it says not defined. It's overwritten in the constructor.

# calculate correct size for title background image or generated text
wCorrect = (s.borderSize * 2) + (s.arrayX * s.boxSize)
hCorrect = s.borderSize + (s.arrayX * s.boxSize) + s.headerHeight
sizeCorrect = (wCorrect, hCorrect)


def TemplateGen():
    """ dropping the common elements onto the non-printable card."""

    # path to picture elements.
    elementsPath = os.path.join(os.path.curdir, "obj", "Picture Elements")

    # background image to draw everything on. Must be the correct size, as determined by marginSize,
    # boxSize, headerHeight. Code will resize as needed but result quality may vary.

    image = os.path.join(elementsPath, "Background.png")
    im = Image.open(image)

    # im is the background image, which the elements are drawn onto.
    with im:

        # check background size is correct
        W, H = im.size

        if W == wCorrect and H == hCorrect:
            pass
        elif W >= wCorrect and H >= hCorrect:
            im = im.crop((0, 0, wCorrect, hCorrect))
            print("Background image not the correct size for the settings. Cropped. Image should be " + str(
                sizeCorrect) + ".")
        else:
            im = im.resize(sizeCorrect, Image.LANCZOS)
            print("Background image too small for the settings. Scaled. Image should be " + str(sizeCorrect) + ".")

        draw = ImageDraw.Draw(im)

        # draw title
        titleBoxSize = ((s.borderSize * 2) + (s.boxSize * s.arrayX), s.headerHeight)

        # picture for title
        titleImage = Image.open(os.path.join(elementsPath, "Title.png"))

        # check that the Title image is not bigger than the space it's going in. Scale if it is.
        # This will make it look awful if it isn't the right shape.
        W, H = titleBoxSize  # space
        w, h = titleImage.size  # pic

        if w > W:
            titleImage = titleImage.resize((W, int(h * W / w)), Image.LANCZOS)
            print("Title picture too wide. Scaling down. Space is " + str(W) + " * " + str(H))
            w, h = titleImage.size  # recalculate the new h for checking that...

        if h > H:
            titleImage = titleImage.resize((int(w * H / h), H), Image.LANCZOS)
            print("Title picture too tall. Scaling down. Space is " + str(W) + " * " + str(H))
            w, h = titleImage.size

        # Once it fits, draw it in the middle.
        titleDrawPos = (W - w) // 2, (H - h) // 2  # has to be an integer
        im.paste(titleImage, titleDrawPos, mask=titleImage)

        # draws the semi opaque white box behind the boxes.

        # solid color, same size as image.
        boxBackground = Image.new(mode="RGB", size=im.size, color=s.boxBackgroundColor)

        FSRectangle = s.borderSize + (s.boxSize * (s.arrayX // 2)), \
            s.headerHeight + (s.boxSize * (s.arrayX // 2)), \
            s.borderSize + (s.boxSize * (1 + s.arrayX // 2)), \
            s.headerHeight + (s.boxSize * (1 + (s.arrayX // 2)))

        # mask determines where it is drawn, and how opaque it is.
        with Image.new(mode="L", size=im.size, color=0) as imMask:
            drawMask = ImageDraw.Draw(imMask)
            maskRectangle = s.borderSize, s.headerHeight, s.borderSize + (
                    s.arrayX * s.boxSize), s.headerHeight + (s.arrayX * s.boxSize)
            drawMask.rectangle(maskRectangle, fill=s.boxBackgroundOpacity)

            # remove free square from mask
            if s.freeSquare:
                drawMask.rectangle(FSRectangle, fill=0)

            im.paste(boxBackground, (0, 0), imMask)

        # draw freeSquare background
        if s.freeSquare:

            # color
            FSBackground = Image.new(mode="RGB", size=im.size, color=s.FSBackgroundColor)
            # position and size

            # mask over freeSquare
            with Image.new(mode="L", size=im.size, color=0) as imFSMask:
                drawMask = ImageDraw.Draw(imFSMask)
                drawMask.rectangle(FSRectangle, fill=s.FSBackgroundOpacity)

            # paste masked color
            im.paste(FSBackground, (0, 0), imFSMask)

            # open the freeSquare image
            FSImage = Image.open(os.path.join(elementsPath, "FreeSquare.png"))

            # check that the FS image is right size for a box, scale if not.
            # This will make it look awful if it isn't at least square.
            size = s.boxSize, s.boxSize
            width, height = FSImage.size
            if width != s.boxSize or height != s.boxSize:
                FSImage = FSImage.resize(size, Image.LANCZOS)
                print("Resizing freeSquare image; should be " + str(s.boxSize[0]) + " * " + str(
                    s.boxSize[1]) + ".")

            # draw
            im.paste(FSImage, FSRectangle, mask=FSImage)

        # lines
        BoxLines(draw, printable=False)
        # save
        imSave(im, fileName="Template")


def TemplatePrintableGen():
    """ dropping the common elements onto the printable card."""

    # background image to draw everything on. Must be the correct size, as determined by marginSize,
    # boxSize, headerHeight. Code will resize as needed but result quality may vary.
    # im is the background image, which the elements are drawn onto.
    im = Image.new(mode="RGB", size=sizeCorrect, color="white")
    draw = ImageDraw.Draw(im)

    with im:
        # Plain text title
        titleBoxSize = ((s.borderSize * 2) + (s.boxSize * s.arrayX), s.headerHeight)

        try:
            titleFont = ImageFont.truetype(s.fontPath, s.titleFontSize)
        except:
            titleFont = ImageFont.load_default()

        draw.text(xy=(titleBoxSize[0] / 2, titleBoxSize[1] / 2), text=s.titleStr, font=titleFont, anchor="mm",
                  fill="black", align="center")
        # lines
        BoxLines(draw, printable=True)
        # save
        imSave(im, fileName="TemplatePrintable")


def imSave(im, fileName):
    # write card to file; create folder if it doesn't exist.
    saveFolder = os.path.join(os.path.curdir, "obj", "GeneratedBackGrounds")
    checkFolder = os.path.isdir(saveFolder)
    if not checkFolder:
        os.makedirs(saveFolder)
    saveStr = os.path.join(saveFolder, fileName + ".png")
    im.save(saveStr, "PNG")


def BoxLines(draw, printable):
    # drawing box lines

    if printable:
        lineColor = "black"
    else:
        lineColor = s.lineColor

    for i in range(s.arrayX + 1):
        # vertical
        line = [s.borderSize + (i * s.boxSize), s.headerHeight,
                s.borderSize + (i * s.boxSize), s.headerHeight + (s.arrayX * s.boxSize)]
        draw.line(line, fill=lineColor, width=s.lineWidth)
        # horizontal
        line = [s.borderSize, s.headerHeight + (i * s.boxSize),
                s.borderSize + (s.arrayX * s.boxSize), s.headerHeight + (i * s.boxSize)]
        draw.line(line, fill=lineColor, width=s.lineWidth)


TemplateGen()
TemplatePrintableGen()
