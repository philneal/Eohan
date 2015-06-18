import sqlite3, codecs, pickle, os, utilities
# -*- coding: utf-8 -*-

# Make the dictionaries.
##os.chdir("makedicts")
##execfile("makeChinesePhonologyDicts.py")
##print "made dictionaries"
##os.chdir("..\\")

# Get codepoints to glyphs
f=codecs.open("dicts\\codepointToGlyphDict.py","rb")
codepointToGlyphDict = pickle.load(f)
f.close()

# The table glyph contains the whole of Unihan. We want to identify which glyphs 
# actually occur in the historical sources as we add them to the database. We
# initialise glyphOccurrenceDict to 0 for each glyph and alter it to 1 as we proceed.

glyphOccurrenceDict = {} 
for key in codepointToGlyphDict.keys():
    glyphOccurrenceDict[key] = 0

# Two statements used to create all the tables
beginSmt = "BEGIN"
commitSmt = "COMMIT"

           ############################################
           ##               Glyphs                   ##
           ############################################

# Create glyph table
con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()
createSmt = "CREATE TABLE glyph(id INTEGER PRIMARY KEY, " \
            "codepoint TEXT UNIQUE, " \
            "glyph TEXT, " \
            "occurrence INTEGER)"
indexSmt =  "CREATE INDEX glyph_idx ON glyph(id,codepoint,glyph,occurrence)"
cur.execute(createSmt)
cur.execute(indexSmt)
con.close()

# We fill each table by converting the input dictionary to tuples and passing
# a tuple of tuples to an INSERT statement.

# Create glyph tuples
# Dictionary to list
glyphList = []
for key in codepointToGlyphDict:
    value = codepointToGlyphDict[key]
    decimal = int(key[2:],16) # input is string
    glyphList.append([decimal,key,value])
glyphList.sort()
# List to tuples
glyphTupleList = []
id = 0
for pair in glyphList:
    codepoint = pair[1]
    glyph = codepointToGlyphDict[codepoint]
    glyphTuple = tuple([id,codepoint,glyph,0])
    glyphTupleList.append(glyphTuple)
    id += 1
glyphTuples = tuple(glyphTupleList)

# Fill glyph table 
con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()
insertSmt = "INSERT INTO glyph(id, codepoint, glyph, occurrence) VALUES (?, ?, ?, ?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,glyphTuples)
cur.execute(commitSmt)
con.close()
print "Done glyph table."

           ############################################
           ##            Zhongyuan Yinyun            ##
           ############################################

# Create Zhongyuan Yinyun tables
con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()

createSmt = "CREATE TABLE zhongyuanyinyun(id INTEGER PRIMARY KEY, " \
            "codepoint TEXT, " \
            "glyph TEXT, " \
            "homophone INTEGER, " \
            "annotation TEXT, " \
            "FOREIGN KEY(homophone) REFERENCES zyhomophone(id))"
indexSmt = "CREATE INDEX zhongyuanyinyun_idx ON " \
           "zhongyuanyinyun(id,codepoint,glyph,homophone,annotation)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE zyhomophone(id INTEGER PRIMARY KEY, " \
            "number TEXT, " \
            "final INTEGER, " \
            "FOREIGN KEY (final) REFERENCES zyfinal(id)," \
            "FOREIGN KEY (final) REFERENCES earlymandarin(id))"
indexSmt =  "CREATE INDEX zyhomophone_idx ON zyhomophone(id,number,final)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE zyfinal(id INTEGER PRIMARY KEY, " \
            "number TEXT, " \
            "tonenumber TEXT, " \
            "toneletter TEXT, " \
            "label TEXT, " \
            "rhyme INTEGER, " \
            "FOREIGN KEY(rhyme) REFERENCES zyrhyme(id))"
indexSmt =  "CREATE INDEX zyfinal_idx ON zyfinal(id,number,tonenumber,toneletter,label,rhyme)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE zyrhyme(id INTEGER PRIMARY KEY, " \
            "number TEXT, " \
            "label TEXT)"
indexSmt =  "CREATE INDEX zyrhyme_idx ON zyrhyme(id,number,label)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE earlymandarin(id INTEGER PRIMARY KEY, " \
            "reading TEXT)"
indexSmt =  "CREATE INDEX earlymandarin_idx ON earlymandarin(id,reading)"
cur.execute(createSmt)
cur.execute(indexSmt)

con.close()

# Get values from the Zhongyuanyinyun dictionaries

f=codecs.open("dicts\\zhongyuanYinyunDict.py","rb")
zhongyuanYinyunDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\earlyMandarinDict.py","rb")
earlyMandarinDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\zhongyuanYinyunHomophoneDict.py","rb")
zhongyuanYinyunHomophoneDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\zhongyuanYinyunFinalDict.py","rb")
zhongyuanYinyunFinalDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\zhongyuanYinyunRhymeDict.py","rb")
zhongyuanYinyunRhymeDict = pickle.load(f)
f.close()

zhongyuanYinyunTupleList = []
for zyId in zhongyuanYinyunDict:
    codepoint = zhongyuanYinyunDict[zyId]["codepoint"]
    glyph = zhongyuanYinyunDict[zyId]["glyph"]
    homophone = zhongyuanYinyunDict[zyId]["homophone"]
    annotation = zhongyuanYinyunDict[zyId]["annotation"]
    if glyphOccurrenceDict[codepoint] == 0:
        glyphOccurrenceDict[codepoint] = 1
    zhongyuanYinyunTupleList.append(tuple([zyId,codepoint,glyph,homophone,annotation]))
zhongyuanYinyunTuple = tuple(zhongyuanYinyunTupleList)

zhongyuanYinyunHomophoneTupleList = []
for zyId in zhongyuanYinyunHomophoneDict:
    number = zhongyuanYinyunHomophoneDict[zyId]["number"]
    final = zhongyuanYinyunHomophoneDict[zyId]["final"]
    zhongyuanYinyunHomophoneTupleList.append(tuple([zyId,number,final]))
zhongyuanYinyunHomophoneTuple = tuple(zhongyuanYinyunHomophoneTupleList)
    
