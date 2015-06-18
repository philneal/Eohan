# -*- coding: utf-8 -*-
import codecs, pickle, utilities

# Create Yunjing initial to articulation dictionary.
# Articulation ("qing" etc) is roughly manner of articulation: see Pulleyblank.
yunjingInitialToArticulationDict = {}
f=codecs.open("..\\sources\\yunjinginitialarticulation.txt","r") # NOT utf8, we want a pure bytestream
lines = []
for line in f:
    lines.append(line[:-1]) # minus return character
f.close()
lines[0] = lines[0][3:] # cut start of file character
for line in lines:
    line = line.split("\t")
    initial = int(line[0])
    articulation = line[1]
    articulationNumber = int(line[1])
    articulationName = line[2]
    yunjingInitialToArticulationDict[initial] = {}
    yunjingInitialToArticulationDict[initial]["number"] = articulationNumber
    yunjingInitialToArticulationDict[initial]["name"] = articulationName
                 
# Write to file.
f=codecs.open("..\\dicts\\yunjingInitialToArticulationDict.py","wb")
pickle.dump(yunjingInitialToArticulationDict,f)
f.close()

