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

f=codecs.open("..\\dicts\\emcToMcbInitialDict.py","rb")
emcToMcbInitialDict = pickle.load(f)
f.close()

f=codecs.open("..\\dicts\\mcbFinalToOcbFinalsDict.py","rb")
mcbFinalToOcbFinalsDict = pickle.load(f)
f.close()

# A dictionary of cross rhymes (explained below)
f=codecs.open("..\\sources\\ocbcrossrhymes.txt","r","utf8")
lines = []
for line in f:
    lines.append(line[:-2]) # Cut end of line characters
f.close()
lines[0] = lines[0][1:] # Cut start of file character.
ocbCrossRhymeDict = {}
for line in lines:
    line = line.split("\t")
    rhyme = line[0]
    crossRhymes = line[1].split(" ")
    ocbCrossRhymeDict[rhyme] = crossRhymes

# tone endings
toneDict = {0: u"",1: u"ʔ", 2: u"s", 3:u"", u"-": u""}

acuteGraveDict = {u"p": u"grave",
u"ph": u"grave",
u"b": u"grave",
u"m": u"grave",
u"t": u"acute",
u"th": u"acute",
u"d": u"acute",
u"n": u"acute",
u"k": u"grave",
u"kh": u"grave",
u"g": u"grave",
u"ng": u"grave",
u"ts": u"acute",
u"tsh": u"acute",
u"dz": u"acute",
u"s": u"acute",
u"z": u"acute",
u"": u"grave",
u"x": u"grave",
u"h": u"grave",
u"j": u"acute",
u"w": u"grave",
u"l": u"acute",
u"ny": u"acute",
u"tr": u"acute",
u"trh": u"acute",
u"dr": u"acute",
u"nr": u"acute",
u"tsr": u"acute",
u"tsrh": u"acute",
u"dzr": u"acute",
u"sr": u"acute",
u"zr": u"acute",
u"tsy": u"acute",
u"tshy": u"acute",
u"zy": u"acute",
u"sy": u"acute",
u"dzy": u"acute",
u"": u""}

retroflexSibilants = [u"tsy", u"tshy", u"dzy"]
dentalRetroflexSibilants = [u"ts", u"tsh", u"dz", u"tsr", u"tshr", u"dzr"]

# Make features list.
# To generate Old Chinese finals we need we need to know
# the OC rhyme category, the phonetic series,
# the EMC final, kaihe and grade, and whether the
# EMC initial is acute or grave.
mcbInitials = []
featuresList = []
for key in gsrDict.keys():
    codepoint = gsrDict[key]["codepoint"]
    phonetic = gsrDict[key]["phonetic"]
    gyHomophone = gsrDict[key]["homophone"]
    # Here, gsrRhyme means a section of GSR:
    # ocbRhyme means its value in the Baxter system.
    # At this point, ocbRhyme is a default value:
    # ot is still at and so on.
    gsrRhyme = gsrPhoneticDict[phonetic]
    ocbRhyme = gsrRhymeDict[gsrRhyme]["baxter"]
    if emcFeaturesDict.has_key(gyHomophone):
        emcInitial = emcFeaturesDict[gyHomophone]["emcinitial"]
        mcbInitial = emcToMcbInitialDict[emcInitial]
        if mcbInitial not in mcbInitials:
            mcbInitials.append(mcbInitial)
        if mcbInitial in retroflexSibilants:    # retroflex sibilants are actually acute 
            acuteGrave = "grave"                # but count as grave for the purpose of
        else:                                   # identifying front vowels
            acuteGrave = acuteGraveDict[mcbInitial]
        kaihe = emcFeaturesDict[gyHomophone]["kaihe"]
        grade = emcFeaturesDict[gyHomophone]["grade"]
        emcFinal = emcFeaturesDict[gyHomophone]["final"]
        gyTone = guangyunFinalDict[emcFinal]["tone"]
        emcFinalNum = emcFinal + 1
        # We combine the EMC features into a single string for ease of lookup.
        emcFeatureString = str(emcFinalNum) + " " + kaihe + " " + str(grade)
        featuresList.append([codepoint,phonetic,ocbRhyme,mcbInitial,emcFeatureString,kaihe,acuteGrave,gyHomophone,gyTone])
        # From now on, we refer to ocbRhyme just as rhyme.
    else:
        featuresList.append([codepoint,phonetic,ocbRhyme,u"-",u"-",u"-",u"-",u"-",u"-"])

