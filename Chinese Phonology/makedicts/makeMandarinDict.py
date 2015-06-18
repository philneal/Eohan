import codecs, pickle
# -*- coding: utf-8 -*-

f=codecs.open('..\\sources\\Unihan.txt','r','utf8')
lines = []
for line in f:
    lines.append(line[:-1]) # lines end in "\n"
f.close()
lines=lines[102:-1] # the first 101 lines are an introduction, the last says end of file

toneDict = {u"iao": {1: u"iāo", 2: u"iáo", 3: u"iǎo", 4: u"iào", 5: u"iao"},
            u"uai": {1: u"uāi", 2: u"uái", 3: u"uǎi", 4: u"uài", 5: u"uai"},
            u"ai": {1: u"āi", 2: u"ái", 3: u"ǎi", 4: u"ài", 5: u"ai"},
            u"ao": {1: u"āo", 2: u"áo", 3: u"ǎo", 4: u"ào", 5: u"ao"},
            u"ia": {1: u"iā", 2: u"iá", 3: u"iǎ", 4: u"ià", 5: u"ia"},
            u"ua": {1: u"uā", 2: u"uá", 3: u"uǎ", 4: u"uà", 5: u"ua"},
            u"a": {1: u"ā", 2: u"á", 3: u"ǎ", 4: u"à", 5: u"a"},
            u"ei": {1: u"ēi", 2: u"éi", 3: u"ěi", 4: u"èi", 5: u"ei"},
            u"ie": {1: u"iē", 2: u"ié", 3: u"iě", 4: u"iè", 5: u"ie"},
            u"ue": {1: u"uē", 2: u"ué", 3: u"uě", 4: u"uè", 5: u"ue"},
            u"üe": {1: u"üē", 2: u"üé", 3: u"üě", 4: u"üè", 5: u"üe"},
            u"e": {1: u"ē", 2: u"é", 3: u"ě", 4: u"è", 5: u"e"},
            u"ui": {1: u"uī", 2: u"uí", 3: u"uǐ", 4: u"uì", 5: u"ui"},
            u"i": {1: u"ī", 2: u"í", 3: u"ǐ", 4: u"ì", 5: u"i"},
            u"io": {1: u"iō", 2: u"ió", 3: u"iǒ", 4: u"iò", 5: u"io"},
            u"ou": {1: u"ōu", 2: u"óu", 3: u"ǒu", 4: u"òu", 5: u"ou"},
            u"o": {1: u"ō", 2: u"ó", 3: u"ǒ", 4: u"ò", 5: u"o"},
            u"uo": {1: u"uō", 2: u"uó", 3: u"uǒ", 4: u"uò", 5: u"uo"},
            u"iu": {1: u"iū", 2: u"iú", 3: u"iǔ", 4: u"iù", 5: u"iu"},
            u"u": {1: u"ū", 2: u"ú", 3: u"ǔ", 4: u"ù", 5: u"u"},
            u"ü": {1: u"ǖ", 2: u"ǘ", 3: u"ǚ", 4: u"ǜ", 5: u"ü"}}
nuclei = [u"iao", u"uai", u"ai", u"ao", u"ia", u"ua", u"ei", u"ie", u"ue",
          u"üe", u"ui", u"io", u"ou", u"uo", u"iu", u"a", u"e", u"i", u"o", u"u",u"ü"] # must be this order so can't use keys()
mandarinDict = {}
id = 0
for line in lines:
    fields = line.split("\t")
    # ^[A-Z\x{308}]+[1-5]$
    if fields[1]=="kMandarin":
        codepoint = fields[0]
        values = fields[2]
        valueList = values.split(" ")
        for value in valueList:
            initial = value[0]
            if len(value[:-1]) > 1: # remove the tone sign
                second = value[1]
            else:
                second = u""
            mandarinDict[id] = {"codepoint":codepoint,"reading":value.lower(),"initial":initial,"second":second,"pinyin": u""}
            id += 1
for mandarinKey in mandarinDict.keys():
    reading = mandarinDict[mandarinKey]["reading"]
    tone = int(reading[-1])
    toneless = reading[:-1]
    found = False
    for toneKey in nuclei:
        if toneKey in toneless and found == False:
            pinyin = toneless.replace(toneKey,toneDict[toneKey][tone])
            found = True
    mandarinDict[mandarinKey]["pinyin"] = pinyin
    mandarinDict[mandarinKey]["tone"] = tone
    mandarinDict[mandarinKey]["toneless"] = toneless
    
f=codecs.open("..\\dicts\\mandarinDict.py","wb")
pickle.dump(mandarinDict,f)
f.close()
