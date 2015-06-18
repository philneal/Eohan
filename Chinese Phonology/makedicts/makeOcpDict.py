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

f=codecs.open("..\\dicts\\emcFinalToOcpFinalsDict.py","rb")
emcFinalToOcpFinalsDict = pickle.load(f)
f.close()

# tone endings
toneDict = {0: u"",1: u"ă", 2: u"ʃ", 3:u"", u"-": u""}

# A dictionary of cross rhymes (explained below)
f=codecs.open("..\\sources\\ocpcrossrhymes.txt","r","utf8")
lines = []
for line in f:
    lines.append(line[:-2]) # Cut end of line characters
f.close()
lines[0] = lines[0][1:] # Cut start of file character.
ocpCrossRhymeDict = {}
for line in lines:
    line = line.split("\t")
    ocpRhyme = line[0]
    crossRhymes = line[1].split(" ")
    ocpCrossRhymeDict[ocpRhyme] = crossRhymes

# A list holding the information needed to generate
# Old Chinese.
#
# To generate Old Chinese finals we need to know
# the OC rhyme and the EMC final, kaihe and grade.
#
# To generate Old Chinese initials we need to know
# the EMC initial, OC vowel and the phonetic series.

featuresList = []
for key in gsrDict.keys():
    codepoint = gsrDict[key]["codepoint"]
    phonetic = gsrDict[key]["phonetic"]
    gyHomophone = gsrDict[key]["homophone"]
    # Here, gsrRhyme means a section of GSR:
    # ocpRhyme means its value in the Pulleyblank system.
    gsrRhyme = gsrPhoneticDict[phonetic]
    ocpRhyme = gsrRhymeDict[gsrRhyme]["pulleyblank"]
    if emcFeaturesDict.has_key(gyHomophone):
        guangyunRhyme = int(emcFeaturesDict[gyHomophone]["guangyunrhyme"]) # temp
        emcInitial = emcFeaturesDict[gyHomophone]["emcinitial"]
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
        featuresList.append([codepoint,phonetic,ocpRhyme,emcInitial,emcFeatureString,gyHomophone,gyTone,gyType])
        # From now on, we refer to ocpRhyme just as rhyme.
    else:
        featuresList.append([codepoint,phonetic,ocpRhyme,u"-",u"-",u"-",u"-",u"-",u"-"])


                    ##########################
                    ### Old Chinese Finals ###
                    ##########################


    
# Karlgren did not distinguish between the Pulleyblank OC rhymes ǝl (Wei 微) and ǝj (Zhi 脂).
# By default we assign a codepoint to ǝl (Wei 微) and reassign to ǝj (Zhi 脂) on the basis
# of the Guangyun. See Baxter, Old Chinese, p. 448.
#
# OC Zhi 脂 corresponds to Guangyun rhyme Qi 15 齊, and
# OC Wei 微 corresponds to Guanyun rhymes Hui 8 灰, Hai 7 咍, Wei 19 微
# except that 
# OC Zhi 脂 corresponds to Guangyun rhymess Zhi 17 脂 kaikou, Jie 10 皆 kaikou, and
# OC Wei 微 corresponds to Guangyun rhymes Zhi 17 脂 hekou, Jie 10 皆 hekou
# except that 
# phonetics gui 癸 and ji 季 are in Zhi 脂.
#
# Guangyun rhyme Qi 齊 has finals 12, 68, 124
# Guangyun rhyme Zhi 脂 has finals 6, 62, 118
# Guangyun rhyme Jie 皆 has finals 14, 70, 128
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
        line[2] = u'ǝj' # Change the OC rhyme from ǝl to ǝj.

# Generate OCP finals from OC rhyme and EMC features by lookup in the
# dictionary emcFinalToOcpFinal.
#
# Normally, this will be emcFinalToOcpFinal[emcFeatureString][ocpRhyme].
#
# However, not every character in a phonetic series belongs to the
# same OC rhyme as its phonetic: e.g. a character whose phonetic is
# in rhyme am may itself be in rhymes ǝm or ap. We call ǝm and ap
# the cross rhymes of am. If normal lookup fails, we look up on the
# cross rhymes and EMC features.
#
# Where several cross rhyme lookups succeed, we generate the OCP final
# from the last successful lookup, but this is a kludge.

