import codecs, pickle
# -*- coding: utf-8 -*-

f=codecs.open("..\\sources\\emctomckfinals.txt","r","utf8")
lines = []
for line in f:
    lines.append(line[:-2])
f.close()
emcToMckFinalDict = {}
lines[0] = lines[0][1:] # start of file character
for line in lines:
    line = line.split("\t")
    key = line[0]
    value = line[1]
    emcToMckFinalDict[key] = value

f=codecs.open("..\\dicts\\emcToMckFinalDict.py","wb")
pickle.dump(emcToMckFinalDict,f)
f.close()
