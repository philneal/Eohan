import codecs, pickle
# -*- coding: utf-8 -*-

f=codecs.open("..\\sources\\emctomcbinitials.txt","r","utf8")
lines = []
for line in f:
    lines.append(line[:-2])
f.close()
emcToMcbInitialDict = {}
lines[0] = lines[0][1:] # start of file character
for line in lines:
    line = line.split("\t")
    key = line[0]
    value = line[1]
    emcToMcbInitialDict[key] = value

f=codecs.open("..\\dicts\\emcToMcbInitialDict.py","wb")
pickle.dump(emcToMcbInitialDict,f)
f.close()
