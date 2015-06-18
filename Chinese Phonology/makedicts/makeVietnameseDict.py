import codecs, pickle
# -*- coding: utf-8 -*-

f=codecs.open('..\\sources\\Unihan.txt','r','utf8')
lines = []
for line in f:
    lines.append(line[:-1]) # lines end in "\n"
f.close()
lines=lines[102:-1] # the first 101 lines are an introduction, the last says end of file

vietnameseDict = {}
id = 0
for line in lines:
    fields = line.split("\t")
    # ^[A-Z\x{308}]+[1-5]$
    if fields[1]=="kVietnamese":
        codepoint = fields[0]
        values = fields[2]
        valueList = values.split(" ")
        for value in valueList:
            vietnameseDict[id] = {"codepoint":codepoint,"reading":value.lower(),"initial": u""}
            id += 1

vietnameseUpperCaseDict = {u"a": u"A", 
                        u"b": u"B", 
                        u"c": u"C", 
                        u"d": u"D", 
                        u"e": u"E", 
                        u"g": u"G", 
                        u"h": u"H", 
                        u"i": u"I", 
                        u"k": u"K", 
                        u"l": u"L", 
                        u"m": u"M", 
                        u"n": u"N", 
                        u"o": u"O", 
                        u"p": u"P", 
                        u"q": u"Q", 
                        u"r": u"R", 
                        u"s": u"S", 
                        u"t": u"T", 
                        u"u": u"U", 
                        u"v": u"V", 
                        u"x": u"X", 
                        u"y": u"Y", 
                        u"à": u"A", 
                        u"á": u"A", 
                        u"â": u"A", 
                        u"ã": u"A", 
                        u"é": u"E", 
                        u"ê": u"E", 
                        u"ì": u"I", 
                        u"í": u"I", 
                        u"ó": u"O", 
                        u"ô": u"O", 
                        u"õ": u"O", 
                        u"ù": u"U", 
                        u"ú": u"U", 
                        u"ý": u"Y", 
                        u"ă": u"A", 
                        u"đ": u"Đ", 
                        u"ũ": u"U", 
                        u"ư": u"U", 
                        u"ạ": u"A", 
                        u"ả": u"A", 
                        u"ấ": u"A", 
                        u"ầ": u"A", 
                        u"ẩ": u"A", 
                        u"ẫ": u"A", 
                        u"ậ": u"A", 
                        u"ắ": u"A", 
                        u"ẵ": u"A", 
                        u"ẳ": u"A", 
                        u"ằ": u"A", 
                        u"ằ": u"A", 
                        u"ặ": u"E", 
                        u"ễ": u"E", 
                        u"ệ": u"E", 
                        u"ẽ": u"E", 
                        u"ẹ": u"E", 
                        u"è": u"E", 
                        u"ẻ": u"E", 
                        u"ể": u"E", 
                        u"ề": u"E", 
                        u"ế": u"E", 
                        u"ỉ": u"I", 
                        u"ĩ": u"I", 
                        u"ị": u"I", 
                        u"ọ": u"O", 
                        u"ỏ": u"O", 
                        u"ố": u"O", 
                        u"ồ": u"O", 
                        u"ổ": u"O", 
                        u"ộ": u"O", 
                        u"ớ": u"O", 
                        u"ở": u"O",
                        u"ò": u"O",
                        u"ợ": u"O",
                        u"ờ": u"O",
                        u"ỡ": u"O",
                        u"ỗ": u"O",
                        u"ơ": u"O",
                        u"ụ": u"U", 
                        u"ủ": u"U", 
                        u"ứ": u"U", 
                        u"ử": u"U", 
                        u"ự": u"U", 
                        u"ừ": u"U", 
                        u"ữ": u"U", 
                        u"ỷ": u"Y", 
                        u"ỳ": u"Y"}

for key in vietnameseDict.keys():
    initial = vietnameseDict[key]["reading"][0]
    initial = vietnameseUpperCaseDict[initial]
    if len(vietnameseDict[key]["reading"]) > 1:
        second = vietnameseDict[key]["reading"][1]
        second = vietnameseUpperCaseDict[second]
    else:
        second = u""
    vietnameseDict[key]["initial"] = initial
    vietnameseDict[key]["second"] = second
f=codecs.open("..\\dicts\\vietnameseDict.py","wb")
pickle.dump(vietnameseDict,f)
f.close()
