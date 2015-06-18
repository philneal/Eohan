# -*- coding: utf-8 -*-
import codecs, pickle, utilities

lineToCodepoints = utilities.lineToCodepoints
pp = utilities.pp

# Get codepoints to glyphs.
f=codecs.open("..\\dicts\\codepointToGlyphDict.py","rb")
codepointToGlyphDict = pickle.load(f)
f.close()

# Get the text of Guangyun.
f=codecs.open('..\\sources\\guangyun.txt','r') # NOT utf8, we want a pure bytestream
lines = []
for line in f:
    lines.append(line[:-1]) # cut end of line character
lines[0] = lines[0][3:] # cut start of file character
f.close()
guangyunLines = lines

# Get matches between Guangyun finals and Yunjing cells
f=codecs.open('..\\sources\\guangyuntoyunjing.txt','r','utf8')
lines = []
for line in f:
    lines.append(line[:-2]) # cut end of line character
lines[0] = lines[0][1:] # cut start of file character
f.close()
guangyunToYunjingList = lines

f=codecs.open('..\\sources\\guangyuntoyunjingalternative.txt','r','utf8')
lines = []
for line in f:
    lines.append(line[:-2]) # cut end of line character
lines[0] = lines[0][1:] # cut start of file character
f.close()
guangyunToYunjingAlternativeList = lines

# Get the Guangyun final type (A, B or mixed AB)
f=codecs.open('..\\sources\\guangyunfinaltype.txt','r','utf8')
lines = []
for line in f:
    lines.append(line[:-2]) # cut end of line character
lines[0] = lines[0][1:] # cut start of file character
f.close()
guangyunFinalTypeList = lines

# Get the Guangyun final labels
f=codecs.open('..\\sources\\guangyunfinallabels.txt','r','utf8')
lines = []
for line in f:
    lines.append(line[:-2]) # cut end of line character
lines[0] = lines[0][1:] # cut start of file character
f.close()
guangyunFinalLabelList = lines

# Make Guangyun dictionaries
#
# guangyunDict maps codepoint to homophone,
# guangyunHomophoneDict maps homophone to final, and
# guangyunSubrhymeDict maps final to tone.
# 
# The file guangyun.txt is marked up with lines "H", "F", "T"
# where a new homophone, final or tone begins and we increment
# the counter.
# A final is that part of a rhyme falling within a single tone.
guangyunDict = {}
guangyunHomophoneDict = {}
guangyunFinalDict = {}
lineCtr = 0
codepointCtr = 0
homophoneCtr = 0
finalCtr = 0
toneCtr = 0
for line in guangyunLines:
    if line == "H":
        guangyunHomophoneDict[homophoneCtr] = {}
        guangyunHomophoneDict[homophoneCtr]["number"] = u"" + str(homophoneCtr + 1)
        guangyunHomophoneDict[homophoneCtr]["final"] = finalCtr
        homophoneCtr += 1
    elif line == "F":
        guangyunFinalDict[finalCtr] = {}
        guangyunFinalDict[finalCtr]["number"] = u"" + str(finalCtr + 1)
        guangyunFinalDict[finalCtr]["tone"] = toneCtr
        finalCtr += 1
    elif line == "T":
        toneCtr += 1
    else:
        codepoints = lineToCodepoints(line)
        codepoints = lineToCodepoints(line)
        if 'U+95' in codepoints:
            codepoints.remove('U+95') # A kludge: lineToCodepoints gags on 坦䦔, can't see why.
        for codepoint in codepoints:
            glyph = codepointToGlyphDict[codepoint]
            homophone = homophoneCtr
            guangyunDict[codepointCtr] = {}
            guangyunDict[codepointCtr]["codepoint"] = codepoint
            guangyunDict[codepointCtr]["glyph"] = glyph
            guangyunDict[codepointCtr]["homophone"] = homophone
            codepointCtr += 1
    lineCtr += 1
# guanyunTone is just the four tones.
guangyunToneDict = {0:1, 1:2, 2:3, 3:4}

