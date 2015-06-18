# -*- coding: utf-8 -*-
import codecs, pickle, utilities

lineToCodepoints = utilities.lineToCodepoints
pp = utilities.pp

# Convert emcfinals.txt into a dictionary
f=codecs.open("..\\sources\\emcfinals.txt","r","utf8")
lines = []
for line in f:
    lines.append(line[:-2]) # Cut end of line characters
f.close()
lines[0] = lines[0][1:] # Cut start of file character

emcFinalDict = {}
emcCtr = 0
#for line in lines[2:]: 
for line in lines:
    # Ignore commented lines.
    if line[0] != "#": 
        emcFinalDict[emcCtr] = {}
        line = line.split("\t")
        emcFinalDict[emcCtr]["number"] = line[1]
        emcFinalDict[emcCtr]["she"] = line[2]
        emcFinalDict[emcCtr]["rhyme"] = line[3]
        emcFinalDict[emcCtr][1] = {}
        emcFinalDict[emcCtr][2] = {}
        emcFinalDict[emcCtr][3] = {}
        emcFinalDict[emcCtr][4] = {}
        emcFinalDict[emcCtr][1]["kai"] = line[4]
        emcFinalDict[emcCtr][2]["kai"] = line[5]
        emcFinalDict[emcCtr][3]["kai"] = line[6]
        emcFinalDict[emcCtr][4]["kai"] = line[7]
        emcFinalDict[emcCtr][1]["he"] = line[8]
        emcFinalDict[emcCtr][2]["he"] = line[9]
        emcFinalDict[emcCtr][3]["he"] = line[10]
        emcFinalDict[emcCtr][4]["he"] = line[11]
        emcFinalDict[emcCtr]["tone"] = line[12]
        emcCtr += 1
# Write to file.
f=codecs.open("..\\dicts\\emcFinalDict.py","wb")
pickle.dump(emcFinalDict,f)
f.close()