### DEBUG
missed = []

ocpFinalsDict = {}
lineCtr = 0
for line in featuresList:
    ocpFinal = "None"
    codepoint = line[0]
    ocpRhyme = line[2]
    emcFeatureString = line[4]
    gyHomophone = line[5]
    crossRhymes = ocpCrossRhymeDict[ocpRhyme]
    gyTone = line[6]
    gyType = line[7]
    # The default when lookup fails.
    if not emcFinalToOcpFinalsDict.has_key(emcFeatureString):
        toneSign = toneDict[gyTone]
        ocpFinal = ocpRhyme + toneSign + u"??" # ocpFinal = u"-"
        if not [ocpRhyme,emcFeatureString] in missed: ### DEBUG
            missed.append([ocpRhyme,emcFeatureString])
    # Normal lookup.
    elif emcFinalToOcpFinalsDict[emcFeatureString].has_key(ocpRhyme):
        ocpFinal = emcFinalToOcpFinalsDict[emcFeatureString][ocpRhyme]
    # Cross rhyme lookup.
    elif len(crossRhymes) > 0:
        for crossRhyme in crossRhymes:
            if emcFinalToOcpFinalsDict[emcFeatureString].has_key(crossRhyme):
                ocpFinal = emcFinalToOcpFinalsDict[emcFeatureString][crossRhyme]
    if ocpFinal == "None": # redundant?
        toneSign = toneDict[gyTone]
        ocpFinal = ocpRhyme + toneSign + u"!!" # ocpFinal = u"-"
        ocpFinalsDict[lineCtr] = ocpFinal
    # Add the final to the dictionary.
    ocpFinalsDict[lineCtr] = ocpFinal
    # Add the vowel of the final to featuresList for use in generating initials
    ocpVowels = [u"á",u"ə́",u"à",u"ə̀"]
    ocpVowel = u"-"
    for vowelCtr in range(0,4):
        if  ocpVowels[vowelCtr] in ocpFinal:
            ocpVowel = ocpVowels[vowelCtr]
    if ocpVowel == u"-":
        if u"a" in ocpFinal and gyType == u"A":
            ocpVowel = u"á"
        elif u"a" in ocpFinal and gyType == u"B":
            ocpVowel = u"a"
        elif u"ǝ" in ocpFinal and gyType == u"A":
            ocpVowel = u"ə́"
        elif u"ǝ" in ocpFinal and gyType == u"B":
            ocpVowel = u"ə̀"
        elif u"a" in ocpFinal: 
            ocpVowel = u"a"
        elif u"ǝ" in ocpFinal:
            ocpVowel = u"ǝ"
    line.append(ocpVowel)
    lineCtr += 1

                    ############################
                    ### Old Chinese Initials ###
                    ############################

# Strategy

# The initial consonants of Old Chinese are not known with any
# certainty, and the reconstructions of Pulleyblank and Baxter
# involve personal judgment. This algorithm is only intended
# to give conjectural values.

