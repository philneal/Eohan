import codecs, pickle

f=codecs.open('..\\sources\\Unihan.txt','r','utf8')
lines = []
for line in f:
    lines.append(line[:-1]) # lines end in "\n"
f.close()
lines=lines[102:-1] # the first 101 lines are an introduction, the last says end of file

radicalDict = {}
strokesDict = {}

id = 0
for line in lines:
    fields = line.split("\t")
    # ^[A-Z\x{308}]+[1-5]$
    if fields[1]=="kRSKangXi":
        codepoint = fields[0]
        radicalStrokes = fields[2]
        radicalStrokesList = radicalStrokes.split(".")
        radical = int(radicalStrokesList[0])
        strokes = int(radicalStrokesList[1])
        radicalDict[id] = {"codepoint":codepoint,"radical":radical}
        strokesDict[id] = {"codepoint":codepoint,"strokes":strokes}
        id += 1

totalStrokesDict = {}
id = 0
for line in lines:
    fields = line.split("\t")
    if fields[1]=="kTotalStrokes":
        codepoint = fields[0]
        totalStrokes = fields[2]
        totalStrokesDict[codepoint] = {"totalstrokes":totalStrokes}
        id += 1

f=codecs.open("..\\dicts\\radicalDict.py","wb")
pickle.dump(radicalDict,f)
f.close()

f=codecs.open("..\\dicts\\strokesDict.py","wb")
pickle.dump(strokesDict,f)
f.close()

f=codecs.open("..\\dicts\\totalStrokesDict.py","wb")
pickle.dump(totalStrokesDict,f)
f.close()

