from PIL import Image, ImageDraw, ImageFont
from mySettingsModule import mySettingsClass as s

#s = mySettingsClass

#make a test box the same size as the boxes on the finished bingo card.
boxImTestBox = (0,0,s.boxSize-s.boxPadding,s.boxSize-s.boxPadding)
boxImTest = Image.new("RGB",(s.boxSize-s.boxPadding,s.boxSize-s.boxPadding))
boxImTestW= boxImTest.size[0]
boxImTestH= boxImTest.size[1] #doesn't need to be calculated as done within TextWrap.textBox
image_draw = ImageDraw.Draw(im=boxImTest)

#reduce the size of the text based on the word; we need the longest word to fit in the box. 
#it goes through the words and keeps reducing the size for each word until the word fits in the box. 
def longWord(text):

    #take the starting font and fontsize
    fontWordResized = ImageFont.truetype(s.fontPath,s.font.size)

    for word in text.split():

        w = fontWordResized.getsize(word)[0]

        #reduce fontsize until word fits                        
        while w>boxImTestW:
                    
            fontWordResized =ImageFont.truetype(s.fontPath,fontWordResized.size-1)
            w = fontWordResized.getsize(word)[0]
            if fontWordResized.size <=6: break

    return fontWordResized

#reduce the size of the text based on the height of the string. 
#takes the text and fontsize from longword, and reduces the text size further so that the string will fit in the box, top to bottom and left to right. 
#Returns the input string with carriage returns added, and the font. These two to make it fit. 
#If the bingo item is too long, it will spill over the box at the smallest font size, which is 6.
def text_box(text, font, **kwargs):

    #until it fits, or hits font.size==6
    while font.size>5: # this should never not be true, as it returns when it gets down to 6.
        lines = text.split('\n') #a line split in the source forces a line split in the output
        
        true_lines = ""
        w, h = [0,0]
        
        for line in lines:

            if font.getsize(line)[0] <= boxImTestW:
                true_lines =line
            else:
                current_line = ""
                for word in line.split(" "):
                    
                    if font.getsize(current_line + word)[0] <= boxImTestW: #if the next word fits on the line
                        if current_line!="":current_line += " " + word #if there's already a word on the line
                        else:current_line = word #for the first word on the line
                    else: 
                        if true_lines =="": true_lines=current_line #for the first line
                        else: true_lines=true_lines+"\n"+current_line #adds subsequent lines
                        current_line = word #putting the current word on the next line

                if true_lines =="": true_lines=current_line #writing the first line to true_lines
                else: true_lines=true_lines+"\n"+current_line #writing subsequent lines to true lines

        w,h = image_draw.textsize(true_lines,font)

        if (w<=boxImTestW and h<=boxImTestH) or font.size==6: #if it fits, or you're down to font size 6, return true lines and the font
            return (true_lines, font)

        else:
            font =ImageFont.truetype(s.fontPath,font.size-1) #else try again with a smaller font. 
