# -*- coding: utf-8 -*-
import codecs, pickle

# Create she dictionary.
# Each table of Yunjing presents a rhyme 
# which maps on to a later, broader category called "she".
yunjingRhymeToSheDict = {}
f=codecs.open("..\\sources\\yunjingshe.txt","r") # NOT utf8, we want a pure bytestream
lines = []
for line in f:
    lines.append(line[:-1]) # minus return character
f.close()
lines[0] = lines[0][3:] # cut start of file character
for line in lines:
    line = line.split("\t")
    rhyme = int(line[0])
    she = int(line[1]) 
    yunjingRhymeToSheDict[rhyme] = int(she)

# Write to file.
f=codecs.open("..\\dicts\\yunjingRhymeToSheDict.py","wb")
pickle.dump(yunjingRhymeToSheDict,f)
f.close()