zhongyuanYinyunFinalTupleList = []
for zyId in zhongyuanYinyunFinalDict:
    number = zhongyuanYinyunFinalDict[zyId]["number"]
    tonenumber = zhongyuanYinyunFinalDict[zyId]["tonenumber"]
    toneletter = zhongyuanYinyunFinalDict[zyId]["toneletter"]
    label = zhongyuanYinyunFinalDict[zyId]["label"]
    rhyme = zhongyuanYinyunFinalDict[zyId]["rhyme"]
    zhongyuanYinyunFinalTupleList.append(tuple([zyId,number,tonenumber,toneletter,label,rhyme]))
zhongyuanYinyunFinalTuple = tuple(zhongyuanYinyunFinalTupleList)

zhongyuanYinyunRhymeTupleList = []
for zyId in zhongyuanYinyunRhymeDict:
    id = zhongyuanYinyunRhymeDict[zyId]["id"]
    number = zhongyuanYinyunRhymeDict[zyId]["number"]
    label = zhongyuanYinyunRhymeDict[zyId]["label"]
    zhongyuanYinyunRhymeTupleList.append(tuple([id,number,label]))
zhongyuanYinyunRhymeTuple = tuple(zhongyuanYinyunRhymeTupleList)
                                                  
earlyMandarinTupleList = []
for emId in earlyMandarinDict:
    id = earlyMandarinDict[emId]["id"]
    reading = earlyMandarinDict[emId]["reading"]
    earlyMandarinTupleList.append(tuple([id,reading]))
earlyMandarinTuple = tuple(earlyMandarinTupleList)

con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()

insertSmt = "INSERT INTO zhongyuanyinyun(id,codepoint,glyph,homophone,annotation) " +\
            "VALUES (?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,zhongyuanYinyunTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO zyhomophone(id,number,final) " +\
            "VALUES (?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,zhongyuanYinyunHomophoneTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO zyfinal(id,number,tonenumber,toneletter,label,rhyme) " +\
            "VALUES (?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,zhongyuanYinyunFinalTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO zyrhyme(id,number,label) " +\
            "VALUES (?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,zhongyuanYinyunRhymeTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO earlymandarin(id,reading) " +\
            "VALUES (?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,earlyMandarinTuple)
cur.execute(commitSmt)
con.close()

print "Done Zhongyuan Yinyun tables."

           ############################################
           ##               Yunjing                  ##
           ############################################

# Create Yunjing tables
con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()

createSmt = "CREATE TABLE yunjing(id INTEGER PRIMARY KEY, " \
            "codepoint TEXT, " \
            "glyph TEXT, " \
            "initial INTEGER, " \
            "phonation INTEGER, " \
            "articulation INTEGER, " \
            "grade INTEGER, " \
            "tone INTEGER, " \
            "line INTEGER, " \
            "lmc TEXT, " \
            "rhyme INTEGER, " \
            "guangyun INTEGER, " \
            "FOREIGN KEY(rhyme) REFERENCES yjrhyme(id), " \
            "FOREIGN KEY(guangyun) REFERENCES guangyun(id))"
indexSmt = "CREATE INDEX yunjing_idx ON " \
           "yunjing(id,codepoint,glyph,initial,phonation,articulation,grade,tone,line,rhyme,guangyun,lmc)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE yjrhyme(id INTEGER PRIMARY KEY, " \
            "kaihe TEXT, " \
            "neiwai TEXT, " \
            "she INTEGER, " \
            "rhymelabel TEXT, " \
            "fanqie TEXT, " \
            "rusheng TEXT, " \
            "gradekeys1 TEXT, " \
            "gradekeys2 TEXT, " \
            "gradekeys3 TEXT, " \
            "gradekeys4 TEXT)"
indexSmt = "CREATE INDEX yjrhyme_idx ON " \
           "yjrhyme(id,kaihe,neiwai,she,rhymelabel,fanqie,rusheng,gradekeys1,gradekeys2,gradekeys3,gradekeys4)"
cur.execute(createSmt)
cur.execute(indexSmt)

con.close()

# Get values from the Yunjing dictionaries.

f=codecs.open("dicts\\yunjingDict.py","rb")
yunjingDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\yunjingRhymeToKaiheDict.py","rb")
yunjingRhymeToKaiheDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\yunjingRhymeToNeiwaiDict.py","rb")
yunjingRhymeToNeiwaiDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\yunjingRhymeToSheDict.py","rb")
yunjingRhymeToSheDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\lmcDict.py","rb")
lmcDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\yunjingAnnotationDict.py","rb")
yunjingAnnotationDict = pickle.load(f)
f.close()

yunjingTupleList = []
for yjId in yunjingDict:
    codepoint = yunjingDict[yjId]["codepoint"]
    glyph = yunjingDict[yjId]["glyph"]
    initial = yunjingDict[yjId]["initial"]
    articulation = yunjingDict[yjId]["articulation"]
    phonation = yunjingDict[yjId]["phonation"]
    grade = yunjingDict[yjId]["grade"]
    tone = yunjingDict[yjId]["tone"]
    line = yunjingDict[yjId]["line"]
    rhyme = yunjingDict[yjId]["rhyme"]
    if lmcDict.has_key(yjId):
        lmc = lmcDict[yjId]
    else:
        lmc = u""
    guangyun = yunjingDict[yjId]["guangyun"]
    if glyphOccurrenceDict[codepoint] == 0:
        glyphOccurrenceDict[codepoint] = 1
    yunjingTupleList.append(tuple([yjId,codepoint,glyph,initial,articulation,phonation,grade,tone,line,rhyme,guangyun,lmc]))
yunjingTuple = tuple(yunjingTupleList)

