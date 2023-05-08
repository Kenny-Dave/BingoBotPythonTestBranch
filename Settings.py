import os
import pathlib

from PIL import ImageFont  # , Image
"""Stores global settings for solution that do not need to change. These will be read at initialisation; if they
change, to implement these changes, a restart is required.

Settings include things like appearance, array size, and behaviour such as idempotency of the card requests."""

"""
TD: 
DONE freeSquare text print
DONE date and version
DONE Name
DONE options for the above two things
DONE Link it up
DONE Change the title, the font is in the folder and the source file 
DONE Check dodgy sizes with error messages
DONE ish, as best as you can. Unpickle the mess.

DONE Need to add serialisation for all the menu options. You've got a funct for it so just a reference at the 
    bottom of each. 
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

DONE made font local for transfer to VM. Licence? Chose a ubuntu default. Check though...
        
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
DONE Add a reissue command: would need to store more than a string for the userName in cardList. 

DONE Card changed flag on cardlist is not picking up correctly when it's amended on load from XML. Investigate.
DONE Or not saving the flag to XML more likely.  

DONE NOT Discord uses Twemoji for it's unicode emojis, but overwrites these with images at times. So in short, 
    you are going to struggle to get these image emojis in as pilmoji is not able to do this using the unicode code.


DONE Change the userName to be the connected guild nick.

DONE Linting botModule https://stackify.com/dependency-injection/
DONE Linting CardGenModule
DONE Linting TextWrap

DONE Add the formatted text to the allBingoList and flip the logic so it's just pulling that rather than calculating 
    every time. Doesn't need to change until a restart and the mySettingsModule variables are pulled.

DONE Maybe something to tidy userName string. Like removing the special symbols from the Discord name print. Or can 
    you even get it from the discord API? Sounds possible. https://discord.com/developers/docs/reference message 
    formatting section. For emojis.

DONE for the platform independent file paths: 
    https://stackoverflow.com/questions/6036129/platform-independent-file-paths

NTH: Add setup status: arrayX, picture desired size and exists, bingolist len, ?

DONE Change the card exists check to the userID. Otherwise it causes problems when a user changes their name.
    Fixed: cast to int.

You aren't deleting instances of allBingoList and cardList, you're just removing them from the list file. How do 
I deal with that? Otherwise you're adding to memory until a reset. Might be being collected automatically, 
need to do some more research or ask Brian. Think it does it automatically. 

You're wiping the XMLs and rebuilding them every time. That's not very efficient, and doesn't allow exposing the 
settings in one settings file without writing the whole lot which would also be hard to code.

DONE The replaceList code is wild, I think you're looping in loops more than you need to perhaps. Inefficient. An 
    absolute shambles at best.
DONE Can merge with addlist too. Have a variable.

Check that message length is not >2000 characters. For when you're including user names. Which is on cardList 
view, and list replace and remove.

Add default header and freeSquare image, and get it to cope if the images are missing completely.
Check all the logic if the image sizes are wrong. They did work, but you might have broken them in tidying up.

API:            https://discordpy.readthedocs.io/en/stable/ext/commands/api.html
permissions:     https://discordpy.readthedocs.io/en/stable/api.html#discord.Permissions

Discord valid image formats:

    Image Formats
    Name	Extension
    JPEG	.jpg, .jpeg
    PNG	.png
    WebP	.webp
    GIF	.gif
    Lottie	.json

python pillow color chart: 
https://stackoverflow.com/questions/54165439/what-are-the-exact-color-names-available-in-pils-imagedraw
but can also use RGB values, or color code.   
"""

# dependencies:
'''
It's a default in ubuntu. Might need to add the path though. Might not be standard in the VM...
fonts - lato_2.0 - 2.1_all.deb
    font folder added to PATH if not automatically done: PATH=$PATH:~/usr/share/fonts/

'''

# Options:

# Behavior options:

messageChannel = False
messageUser = True

saveCards = True  # save the generated bingo cards in a folder.
idempotentCardRequest = True  # card requests for a date and version will be consistent. If false a second
# request will just overwrite in the card DB, the DB will still exist.

arrayX = 5  # how big the bingo card is.
freeSquare = True  # prints a freeSquare in the centreSquare with an image.

# Visual options:

titleStr = "Echo Ridge Gaming\nBingo"
titleFontSize = 50  # this and the above is used for the printable version, and as a fallback if there is no

drawName = True  # items at the bottom of the card, print or no.
drawDate = True
drawVersion = True
# drawPrintable = False #if this is true it prints a simple version without the pictures and stuff.

# Font options

fontSize = 50  # for the bingo items. This is the max font size, the code will reduce this to fit the box.

currDirPrint = str(pathlib.Path(__file__).parent.resolve())  # printing in the startup message

parentPathStr = os.path.curdir

# this requires any non-standard fonts to be added to the VM, and possibly adding to PATH, as listed in
# dependencies. There is also an over-ride for arial, a standard windows font if it's running on that.
fontPath = "Lato-Black.ttf"

fontColor = "black"  # just the element text

# Font footer options
fontFooterSize = 20
# list of named colors at:
# https://stackoverflow.com/questions/54165439/what-are-the-exact-color-names-available-in-pils-imagedraw
# or can make own color with RGB function
fontFooterColor = "grey"
footerIndent = 10
footerOpacity = 100
footerEmojiOffset = (0, -3)

headerHeight = 200
borderSize = 50  # round the outside of the boxes. Needs to be something, to leave space for the Username and
# date at the bottom, if they are enabled.
boxSize = 100  # that the bingo items go in
boxPadding = 6  # this is the space inside the box before the text is printed, boxPadding/2 per side.

lineWidth = 3
lineColor = "black"
boxBackgroundColor = "white"
boxBackgroundOpacity = 100  # 0 is completely transparent, 255 is solid.

FSBackgroundColor = "yellow"
FSBackgroundOpacity = 100  # 0 is completely transparent, 255 is solid.

fileVersion = "0.0.6A"
freeSquareText = "Free"

notModText = "Only moderators have permission to access mod commands, and you do not seem to."

"""
images used in generation can be changed by changing the images in ./obj/Picture Elements/. 
They are: background.png, freeSquare.png, Title.png. 

Background should be 600*750 with the default settings, but changes depending on boxSize, headerHeight, 
borderSize, arrayX. freeSquare should be 100*100 default, depending on boxSize. Title should be 600*200 default, 
depending on boxSize, headerHeight, and arrayX.

All will work with the wrong size, as it will adjust the images appropriately. But it won't look so good. 
"""

# Calculated:

if arrayX // 2 == arrayX / 2:
    freeSquare = False  # no freeSquare unless there is a centreSquare. Could put it as random, maybe.
else:
    freeSquareElement = arrayX ** 2 // 2  # element for list

try:
    font = ImageFont.truetype(font=fontPath, size=fontSize)
except:
    fontPath = "arial.ttf"
    font = ImageFont.truetype(font=fontPath, size=fontSize)
    print("Font path: ", fontPath)
fontFooter = ImageFont.truetype(font=fontPath, size=fontFooterSize)
