import pathlib
import datetime
#from datetime import date
from datetime import datetime
#from fileinput import filename
datetime.strftime

from PIL import ImageFont#, Image

#@staticmethod
class mySettingsClass:
    """Stores global settings for solution that do not need to change. These will be read at initialisation; if they change, to implement these 
    changes, a restrart is required. 

    Settings include things like appearance, array size, and behaviour such as idempotency of the card requests.
    """
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

    DONE made font local for transfer to VM. Licence?
            
    DONE Write the help file to return.
    DONE Check the input file strip.
    DONE Option for printing the footers

    DONE Delete the picture cards when the date or version changes. 
    
    DONE On off switch for assigning bingo cards. 

    DONE Add in card consistency, which means a list of objects of these. 
    DONE Which also means serialisation.
    DONE Add a flipper option for this. Card sorting disabled when on. CardDB still exists. 

    DONE Add options for viewing or controlling the cardDB from Discord. 
    DONE add helpfile 

    DONE Add printable version
    DONE Add mod controlled add and remove for the bingoList
    DONE Summary of all the learnings in folder, and all the changes required. 
    DONE See what else Brian said and tick them all off. This is in the code-monkeys thread

    DONE Add lower to the message before splitting into messageList. 

    DONE Sort out the DM issue. Need an option for it. One for mods, one for users. 
    DONE It also falls over on the moderator guild permission, because user doesn't have this property. 
    Echo says only one guild for this list.

    DONE Add a status: date, ver, cardList len, bingo list len, 
    Add setup status: arrayX, picture desired size and exists, bingolist len, ?

    DONE Add a reissue command: would need to store more than a string for the userName in cardList. 

    Linting botModule
    Linting CardGenModule
    Linting TextWrap

    You aren't deleting instances of allBingoList and cardList, you're just removing them from the list file. How do I deal with that? Otherwise you're adding to memory until a reset. 
    Might be being collected automatically, need to do some more research or ask Brian. 

    You're wiping the XMLs and rebuilding them every time. That's not very efficient, and doesn't allow exposing the settings in one settings file without writing the whole lot which would also be 
    hard to code.

    The replacelist code is wild, I think you're looping in loops more than you need to perhaps. Inefficient. An absolute shambles at best.

    Add the formatted text to the allBingoList and flip the logic so it's just pulling that rather than calcing every time. Doesn't need to change until a restart and the mySettingsModule variables are pulled.

    Maybe something to tidy userName string. Like removing the special symbols from the Discord name print. Or can you even get it from the discord API? Sounds possible. 
    https://discord.com/developers/docs/reference message formatting section. For emojis.

    check that message length is not >2000 characters. For when you're including user names. Which is on cardList view, and list replace and remove.
    
    Add default header and freesquare image, and get it to cope if the images are missing completely.
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
    #Options:
    
    #Behavior options:
        
    messageChannel = False
    messageUser = True

    saveCards = False #save the generated bingo cards in a folder.
    idempotentCardRequest = True #card requests for a date and version will be consistent. If false a second request will just overwrite in the card DB, the DB will still exist. 

    arrayX =5 #how big the bingo card is.
    freeSquare = True #prints a freesquare in the centreSquare with an image.

    #Visual options:

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
    #this will need to be changed updated for unix. Could potentially just copy required fonts locally and reference there. 
    #It may auto search unix folders with just the name string but that is not clear from a quick google. Failed with fonts in your font folder too, so don't know. 
    #You have put a copy of the font that you've used locally
    parentPathStr = str(pathlib.Path(__file__).parent.resolve())
    elementsPath = parentPathStr+"\\obj\\Fonts\\"
    fontPath=elementsPath+"Lato-Black.ttf" 
    
    #fontAlign = "center" #taken out as it gets complicated with left align, and looks super spiffy center aligned. So it's hard set.
    fontColor = "black"
    
    #Font footer options
    fontFooterSize = 20
    # list of named colors at: https://stackoverflow.com/questions/54165439/what-are-the-exact-color-names-available-in-pils-imagedraw
    # or can make own color with RGB function
    fontFooterColor = "yellow" 
    footerIndent = 10
    footerOpacity = 100


    headerHeight = 200
    borderSize = 50 #round the outside of the boxes. Needs to be something, to leave space for the Username and date at the bottom, if they are enabled. 
    boxSize = 100 #that the bingo items go in
    boxPadding = 6 #this is the space inside the box before the text is printed, boxPadding/2 per side.

    lineWidth = 3
    lineColor = "black"
    boxBackgroundColor = "white"
    boxBackgroundOpacity = 100 # 0 is completely transparent, 255 is solid.

    FSBackgroundColor = "yellow"
    FSBackgroundOpacity = 100 # 0 is completely transparent, 255 is solid.

    fileVersion = "0.0.4A"
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

