import codecs, pickle

f=codecs.open('..\\sources\\Unihan.txt','r','utf8')
lines = []
for line in f:
    lines.append(line[:-1]) # lines end in "\n"
f.close()
lines=lines[102:-1] # the first 101 lines are an introduction, the last says end of file

cantoneseDict = {}
id = 0
for line in lines:
    fields = line.split("\t")
    # ^[A-Z\x{308}]+[1-5]$
    if fields[1]=="kCantonese":
        codepoint = fields[0]
        values = fields[2]
        valueList = values.split(" ")
        for value in valueList:
            cantoneseDict[id] = {"codepoint":codepoint,"reading":value.lower(),"initial": u"","second": u""}
            id += 1

cantoneseInitialDict = {u"a": u"A", 
                        u"b": u"B", 
                        u"c": u"C", 
                        u"d": u"D", 
                        u"e": u"E", 
                        u"f": u"F", 
                        u"g": u"G", 
                        u"h": u"H", 
                        u"j": u"J", 
                        u"k": u"K", 
                        u"l": u"L", 
                        u"m": u"M", 
                        u"n": u"N", 
                        u"o": u"O", 
                        u"p": u"P", 
                        u"s": u"S", 
                        u"t": u"T", 
                        u"u": u"U", 
                        u"w": u"W", 
                        u"z": u"Z"}
for key in cantoneseDict.keys():
    initial = cantoneseDict[key]["reading"][0]
    initial = cantoneseInitialDict[initial]
    if len(cantoneseDict[key]["reading"][:-1]): # remove tone number
        toneless = cantoneseDict[key]["reading"][:-1]
        tone = cantoneseDict[key]["reading"][-1]
        second = cantoneseDict[key]["reading"][1]
    else:
        toneless = u""
        tone = u""
        second = u""
    cantoneseDict[key]["initial"] = initial
    cantoneseDict[key]["second"] = second
    cantoneseDict[key]["tone"] = tone
    cantoneseDict[key]["toneless"] = toneless

f=codecs.open("..\\dicts\\cantoneseDict.py","wb")
pickle.dump(cantoneseDict,f)
f.close()