# Karlgren did not distinguish between the Pulleyblank rhymes ɨj (Wei) and ij (Zhi).
# By default we assign a codepoint to ɨj (Wei) and reassign to j (Zhi) on the basis
# of the Guangyun. See Baxter, Old Chinese, p. 448.
#
# Zhi corresponds to Guangyun rhyme Qi, and
# Wei corresponds to Guanyun rhymes Hui, Hai, Wai
# except that 
# Zhi corresponds to Guangyun rhymess Zhi kaikou, Jie kaikou, and
# Wei corresponds to Guangyun rhymes Zhi hekou, Jie hekou
# except that 
# phonetics gui and ji are in Zhi.
#
# Guangyun rhyme Qi has finals 12, 68, 124
# Guangyun rhyme Zhi has finals 6, 62, 118
# Guangyun rhyme Jie has finals 14, 70, 128
#
# As a data structure:
zhiFeatureStrings = ["12 kai 1", "12 kai 2", "12 kai 3", "12 kai 4", \
                     "12 he 1", "12 he 2", "12 he 3", "12 he 4", \
                     "68 kai 1", "68 kai 2", "68 kai 3", "68 kai 4", \
                     "68 he 1", "68 he 2", "68 he 3", "68 he 4", \
                     "124 kai 1", "124 kai 2", "124 kai 3", "124 kai 4", \
                     "124 he 1", "124 he 2", "124 he 3", "124 he 4", \
                     "6 kai 1", "6 kai 2", "6 kai 3", "6 kai 4", \
                     "62 kai 1", "62 kai 2", "62 kai 3", "62 kai 4", \
                     "118 kai 1", "118 kai 2", "118 kai 3", "118 kai 4", \
                     "14 kai 1", "14 kai 2", "14 kai 3", "14 kai 4", \
                     "70 kai 1", "70 kai 2", "70 kai 3", "70 kai 4", \
                     "128 kai 1", "128 kai 2", "128 kai 3", "128 kai 4"]
for line in featuresList:
    emcFeatureString = line[4]
    if emcFeatureString in zhiFeatureStrings:
        line[2] = u'ij' # Change the OC rhyme from ǝl to ǝj.

# Baxter reconstructs six vowels for Old Chinese. In some cases,
# the vowel is implicit in the Grammata Serica Recensa rhyme, but
# in others it must be determined from the EMC features or from
# the vowel of the phonetic series which a character belongs to.

# These distinctions cannot be determined on the basis of EMC:
# an/on, aj/oj, am/om, ap/op, ɨm/um, ɨp/up.
# These can: at/ot, ɨn/un, ɨt/ut, ɨj/uj because in these cases
# EMC hekou after a grave initial always represents a or u.

# For each phonetic, determine its type and height.
phoneticFeatureDict = {}
for line in featuresList:
    phonetic = line[1]
    ocbRhyme = line[2]
    emcFeatureString = line[4]
    kaihe = line[5]
    acuteGrave = line[6]
    # Cross-rhymes are not relevant here as we are only interested in phonetics.
    if mcbFinalToOcbFinalsDict.has_key(emcFeatureString) and \
       mcbFinalToOcbFinalsDict[emcFeatureString].has_key(ocbRhyme):
        ocbType = mcbFinalToOcbFinalsDict[emcFeatureString][ocbRhyme]["type"]
        ocbHeight = mcbFinalToOcbFinalsDict[emcFeatureString][ocbRhyme]["height"]
        # Correct back vowels to front on the basis of EMC.
        if ocbRhyme in [u"at",u"ɨn", u"ɨt",u"ɨj"] and kaihe == "he" and acuteGrave == "acute":
            ocbType = "front"
        if not phoneticFeatureDict.has_key(phonetic):
            phoneticFeatureDict[phonetic] = {"type":ocbType,"height":ocbHeight}
    else:
        phoneticFeatureDict[phonetic] = {"type":"none","height":"none"}

