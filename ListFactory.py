import Settings as s
import TextWrap

bingoList = []


def NewBingoItem(rawText, index):
    # create item
    bingoListItem = BingoItemClass(rawText, index)

    # add to list, unless blank or equal to freeSquare text
    if bingoListItem.rawText != "" and bingoListItem.rawText != s.freeSquareText:
        bingoList.append(bingoListItem)

    return bingoList


class BingoItemClass:
    rawText = ""
    formattedText = ""
    fontSize = 0
    index = 0

    def __init__(self, rawText=rawText, index=index):

        self.rawText = str(rawText).rstrip("\n")  # Read XML for the raw text of each item
        self.index = int(str(index).rstrip("\n"))  # Read XML for the index of each item

        # calculate index if not sent
        if self.index == 0:
            maxIndex = 0
            for item in bingoList:
                if item.index > maxIndex:
                    maxIndex = item.index

            # print(maxIndex)
            self.index = maxIndex + 1

        fontWordResized = TextWrap.longWord(text=self.rawText)
        self.formattedText, self.fontSize = TextWrap.text_box(self.rawText, font=fontWordResized)
