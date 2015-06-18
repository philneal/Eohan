# -*- coding: utf-8 -*-
import codecs, pickle, utilities

lineToCodepoints = utilities.lineToCodepoints
pp = utilities.pp

# The file emctooc.txt is a mapping of EMC finals to OC finals
# based on Pulleyblank, The Final Consonants of Old Chinese (Appendix)
# and Baxter, Old Chinese, ch. 5.
# Commented lines in the text supply the references with a summary.

###	侵 Qin I b
###	10.3.3
###	Pulleyblank:  	ə́m, jə́m, rə́m, ə̀m, wə̀m
###			78   85    81      94   45
###	Baxter:		ə́m, rə́m, ə̀m, ə̀m, ə̀m, ə̀m, ə̀m, rə̀m
###			78   81    45    94   94    45   94    94
###			jə́m, rə́m, jə̀m, ə̀m, ə̀m, rə̀m, ə̀m
###			85    81     94     94   94    94     94
###

f=codecs.open("..\\sources\\emctooc.txt","r","utf8")
lines = []
for line in f:
    lines.append(line[:-2]) # Cut end of line characters
f.close()
lines[0] = lines[0][1:] # Cut start of file character.

# Ignore commented lines.
emcToOcLines = []
for line in lines:
    if line[0] != "#":
        emcToOcLines.append(line)

# For four, read six: Karlgren has now been added to the file.

# The uncommented lines are intended to be read in sixes, referring to
# EMC, OCP, MCB, OCB, MCK, MCB (Middle Chinese and Old Chinese * Pulleyblank,
# Baxter and Karlgren's systems).
#
# Columns 0 to 4 refer to
# 0: Old Chinese rhyme (Pulleyblank system)
# 1: Guangyun pingsheng final
# 2: Guangyun shangsheng final
# 3: Guangyun qusheng final
# 4: Qieyun rhyme (for information, not actually used)
#    Not all finals appear in all tones, in which case 0 is used as a null.
#    Rusheng is assigned to column 1.
# Columns 5 to 8 refer to the four grades kaikou, 9 to 12 the four grades hekou.

##ǝm	50	105	165	78	ǝm	-	-	-	-	-	-	-	
##ǝm	50	105	165	78	ə́m	-	-	-	-	-	-	-	
##ǝm	50	105	165	78	om	-	-	-	-	-	-	-	
##ǝm	50	105	165	78	ɨm	-	-	-	-	-	-	-	
##ǝm	50	105	165	78	ậm	-	-	-	-	-	-	-	
##ǝm	50	105	165	78	ǝm	-	-	-	-	-	-	-	

kaiheStrings =   [u"kai",u"he"]
ocpToneStrings = [u"", u"ă", u"ʃ"]
ocbToneStrings = [u"", u"ʔ", u"s"]

# temp
mckChars = u""
ockChars = u""

featuresToOcList = []
lineCtr = 0
# Read the lines six at a time.
while lineCtr < len(emcToOcLines):
    emcLine = emcToOcLines[lineCtr   ]
    ocpLine = emcToOcLines[lineCtr +1]
    mcbLine = emcToOcLines[lineCtr +2]
    ocbLine = emcToOcLines[lineCtr +3]
    mckLine = emcToOcLines[lineCtr +4]
    ockLine = emcToOcLines[lineCtr +5]
    emcLine = emcLine.split("\t")
    ocpLine = ocpLine.split("\t")
    mcbLine = mcbLine.split("\t")
    ocbLine = ocbLine.split("\t")
    mckLine = mckLine.split("\t")
    ockLine = ockLine.split("\t")
    ocpRhyme = emcLine[0]          # ǝm
    ocbRhyme = mcbLine[0]       # ɨm
    ockRhyme = mckLine[0]       # ɨm
    finals = emcLine[1:4]       # 50 105 165
    qieyun = emcLine[4]         # 78 (not actually used)
    emcFinals = emcLine[5:13]   # ǝm	-	-	-	-	-	-	-
    ocpFinals = ocpLine[5:13]   # ə́m	-	-	-	-	-	-	-
    mcbFinals = mcbLine[5:13]   # ɨm	-	-	-	-	-	-	-
    ocbFinals = ocbLine[5:13]   # ɨm	-	-	-	-	-	-	-
    mckFinals = mckLine[5:13]   # ậm	-	-	-	-	-	-	-
    ockFinals = ockLine[5:13]   # ǝm	-	-	-	-	-	-	-
    finalCtr = 0
    while finalCtr < 8:
        emcFinal = emcFinals[finalCtr]
        ocpFinal = ocpFinals[finalCtr]
        mcbFinal = mcbFinals[finalCtr]
        ocbFinal = ocbFinals[finalCtr]
        mckFinal = mckFinals[finalCtr]
        ockFinal = ockFinals[finalCtr]
        gradeNum = str(finalCtr % 4 + 1)   # 1 2 3 4 1 2 3 4
        kaiheNum = finalCtr / 4            # 0 0 0 0 1 1 1 1
        grade = str(gradeNum)
        kaihe = kaiheStrings[kaiheNum]
        # ǝm
        if emcFinal != "-":             # If emcFinal is - then so are the rest.
            toneNum = 0
            while toneNum < 3:
                if finals[toneNum] != "0": # Ignore nulls.
                    # 50 105 165 ->  
                    # 50 kai 1
                    # 105 kai 1
                    # 165 kai 1
                    features = finals[toneNum] + " " + \
                                    kaihe + " " + \
                                    grade
                    # "ə́m" + "ă" -> "ə́mă"
                    # "ɨm" + "ʔ" -> "ɨmʔ"
                    ocpTone = ocpToneStrings[toneNum]
                    ocbTone = ocbToneStrings[toneNum]
                    ockTone = str(toneNum + 1)
                    ocp = ocpFinal + ocpTone
                    ocb = ocbFinal + ocbTone
                    ock = ockFinal + ockTone
                    # [
                    # ["50 kai 1", "ǝm", "ə́m", "ɨm"],
                    # ["105 kai 1", "ǝm", "ə́mă", "ɨmʔ"],
                    # ["165 kai 1", "ǝm", "ə́mʃ", "ɨms"] ...
                    featuresToOc = [features,ocpRhyme,ocbRhyme,ockRhyme,ocp,ocb,ock]
                    featuresToOcList.append(featuresToOc)
                toneNum += 1
        for char in mckFinal: # temp
            if char not in mckChars:
                mckChars += char
        for char in ockFinal: # temp
            if char not in ockChars:
                ockChars += char
        finalCtr += 1
    lineCtr += 6 # we are reading six lines at once

