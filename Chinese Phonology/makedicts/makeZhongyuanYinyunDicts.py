# -*- coding: utf-8 -*-
import codecs, pickle, utilities

lineToCodepoints = utilities.lineToCodepoints
pp = utilities.pp

# get codepoints to glyphs
f=codecs.open("..\\dicts\\codepointToGlyphDict.py","rb")
codepointToGlyphDict = pickle.load(f)
f.close()

# Get the text of Zhongyuan Yinyun

# 平聲陰	東冬
# 平聲陰	鍾鐘中蓪忠衷終
# ...

f=codecs.open("..\\sources\\zhongyuanyinyun.txt","r") # NOT utf8, we want a pure bytestream
lines = []
for line in f:
    line = line[:-1]
    lines.append(line)
f.close()
lines[0] = lines[0][3:] # start of file char
textLines = lines

# Get the homophone labels of Zhongyuan Yinyun

# (after Pulleyblank).
# tuŋ	1	a	1	1
# tʂuŋ	1	a	1	2
# ...

f=codecs.open("..\\sources\\zhongyuanyinyunhomophonelabels.txt","r","utf8")
lines = []
for line in f:
    line = line[:-1]
    lines.append(line[:-1]) # cut EOL
f.close()
lines[0] = lines[0][1:] # start of file char
homophoneLabels = []
for line in lines:
    labelList = line.split("\t")
    homophoneLabels.append(labelList)    
f.close()

# Get the rhyme labels of Zhongyuan Yinyun

# 東鍾
# 江陽
# 支思
# ...

f=codecs.open("..\\sources\\zhongyuanyinyunrhymelabels.txt","r","utf8")
lines = []
for line in f:
    line = line[:-1]
    lines.append(line[:-1]) # cut EOL
f.close()
lines[0] = lines[0][1:] # start of file char
rhymeLabels = lines

# A line consists of toneString "\t" text, e.g. 平聲陰	東冬
# The text contains annotations here enclosed in brackets, e.g. 【煙突】.
# Separate annotations into a new list.
newLines = []
annotations = []
toneStrings = []
for line in textLines:
    splitLine = line.split("\t")
    toneString = splitLine[0]
    toneStringCodepoints = lineToCodepoints(toneString) # to utf8
    toneString = u""
    for codepoint in toneStringCodepoints:
        toneString += codepointToGlyphDict[codepoint]
    text = splitLine[1]
    codepoints = lineToCodepoints(text)
    textCodepoints = []
    lineAnnotations = []
    annotation = u""
    isAnnotation = False
    for codepoint in codepoints:
        glyph = codepointToGlyphDict[codepoint]
        if glyph == u"【":
            isAnnotation = True
            annotation = u""
        elif glyph == u"】":      # at the end of an annotation sequence add the annotation to lineAnnotations
            isAnnotation = False
            #textCodepoints.append(codepoint)
            lineAnnotations.append(annotation)
            annotation = u""
        elif isAnnotation: # during an annotation, add the current glyph to the annotation
            annotation += glyph
        else:               # while not in an annotation, add the codepoint to codepoints and an null annotation to annotations
            textCodepoints.append(codepoint)
            lineAnnotations.append(annotation)
    lineAnnotations.append(annotation) # does not get added within the loop
    lineAnnotations = lineAnnotations[1:] # the first codepoint cannot be an annotation
    newLines.append(textCodepoints)
    annotations.append(lineAnnotations)
    toneStrings.append(toneString)
lines = newLines

# Combine the lists of lines, annotations and labels into a list of lists
# [['平聲陰'], [[u'U+6771', '東', u''], [u'U+51AC', '冬', u'']]]
lineEntries = []
lineCtr = 0
for line in lines:
    codepointCtr = 0
    toneString = toneStrings[lineCtr]
    lineAnnotations = annotations[lineCtr]
    lineLabels = homophoneLabels[lineCtr]
    codepointEntries = []
    for codepoint in line:
        glyph = codepointToGlyphDict[codepoint]
        annotation = lineAnnotations[codepointCtr]
        codepointEntry = [codepoint,glyph,annotation]
        codepointEntries.append(codepointEntry)
        codepointCtr += 1
    lineEntry = [lineLabels,[toneString],codepointEntries]
    lineEntries.append(lineEntry)
    lineCtr += 1