# Every consonantal initial of Old Chinese developed into an
# Early Middle Chinese initial, but which particular EMC initial it
# develops into depends on the vowel which follows it: for instance
# OC ná becomes EMC na but OC nà becomes EMC ɲɨa. In the following
# table, columns represent OC vowels, rows represent OC initials
# and cell entries represent the resulting EMC initial. OC initials
# fall into groups such that, if a phonetic series contains one
# initial from a given group it many contain any other initial from
# that group: the grouping of rows in the table reflects this.
#
##
##	   	|	á	ə́	à	ə̀
##      -------------------------------------------
##	n:  n	|	n	n			
##	    n	|			ɲ	ɲ	
##	    nr	|	nr	nr	nr	nr
##      --------|----------------------------------
##	p:  p	|	p	p	p	p
##	    ăp	|	b	b	b	b
##	    p-p	|	p‘	p‘	p‘	p‘
##          ...
##          ...
#
# To determine what Old Chinese initial an Early Middle Chinese
# initial is derived from, we start with a similar table
# but with rows representing EMC initials and cell values
# representing the corresponding OC initials.
#
##			á	ə́	à	ə̀
##      --------|----------------------------------
##	n  n	|	n	n			
##	ɲ  n	|	        	n	n
##	nr n	|	nr	nr	nr	nr
##      --------|----------------------------------
##	p  p	|	p	p	p	p
##	b  p	|	ăp	ăp	ăp	ăp
##	p‘ p	|	p-p	p-p	p-p	p-p
##      ...
##      ...
##
# The file emctoocinitials.txt holds such a table:
# it is mainly based on Pulleyblank, The Ganzhi as Phonograms
# augmented by remarks elsewhere in his publications.
#
# We read it into emcToOcInitialsDict.
#
# Since many EMC initials can be derived from more than
# one OC initial (e.g. EMC tɕ may come from OC t or k)
# we need to make a best guess at which one. We proceed
# on the principle that a phonetic series should include
# as few OC initial groups as possible.

## A phonetic series such as 104 has EMC initials m, p which
## may be reflexes of OC initial groups m, ŋw, p.
## This can be represented as a table, which we shall construct for each phonetic series:

##104			        xj xɥ ʔ xw ŋɥ ŋj ŋ ŋw x ɣ ɥ kɥ kj k j m l n p s kw t w Cr 
##			        0  0  0 0  0  0  0 2  0 0 0 0  0  0 0 2 0 0 2 0 0  0 0 0
##
##104a 武	muăˀ	wàɣă	-  -  - -  -  -  - ŋw - - - -  -  - - m - - - - -  - - -  [898]
##104f 鵡	muăˀ	wàɣă	-  -  - -  -  -  - ŋw - - - -  -  - - m - - - - -  - - -  [899]
##104g 賦	puăʰ	wàɣʃ	-  -  - -  -  -  - -  - - - -  -  - - - - - p - -  - - -  [900]

# Two assignments of OC initials minimise the number of initial groups in the series:

##104a 武	muăˀ < ŋwàɣă	 and	muăˀ < màɣă
##104f 鵡	muăˀ < ŋwàɣă	 	muăˀ < màɣă
##104g 賦	puăʰ < pàɣʃ		puăʰ < pàɣʃ

# The table is implemented as a dictionary of dictionaries
# representing rows and columns like this:
## phoneticTableDict = {...
##                       {104:
##                           {104a: {u"xj": u"", u"xɥ": u"", u"ʔ": u"", u"xw": u"", u"ŋɥ": u"",
##                                   u"ŋj": u"", u"ŋ": u"", u"ŋw": u"ŋw", u"x": u"", u"ɣ": u"",
##                                                                 ****
##                                   u"ɥ": u"", u"kɥ": u"", u"kj": u"", u"k": u"", u"j": u"",
##                                   u"m": u"m", u"l": u"", u"n": u"", u"p": u"", u"s": u"",
##                                         ***
##                                   u"kw": u"", u"t": u"", u"w": u"", u"Cr"},
##                           {104f: {u"xj": u"", u"xɥ": u"", u"ʔ": u"", u"xw": u"", u"ŋɥ": u"",
##                                   u"ŋj": u"", u"ŋ": u"", u"ŋw": u"ŋw", u"x": u"", u"ɣ": u"",
##                                                                 ****
##                                   u"ɥ": u"", u"kɥ": u"", u"kj": u"", u"k": u"", u"j": u"",
##                                   u"m": u"m", u"l": u"", u"n": u"", u"p": u"", u"s": u"",
##                                         ***
##                                   u"kw": u"", u"t": u"", u"w": u"", u"Cr"},
##                           {104g: {u"xj": u"", u"xɥ": u"", u"ʔ": u"", u"xw": u"", u"ŋɥ": u"",
##                                   u"ŋj": u"", u"ŋ": u"", u"ŋw": u"ŋw", u"x": u"", u"ɣ": u"",
##                                   u"ɥ": u"", u"kɥ": u"", u"kj": u"", u"k": u"", u"j": u"",
##                                   u"m": u"m", u"l": u"", u"n": u"", u"p": u"p", u"s": u"",
##                                                                     ****
##                                   u"kw": u"", u"t": u"", u"w": u"", u"Cr"}} ...

