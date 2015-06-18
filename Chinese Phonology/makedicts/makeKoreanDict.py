import codecs, pickle

f=codecs.open('..\\sources\\Unihan.txt','r','utf8')
lines = []
for line in f:
    lines.append(line[:-1]) # lines end in "\n"
f.close()
lines=lines[102:-1] # the first 101 lines are an introduction, the last says end of file

koreanDict = {}
id = 0
for line in lines:
    fields = line.split("\t")
    # ^[A-Z\x{308}]+[1-5]$
    if fields[1]=="kKorean":
        codepoint = fields[0]
        values = fields[2]
        valueList = values.split(" ")
        for value in valueList:
            initial = value[0]
            if len(value) > 1:
                second = value[1]
            else:
                second = u""
            koreanDict[id] = {"codepoint":codepoint,"reading":value.lower(),"initial":initial,"second":second}
            id += 1

f=codecs.open("..\\dicts\\koreanDict.py","wb")
pickle.dump(koreanDict,f)
f.close()
