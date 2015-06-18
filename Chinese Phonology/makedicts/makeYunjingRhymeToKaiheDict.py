# -*- coding: utf-8 -*-
import codecs, pickle

# Create kaihe dictionary.
# Each table of Yunjing is labelled "kai" or "he":
# roughly, "kai" means unrounded and "he" means rounded.
yunjingRhymeToKaiheDict = {}
f=codecs.open("..\\sources\\yunjingkaihe.txt","r") # NOT utf8, we want a pure bytestream
lines = []
for line in f:
    lines.append(line[:-1]) # minus return character
f.close()
lines[0] = lines[0][3:] # cut start of file character
for line in lines:
    line = line.split("\t")
    rhyme = int(line[0])
    textKaihe = line[1] # The text of the Yunjing is corrupt and needs correction: see Pulleyblank.
    correctedKaihe = line[2]
    yunjingRhymeToKaiheDict[rhyme] = {}
    yunjingRhymeToKaiheDict[rhyme]["text"] = textKaihe
    yunjingRhymeToKaiheDict[rhyme]["corrected"] = correctedKaihe
 
# Write to file.
f=codecs.open("..\\dicts\\yunjingRhymeToKaiheDict.py","wb")
pickle.dump(yunjingRhymeToKaiheDict,f)
f.close()