# Add the fanqie to guangyunHomophoneDict.
f=codecs.open('..\\sources\\guangyunfanqie.txt','r') # NOT utf8, we want a pure bytestream
lines = []
for line in f:
    lines.append(line[:-1]) # cut end of line character
lines[0] = lines[0][3:] # cut start of file character
f.close()
guangyunFanqieLines = lines

homophoneCtr = 0
for line in guangyunFanqieLines:
    codepoints = lineToCodepoints(line)
    homophoneCodepoint = codepoints[0]
    homophoneGlyph = codepointToGlyphDict[homophoneCodepoint]
    initialFanqieCodepoint = codepoints[1]
    initialFanqieGlyph = codepointToGlyphDict[initialFanqieCodepoint]
    finalFanqieCodepoint = codepoints[2]
    finalFanqieGlyph = codepointToGlyphDict[finalFanqieCodepoint]
    guangyunHomophoneDict[homophoneCtr]["initialfanqiecodepoint"] = initialFanqieCodepoint
    guangyunHomophoneDict[homophoneCtr]["initialfanqieglyph"] = initialFanqieGlyph
    guangyunHomophoneDict[homophoneCtr]["finalfanqiecodepoint"] = finalFanqieCodepoint
    guangyunHomophoneDict[homophoneCtr]["finalfanqieglyph"] = finalFanqieGlyph
    homophoneCtr += 1

# Add Yunjing matches to guangyunHomophoneDict
ctr = 0 # debug
for line in guangyunToYunjingList:
    line = line.split("\t")
    guangyunHomophoneNumber = int(line[0])
    guangyunHomophoneId = guangyunHomophoneNumber - 1
    yunjingId = int(line[1])
    guangyunHomophoneDict[guangyunHomophoneId]["yunjing"] = yunjingId
    guangyunHomophoneDict[guangyunHomophoneId]["yunjingtype"] = 1
    ctr += 1 # debug
    
for line in guangyunToYunjingAlternativeList:
    line = line.split("\t")
    guangyunHomophoneNumber = int(line[0])
    guangyunHomophoneId = guangyunHomophoneNumber - 1
    yunjingId = int(line[1])
    guangyunHomophoneDict[guangyunHomophoneId]["yunjing"] = yunjingId
    guangyunHomophoneDict[guangyunHomophoneId]["yunjingtype"] = 0

# Add Guangyun final type to guangyunFinalDict
for line in guangyunFinalTypeList:
    line = line.split("\t")
    guangyunFinalNumber = int(line[0])
    guangyunFinalId = guangyunFinalNumber - 1
    guangyunFinalType = line[1]
    guangyunFinalDict[guangyunFinalId]["type"] = guangyunFinalType

# Add Guangyun final label to guangyunFinalDict

guangyunFinalId = 0
for line in guangyunFinalLabelList:
    line = line.split("\t")
    guangyunFinalGlyph = line[0]
    guangyunFinalSectionNumber = line[1]
    guangyunFinalTongyong = line[2]
    guangyunFinalDict[guangyunFinalId]["finalglyph"] = guangyunFinalGlyph
    guangyunFinalDict[guangyunFinalId]["sectionlabel"] = guangyunFinalSectionNumber
    guangyunFinalDict[guangyunFinalId]["tongyong"] = guangyunFinalTongyong
    guangyunFinalId += 1
    
# Write to file.
f=codecs.open("..\\dicts\\guangyunDict.py","wb")
pickle.dump(guangyunDict,f)
f.close()

f=codecs.open("..\\dicts\\guangyunHomophoneDict.py","wb")
pickle.dump(guangyunHomophoneDict,f)
f.close()

f=codecs.open("..\\dicts\\guangyunFinalDict.py","wb")
pickle.dump(guangyunFinalDict,f)
f.close()

f=codecs.open("..\\dicts\\guangyunToneDict.py","wb")
pickle.dump(guangyunToneDict,f)
f.close()

