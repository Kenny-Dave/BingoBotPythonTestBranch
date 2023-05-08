import ListFactory as b


def selBingItem(selIndex):
    """This selects the item in allBingo list based on the text given it. Used when replacing text. """
    selItem = None
    for sel in b.bingoList:
        if sel.index == selIndex:
            selItem = sel
            return selItem

    return selItem


def clean(rawText):
    """this cleans the input string, or lines if it's an input file"""

    # removing or changing characters that will confuse XML.
    rawTextClean = ""
    for char in rawText:
        if char == "<":
            charClean = "["
        elif char == ">":
            charClean = "]"
        elif char == "\"":
            charClean = ""
        elif char == "\'":
            charClean = ""
        else:
            charClean = char
        rawTextClean += charClean
    rawText = rawTextClean

    # Text "Free" needs to be reserved as there is logic attached to it for the freeSquare. It won't print when
    # appropriate, we don't want it in the list.
    if rawText == "Free":
        rawText = "Free square"

    rawSplit = rawText.split(".")
    # remove the leading number and dot, which could be there if it's a list from generated data.
    if len(rawSplit) > 1:
        if rawSplit[0].isdigit:
            rawText = rawText.lstrip(rawSplit[0] + ". ")

    return rawText
