# -*- coding: utf-8 -*-
import codecs, pickle

# Create dictionary of marginal annotations in Yunjing from yunjingannotions.txt.
# Column 0: rhyme number
# Column 1: rhyme label (top right hand margin of Yunjing)
# Column 2: fanqie (top right hand margin of Yunjing)
# Column 3: rusheng is qusheng (bottom right hand margin of Yunjing)
# Columns 4-7: keys to Guangyun/Qieyun (left hand margin of Yunjing)

yunjingAnnotationDict = {}
f=codecs.open("..\\sources\\yunjingannotations.txt","r","utf8")
lines = []
for line in f:
    lines.append(line[:-1]) # minus return character
f.close()
lines[0] = lines[0][1:] # cut start of file character
for line in lines:
    line = line.split("\t")
    rhymeNumber = int(line[0])
    yunjingAnnotationDict[rhymeNumber] = {}
    yunjingAnnotationDict[rhymeNumber]["rhymelabel"], \
    yunjingAnnotationDict[rhymeNumber]["fanqie"], \
    yunjingAnnotationDict[rhymeNumber]["rusheng"], \
    yunjingAnnotationDict[rhymeNumber]["gradekeys1"], \
    yunjingAnnotationDict[rhymeNumber]["gradekeys2"], \
    yunjingAnnotationDict[rhymeNumber]["gradekeys3"], \
    yunjingAnnotationDict[rhymeNumber]["gradekeys4"] = line[1:]
    
                                                

# Write to file.
f=codecs.open("..\\dicts\\yunjingAnnotationDict.py","wb")
pickle.dump(yunjingAnnotationDict,f)
f.close()
