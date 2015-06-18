# -*- coding: utf-8 -*-
import codecs, pickle, utilities

# Create initial to phonation dictionary.
# Phonation ("chunyin" etc) is roughly place of articulation: see Pulleyblank.
yunjingInitialToPhonationDict = {}
f=codecs.open("..\\sources\\yunjinginitialphonation.txt","r") # NOT utf8, we want a pure bytestream
lines = []
for line in f:
    lines.append(line[:-1]) # minus return character
f.close()
lines[0] = lines[0][3:] # cut start of file character
for line in lines:
    line = line.split("\t")
    initial = int(line[0])
    phonationNumber = int(line[1])
    phonationName = line[2]
    yunjingInitialToPhonationDict[initial] = {}
    yunjingInitialToPhonationDict[initial]["number"] = phonationNumber
    yunjingInitialToPhonationDict[initial]["name"] = phonationName
                 
# Write to file.
f=codecs.open("..\\dicts\\yunjingInitialToPhonationDict.py","wb")
pickle.dump(yunjingInitialToPhonationDict,f)
f.close()

