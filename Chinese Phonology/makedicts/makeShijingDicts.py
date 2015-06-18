# -*- coding: utf-8 -*-
import codecs, pickle, utilities

lineToCodepoints = utilities.lineToCodepoints
pp = utilities.pp

# Get codepoints to glyphs
f=codecs.open("..\\dicts\\codepointToGlyphDict.py","rb")
codepointToGlyphDict = pickle.load(f)
f.close()

# Get the text of Shijing.
f=codecs.open("..\\sources\\shijingtext.txt","r")
lines = []
for line in f:
    line = line[:-1] # End of line character.
    lines.append(line)
f.close()
lines[0] = lines[0][3:] # Start of file character.
shijingLines = lines

shijingDict = {}
shijingLineDict = {}
shijingStanzaDict = {}
shijingOdeDict = {}
shijingBookDict = {}
shijingPartDict = {}
shijingCodepointCtr = 0
shijingLineCtr = 0
shijingStanzaCtr = -1 # -1 because we increment at the start of a stanza/ode/book/part
shijingOdeCtr = -1    # and we want to start the numbering at 0
shijingBookCtr = -1
shijingPartCtr = -1
newShijingLines = []
for shijingLine in shijingLines:
    if shijingLine != '':        # Ignore blank lines.
        shijingLine = shijingLine.split("\t")
        # Part, Book, Ode, Stanza in that order to generate
        # foreign keys: the dictionaries also hold the titles of
        # the odes, books and parts. Since we read the lines
        # in as a bytestream we have to convert titles to 
        # codepoints and then back to glyphs.
        # Part
        partTitle = shijingLine[0]
        if partTitle != '':
            shijingPartCtr += 1
            partTitleCodepoints = lineToCodepoints(partTitle)
            partTitle = u""
            for codepoint in partTitleCodepoints:
                partTitle += codepointToGlyphDict[codepoint]
            shijingPartDict[shijingPartCtr] = partTitle
        # Book
        bookTitle = shijingLine[1]
        if bookTitle != '':
            shijingBookCtr += 1
            bookTitleCodepoints = lineToCodepoints(bookTitle)
            bookTitle = u""
            for codepoint in bookTitleCodepoints:
                bookTitle += codepointToGlyphDict[codepoint]
            shijingBookDict[shijingBookCtr] = {}
            shijingBookDict[shijingBookCtr]["title"] = bookTitle
            shijingBookDict[shijingBookCtr]["number"] = shijingBookCtr + 1
            shijingBookDict[shijingBookCtr]["part"] = shijingPartCtr
        # Ode
        odeTitle = shijingLine[2]
        odeNumber = shijingLine[3]
        if odeTitle != '':
            shijingOdeCtr += 1
            odeTitleCodepoints = lineToCodepoints(odeTitle)
            odeTitle = u""
            for codepoint in odeTitleCodepoints:
                odeTitle += codepointToGlyphDict[codepoint]
            shijingOdeDict[shijingOdeCtr] = {}
            shijingOdeDict[shijingOdeCtr]["title"] = odeTitle
            shijingOdeDict[shijingOdeCtr]["book"] = shijingBookCtr
            shijingOdeDict[shijingOdeCtr]["number"] = odeNumber
        # Stanza
        shijingStanza = u'' + shijingLine[4]
        if shijingStanza != u'':
            shijingStanzaCtr += 1
            shijingStanzaDict[shijingStanzaCtr] = {}
            shijingStanzaDict[shijingStanzaCtr]["number"] = shijingStanza
            shijingStanzaDict[shijingStanzaCtr]["ode"] = shijingOdeCtr
        # Line, rhyme, rhymeset, Duan rhyme, codepoints:
        # here 'rhyme' refers to the characters which
        # do the rhyming and 'rhymeset' to the labels
        # A B C... identifying lines which rhyme with
        # each other. Occasionally a line contains two
        # rhyming characters, hence the list.
        rhyme = shijingLine[6]
        if rhyme != '': 
            rhymeCodepoints = lineToCodepoints(rhyme)
            rhymeSet = u'' + shijingLine[7]
            duanRhyme = u'' + shijingLine[8]
            shijingLineDict[shijingLineCtr] = {}
            shijingLineDict[shijingLineCtr]["rhymecodepoints"] = rhymeCodepoints
            shijingLineDict[shijingLineCtr]["rhymeset"] = rhymeSet
            shijingLineDict[shijingLineCtr]["duanrhyme"] = duanRhyme
            shijingLineDict[shijingLineCtr]["stanza"] = shijingStanzaCtr
        else:
            duanRhyme = u'' + shijingLine[8]
            shijingLineDict[shijingLineCtr] = {}
            shijingLineDict[shijingLineCtr]["rhymecodepoints"] = []
            shijingLineDict[shijingLineCtr]["rhymeset"] = u""
            shijingLineDict[shijingLineCtr]["duanrhyme"] = u""
            shijingLineDict[shijingLineCtr]["stanza"] = shijingStanzaCtr
        lineText = shijingLine[5]
        # Codepoints
        lineCodepoints = lineToCodepoints(lineText)
        for lineCodepoint in lineCodepoints:
            shijingDict[shijingCodepointCtr] = {}
            shijingDict[shijingCodepointCtr]["codepoint"] = lineCodepoint
            shijingDict[shijingCodepointCtr]["glyph"] = codepointToGlyphDict[lineCodepoint]
            # We do not pass rhyme codepoints to shijingLineDict:
            # instead we note which codepoints of the line text
            # represent the rhyming characters.
            if lineCodepoint in shijingLineDict[shijingLineCtr]["rhymecodepoints"]:
                shijingDict[shijingCodepointCtr]["isrhyme"] = 1
            else:
                shijingDict[shijingCodepointCtr]["isrhyme"] = 0
            shijingDict[shijingCodepointCtr]["line"] = shijingLineCtr
            shijingCodepointCtr += 1
        shijingLineCtr += 1



# Write to file
f=codecs.open("..\\dicts\\shijingDict.py","wb")
pickle.dump(shijingDict,f)
f.close()

f=codecs.open("..\\dicts\\shijingLineDict.py","wb")
pickle.dump(shijingLineDict,f)
f.close()

f=codecs.open("..\\dicts\\shijingStanzaDict.py","wb")
pickle.dump(shijingStanzaDict,f)
f.close()

f=codecs.open("..\\dicts\\shijingOdeDict.py","wb")
pickle.dump(shijingOdeDict,f)
f.close()

f=codecs.open("..\\dicts\\shijingBookDict.py","wb")
pickle.dump(shijingBookDict,f)
f.close()

f=codecs.open("..\\dicts\\shijingPartDict.py","wb")
pickle.dump(shijingPartDict,f)
f.close()