yunjingRhymeTupleList = []
for yjId in yunjingRhymeToKaiheDict:
    kaihe = yunjingRhymeToKaiheDict[yjId]["corrected"]    # There are four dictionaries not one because 
    neiwai = yunjingRhymeToNeiwaiDict[yjId]["corrected"] # they are reused elsewhere.
    she = yunjingRhymeToSheDict[yjId]
    rhymeLabel = yunjingAnnotationDict[yjId]["rhymelabel"]
    fanqie = yunjingAnnotationDict[yjId]["fanqie"]
    rusheng = yunjingAnnotationDict[yjId]["rusheng"]
    gradeKeys1 = yunjingAnnotationDict[yjId]["gradekeys1"]
    gradeKeys2 = yunjingAnnotationDict[yjId]["gradekeys2"]
    gradeKeys3 = yunjingAnnotationDict[yjId]["gradekeys3"]
    gradeKeys4 = yunjingAnnotationDict[yjId]["gradekeys4"]
    yunjingRhymeTupleList.append(tuple([yjId,kaihe,neiwai,she,rhymeLabel,fanqie,rusheng,gradeKeys1,gradeKeys2,gradeKeys3,gradeKeys4]))
yunjingRhymeTuple = tuple(yunjingRhymeTupleList)

con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()

insertSmt = "INSERT INTO yunjing(id,codepoint,glyph,initial,articulation,phonation,grade,tone,line,rhyme,guangyun,lmc) " +\
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,yunjingTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO yjrhyme(id,kaihe,neiwai,she,rhymelabel,fanqie,rusheng,gradeKeys1,gradeKeys2,gradeKeys3,gradeKeys4) " +\
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,yunjingRhymeTuple)
cur.execute(commitSmt)

con.close()

print "Done Yunjing tables."

           ############################################
           ##              Guangyun                  ##
           ############################################

# Create Guangyun tables
con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()

createSmt = "CREATE TABLE guangyun(id INTEGER PRIMARY KEY, " \
            "codepoint TEXT, " \
            "glyph TEXT, " \
            "homophone INTEGER, " \
            "FOREIGN KEY(homophone) REFERENCES guangyunhomophone(id)) "
indexSmt = "CREATE INDEX guangyun_idx ON " \
           "guangyun(id,codepoint,glyph,homophone)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE gyhomophone(id INTEGER PRIMARY KEY, " \
            "number TEXT, " \
            "initialfanqiecodepoint TEXT, " \
            "initialfanqieglyph TEXT, " \
            "finalfanqiecodepoint TEXT, " \
            "finalfanqieglyph TEXT, " \
            "final INTEGER, " \
            "yunjing INTEGER, " \
            "yunjingtype INTEGER, " \
            "emc TEXT, " \
            "mcb TEXT, " \
            "mck TEXT, " \
            "FOREIGN KEY(final) REFERENCES gyfinal(id))"
indexSmt = "CREATE INDEX gyhomophone_idx ON " \
           "gyhomophone(id,number,initialfanqiecodepoint,initialfanqieglyph,finalfanqiecodepoint,finalfanqieglyph,final,yunjing,yunjingtype,emc,mcb,mck)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE gyfinal(id INTEGER PRIMARY KEY, " \
            "number TEXT, " \
            "type TEXT, "\
            "tone INTEGER, " \
            "rhyme INTEGER, " \
            "finalglyph TEXT, " \
            "sectionlabel TEXT, " \
            "tongyong TEXT, " \
            "FOREIGN KEY(tone) REFERENCES gytone(id))"
indexSmt = "CREATE INDEX gyfinal_idx ON " \
           "gyfinal(id,number,type,tone,rhyme,finalglyph,sectionlabel,tongyong)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE gytone(id INTEGER PRIMARY KEY, " \
            "number INTEGER)"
indexSmt = "CREATE INDEX gytone_idx ON " \
           "gytone(id,number)"
cur.execute(createSmt)
cur.execute(indexSmt)

con.close()

# Get values from the Guangyun dictionaries.

f=codecs.open("dicts\\guangyunDict.py","rb")
guangyunDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\guangyunHomophoneDict.py","rb")
guangyunHomophoneDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\guangyunFinalDict.py","rb")
guangyunFinalDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\guangyunToneDict.py","rb")
guangyunToneDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\guangyunToneDict.py","rb")
guangyunToneDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\emcFinalDict.py","rb")
emcFinalDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\lmcDict.py","rb")
lmcDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\emcDict.py","rb")
emcDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\mcbDict.py","rb")
mcbDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\mckDict.py","rb")
mckDict = pickle.load(f)
f.close()

guangyunTupleList = []
for gyId in guangyunDict:
    codepoint = guangyunDict[gyId]["codepoint"]    
    glyph = guangyunDict[gyId]["glyph"]    
    homophone = guangyunDict[gyId]["homophone"]    
    if glyphOccurrenceDict[codepoint] == 0:
        glyphOccurrenceDict[codepoint] = 1
    guangyunTupleList.append(tuple([gyId,codepoint,glyph,homophone]))
guangyunTuple = tuple(guangyunTupleList)

guangyunHomophoneTupleList = []
for gyId in guangyunHomophoneDict:
    number = guangyunHomophoneDict[gyId]["number"]
    initialfanqiecodepoint = guangyunHomophoneDict[gyId]["initialfanqiecodepoint"]    
    initialfanqieglyph = guangyunHomophoneDict[gyId]["initialfanqieglyph"]    
    finalfanqiecodepoint = guangyunHomophoneDict[gyId]["finalfanqiecodepoint"]    
    finalfanqieglyph = guangyunHomophoneDict[gyId]["finalfanqieglyph"]
    final = guangyunHomophoneDict[gyId]["final"]    
    yunjing = guangyunHomophoneDict[gyId]["yunjing"]    
    yunjingType = guangyunHomophoneDict[gyId]["yunjingtype"]
    emc = emcDict[gyId]
    mcb = mcbDict[gyId]
    mck = mckDict[gyId]
    guangyunHomophoneTupleList.append(tuple([gyId,number,initialfanqiecodepoint,initialfanqieglyph,finalfanqiecodepoint,finalfanqieglyph,final,yunjing,yunjingType,emc,mcb,mck]))
guangyunHomophoneTuple = tuple(guangyunHomophoneTupleList)

