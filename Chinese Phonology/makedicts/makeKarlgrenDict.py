import sqlite3, codecs, pickle
# -*- coding: utf-8 -*-

# routines for converting glyphs into codepoints
# gets round the problem of Windows narrow build
def hexStringToBin(s):
    return bin(int(repr(s)[3:-1],16))[2:]

def binStringToHex(s):
    # '11110000' -> '80' -> '0x8d' -> '8d'
    #print hex(int(s,2))[2:]
    return hex(int(s,2))[2:]
  
def lineToCodepoints(line):
    l = []
    while len(line) > 0:
        nextByte = hexStringToBin(line[0])
        line = line[1:]
        firstBit = nextByte[0]
        nextByte = nextByte[1:]
        if firstBit == "0":
            codepoint = binStringToHex(nextByte)
        elif firstBit == "1":
            while nextByte[0] == "1":
                nextByte = nextByte[1:] + hexStringToBin(line[0])[2:]
                line = line[1:]
            codepoint = binStringToHex(nextByte)
            codepoint = codepoint.upper()
        l.append(u"U+" + codepoint)
    return l

# get codepoints to glyphs and glyphs to codepoints
f=codecs.open("..\\dicts\\codepointToGlyphDict.py","rb")
codepointToGlyphDict = pickle.load(f)
f.close()

# make dictionary of karlgren phonetic series

lines = []
f=codecs.open("..\\sources\\karlgren.txt","r") # NOT utf8, we want a pure bytestream
lines = []
for line in f:
    line = line[:-1]
    line = line.replace("[","").replace("]","")
    line = line.split("\t")
    id = line[0]
    phoneticMembers = lineToCodepoints(line[1])
    semanticMembers = []
    if len(line) == 3:
        semanticMembers = lineToCodepoints(line[2])
    lines.append([id,phoneticMembers,semanticMembers])
lines[0][0] = lines[0][0][3:] # FFEF
karlgrenDict = {}
id = 0
for line in lines:
    series = line[0]
    phoneticMembers = line[1]
    semanticMembers = line[2]
    for codepoint in phoneticMembers:
        karlgrenDict[id] = {"codepoint":codepoint,"series":series,"type":"phonetic"}
        id += 1
    for codepoint in semanticMembers:
        karlgrenDict[id] = {"codepoint":codepoint,"series":series,"type":"semantic"}
        id += 1
f=codecs.open("..\\dicts\\karlgrenDict.py","wb")
pickle.dump(karlgrenDict,f)
f.close()
