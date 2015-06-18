# -*- coding: utf-8 -*-
import codecs, pickle

# Create neiwai dictionary.
# Each table of Yunjing is labelled "nei" or "wai",
# roughly corresponding to the vowels schwa and a.
yunjingRhymeToNeiwaiDict = {}
f=codecs.open("..\\sources\\yunjingneiwai.txt","r") # NOT utf8, we want a pure bytestream
lines = []
for line in f:
    lines.append(line[:-1]) # minus return character
f.close()
lines[0] = lines[0][3:] # cut start of file character
for line in lines:
    line = line.split("\t")
    rhyme = int(line[0])
    textNeiwai = line[1] # The text of the Yunjing is corrupt and needs correction: see Pulleyblank.
    correctedNeiwai = line[2]
    yunjingRhymeToNeiwaiDict[rhyme] = {}
    yunjingRhymeToNeiwaiDict[rhyme]["text"] = textNeiwai
    yunjingRhymeToNeiwaiDict[rhyme]["corrected"] = correctedNeiwai

# Write to file.
f=codecs.open("..\\dicts\\yunjingRhymeToNeiwaiDict.py","wb")
pickle.dump(yunjingRhymeToNeiwaiDict,f)
f.close()