# Flatten the list.
newLineEntries = []
for line in lineEntries:
    lineLabels = line[0]       # [tuŋ, 1, a, 1, 1]
    toneString = line[1][0]    # [平聲陰][0]
    codepointEntries = line[2] # [[U+6771, 東, ], [U+51AC, 冬, ]]
    for codepointEntry in codepointEntries:
        codepoint = codepointEntry[0]
        glyph = codepointEntry[1]
        annotation = codepointEntry[2]
        newEntry = list(lineLabels) # We want a copy not a reference.
        newEntry.append(toneString)
        newEntry.append(codepoint)
        newEntry.append(glyph)
        newEntry.append(annotation)
        newLineEntries.append(newEntry)
lineEntries = newLineEntries

zhongyuanYinyunDict = {}
earlyMandarinDict = {}
zhongyuanYinyunHomophoneDict = {}
zhongyuanYinyunFinalDict = {}
zhongyuanYinyunRhymeDict = {}

oldToneNumber = u""
oldToneLetter = u""
oldRhyme = u""
oldHomophoneNumber = u""
codepointId = 0
homophoneId = -1
finalId = -1
rhymeId = -1
for line in lineEntries:
    reading = line[0]
    rhyme = line[1]
    toneLetter = line[2]
    toneNumber = line[3]
    homophoneNumber = line[4]
    toneLabel = line[5]
    codepoint = line[6]
    glyph = line[7]
    annotation = line[8]
    if rhyme != oldRhyme:
        rhymeId += 1
        rhymeLabel = rhymeLabels[rhymeId]
        zhongyuanYinyunRhymeDict[rhymeId] = {"id":rhymeId,
                                           "number":rhyme,
                                           "label":rhymeLabel}
        oldRhyme = rhyme
    if toneNumber != oldToneNumber or toneLetter != oldToneLetter:
        finalId += 1
        finalNumber = str(finalId + 1)
        zhongyuanYinyunFinalDict[finalId] = {"id":finalId,
                                             "number":finalNumber,
                                             "toneletter":toneLetter,
                                             "tonenumber":toneNumber,
                                             "label":toneLabel,
                                             "rhyme":rhymeId}
        oldToneNumber = toneNumber
        oldToneLetter = toneLetter
    if oldHomophoneNumber != homophoneNumber:
        homophoneId += 1
        zhongyuanYinyunHomophoneDict[homophoneId] = {"id":homophoneId,
                                                     "number":homophoneNumber,
                                                     "final":finalId}
        earlyMandarinDict[homophoneId] = {"id":homophoneId,
                                          "reading":reading}
        oldHomophoneNumber = homophoneNumber
    zhongyuanYinyunDict[codepointId] = {"id":codepointId,
                                        "codepoint":codepoint,
                                        "glyph":glyph,
                                        "annotation":annotation,
                                        "homophone":homophoneId}
    codepointId += 1

# Serialise dictionaries with pickle.

f=codecs.open("..\\dicts\\zhongyuanYinyunDict.py","wb")
pickle.dump(zhongyuanYinyunDict,f)
f.close()

f=codecs.open("..\\dicts\\earlyMandarinDict.py","wb")
pickle.dump(earlyMandarinDict,f)
f.close()

f=codecs.open("..\\dicts\\zhongyuanYinyunHomophoneDict.py","wb")
pickle.dump(zhongyuanYinyunHomophoneDict,f)
f.close()

f=codecs.open("..\\dicts\\zhongyuanYinyunFinalDict.py","wb")
pickle.dump(zhongyuanYinyunFinalDict,f)
f.close()

f=codecs.open("..\\dicts\\zhongyuanYinyunRhymeDict.py","wb")
pickle.dump(zhongyuanYinyunRhymeDict,f)
f.close()
