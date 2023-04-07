import datetime
from datetime import date
from datetime import datetime
from fileinput import filename
datetime.strftime

from PIL import ImageFont, Image

#@staticmethod
class mySettingsClass:
    """Stores global settings for solution that do not need to change."""


    """
    TD: 
    DONE freesquare text print
    DONE date and version
    DONE Name
    DONE options for the above two things
    DONE Link it up
    DONE Change the title, the font is in the folder and the source file 
    DONE Check dodgy sizes with error messages
    DONE ish, as best as you can. Unpickle the mess.

    DONE Need to add serialisation for all the menu options. You've got a funct for it so just a reference at the bottom of each. 
    DONE serialise date and version

    DONE if the bingo list is blank it chucks a silent error at present. Silent in discord anyway. 
    DONE check enough bingo list items for array.

    DONE Deduping the list for add and replace. 
    DONE Add an index reset and sort for changing the date and version.
    DONE And a reset index option. Or even just reset if date and version are not enabled.
    DONE ***Get add and replace on an attachment. ***

    DONE Format inputs to remove the 
            leading number.
            <
            "Free"
            What else? 

    DONE Write the help file to return.
    DONE Check the input file strip.
    DONE Option for printing the footers
    
    On off switch for assigning bingo cards. 

    sort out the DM issue. Need an option for it. 
    It also falls over on the moderator guild permission, because user doesn't have this property. Could either do something clever, or not.
    Echo says only one guild for this list.

    Add in card consistency, which means a list of objects of these. 
    Which also means serialisation.

    Add the formatted text to the allBingoList and flip the logic so it's just pulling that rather than calcing every time. 

    Maybe something to tidy userName string. Like removing the special symbols from the Discord name print. Or can you even get it from the discord API? Sounds possible. 
    https://discord.com/developers/docs/reference message formatting section. For emojis.

    Add default header and freesquare image, and get it to cope if the images are missing completely.
    DONE Add printable version
    DONE Add mod controlled add and remove for the bingoList
    https://stackoverflow.com/questions/71174697/discord-js-v13-how-to-prevent-mod-commands-from-working-on-mods
    the above is for js mind. 

    Check all the logic if the imagesizes are wrong. They did work, but you might have broken them in tidying up.

    API:            https://discordpy.readthedocs.io/en/stable/ext/commands/api.html
    permissons:     https://discordpy.readthedocs.io/en/stable/api.html#discord.Permissions

    Discord valid imageformats:

        Image Formats
        Name	Extension
        JPEG	.jpg, .jpeg
        PNG	.png
        WebP	.webp
        GIF	.gif
        Lottie	.json

    """

    arrayX =5 #how big the bingo card is.
    freeSquare = True #prints a freesquare in the centreSquare with an image.

    titleStr = "Echo Ridge Gaming\nBingo"
    titleFontSize = 50 #this and the above is used for the printable version, and as a fall back if there is no title image found. 
    #bingoDate = datetime(2023,3,29)
    #v =1 #version for the date of bingoDate

    drawName = True #items at the bottom of the card, print or no.
    drawDate = True
    drawVersion = True
    #drawPrintable = False #if this is true it prints a simple version without the pictures and stuff. 

    #Font options
    
    fontSize = 50 # for the bingo items. This is the max font size, the code will reduce this to fit the box.
    
    #this doesn't like just the name, it's supposed to look in the system folder determined by path but it appears to be busto.
    #Adding to path in windows: https://stackoverflow.com/questions/49966547/pip-10-0-1-warning-consider-adding-this-directory-to-path-or
    #this will need to be changed updated for unix. Can just copy required fonts locally and reference there. 
    #It may auto search unix folders with just the name string but that is not clear from a quick google. Failed with fonts in your font folder too, so don't know. 
    fontPath="C:\\Users\\Name\\AppData\\Local\\Microsoft\\Windows\\Fonts\\Lato-Black.ttf" 
    
    #fontAlign = "center" #taken out as it gets complicated with left align, and looks super spiffy center aligned. 
    fontColor = "black"
    
    #Font footer options
    fontFooterSize = 20
    # list of named colors at: https://stackoverflow.com/questions/54165439/what-are-the-exact-color-names-available-in-pils-imagedraw
    # or can make own color with RGB function
    fontFooterColor = "yellow" 
    footerIndent = 10
    footerOpacity = 100

    persistentCard = True #not currently functional. Need list and serialisation. 

    messageChannel = False
    messageUser = True

    saveCards = False #save the generated bingo cards in a folder. 

    headerHeight = 200
    borderSize = 50
    boxSize = 100
    boxPadding = 6 #this is the space inside the box before the text is printed, boxPadding/2 per side.

    lineWidth = 3
    lineColor = "black"
    boxBackgroundColor = "white"
    boxBackgroundOpacity = 100 # 0 is completely transparent, 255 is solid.

    FSBackgroundColor = "yellow"
    FSBackgroundOpacity = 100 # 0 is completely transparent, 255 is solid.

    fileVersion = "0.1A"
    freeSquareText="Free"

    """
    images used in generation can be changed by changing the images in .\\obj\\Picture Elements\\. 
    They are: background.png, freesquare.png, Title.png. 

    Background should be 600*750 with the default settings, but changes depending on boxsize, headerheight, bordersize, arrayX.
    freesquare should be 100*100 default, depending on boxsize. 
    Title should be 600*200 default, depending on boxsize, headersheight, and arrayX.

    All will work with the wrong size, as it will adjust the images appropriately. But it won't look so good. 
    """

    #Calculated:

    #bingoDateStr = bingoDate.strftime("%d %b %Y")

    

    if arrayX//2 == arrayX/2: 
        freeSquare = False # no freesquare unless there is a centreSquare. Could put it as random maybe. 
    else:
        freeSquareElement = arrayX**2//2 #element for list

    font = ImageFont.truetype(font=fontPath, size=fontSize) 
    fontFooter = ImageFont.truetype(font=fontPath, size=fontFooterSize) 