# Our algorithm selects the columns intersecting with the most rows,
# assigns the column values to the rows, and recurses on the remaining
# rows until all have been assigned values.

# Make emcToOcInitialsDict

# Read file
lines = []
f=codecs.open("..\\sources\\emctoocinitials.txt","r","utf8")
for line in f:
    line = line[:-2] # Cut end of line characters
    lines.append(line)
f.close()
lines[0] = lines[0][1:] # Cut start of file character
emcToOcInitialLines = []

emcToOcInitialsDict = {}
for line in lines[2:]: # The first two lines are a header
    line = line.split("\t")
    emcInitial= line[0]
    ocInitialGroup = line[1]
    ocInitial1 = line[2]
    ocInitial2 = line[3]
    ocInitial3 = line[4]
    ocInitial4 = line[5]
    if not emcToOcInitialsDict.has_key(emcInitial):
        emcToOcInitialsDict[emcInitial] = {}
    emcToOcInitialsDict[emcInitial][ocInitialGroup] = {}
    emcToOcInitialsDict[emcInitial][ocInitialGroup][u"á"] = ocInitial1
    emcToOcInitialsDict[emcInitial][ocInitialGroup][u"ə́"] = ocInitial2
    emcToOcInitialsDict[emcInitial][ocInitialGroup][u"à"] = ocInitial3
    emcToOcInitialsDict[emcInitial][ocInitialGroup][u"ə̀"] = ocInitial4

# Create phoneticTableDict.
# Two dictionaries used in each table.
# The column dictionary: initialised to empty strings
columnDict = {u"xj": u"", u"xɥ": u"", u"ʔ": u"", u"xw": u"", u"ŋɥ": u"",u"ŋj": u"",
              u"ŋ": u"", u"ŋw": u"", u"x": u"", u"ɣ": u"",u"ɥ": u"", u"kɥ": u"",
              u"kj": u"", u"k": u"", u"j": u"",u"m": u"", u"l": u"", u"n": u"",
              u"p": u"", u"s": u"",u"kw": u"", u"t": u"", u"w": u"", u"Cr": u""}
# Holds the number of rows the columns intersect with: initialised to 0
intersectionDict = {u"xj": 0, u"xɥ": 0, u"ʔ": 0, u"xw": 0, u"ŋɥ": 0,u"ŋj": 0,
              u"ŋ": 0, u"ŋw": 0, u"x": 0, u"ɣ": 0,u"ɥ": 0, u"kɥ": 0,
              u"kj": 0, u"k": 0, u"j": 0,u"m": 0, u"l": 0, u"n": 0,
              u"p": 0, u"s": 0,u"kw": 0, u"t": 0, u"w": 0, u"Cr": 0}

