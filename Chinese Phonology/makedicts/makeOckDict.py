# -*- coding: utf-8 -*-
import codecs, pickle, utilities

lineToCodepoints = utilities.lineToCodepoints
pp = utilities.pp

# get codepoints to glyphs
f=codecs.open("..\\dicts\\codepointToGlyphDict.py","rb")
codepointToGlyphDict = pickle.load(f)
f.close()

# Dictionaries needed.
f=codecs.open("..\\dicts\\gsrDict.py","rb")
gsrDict = pickle.load(f)
f.close()

f=codecs.open("..\\dicts\\gsrPhoneticDict.py","rb")
gsrPhoneticDict = pickle.load(f)
f.close()

f=codecs.open("..\\dicts\\gsrRhymeDict.py","rb")
gsrRhymeDict = pickle.load(f)
f.close()

f=codecs.open("..\\dicts\\emcFeaturesDict.py","rb")
emcFeaturesDict = pickle.load(f)
f.close()

f=codecs.open("..\\dicts\\guangyunFinalDict.py","rb")
guangyunFinalDict = pickle.load(f)
f.close()

f=codecs.open("..\\dicts\\emcToMckInitialDict.py","rb")
emcToMckInitialDict = pickle.load(f)
f.close()

f=codecs.open("..\\dicts\\mckFinalToOckFinalsDict.py","rb")
mckFinalToOckFinalsDict = pickle.load(f)
f.close()

# A dictionary of cross rhymes (explained below)
f=codecs.open("..\\sources\\ockcrossrhymes.txt","r","utf8")
lines = []
for line in f:
    lines.append(line[:-2]) # Cut end of line characters
f.close()
lines[0] = lines[0][1:] # Cut start of file character.
ockCrossRhymeDict = {}
for line in lines:
    line = line.split("\t")
    ockRhyme = line[0]
    crossRhymes = line[1].split(" ")
    ockCrossRhymeDict[ockRhyme] = crossRhymes

# A list holding the information needed to generate
# Old Chinese.
#
# To generate Old Chinese finals we need to know
# the OC rhyme and the EMC final, kaihe and grade.
#
# To generate Old Chinese initials we need to know
# the EMC initial, OC vowel and the phonetic series.
#
featuresList = []
for key in gsrDict.keys():
    codepoint = gsrDict[key]["codepoint"]
    phonetic = gsrDict[key]["phonetic"]
    gyHomophone = gsrDict[key]["homophone"]
    # Here, gsrRhyme means a section of GSR:
    # ockRhyme means its value in the Karlgren system.
    gsrRhyme = gsrPhoneticDict[phonetic]
    ockRhyme = gsrRhymeDict[gsrRhyme]["karlgren"]
    if emcFeaturesDict.has_key(gyHomophone):
        guangyunRhyme = int(emcFeaturesDict[gyHomophone]["guangyunrhyme"]) # temp
        emcInitial = emcFeaturesDict[gyHomophone]["emcinitial"]
        mckInitial = emcToMckInitialDict[emcInitial]
        emcFinal = emcFeaturesDict[gyHomophone]["final"]
        emcFinalNum = emcFinal + 1
        kaihe = emcFeaturesDict[gyHomophone]["kaihe"]
        grade = emcFeaturesDict[gyHomophone]["grade"]
        gyTone = guangyunFinalDict[emcFinal]["tone"]
        gyType = guangyunFinalDict[emcFinal]["type"]
        if gyType == u"AB" and grade in [1,2]:
            gyType = u"A"
        else:
            gyType = u"B"
        # We combine the EMC features into a single string for ease of lookup.
        emcFeatureString = str(emcFinalNum) + " " + kaihe + " " + str(grade)
        featuresList.append([codepoint,phonetic,ockRhyme,mckInitial,emcFeatureString,gyHomophone,gyTone,gyType,grade])
        # From now on, we refer to ocpRhyme just as rhyme.
    else:
        featuresList.append([codepoint,phonetic,ockRhyme,u"-",u"-",u"-",0,u"-",u"-"])

ockFinalsDict = {}
lineCtr = 0
for line in featuresList:
    ockFinal = "None"
    codepoint = line[0]
    ockRhyme = line[2]
    emcFeatureString = line[4]
    gyHomophone = line[5]
    crossRhymes = ockCrossRhymeDict[ockRhyme]
    gyTone = line[6]
    gyType = line[7]
    # The default when lookup fails.
    if not mckFinalToOckFinalsDict.has_key(emcFeatureString):
        toneSign  =  str(gyTone + 1)
        ockFinal = ockRhyme + toneSign + u"??" 
    # Normal lookup.
    elif mckFinalToOckFinalsDict[emcFeatureString].has_key(ockRhyme):
        ockFinal = mckFinalToOckFinalsDict[emcFeatureString][ockRhyme]
    # Cross rhyme lookup.
    elif len(crossRhymes) > 0:
        for crossRhyme in crossRhymes:
            if mckFinalToOckFinalsDict[emcFeatureString].has_key(crossRhyme):
                ockFinal = mckFinalToOckFinalsDict[emcFeatureString][crossRhyme]
    if ockFinal == "None": # redundant?
        toneSign = str(gyTone + 1)
        ockFinal = ockRhyme + toneSign + u"!!" 
        ockFinalsDict[lineCtr] = ockFinal
    # Add the final to the dictionary.
    ockFinalsDict[lineCtr] = ockFinal
    lineCtr += 1
    
                    ############################
                    ### Old Chinese Initials ###
                    ############################

# Karlgren's Old Chinese initials are little different from his Middle Chinese.
# Make emcToOcInitialsDict

# Read file
lines = []
f=codecs.open("..\\sources\\mcktoockinitials.txt","r","utf8")
for line in f:
    line = line[:-2] # Cut end of line characters
    lines.append(line)
f.close()
lines[0] = lines[0][1:] # Cut start of file character

mckInitialToOckInitialDict = {}
for line in lines:
    line = line.split("\t")
    mckInitial = line[0]
    ockInitial = line[1]
    mckInitialToOckInitialDict[mckInitial] = ockInitial

ockInitialsDict = {}
ctr = 0
for line in featuresList:
    mckInitial = line[3]
    ockInitial = mckInitialToOckInitialDict[mckInitial]
    ockInitialsDict[ctr] = ockInitial
    ctr += 1

# Original 
##for line in featuresList:
##    mckInitial = line[3]
##    grade = line[8]
##    ockInitial = mckInitialToOckInitialDict[mckInitial]
    
                    ############################
                    ### Old Chinese Readings ###
                    ############################

# Combine OC initials and OC finals
for codepointId in ockFinalsDict.keys():
    ockInitial = ockInitialsDict[codepointId]
    ockFinal = ockFinalsDict[codepointId]
    reading  = ockInitial + ockFinal
    gsrDict[codepointId]["karlgren"] = reading
    gsrDict[codepointId]["karlgreninitial"] = ockInitial
    gsrDict[codepointId]["karlgrenfinal"] = ockFinal

# Write to file.
f=codecs.open("..\\dicts\\gsrDict.py","wb")
pickle.dump(gsrDict,f)
f.close()


    