# For each character in the series, force it to the same type as its phonetic.
ocbFinalsDict = {}
lineCtr = 0
for line in featuresList:
    codepoint = line[0]
    phonetic = line[1]
    ocbRhyme = line[2]
    emcFeatureString = line[4]
    gyTone = line[8]
    crossRhymes = ocbCrossRhymeDict[ocbRhyme]
    ocbFinal = "None"
    # The default when lookup fails.
    if not mcbFinalToOcbFinalsDict.has_key(emcFeatureString):
        ocbFinals = {'type': 'none', 'height': 'none', 'none': u'-'}
        toneSign = toneDict[gyTone]
        ocbFinal = ocbRhyme + toneSign + u"??"
        ### debug print lineCtr, codepointToGlyphDict[codepoint], line
    # Normal lookup.
    elif mcbFinalToOcbFinalsDict[emcFeatureString].has_key(ocbRhyme):
        ocbFinals = mcbFinalToOcbFinalsDict[emcFeatureString][ocbRhyme]
    # Cross rhyme lookup.
    elif len(crossRhymes) > 0:
        ocbFinals = {'type': 'none', 'height': 'none', 'none': ocbFinal}
        for crossRhyme in crossRhymes:
            if mcbFinalToOcbFinalsDict[emcFeatureString].has_key(crossRhyme):
                ocbFinals = mcbFinalToOcbFinalsDict[emcFeatureString][crossRhyme]
    ocbType = ocbFinals["type"]
    ocbHeight = ocbFinals["height"]
    # Correct back vowels to front on the basis of EMC.
    if ocbRhyme in [u"at",u"ɨn", u"ɨt",u"ɨj"] and kaihe == "he" and acuteGrave == "acute":
        ocbType = "front"
    # Correct type to front or rounded on the basis of the phonetic,
    # where the character and its phonetic are of the same height
    # (e.g. we correct am to om if the phonetic is op,
    # but not if the phonetic is um).
    phoneticType = phoneticFeatureDict[phonetic]["type"]
    phoneticHeight = phoneticFeatureDict[phonetic]["height"]
    if ocbHeight == phoneticHeight and ocbFinals.has_key(phoneticType):
        ocbType = phoneticType
    if not ocbFinals["type"] == "none":
        ocbFinal = ocbFinals[ocbType]
    if ocbFinal == "None":
        toneSign = toneDict[gyTone]
        ocbFinal = ocbRhyme + toneSign + u"!!" # ocpFinal = u"-"
    # Cases where wa and wɨ have been fronted.
    ocbFinal.replace(u"wo",u"o")
    ocbFinal.replace(u"wu",u"u")
    ocbFinalsDict[lineCtr] = ocbFinal
    lineCtr += 1

                    ############################
                    ### Old Chinese Initials ###
                    ############################

# Strategy

# The initial consonants of Old Chinese are not known with any
# certainty, and the reconstructions of Pulleyblank and Baxter
# involve personal judgment. This algorithm is only intended
# to give conjectural values.
 
# Make emcToOcInitialsDict

# Read file
lines = []
f=codecs.open("..\\sources\\mcbtoocbinitials.txt","r","utf8")
for line in f:
    line = line[:-2] # Cut end of line characters
    lines.append(line)
f.close()
lines[0] = lines[0][1:] # Cut start of file character
mcbToOcbInitialLines = []

mcbToOcbInitialsDict = {}
for line in lines: 
    line = line.split("\t")
    mcbInitial = line[0]
    ocbInitialGroup = line[1]
    ocbInitial = line[2]
    if not mcbToOcbInitialsDict.has_key(mcbInitial):
        mcbToOcbInitialsDict[mcbInitial] = {}
    mcbToOcbInitialsDict[mcbInitial][ocbInitialGroup] = ocbInitial

columnDict = {u"p": u"", u"m": u"", u"t": u"", u"n": u"", u"l": u"",
              u"r": u"", u"j": u"", u"ts": u"", u"s": u"", u"k": u"",
              u"?": u"", u"x": u"", u"H": u"", u"kw": u"", u"ngw": u"",
              u"?w": u"", u"hw": u"", u"w": u"", u"ng": u""}

intersectionDict = {u"p": 0, u"m": 0, u"t": 0, u"n": 0, u"l": 0,
              u"r": 0, u"j": 0, u"ts": 0, u"s": 0, u"k": 0,
              u"?": 0, u"x": 0, u"H": 0, u"kw": 0, u"ngw": 0,
              u"?w": 0, u"hw": 0, u"w": 0, u"ng": 0}

phoneticTableDict = {}
codepointId = 0              # The codepoint and its label in GSR cannot be used as the ID      
for line in featuresList:    # because some codepoints have multiple readings.
    codepoint = line[0]
    phonetic = line[1]
    mcbInitial  = line[3]
    gyHomophone = line[7]
    #ocVowel = line[6]
    if not phoneticTableDict.has_key(phonetic):
        phoneticTableDict[phonetic] = {"rows":{}}
    phoneticTableDict[phonetic]["rows"][codepointId] = {"columns": columnDict.copy()}
    phoneticTableDict[phonetic]["rows"][codepointId]["ocbinitials"] = []
    phoneticTableDict[phonetic]["rows"][codepointId]["codepoint"] = codepoint
    phoneticTableDict[phonetic]["rows"][codepointId]["homophone"] = gyHomophone
    # If the GSR codepoint is not in Guangyun then there is no OC initial to find
    # and ocVowel is u"-"
    # so we assign a null OC initial and count the row as assigned to it.
    if mcbInitial == u"-":
        phoneticTableDict[phonetic]["rows"][codepointId]["ocinitials"] = [u"-"] #!!!
    else:
        # For each row of emctoocinitials.txt beginning with emcInitial
        # get the OC initial in the OC vowel column (this may be the string u"")
        # and insert in into the table at the intersection of the row and the column.        
        for ocbInitialGroup in mcbToOcbInitialsDict[mcbInitial].keys():
            ocbInitial = mcbToOcbInitialsDict[mcbInitial][ocbInitialGroup]
            phoneticTableDict[phonetic]["rows"][codepointId]["columns"][ocbInitialGroup] = ocbInitial
    phoneticTableDict[phonetic]["intersections"] = intersectionDict.copy()
    codepointId += 1

