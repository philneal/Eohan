import codecs, pickle
# -*- coding: utf-8 -*-

f=codecs.open("..\\sources\\emctomcbfinals.txt","r","utf8")
lines = []
for line in f:
    lines.append(line[:-2])
f.close()
emcToMcbFinalDict = {}
lines[0] = lines[0][1:] # start of file character
for line in lines:
    line = line.split("\t")
    key = line[0]
    value = line[1]
    emcToMcbFinalDict[key] = value

f=codecs.open("..\\dicts\\emcToMcbFinalDict.py","wb")
pickle.dump(emcToMcbFinalDict,f)
f.close()
