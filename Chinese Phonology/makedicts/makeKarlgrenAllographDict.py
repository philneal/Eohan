import codecs, pickle
# -*- coding: utf-8 -*-

# allographs and semantic variants of characters in karlgren
f=codecs.open("..\\sources\\karlgren_allographs.txt","r","utf8")
lines = []
for line in f:
    lines.append(line[:-2])
f.close()
karlgrenAllographDict = {}
id = 0
for line in lines:
    line = line.split("\t")
    karlgrenCodepoint = line[0]
    allographCodepoint = line[1]
    karlgrenAllographDict[id] = {}
    karlgrenAllographDict[id]["codepoint"] = karlgrenCodepoint
    karlgrenAllographDict[id]["allograph"] = allographCodepoint
    id += 1

f=codecs.open("..\\dicts\\karlgrenAllographDict.py","wb")
pickle.dump(karlgrenAllographDict,f)
f.close()

    
