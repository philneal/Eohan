# -*- coding: utf-8 -*-
import codecs, pickle, utilities

lineToCodepoints = utilities.lineToCodepoints
pp = utilities.pp

# Get codepoints to glyphs
f=codecs.open("..\dicts\\codepointToGlyphDict.py","rb")
codepointToGlyphDict = pickle.load(f)
f.close()

f=codecs.open("..\\dicts\\guangyunDict.py","rb")
guangyunDict = pickle.load(f)
f.close()

# Karlgren's Grammata Serica Recensa

# Part of the Unihan database.
f=codecs.open('..\\sources\\Unihan.txt','r','utf8')
lines = []
for line in f:
    lines.append(line[:-1]) # lines end in "\n"
f.close()
lines=lines[102:-1] # the first 101 lines are an introduction, the last says end of file
gsrLines = lines

# A mapping of codepoint to Guangyun homophones
# (a codepoint can occur in more than one homophone).
codepointToGyHomophoneDict = {}
for key in guangyunDict.keys():
    codepoint = guangyunDict[key]["codepoint"]
    homophone = guangyunDict[key]["homophone"]
    if not codepointToGyHomophoneDict.has_key(codepoint):
        codepointToGyHomophoneDict[codepoint] = [homophone]
    else:
        codepointToGyHomophoneDict[codepoint].append(homophone)

# Read lines, split into fields. 
gsr = []
for gsrLine in gsrLines:
    # Each line = codepoint, key, value(s) separated by tab.
    fields = gsrLine.split("\t")
    if fields[1]=="kGSR":
        codepoint = fields[0]
        glyph = codepointToGlyphDict[codepoint]
        values = fields[2]
        valueList = values.split(" ")
        # Grammata Serica Recensa assigns a number to each
        # phonetic and a letter to each glyph within a
        # phonetic series. Beyond z, the sequence of letters
        # continues a' b' etc. For the purpose of sorting,
        # we replace this with a prefixed pound sign.
        for value in valueList:
            glyphLabel = u""
            if value[-1:] == u"'":
                glyphLabel = u"£"
                value = value[:-1]
            glyphLabel += value[-1:]
            phoneticLabel = value[:-1]
            phonetic = int(phoneticLabel) -1 # Foreign keys numbered from 0.
            if codepointToGyHomophoneDict.has_key(codepoint):
                gyHomophones = codepointToGyHomophoneDict[codepoint]
                for gyHomophone in gyHomophones:
                    gsr.append([phoneticLabel,glyphLabel,codepoint,glyph,phonetic,gyHomophone]) # Ordered this way for sorting, change it when making dictionary.
            else:
                gsr.append([phoneticLabel,glyphLabel,codepoint,glyph,phonetic,None])
gsr.sort()

# Store as dictionary.
gsrDict = {}
gsrId = 0
for gsrLine in gsr:
    phoneticLabel = gsrLine[0]
    glyphLabel = gsrLine[1]
    codepoint = gsrLine[2]
    glyph = gsrLine[3]
    phonetic = gsrLine[4]
    gyHomophone = gsrLine[5]
    # The phonetic label is a zero-padded number: remove initial zeros.
    while phoneticLabel[0] == u"0":
        phoneticLabel = phoneticLabel[1:]
    # Restore the apostrophes.
    if glyphLabel[0] == u"£":
        glyphLabel = glyphLabel[1] + u"'"
    gsrDict[gsrId] = {"codepoint": codepoint,"glyph":glyph,"phoneticlabel": phoneticLabel, "glyphlabel": glyphLabel,  "phonetic":phonetic, "homophone": gyHomophone}
    gsrId += 1

# Grammata Serica Recensa is ordered by Old Chinese rhymes.
# These are not given in the Unihan database but can be restored
# from the ordering of the entries.
f=codecs.open("..\\sources\\gsrphonetics.txt","r","utf8")
lines = []
for line in f:
    lines.append(line[:-2]) # Cut end of line characters.
f.close()
lines[0] = lines[0][1:] # Cut start of file character.
gsrPhoneticLines = lines

# This file has 6 columns:
# First phonetic in rhyme, last phonetic in rhyme, name,
# and readings in the sytems of Pulleyblank, Baxter and Karlgren
# (some rhymes have more than one Karlgren reading: the first is used).
# The name is taken from Pulleyblank, The Final Consonants of
# Old Chinese. gsrPhoneticDict maps phonetics on to rhymes
# and gsrRhymeDict holds the other information.

gsrRhymeDict = {}
gsrPhoneticDict = {}
rhymeId = 0
for gsrPhoneticLine in gsrPhoneticLines:
    gsrPhoneticLine = gsrPhoneticLine.split("\t")
    first = int(gsrPhoneticLine[0])
    last = int(gsrPhoneticLine[1])
    name = gsrPhoneticLine[2]
    pulleyblank = gsrPhoneticLine[3]
    baxter = gsrPhoneticLine[4]
    karlgren = gsrPhoneticLine[5]
    gsrRhymeDict[rhymeId] = {}
    gsrRhymeDict[rhymeId]["name"] = name
    gsrRhymeDict[rhymeId]["pulleyblank"] = pulleyblank
    gsrRhymeDict[rhymeId]["baxter"] = baxter
    gsrRhymeDict[rhymeId]["karlgren"] = karlgren
    for phoneticId in range(first-1, last): # We want foreign keys numbered from 0
        gsrPhoneticDict[phoneticId] = rhymeId
    rhymeId += 1

# Write to file.
f=codecs.open("..\\dicts\\gsrDict.py","wb")
pickle.dump(gsrDict,f)
f.close()
   
f=codecs.open("..\\dicts\\gsrPhoneticDict.py","wb")
pickle.dump(gsrPhoneticDict,f)
f.close()
   
f=codecs.open("..\\dicts\\gsrRhymeDict.py","wb")
pickle.dump(gsrRhymeDict,f)
f.close()
   