phoneticTableDict = {}
codepointId = 0              # The codepoint and its label in GSR cannot be used as the ID      
for line in featuresList:    # because some codepoints have multiple readings.
    codepoint = line[0]
    phonetic = line[1]
    emcInitial  = line[3]
    gyHomophone = line[5]
    ocVowel = line[8]
    if not phoneticTableDict.has_key(phonetic):
        phoneticTableDict[phonetic] = {"rows":{}}
        phoneticTableDict[phonetic]["spentrows"] = []
        phoneticTableDict[phonetic]["spentcolumns"] = []
    phoneticTableDict[phonetic]["rows"][codepointId] = {"columns": columnDict.copy()}
    phoneticTableDict[phonetic]["rows"][codepointId]["ocinitials"] = []
    phoneticTableDict[phonetic]["rows"][codepointId]["codepoint"] = codepoint
    phoneticTableDict[phonetic]["rows"][codepointId]["homophone"] = gyHomophone
    phoneticTableDict[phonetic]["rows"][codepointId]["emcinitial"] = emcInitial
    # If the GSR codepoint is not in Guangyun then there is no OC initial to find
    # and ocVowel is u"-"
    # so we assign a null OC initial and count the row as assigned to it.
    if emcInitial == u"-":
        phoneticTableDict[phonetic]["rows"][codepointId]["ocinitials"] = [u"-"]
        phoneticTableDict[phonetic]["spentrows"].append(codepointId)
    else:
        # For each row of emctoocinitials.txt beginning with emcInitial
        # get the OC initial in the OC vowel column (this may be the string u"")
        # and insert in into the table at the intersection of the row and the column.        
        for ocInitialGroup in emcToOcInitialsDict[emcInitial].keys():
            if emcToOcInitialsDict[emcInitial][ocInitialGroup].has_key(ocVowel):
                ocInitial = emcToOcInitialsDict[emcInitial][ocInitialGroup][ocVowel]
            else:
                ocInitial = u"*"
            phoneticTableDict[phonetic]["rows"][codepointId]["columns"][ocInitialGroup] = ocInitial
    phoneticTableDict[phonetic]["intersections"] = intersectionDict.copy()
    # EMC initials with no corresponding OC initial in Pulleyblank's scheme
    intersectionCount = 0
    for  column in columnDict.keys():
        if phoneticTableDict[phonetic]["rows"][codepointId]["columns"][column] != u"":
            intersectionCount += 1
    if intersectionCount == 0:
        phoneticTableDict[phonetic]["spentrows"].append(codepointId)
    codepointId += 1

# Use the tables to guess the correct OC initials.
codepointId = 0
ocpInitialsDict = {}
for tableId in phoneticTableDict.keys():
    table = phoneticTableDict[tableId]
    spentRows = phoneticTableDict[tableId]["spentrows"]
    spentColumns = []
    totalRows = len(table["rows"])
    rows = table["rows"]
    columns = columnDict.keys()
    intersections = intersectionDict.copy()
    # Rows that were assigned a null initial are already spent.
    for row in rows:
        ocInitials = table["rows"][row]["ocinitials"]
        if ocInitials != []:
            spentRows.append(row)
    # Recursively score the columns until all rows have an OC initial.
    # While there are rows with no OC initials
    while len(spentRows) < totalRows:
        # If the row has not been assigned an OC initial and
        # If the intersection of column and row is not empty,
        # increment the column score.
        intersections = intersectionDict.copy()
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
        maxScoringColumns.sort() # A hack: where there is a choice of e.g. ŋɥ and m we want m.
        # Which rows intersect with those columns?
        for column in maxScoringColumns:
            for row in rows:
                ocInitial = table["rows"][row]["columns"][column]
                if row not in spentRows and ocInitial != u"":
                    table["rows"][row]["ocinitials"].append(ocInitial)
                    spentRows.append(row)
                    spentColumns.append(column)
    # End of recursion.
    # Add initials to the dictionary.
    for row in table["rows"]:
        ocInitials = table["rows"][row]["ocinitials"]
        ocpInitialsDict[row] = ocInitials
        codepointId += 1

                    ############################
                    ### Old Chinese Readings ###
                    ############################

# Combine OC initials and OC finals

