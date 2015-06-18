import codecs, pickle

# dictionary of codepoints to glyphs
glyphTupleList = []
lines = []
keys = []
values = []
f=codecs.open('..\\sources\\unihan_codepoints.txt','r','utf-8')
for line in f:
    lines.append(line)
f.close()
lines[0] = lines[0][1:] # Cut start of file character u'\ufeff'
for line in lines:
    pair = line[:-2].split("\t") # -2 to cut "\r\n"
    codepointStr = pair[0]
    glyph = pair[1]
    glyphTuple = tuple([(codepointStr),(glyph)])
    glyphTupleList.append(glyphTuple)
    keys.append(codepointStr)
    values.append(glyph)
glyphTuples = tuple(glyphTupleList)
codepointToGlyphDict = dict(zip(keys, values))
glyphToCodepointDict = dict(zip(values,keys))

f=codecs.open("..\\dicts\\codepointToGlyphDict.py","wb")
pickle.dump(codepointToGlyphDict,f)
f.close()

f=codecs.open("..\\dicts\\glyphToCodepointDict.py","wb")
pickle.dump(glyphToCodepointDict,f)
f.close()