# temp
print mckChars
print ockChars

print "done featuresToOcList"

# list to dictionary

emcFinalToOcpFinalsDict = {}
for line in featuresToOcList:
    features = line[0]
    ocpRhyme = line[1]
    ocp = line[4]
    # 
    if emcFinalToOcpFinalsDict.has_key(features):
        emcFinalToOcpFinalsDict[features][ocpRhyme] = ocp
    else:
        emcFinalToOcpFinalsDict[features] = {ocpRhyme: ocp}
        
mcbFinalToOcbFinalsDict = {}
for line in featuresToOcList:
    features = line[0]
    ocbRhyme = line[2]
    if not mcbFinalToOcbFinalsDict.has_key(features):
        mcbFinalToOcbFinalsDict[features] = {ocbRhyme: {}}
    elif not mcbFinalToOcbFinalsDict[features].has_key(ocbRhyme):
        mcbFinalToOcbFinalsDict[features][ocbRhyme] = {}
for line in featuresToOcList:
    features = line[0]
    ocbRhyme = line[2]
    ocb = line[5]
    if u"a" in ocb:
        vowelType = "plain"
        rounded = ocb.replace(u"a",u"o")
        front = ocb.replace(u"a",u"e")
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["plain"] = ocb
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["rounded"] = rounded
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["front"] = front
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["height"] = "low"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["type"] = vowelType
    elif u"ɨ" in ocb:
        vowelType = "plain"
        rounded = ocb.replace(u"ɨ",u"u")
        front = ocb.replace(u"ɨ",u"i")
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["plain"] = ocb
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["rounded"] = rounded
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["front"] = front
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["height"] = "high"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["type"] = vowelType
    elif u"e" in ocb:
        vowelType = "front"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["front"] = ocb
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["height"] = "low"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["type"] = vowelType
    elif u"i" in ocb:
        vowelType = "front"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["front"] = ocb
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["height"] = "high"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["type"] = vowelType
    elif u"o" in ocb:
        vowelType = "rounded"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["rounded"] = ocb #front
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["height"] = "low"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["type"] = vowelType
    elif u"u" in ocb:
        vowelType = "rounded"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["rounded"] = ocb # front
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["height"] = "high"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["type"] = vowelType
    elif u"A" in ocb:
        vowelType = "plain"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["plain"] = ocb
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["height"] = "low"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["type"] = vowelType
    elif u"-" in ocb:
        vowelType = "none"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["none"] = ocb
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["height"] = "none"
        mcbFinalToOcbFinalsDict[features][ocbRhyme]["type"] = vowelType

mckFinalToOckFinalsDict = {}
for line in featuresToOcList:
    features = line[0]
    ockRhyme = line[3]
    ock = line[6]
    # 
    if mckFinalToOckFinalsDict.has_key(features):
        mckFinalToOckFinalsDict[features][ockRhyme] = ock
    else:
        mckFinalToOckFinalsDict[features] = {ockRhyme: ock}
        
f=codecs.open("..\\dicts\\emcFinalToOcpFinalsDict.py","wb")
pickle.dump(emcFinalToOcpFinalsDict,f)
f.close()

f=codecs.open("..\\dicts\\mcbFinalToOcbFinalsDict.py","wb")
pickle.dump(mcbFinalToOcbFinalsDict,f)
f.close()

f=codecs.open("..\\dicts\\mckFinalToOckFinalsDict.py","wb")
pickle.dump(mckFinalToOckFinalsDict,f)
f.close()