guangyunFinalTupleList = []
for gyId in guangyunFinalDict:
    number = guangyunFinalDict[gyId]["number"]
    finalType = guangyunFinalDict[gyId]["type"]    
    tone = guangyunFinalDict[gyId]["tone"]
    rhyme = emcFinalDict[gyId]["rhyme"]
    finalglyph = guangyunFinalDict[gyId]["finalglyph"]
    sectionlabel = guangyunFinalDict[gyId]["sectionlabel"]
    tongyong = guangyunFinalDict[gyId]["tongyong"]
    guangyunFinalTupleList.append(tuple([gyId,number,finalType,tone,rhyme,finalglyph,sectionlabel,tongyong]))
guangyunFinalTuple = tuple(guangyunFinalTupleList)

guangyunToneTupleList = []
for gyId in guangyunToneDict:
    number = guangyunToneDict[gyId]    
    guangyunToneTupleList.append(tuple([gyId,number]))
guangyunToneTuple = tuple(guangyunToneTupleList)

# Insert Guangyun.

con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()

insertSmt = "INSERT INTO guangyun(id,codepoint,glyph,homophone) " +\
            "VALUES (?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,guangyunTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO gyhomophone(id,number,initialfanqiecodepoint,initialfanqieglyph,finalfanqiecodepoint,finalfanqieglyph,final,yunjing,yunjingtype,emc,mcb,mck) " +\
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,guangyunHomophoneTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO gyfinal(id,number,type,tone,rhyme,finalglyph,sectionlabel,tongyong) " +\
            "VALUES (?,?,?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,guangyunFinalTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO gytone(id,number) " +\
            "VALUES (?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,guangyunToneTuple)
cur.execute(commitSmt)

con.close()

print "Done Guangyun tables."

           ############################################
           ##       Grammata Serica Recensa         ##
           ############################################

# Create GSR tables.
con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()

createSmt = "CREATE TABLE gsr(id INTEGER PRIMARY KEY, " \
            "codepoint TEXT, " \
            "glyph TEXT, " \
            "phoneticlabel TEXT, " \
            "glyphlabel TEXT, " \
            "phonetic INTEGER , " \
            "pulleyblankinitial TEXT , " \
            "pulleyblankfinal TEXT , " \
            "pulleyblank TEXT , " \
            "baxter TEXT , " \
            "baxterinitial TEXT , " \
            "baxterfinal TEXT , " \
            "karlgren TEXT , " \
            "karlgreninitial TEXT , " \
            "karlgrenfinal TEXT , " \
            "gyhomophone INTEGER , " \
            "pulleyblankinitialerror TEXT , " \
            "pulleyblankfinalerror TEXT , " \
            "baxterinitialerror TEXT , " \
            "baxterfinalerror TEXT , " \
            "FOREIGN KEY(phonetic) REFERENCES gsrphonetic(id)) "
indexSmt = "CREATE INDEX gsr_idx ON " \
           "gsr(id,codepoint,glyph,phoneticlabel,glyphlabel,phonetic,pulleyblankinitial,pulleyblankfinal,pulleyblank,baxterinitial,baxterfinal,baxter,gyhomophone,pulleyblankinitialerror,pulleyblankfinalerror,baxterinitialerror,baxterfinalerror,karlgren,karlgreninitial,karlgrenfinal)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE gsrphonetic(id INTEGER PRIMARY KEY, " \
            "rhyme INTEGER, " \
            "FOREIGN KEY(rhyme) REFERENCES gsrrhyme(id)) "
indexSmt = "CREATE INDEX gsrphonetic_idx ON " \
           "gsrphonetic(id,rhyme)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE gsrrhyme(id INTEGER PRIMARY KEY, " \
            "name TEXT, " \
            "pulleyblank TEXT, " \
            "baxter TEXT, " \
            "karlgren TEXT) " 
indexSmt = "CREATE INDEX gsr_rhyme ON " \
           "gsrrhyme(id,pulleyblank,baxter,karlgren)"
cur.execute(createSmt)
cur.execute(indexSmt)

con.close()

# Get values from the GSR dictionaries.

f=codecs.open("dicts\\gsrDict.py","rb")
gsrDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\gsrPhoneticDict.py","rb")
gsrPhoneticDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\gsrRhymeDict.py","rb")
gsrRhymeDict = pickle.load(f)
f.close()

gsrTupleList = []
for gsrId in gsrDict:
    codepoint = gsrDict[gsrId]["codepoint"]    
    glyph = gsrDict[gsrId]["glyph"]    
    phoneticLabel = gsrDict[gsrId]["phoneticlabel"]
    glyphLabel = gsrDict[gsrId]["glyphlabel"]    
    phonetic = gsrDict[gsrId]["phonetic"]
    pulleyblankInitial = gsrDict[gsrId]["pulleyblankinitial"]
    pulleyblankFinal = gsrDict[gsrId]["pulleyblankfinal"]
    pulleyblank = gsrDict[gsrId]["pulleyblank"]
    baxterInitial = gsrDict[gsrId]["baxterinitial"]
    baxterFinal = gsrDict[gsrId]["baxterfinal"]
    baxter = gsrDict[gsrId]["baxter"]
    karlgrenInitial = gsrDict[gsrId]["karlgreninitial"]
    karlgrenFinal = gsrDict[gsrId]["karlgrenfinal"]
    karlgren = gsrDict[gsrId]["karlgren"]
    gyHomophone = gsrDict[gsrId]["homophone"]
    pulleyblankInitialError = gsrDict[gsrId]["pulleyblankinitialerror"]
    pulleyblankFinalError = gsrDict[gsrId]["pulleyblankfinalerror"]
    baxterInitialError = gsrDict[gsrId]["baxterinitialerror"]
    baxterFinalError = gsrDict[gsrId]["baxterfinalerror"]
    if glyphOccurrenceDict[codepoint] == 0:
        glyphOccurrenceDict[codepoint] = 1
    gsrTupleList.append(tuple([gsrId,codepoint,glyph,phoneticLabel,glyphLabel,phonetic,pulleyblankInitial,pulleyblankFinal,pulleyblank,baxterInitial,baxterFinal,baxter,gyHomophone,pulleyblankInitialError,pulleyblankFinalError,baxterInitialError,baxterFinalError,karlgrenInitial,karlgrenFinal,karlgren]))
gsrTuple = tuple(gsrTupleList)

gsrPhoneticTupleList = []
for gsrPhoneticId in gsrPhoneticDict:
    rhyme = gsrPhoneticDict[gsrPhoneticId]    
    gsrPhoneticTupleList.append(tuple([gsrPhoneticId,rhyme]))
gsrPhoneticTuple = tuple(gsrPhoneticTupleList)

gsrRhymeTupleList = []
for gsrRhymeId in gsrRhymeDict:
    name = gsrRhymeDict[gsrRhymeId]["name"]    
    pulleyblank = gsrRhymeDict[gsrRhymeId]["pulleyblank"]    
    baxter = gsrRhymeDict[gsrRhymeId]["baxter"]    
    karlgren = gsrRhymeDict[gsrRhymeId]["karlgren"]    
    gsrRhymeTupleList.append(tuple([gsrRhymeId,name,pulleyblank,baxter,karlgren]))
gsrRhymeTuple = tuple(gsrRhymeTupleList)

# Insert Grammata Serica Recensa.

con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()

insertSmt = "INSERT INTO gsr(id,codepoint,glyph,phoneticlabel,glyphlabel,phonetic,pulleyblankinitial,pulleyblankfinal,pulleyblank,baxterinitial,baxterfinal,baxter,gyhomophone,pulleyblankinitialerror,pulleyblankfinalerror,baxterinitialerror,baxterfinalerror,karlgreninitial,karlgrenfinal,karlgren) " +\
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,gsrTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO gsrphonetic(id,rhyme) " +\
            "VALUES (?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,gsrPhoneticTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO gsrrhyme(id,name,pulleyblank,baxter,karlgren) " +\
            "VALUES (?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,gsrRhymeTuple)
cur.execute(commitSmt)

con.close()

print "Done Grammata Serica Recensa tables."


           ############################################
           ##               Shijing                  ##
           ############################################

con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()

createSmt = "CREATE TABLE shijing(id INTEGER PRIMARY KEY, " \
            "codepoint TEXT, " \
            "glyph TEXT, " \
            "isrhyme INTEGER , " \
            "line INTEGER, " \
            "FOREIGN KEY(line) REFERENCES sjline(id)) "
indexSmt = "CREATE INDEX shijing_idx ON " \
           "shijing(id,codepoint,isrhyme,line)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE shijingline(id INTEGER PRIMARY KEY, " \
            "rhymeset TEXT, " \
            "duanrhyme TEXT, " \
            "stanza INTEGER, " \
            "FOREIGN KEY(stanza) REFERENCES shijingstanza(id)) "
indexSmt = "CREATE INDEX shijingline_idx ON " \
           "shijingline(id,rhymeset,duanrhyme,stanza)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE shijingstanza(id INTEGER PRIMARY KEY, " \
            "number TEXT, " \
            "ode INTEGER, " \
            "FOREIGN KEY(ode) REFERENCES shijingode(id)) "
indexSmt = "CREATE INDEX shijingstanza_idx ON " \
           "shijingstanza(id,number,ode)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE shijingode(id INTEGER PRIMARY KEY, " \
            "title TEXT, " \
            "number TEXT, " \
            "book INTEGER, " \
            "FOREIGN KEY(book) REFERENCES shijingbook(id)) "
indexSmt = "CREATE INDEX shijingode_idx ON " \
           "shijingode(id,title,number,book)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE shijingbook(id INTEGER PRIMARY KEY, " \
            "title TEXT, " \
            "number INTEGER, " \
            "part INTEGER, " \
            "FOREIGN KEY(part) REFERENCES shijingpart(id)) "
indexSmt = "CREATE INDEX shijingbook_idx ON " \
           "shijingbook(id,title,number,part)"
cur.execute(createSmt)
cur.execute(indexSmt)

createSmt = "CREATE TABLE shijingpart(id INTEGER PRIMARY KEY, " \
            "title TEXT) "
indexSmt = "CREATE INDEX shijingpart_idx ON " \
           "shijingpart(id,title)"
cur.execute(createSmt)
cur.execute(indexSmt)

con.close()

# Get values from the Shijing dictionaries.

f=codecs.open("dicts\\shijingDict.py","rb")
shijingDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\shijingLineDict.py","rb")
shijingLineDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\shijingStanzaDict.py","rb")
shijingStanzaDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\shijingOdeDict.py","rb")
shijingOdeDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\shijingBookDict.py","rb")
shijingBookDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\shijingPartDict.py","rb")
shijingPartDict = pickle.load(f)
f.close()

shijingTupleList = []
for sjId in shijingDict:
    codepoint = shijingDict[sjId]["codepoint"]    
    glyph = shijingDict[sjId]["glyph"]    
    isRhyme = shijingDict[sjId]["isrhyme"]
    line = shijingDict[sjId]["line"]    
    if glyphOccurrenceDict[codepoint] == 0:
        glyphOccurrenceDict[codepoint] = 1
    shijingTupleList.append(tuple([sjId,codepoint,glyph,isRhyme,line]))
shijingTuple = tuple(shijingTupleList)

shijingLineTupleList = []
for sjId in shijingLineDict:
    rhymeSet = shijingLineDict[sjId]["rhymeset"]    
    duanRhyme = shijingLineDict[sjId]["duanrhyme"]    
    stanza = shijingLineDict[sjId]["stanza"]
    shijingLineTupleList.append(tuple([sjId,rhymeSet,duanRhyme,stanza]))
shijingLineTuple = tuple(shijingLineTupleList)

shijingStanzaTupleList = []
for sjId in shijingStanzaDict:
    number = shijingStanzaDict[sjId]["number"]    
    ode = shijingStanzaDict[sjId]["ode"]    
    shijingStanzaTupleList.append(tuple([sjId,number,ode]))
shijingStanzaTuple = tuple(shijingStanzaTupleList)

shijingOdeTupleList = []
for sjId in shijingOdeDict:
    title = shijingOdeDict[sjId]["title"]
    number = shijingOdeDict[sjId]["number"]
    book = shijingOdeDict[sjId]["book"]    
    shijingOdeTupleList.append(tuple([sjId,title,number,book]))
shijingOdeTuple = tuple(shijingOdeTupleList)

shijingBookTupleList = []
for sjId in shijingBookDict:
    title = shijingBookDict[sjId]["title"]
    number = shijingBookDict[sjId]["number"]
    part = shijingBookDict[sjId]["part"]    
    shijingBookTupleList.append(tuple([sjId,title,number,part]))
shijingBookTuple = tuple(shijingBookTupleList)

shijingPartTupleList = []
for sjId in shijingPartDict:
    title = shijingPartDict[sjId]    
    shijingPartTupleList.append(tuple([sjId,title]))
shijingPartTuple = tuple(shijingPartTupleList)

# Insert Shijing.

con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()

insertSmt = "INSERT INTO shijing(id,codepoint,glyph,isrhyme,line) " +\
            "VALUES (?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,shijingTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO shijingline(id,rhymeset,duanrhyme,stanza) " +\
            "VALUES (?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,shijingLineTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO shijingstanza(id,number,ode) " +\
            "VALUES (?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,shijingStanzaTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO shijingode(id,title,number,book) " +\
            "VALUES (?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,shijingOdeTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO shijingbook(id,title,number,part) " +\
            "VALUES (?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,shijingBookTuple)
cur.execute(commitSmt)

insertSmt = "INSERT INTO shijingpart(id,title) " +\
            "VALUES (?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,shijingPartTuple)
cur.execute(commitSmt)

con.close()

print "Done Shijing tables."

           ############################################
           ##      Dialects and Sinoxenic            ##
           ############################################

# Get values from the dictionaries.

con = sqlite3.connect('cp.db',isolation_level=None)
cur = con.cursor()
createSmt = "CREATE TABLE mandarin(id INTEGER PRIMARY KEY" +\
            ",codepoint TEXT" +\
            ",glyph TEXT" +\
            ",reading TEXT" +\
            ",pinyin TEXT" +\
            ",toneless TEXT" +\
            ",tone TEXT" +\
            ",initial TEXT" +\
            ",second TEXT" +\
            ",FOREIGN KEY (codepoint) REFERENCES glyphs(codepoint)" +\
            ")"
cur.execute(createSmt)
indexSmt =  "CREATE INDEX mandarin_idx ON mandarin(id,codepoint,glyph,reading,pinyin,toneless,tone,initial,second)"
cur.execute(indexSmt)
createSmt = "CREATE TABLE cantonese(id INTEGER PRIMARY KEY" +\
            ",codepoint TEXT" +\
            ",glyph TEXT" +\
            ",reading TEXT" +\
            ",toneless TEXT" +\
            ",tone TEXT" +\
            ",initial TEXT" +\
            ",second TEXT" +\
            ",FOREIGN KEY (codepoint) REFERENCES glyphs(codepoint)" +\
            ")"
cur.execute(createSmt)
indexSmt =  "CREATE INDEX cantonese_idx ON cantonese(id,codepoint,glyph,reading,toneless,tone,initial,second)"
cur.execute(indexSmt)
createSmt = "CREATE TABLE japaneseon(id INTEGER PRIMARY KEY" +\
            ",codepoint TEXT" +\
            ",glyph TEXT" +\
            ",reading TEXT" +\
            ",initial TEXT" +\
            ",second TEXT" +\
            ",FOREIGN KEY (codepoint) REFERENCES glyphs(codepoint)" +\
            ")"
cur.execute(createSmt)
indexSmt =  "CREATE INDEX japaneseon_idx ON japaneseon(id,codepoint,glyph,reading,initial,second)"
cur.execute(indexSmt)
createSmt = "CREATE TABLE korean(id INTEGER PRIMARY KEY" +\
            ",codepoint TEXT" +\
            ",glyph TEXT" +\
            ",reading TEXT" +\
            ",initial TEXT" +\
            ",second TEXT" +\
            ",FOREIGN KEY (codepoint) REFERENCES glyphs(codepoint)" +\
            ")"
cur.execute(createSmt)
indexSmt =  "CREATE INDEX korean_idx ON korean(id,codepoint,glyph,reading,initial,second)"
cur.execute(indexSmt)
createSmt = "CREATE TABLE vietnamese(id INTEGER PRIMARY KEY" +\
            ",codepoint TEXT" +\
            ",glyph TEXT" +\
            ",reading TEXT" +\
            ",initial TEXT" +\
            ",second TEXT" +\
            ",FOREIGN KEY (codepoint) REFERENCES glyphs(codepoint)" +\
            ")"
cur.execute(createSmt)
indexSmt =  "CREATE INDEX vietnamese_idx ON vietnamese(id,codepoint,glyph,reading,initial,second)"
cur.execute(indexSmt)

f=codecs.open("dicts\\mandarinDict.py","rb")
mandarinDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\cantoneseDict.py","rb")
cantoneseDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\japaneseOnDict.py","rb")
japaneseOnDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\koreanDict.py","rb")
koreanDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\vietnameseDict.py","rb")
vietnameseDict = pickle.load(f)
f.close()

mandarinTupleList = []
for key in mandarinDict.keys():
    codepoint = mandarinDict[key]["codepoint"]
    glyph = codepointToGlyphDict[codepoint]
    reading = mandarinDict[key]["reading"]
    pinyin = mandarinDict[key]["pinyin"]
    toneless = mandarinDict[key]["toneless"]
    tone = mandarinDict[key]["tone"]
    initial = mandarinDict[key]["initial"]
    second = mandarinDict[key]["second"]
    mandarinTupleList.append(tuple([key,codepoint,glyph,reading,pinyin,toneless,tone,initial,second]))
mandarinTuple = tuple(mandarinTupleList)

cantoneseTupleList = []
for key in cantoneseDict.keys():
    codepoint = cantoneseDict[key]["codepoint"]
    if codepointToGlyphDict.has_key(codepoint):
        glyph = codepointToGlyphDict[codepoint]
    else:
        glyph = u"[" + codepoint + u"]"
    reading = cantoneseDict[key]["reading"]
    toneless = cantoneseDict[key]["toneless"]
    tone = cantoneseDict[key]["tone"]
    initial = cantoneseDict[key]["initial"]
    second = cantoneseDict[key]["second"]
    cantoneseTupleList.append(tuple([key,codepoint,glyph,reading,toneless,tone,initial,second]))
cantoneseTuple = tuple(cantoneseTupleList)

japaneseOnTupleList = []
for key in japaneseOnDict.keys():
    codepoint = japaneseOnDict[key]["codepoint"]
    glyph = codepointToGlyphDict[codepoint]
    reading = japaneseOnDict[key]["reading"]
    initial = japaneseOnDict[key]["initial"]
    second = japaneseOnDict[key]["second"]
    japaneseOnTupleList.append(tuple([key,codepoint,glyph,reading,initial,second]))
japaneseOnTuple = tuple(japaneseOnTupleList)

koreanTupleList = []
for key in koreanDict.keys():
    codepoint = koreanDict[key]["codepoint"]
    glyph = codepointToGlyphDict[codepoint]
    reading = koreanDict[key]["reading"]
    initial = koreanDict[key]["initial"]
    second = koreanDict[key]["second"]
    koreanTupleList.append(tuple([key,codepoint,glyph,reading,initial,second]))
koreanTuple = tuple(koreanTupleList)

vietnameseTupleList = []
for key in vietnameseDict.keys():
    codepoint = vietnameseDict[key]["codepoint"]
    glyph = codepointToGlyphDict[codepoint]
    reading = vietnameseDict[key]["reading"]
    initial = vietnameseDict[key]["initial"]
    second = vietnameseDict[key]["second"]
    vietnameseTupleList.append(tuple([key,codepoint,glyph,reading,initial,second]))
vietnameseTuple = tuple(vietnameseTupleList)

# Insert into tables.

con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()
insertSmt = "INSERT INTO mandarin(id,codepoint,glyph,reading,pinyin,toneless,tone,initial,second) VALUES (?,?,?,?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,mandarinTuple)
cur.execute(commitSmt)
insertSmt = "INSERT INTO cantonese(id,codepoint,glyph,reading,toneless,tone,initial,second) VALUES (?,?,?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,cantoneseTuple)
cur.execute(commitSmt)
insertSmt = "INSERT INTO japaneseon(id,codepoint,glyph,reading,initial,second) VALUES (?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,japaneseOnTuple)
cur.execute(commitSmt)
insertSmt = "INSERT INTO korean(id,codepoint,glyph,reading,initial,second) VALUES (?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,koreanTuple)
cur.execute(commitSmt)
insertSmt = "INSERT INTO vietnamese(id,codepoint,glyph,reading,initial,second) VALUES (?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,vietnameseTuple)
cur.execute(commitSmt)
con.close()

print "Done dialects and Sinoxenic."

           ############################################
           ##      Radicals and Four Corner Code     ##
           ############################################

# Create radical and strokes tables.

con = sqlite3.connect('cp.db',isolation_level=None)
cur = con.cursor()
createSmt = "CREATE TABLE radical(id INTEGER PRIMARY KEY" +\
            ",codepoint TEXT" +\
            ",glyph TEXT" +\
            ",radicalnumber INTEGER" +\
            ",strokecount INTEGER" +\
            ",totalstrokes INTEGER" +\
            ",FOREIGN KEY (codepoint) REFERENCES glyphs(codepoint)" +\
            ")"
cur.execute(createSmt)
indexSmt =  "CREATE INDEX radical_idx ON radical(id,codepoint,glyph,radicalnumber,strokecount,totalstrokes)"
cur.execute(indexSmt)

# Get radical and strokes data from the dictionaries.

f=codecs.open("dicts\\radicalDict.py","rb")
radicalDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\strokesDict.py","rb")
strokesDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\totalStrokesDict.py","rb")
totalStrokesDict = pickle.load(f)
f.close()

radicalTupleList = []
for key in radicalDict.keys():
    codepoint = radicalDict[key]["codepoint"]
    radical = radicalDict[key]["radical"]
    strokes = strokesDict[key]["strokes"]
    if totalStrokesDict.has_key(codepoint):
        totalStrokes = totalStrokesDict[codepoint]["totalstrokes"]
    else:
        totalStrokes = 0
    if codepointToGlyphDict.has_key(codepoint):
        glyph = codepointToGlyphDict[codepoint]
    else:
        glyph = u"[" + codepoint + u"]"
    radicalTupleList.append(tuple([key,codepoint,glyph,radical,strokes,totalStrokes]))
radicalTuple = tuple(radicalTupleList)

# Insert into radical and strokes tables.

con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()
insertSmt = "INSERT INTO radical(id,codepoint,glyph,radicalnumber,strokecount,totalstrokes) VALUES (?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,radicalTuple)
cur.execute(commitSmt)
con.close()

print "Done radicals and strokes."

con = sqlite3.connect('cp.db',isolation_level=None)
cur = con.cursor()
createSmt = "CREATE TABLE fourcornercode(id INTEGER PRIMARY KEY" +\
            ",codepoint TEXT" +\
            ",glyph TEXT" +\
            ",nwcorner INTEGER" +\
            ",necorner INTEGER" +\
            ",swcorner INTEGER" +\
            ",secorner INTEGER" +\
            ",esecorner INTEGER" +\
            ",FOREIGN KEY (codepoint) REFERENCES glyphs(codepoint)" +\
            ")"
cur.execute(createSmt)
indexSmt =  "CREATE INDEX fourcornercode_idx ON fourcornercode(id,codepoint,glyph,nwcorner,necorner,swcorner,secorner,esecorner)"
cur.execute(indexSmt)

# Get four corner code data from the dictionaries.

f=codecs.open("dicts\\fourCornerCodeDict.py","rb")
fourCornerCodeDict = pickle.load(f)
f.close()

fourCornerCodeTupleList = []
for key in fourCornerCodeDict.keys():
    codepoint = fourCornerCodeDict[key]["codepoint"]
    glyph = codepointToGlyphDict[codepoint]
    nwCorner = fourCornerCodeDict[key]["nwcorner"]
    neCorner = fourCornerCodeDict[key]["necorner"]
    swCorner = fourCornerCodeDict[key]["swcorner"]
    seCorner = fourCornerCodeDict[key]["secorner"]
    eseCorner = fourCornerCodeDict[key]["esecorner"]
    fourCornerCodeTupleList.append(tuple([key,codepoint,glyph,nwCorner,neCorner,swCorner,seCorner,eseCorner]))
fourCornerCodeTuple = tuple(fourCornerCodeTupleList)

# Insert into four corner code table.

con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()
insertSmt = "INSERT INTO fourcornercode(id,codepoint,glyph,nwcorner,necorner,swcorner,secorner,esecorner) VALUES (?,?,?,?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,fourCornerCodeTupleList)
cur.execute(commitSmt)
con.close()

print "Done four corner code."

           ############################################
           ##           Phonetic Series              ##
           ############################################

# Create radical and strokes tables.

# create phonetic series tables

con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()

createSmt = "CREATE TABLE karlgren(id INTEGER PRIMARY KEY" +\
            ", series INTEGER" +\
            ", codepoint TEXT" +\
            ", glyph TEXT" +\
            ", type TEXT" +\
            ")" 
cur.execute(createSmt)
indexSmt =  "CREATE INDEX karlgren_idx ON karlgren(id,series,codepoint,glyph,type)"
cur.execute(indexSmt)

createSmt = "CREATE TABLE karlgrenallograph(id INTEGER PRIMARY KEY" +\
            ", codepoint TEXT" +\
            ", allograph TEXT" +\
            ")" 
cur.execute(createSmt)
indexSmt =  "CREATE INDEX karlgrenallograph_idx ON karlgrenallograph(id,codepoint,allograph)"
cur.execute(indexSmt)

createSmt = "CREATE TABLE wieger(id INTEGER PRIMARY KEY" +\
            ", codepoint TEXT" +\
            ", glyph TEXT" +\
            ", phonetic INTEGER" +\
            ", type TEXT" +\
            ",FOREIGN KEY (codepoint) REFERENCES glyphs(codepoint)" +\
            ")"
cur.execute(createSmt)
indexSmt =  "CREATE INDEX wieger_idx ON wieger(id,codepoint,glyph,phonetic,type)"
cur.execute(indexSmt)
con.close()

# fill phonetic series tables

# get dictionaries
f=codecs.open("dicts\\karlgrenDict.py","rb")
karlgrenDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\karlgrenAllographDict.py","rb")
karlgrenAllographDict = pickle.load(f)
f.close()

f=codecs.open("dicts\\wiegerDict.py","rb")
wiegerDict = pickle.load(f)
f.close()

karlgrenTupleList = []
for key in karlgrenDict.keys():
    series = karlgrenDict[key]["series"]
    codepoint = karlgrenDict[key]["codepoint"]
    glyph = codepointToGlyphDict[codepoint]
    type = karlgrenDict[key]["type"]
    if glyphOccurrenceDict[codepoint] == 0:
        glyphOccurrenceDict[codepoint] = 1
    karlgrenTupleList.append(tuple([key,series,codepoint,glyph,type]))
karlgrenTuple = tuple(karlgrenTupleList)

karlgrenAllographTupleList = []
for key in karlgrenAllographDict.keys():
    codepoint = karlgrenAllographDict[key]["codepoint"]
    allograph = karlgrenAllographDict[key]["allograph"]
    karlgrenAllographTupleList.append(tuple([key,codepoint,allograph]))
karlgrenAllographTuple = tuple(karlgrenAllographTupleList)

wiegerTupleList = []
for key in wiegerDict.keys():
    codepoint = wiegerDict[key]["codepoint"]
    phonetic = wiegerDict[key]["phonetic"]
    glyph = codepointToGlyphDict[codepoint]
    type = wiegerDict[key]["type"]
    if glyphOccurrenceDict[codepoint] == 0:
        glyphOccurrenceDict[codepoint] = 1
    wiegerTupleList.append(tuple([key,codepoint,glyph,phonetic,type]))
wiegerTuple = tuple(wiegerTupleList)

con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()
insertSmt = "INSERT INTO karlgren(id,series,codepoint,glyph,type) VALUES (?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,karlgrenTuple)
cur.execute(commitSmt)
insertSmt = "INSERT INTO karlgrenallograph(id,codepoint,allograph) VALUES (?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,karlgrenAllographTuple)
cur.execute(commitSmt)
insertSmt = "INSERT INTO wieger(id,codepoint,glyph,phonetic,type) VALUES (?,?,?,?,?)"
cur.execute(beginSmt)
cur.executemany(insertSmt,wiegerTuple)
cur.execute(commitSmt)
con.close()

print "Done phonetic series."

           ############################################
           ##           Glyph Occurrence             ##
           ############################################

# update glyph occurrences
glyphOccurrenceTupleList = []
for pair in glyphList:
    codepoint = pair[1]
    occurrence = glyphOccurrenceDict[codepoint]
    glyphOccurrenceTuple = tuple([occurrence,codepoint])
    glyphOccurrenceTupleList.append(glyphOccurrenceTuple)
glyphOccurrenceTuples = tuple(glyphOccurrenceTupleList)
    
con = sqlite3.connect('cp.db',isolation_level=None)
con.text_factory = sqlite3.OptimizedUnicode
cur = con.cursor()
updateSmt = "UPDATE glyph SET occurrence = (?) WHERE codepoint = (?)"
cur.execute(beginSmt)
cur.executemany(updateSmt,glyphOccurrenceTuples)
cur.execute(commitSmt)
con.close()
print "Updated glyph occurrences."
