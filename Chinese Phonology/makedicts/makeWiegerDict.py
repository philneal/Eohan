import codecs, pickle

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

f=codecs.open("..\\sources\\wieger.txt","r") # NOT utf8, we want a pure bytestream
lines = []
for line in f:
    line = line[:-1]
    if len(line) > 0:
        line = line.split("\t")
        codepoints = []
        for subline in line:
            sublineCodepoints = lineToCodepoints(subline)
            codepoints.append(sublineCodepoints)
        lines.append(codepoints)
f.close()
lines[0][0] = lines[0][0][1:] # FFEF
wiegerDict = {}
id = 0
phonetic = 1
for line in lines:
    if len(line) == 1:
        codepoint = line[0][0]
        wiegerDict[id] = {"codepoint":codepoint,"phonetic":phonetic,"type":"head"}
        id += 1
        for codepoint in line[0][1:]:
            wiegerDict[id] = {"codepoint":codepoint,"phonetic":phonetic,"type":"main"}
            id += 1
    elif len(line) == 2:
        codepoint = line[0][0]
        wiegerDict[id] = {"codepoint":codepoint,"phonetic":phonetic,"type":"head"}
        id += 1
        for codepoint in line[0][1:]:
            wiegerDict[id] = {"codepoint":codepoint,"phonetic":phonetic,"type":"main"}
            id += 1
        for codepoint in line[1]:
            wiegerDict[id] = {"codepoint":codepoint,"phonetic":phonetic,"type":"alternative"}
            id += 1  
    phonetic += 1

f=codecs.open("..\\dicts\\wiegerDict.py","wb")
pickle.dump(wiegerDict,f)
f.close()
