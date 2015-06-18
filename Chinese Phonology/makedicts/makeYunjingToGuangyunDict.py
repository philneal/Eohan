# -*- coding: utf-8 -*-
import codecs, pickle

# Every filled cell of Yunjing, and some empty ones
# corresponds to a homophone group in Guangyun.
f=codecs.open("..\\sources\\yunjingtoguangyun.txt","r","utf8")
yunjingToGuangyunDict = {}
lines = []
for line in f:
    lines.append(line[:-2]) # dock "\r\n"
f.close()
lines[0] = lines[0][1:] # ffef
for line in lines:
    pair = line.split("\t")
    yunjingToGuangyunDict[int(pair[0])] = int(pair[1])

f=codecs.open("..\\dicts\\yunjingToGuangyunDict.py","wb")
pickle.dump(yunjingToGuangyunDict,f)
f.close()