##codepointId = 0
##vowels = [u"á", u"à", u"ə́", u"ə̀"]
##labials = [u"p",u"b",u"m"]
##for codepoint in ocpInitialsDict:
##    initialString = u""
##    initials = ocpInitialsDict[codepointId]
##    final = ocpFinalsDict[codepointId]
##    finalError = u""
##    if "??" in final:
##        final = final.replace("??","")
##        finalError = "No MC to OC mapping"
##    if "!!" in final:
##        final = final.replace("!!","")
##        finalError = "MC not derived from OC"
##    ocVowel = u""
##    for initial in initials:
##        for vowel in vowels:
##            if vowel in final:
##                ocVowel = vowel
##        midpoint = final.find(ocVowel)
##        medial = final[:midpoint]
##        rhyme = final[midpoint:]
##        # construct a new medial (w)(r)(j)
##        newMedial = u""
##        # w
##        isLabial = False
##        for labial in labials:
##            if labial in initial:
##                isLabial = True
##        if u"ɥ" in initial:
##            newMedial += u"ɥ"
##        elif u"w" in initial or u"w" in final:
##            if not isLabial:
##                newMedial += u"w"
##                initial = initial.replace(u"w",u"")
##        # r
##        if u"r" in initial and u"(r)" in medial:
##            newMedial += u"r"
##            initial = initial.replace(u"r",u"")
##        elif u"(r)" in medial:
##            newMedial += u"(r)"
##        elif u"r" in initial or u"r" in medial:
##            newMedial += u"r"
##            initial = initial.replace(u"r",u"")
##        # j
##        if u"j" in initial or u"j" in medial:
##            newMedial += u"j"
##            initial = initial.replace(u"j",u"")
##        initial = initial + newMedial
##        initialString += initial + u"/"
##    initial = initialString[:-1]
##    # Rewrite hyphen as non-breaking hyphen
##    initial = initial.replace(u"-",u"\u2011")
##    initial = u"[" + initial + u"]"
##    initialError = u""
##    if "[-" in initial:
##        initialError = u"GSR character not in Guangyun"
##    if "*" in initial:
##        initialError = u"No mapping from MC to OC"
##    if "[" in final:
##        finalError = u"Guessed mapping from MC to  OC"
##    ocpReading = initial + rhyme
##    gsrDict[codepointId]["pulleyblank"] = ocpReading
##    gsrDict[codepointId]["pulleyblankinitial"] = initialString[:-1]
##    gsrDict[codepointId]["pulleyblankfinal"] = final
##    gsrDict[codepointId]["pulleyblankfinalerror"] = finalError
##    gsrDict[codepointId]["pulleyblankinitialerror"] = initialError
##    codepointId += 1

codepointId = 0
vowels = [u"á", u"à", u"ə́", u"ə̀"]
labials = [u"p",u"b",u"m"]
for codepoint in ocpInitialsDict:
    initialString = u""
    initials = ocpInitialsDict[codepointId]
    final = ocpFinalsDict[codepointId]
    finalError = u""
    if "??" in final:
        final = final.replace("??","")
        finalError = "No MC to OC mapping"
    if "!!" in final:
        final = final.replace("!!","")
        finalError = "MC not derived from OC"
    ocVowel = u""
    for initial in initials:
        for vowel in vowels:
            if vowel in final:
                ocVowel = vowel
        midpoint = final.find(ocVowel)
        medial = final[:midpoint]
        rhyme = final[midpoint:]
        # construct a new medial (w)(r)(j)
        newMedial = u""
        # w
        isLabial = False
        for labial in labials:
            if labial in initial:
                isLabial = True
        if u"ɥ" in initial:
            newMedial += u"ɥ"
        elif u"w" in initial or u"w" in final:
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
    # Rewrite hyphen as non-breaking hyphen
    initial = initial.replace(u"-",u"\u2011")
    initial = u"[" + initial + u"]"
    initialError = u""
    if "[-" in initial:
        initialError = u"GSR character not in Guangyun"
    if "*" in initial:
        initialError = u"No mapping from MC to OC"
    if "[" in final:
        finalError = u"Guessed mapping from MC to  OC"
    ocpReading = initial + rhyme
    gsrDict[codepointId]["pulleyblank"] = ocpReading
    gsrDict[codepointId]["pulleyblankinitial"] = initialString[:-1]
    gsrDict[codepointId]["pulleyblankfinal"] = final
    gsrDict[codepointId]["pulleyblankfinalerror"] = finalError
    gsrDict[codepointId]["pulleyblankinitialerror"] = initialError
    codepointId += 1

# Write to file.
f=codecs.open("..\\dicts\\gsrDict.py","wb")
pickle.dump(gsrDict,f)
f.close()

