import codecs, pickle

f=codecs.open('..\\sources\\Unihan.txt','r','utf8')
lines = []
for line in f:
    lines.append(line[:-1]) # lines end in "\n"
f.close()
lines=lines[102:-1] # the first 101 lines are an introduction, the last says end of file

fourCornerCodeDict = {}
id = 0
for line in lines:
    fields = line.split("\t")
    # ^[A-Z\x{308}]+[1-5]$
    if fields[1]=="kFourCornerCode":
        codepoint = fields[0]
        fourCornerCode = fields[2]
        nwCorner = fourCornerCode[0] # a code 4321.9 refers to northwest, northeast etc.
        neCorner = fourCornerCode[1]
        swCorner = fourCornerCode[2]
        seCorner = fourCornerCode[3]
        eseCorner = u""
        if len(fourCornerCode) == 6:
            eseCorner = fourCornerCode[5]
        fourCornerCodeDict[id] = {"codepoint": codepoint,
                                  "nwcorner": nwCorner,
                                  "necorner": neCorner,
                                  "swcorner": swCorner,
                                  "secorner": seCorner,
                                  "esecorner": eseCorner}
        id += 1

f=codecs.open("..\\dicts\\fourCornerCodeDict.py","wb")
pickle.dump(fourCornerCodeDict,f)
f.close()


        
