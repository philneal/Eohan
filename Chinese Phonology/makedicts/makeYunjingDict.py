# -*- coding: utf-8 -*-
import codecs, pickle, utilities

lineToCodepoints = utilities.lineToCodepoints
pp = utilities.pp

# Get codepoints to glyphs.
f=codecs.open("..\\dicts\\codepointToGlyphDict.py","rb")
codepointToGlyphDict = pickle.load(f)
f.close()

# Get mapping of Yunjing character to Guangyun homophone.
f=codecs.open("..\\dicts\\yunjingToGuangyunDict.py","rb")
yunjingToGuangyunDict = pickle.load(f)
f.close()

# Get initial to phonation dictionary.
# Phonation ("chunyin" etc) is roughly place of articulation: see Pulleyblank p. 64-7
f=codecs.open("..\\dicts\\yunjingInitialToPhonationDict.py","rb")
yunjingInitialToPhonationDict = pickle.load(f)
f.close()

# Get initial to articulation dictionary.
# Articulation ("qing" etc) is roughly manner of articulation: see Pulleyblank p. 67-8
f=codecs.open("..\\dicts\\yunjingInitialToArticulationDict.py","rb")
yunjingInitialToArticulationDict = pickle.load(f)
f.close()

# Get the text of Yunjing.
f=codecs.open("..\\sources\\yunjing.txt","r") # NOT utf8, we want a pure bytestream
lines = []
for line in f:
    lines.append(line)
f.close()
lines[0] = lines[0][1:] # cut start of file character
yunjingLines = []
for line in lines:
    line = line.split("\t")
    line = line[1] # we do not want the material in the left margin
    line = line[:-1] # we do not want the end of line character
    if len(line) > 7: # because the input file contains markup "    I" "    II" etc
        line = line.replace("[","").replace("]","") # used to mark doubtful transcriptions
        yunjingLines.append(line) 

# Make Yunjing dictionary.               
lineCtr = 0
codepointCtr = 0
rhyme = 1
tone = 1
grade = 1
yunjingDict = {}
for line in yunjingLines:
    codepoints = lineToCodepoints(line)
    initial = 23 # 23 columns, table is intended to be read right to left
    for codepoint in codepoints:
        glyph = codepointToGlyphDict[codepoint]
        phonation = int(yunjingInitialToPhonationDict[initial]["number"])
        articulation = int(yunjingInitialToArticulationDict[initial]["number"])
        if yunjingToGuangyunDict.has_key(codepointCtr):
            guangyun = int(yunjingToGuangyunDict[codepointCtr])
        else:
            guangyun = 0
        grade = lineCtr % 4 + 1        # 4 grades alternate line by line.
        tone = lineCtr / 4 % 4 + 1     # 4 tones alternate every four lines.
        line = lineCtr                 # 43 rhymes, one per page of 16 lines.
        rhyme  = lineCtr / 16 + 1      # Grades,tones and rhymes are numbered from 1.
        yunjingDict[codepointCtr] = {}
        yunjingDict[codepointCtr]["codepoint"] = codepoint
        yunjingDict[codepointCtr]["glyph"] = glyph
        yunjingDict[codepointCtr]["initial"] = initial
        yunjingDict[codepointCtr]["phonation"] = phonation
        yunjingDict[codepointCtr]["articulation"] = articulation
        yunjingDict[codepointCtr]["grade"] = grade
        yunjingDict[codepointCtr]["tone"] = tone
        yunjingDict[codepointCtr]["line"] = line
        yunjingDict[codepointCtr]["rhyme"] = rhyme
        yunjingDict[codepointCtr]["guangyun"] = guangyun        
        initial -= 1
        codepointCtr += 1
    lineCtr += 1

# Write to file.
f=codecs.open("..\\dicts\\yunjingDict.py","wb")
pickle.dump(yunjingDict,f)
f.close()