# Use the tables to guess the correct OC initials.
codepointId = 0
ocbInitialsDict = {}
for tableId in phoneticTableDict.keys():
    table = phoneticTableDict[tableId]
    spentRows = []
    spentColumns = []
    totalRows = len(table["rows"])
    rows = table["rows"]
    columns = columnDict.keys()
    intersections = intersectionDict.copy()
    # Rows that were assigned a null initial are already spent.
    for row in rows:
        ocbInitials = table["rows"][row]["ocbinitials"]
        if ocbInitials != []:
            spentRows.append(row)
    # Recursively score the columns until all rows have an OC initial.
    # While there are rows with no OC initials
    while len(spentRows) < totalRows:
        # If the row has not been assigned an OC initial and
        # If the intersection of column and row is not empty,
        # increment the column score.
        for column in columns:
            if column not in spentColumns:
                for row in rows:
                    if row not in spentRows:
                        if table["rows"][row]["columns"][column] != u"":
                            intersections[column] +=1
        # What was the highest column score?
        maxScore = max(intersections.values())
        # Which columns scored highest?
        maxScoringColumns = []
        for column in columns:
            if intersections[column] == maxScore:
                maxScoringColumns.append(column)
        # Which rows intersect with those columns?
        for column in maxScoringColumns:
            for row in rows:
                if row not in spentRows:
                    ocbInitial = table["rows"][row]["columns"][column]
                    table["rows"][row]["ocbinitials"].append(ocbInitial)
                    spentRows.append(row)
                    spentColumns.append(column)
    # End of recursion.
    # Add initials to the dictionary.
    for row in table["rows"]:
        ocbInitials = table["rows"][row]["ocbinitials"]
        ocbInitialsDict[codepointId] = ocbInitials
        codepointId += 1

                    ############################
                    ### Old Chinese Readings ###
                    ############################

# Combine OC initials and OC finals

codepointId = 0
labials = [u"p",u"b",u"m"]
vowels = [u"a", u"e", u"i", u"ɨ", u"o", u"u",]
for codepoint in ocbInitialsDict:
    initialString = u""
    initials = ocbInitialsDict[codepointId]
    final = ocbFinalsDict[codepointId]
    finalError = u""
    if "??" in final:
        final = final.replace("??","")
        finalError = "No MC to OC mapping"
    if "!!" in final:
        final = final.replace("!!","")
        finalError = "MC not derived from OC"
    ocbVowel = u""
    for initial in initials:
        for vowel in vowels:
            if vowel in final:
                ocbVowel = vowel
        midpoint = final.find(ocbVowel)
        medial = final[:midpoint]
        rhyme = final[midpoint:]
        # construct a new medial (w)(r)(j)
        newMedial = u""
        # w
        isLabial = False
        for labial in labials:
            if labial in initial:
                isLabial = True
        if u"w" in initial or u"w" in final:
            if not isLabial:
                newMedial += u"w"
                initial = initial.replace(u"w",u"")
        # r
        if u"r" in initial and u"(r)" in medial:
            newMedial += u"r"
            initial = initial.replace(u"r",u"")
        elif u"(r)" in medial:
            newMedial += u"(r)"
        elif u"r" in initial or u"r" in medial:
            newMedial += u"r"
            initial = initial.replace(u"r",u"")
        # j
        if u"j" in initial or u"j" in medial:
            newMedial += u"j"
            initial = initial.replace(u"j",u"")
        initial = initial + newMedial 
        initialString += initial + u"/"
    initial = initialString[:-1]
    initial = u"[" + initial + u"]"
    initialError = u""
    if u"-" in initial:
        initialError = u"GSR codepoint not in Guangyun"
    ocbReading = initial + rhyme
    gsrDict[codepointId]["baxter"] = ocbReading
    gsrDict[codepointId]["baxterinitial"] = initialString[:-1]
    gsrDict[codepointId]["baxterfinal"] = final
    gsrDict[codepointId]["baxterfinalerror"] = finalError
    gsrDict[codepointId]["baxterinitialerror"] = initialError
    codepointId += 1

# Write to file.
f=codecs.open("..\\dicts\\gsrDict.py","wb")
pickle.dump(gsrDict,f)
f.close()
   
