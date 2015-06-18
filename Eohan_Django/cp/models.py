# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models, connection

    ######################
    #     Cantonese      #
    ######################
    
class CantoneseManager(models.Manager):
    
    # cantonese()
    # Returns all characters with the passed-in Cantonese reading (Jyutping romanisation)
    # with the readings in Late Middle Chinese (Pulleyblank), Early Middle Chinese (Pulleyblank),
    # Middle Chinese (Baxter), Old Chinese (Pulleyblank) and Old Chinese (Baxter).
    
    # URL:      /cantonese/([a-z]{1,6}[1-6])
    # View:     cantonese()
    # Template: cantonese.html

    # Returns fields to be presented like this:
    # 東    dung1     tǝwŋ towŋ tuwng tung1 [kj]aŋɥ [t]ong
    # glyph cantonese lmc  emc  mcb   mck   ocp     ocb

    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # A dictionary of dictionaries, so lines appear in no particular order.

    def cantonese(self,reading):
        cur = connection.cursor()
        cantoneseQuery = "SELECT * FROM " \
                        "( " \
                    "SELECT cantonese.codepoint, cantonese.glyph, mc.lmc AS reading, 'lmc' AS period FROM " \
                    "cantonese " \
                    "LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc " \
                    "ON cantonese.glyph = mc.glyph WHERE cantonese.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT cantonese.codepoint, cantonese.glyph, g.emc AS reading, 'emc' AS period " \
                    "FROM cantonese LEFT JOIN " \
                    "(SELECT glyph, emc FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) g " \
                    "ON cantonese.glyph = g.glyph WHERE cantonese.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT cantonese.codepoint, cantonese.glyph, g.mcb AS reading, 'mcb' AS period " \
                    "FROM cantonese LEFT JOIN " \
                    "(SELECT glyph, mcb FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) g " \
                    "ON cantonese.glyph = g.glyph WHERE cantonese.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT cantonese.codepoint, cantonese.glyph, g.mck AS reading, 'mck' AS period " \
                    "FROM cantonese LEFT JOIN " \
                    "(SELECT glyph, mck FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) g " \
                    "ON cantonese.glyph = g.glyph WHERE cantonese.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT cantonese.codepoint, cantonese.glyph, gsr.pulleyblank AS reading, 'ocp' AS period " \
                    "FROM cantonese LEFT JOIN gsr " \
                    "ON cantonese.glyph = gsr.glyph WHERE cantonese.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT cantonese.codepoint, cantonese.glyph, gsr.baxter AS reading, 'ocb' AS period " \
                    "FROM cantonese LEFT JOIN gsr " \
                    "ON cantonese.glyph = gsr.glyph WHERE cantonese.reading = '{0}' " \
                    "   ) AS readings, glyph " \
                    "WHERE readings.codepoint = glyph.codepoint AND glyph.occurrence = 1 " \
                    "ORDER BY readings.glyph, readings.period, readings.reading ".format(reading)
        cur.execute(cantoneseQuery)
        cantoneseList = cur.fetchall()
        cantoneseDict = {}
        for line in cantoneseList:
            codepoint = line[0]
            glyph = line[1]
            if not cantoneseDict.has_key(codepoint):
                cantoneseDict[codepoint] = {"glyph": glyph, \
                                           "cantonese": reading, "lmc": [], \
                                           "emc": [], "mcb": [], "mck": [], \
                                           "ocp": [], "ocb": []} 
        for line in cantoneseList:
            codepoint = line[0]
            periodReading = line[2]
            period = line[3]
            cantoneseDict[codepoint][period].append(periodReading)
        return cantoneseDict
    
    # initial()
    # Returns all Cantonese syllables having the passed-in letter as initial.
    
    # URL:      /cantoneseinitial/([A-Z]
    # View:     cantoneseinitial()
    # Template: cantoneseinitial.html
    
    # Returns e.g [{'reading': 'aa1', 'toneless': 'aa'},
    #               'reading': 'aa2', 'toneless': 'aa'}...]
    # so that e.g. aa1 aa2 aa3 aa4 aa6 can be displayed together.
    # A list, not a dictionary of dictionaries to preserve the ordering.
    
    def initial(self,initial):
        cur = connection.cursor()
        initialQuery = "SELECT DISTINCT cantonese.reading, cantonese.toneless FROM cantonese, glyph " +\
                       "WHERE cantonese.codepoint = glyph.codepoint " +\
                       "AND cantonese.initial = '{0}' AND glyph.occurrence = 1 " \
                       "ORDER BY cantonese.toneless, cantonese.tone ".format(initial)
        cur.execute(initialQuery)
        lines = cur.fetchall()
        cantoneseInitialList = []
        for line in lines:
            reading, toneless = line
            cantoneseInitialList.append({"reading": reading,"toneless":toneless})
        return cantoneseInitialList

class Cantonese(models.Model):
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    reading = models.TextField(blank=True)
    initial = models.TextField(blank=True)
    objects = CantoneseManager()
    class Meta:
        db_table = 'cantonese'

class Earlymandarin(models.Model):
    reading = models.TextField(blank=True)
    class Meta:
        db_table = 'earlymandarin'

    # Early Mandarin readings are in Zhongyuanyinyun

    # Early Middle Chinese readings are in Guangyun

    ######################
    # Four Corner Code   #
    ######################
    
class FourcornercodeManager(models.Manager):

    # fourcornercode()
    # Returns all characters with the passed-in four corner code sorted by stroke count.
    # Four permutations of the code return four result sets with simiar top, bottom, left or
    # right elements, labelled N, S, E, W.
    
    # URL:      fourcornercode/([0-9]{4}(\.[0-9])?)/
    # View:     fourcornercode()
    # Template: fourcornercode.html

    # Returns fields to be presented like this:
    # N           丈扌丸中丰夫  
    # Permutation  glyphs

    # A list, not a dictionary, of dictionaries to preserve the ordering.

    def fourcornercode(self,codepoint):
        cur = connection.cursor()
        # glyph c, glyph d because we want to check the occurrence of each glyph not just the input one
        fourcornercodeQuery = "SELECT b.codepoint, b.glyph, b.nwcorner, b.necorner, b.swcorner, b.secorner, b.esecorner, radical.totalstrokes, '0' as direction " \
                              "FROM fourcornercode a, fourcornercode b, glyph c, glyph d, radical " \
                              "WHERE " \
                              "c.codepoint = '{0}' " \
                              "AND b.codepoint = radical.codepoint " \
                              "AND a.codepoint = c.codepoint " \
                              "AND b.codepoint = d.codepoint " \
                              "AND d.occurrence = 1 " \
                              "AND a.necorner = b.necorner AND a.nwcorner = b.nwcorner "\
                              "AND a.secorner = b.secorner AND a.swcorner = b.swcorner " \
                              "UNION ALL " \
                              "SELECT b.codepoint, b.glyph, b.nwcorner, b.necorner, b.swcorner, b.secorner, b.esecorner, radical.totalstrokes, '1' as direction " \
                              "FROM fourcornercode a, fourcornercode b, glyph c, glyph d, radical " \
                              "WHERE " \
                              "c.codepoint = '{0}' " \
                              "AND b.codepoint = radical.codepoint " \
                              "AND a.codepoint = c.codepoint " \
                              "AND b.codepoint = d.codepoint " \
                              "AND d.occurrence = 1 " \
                              "AND a.necorner = b.necorner AND a.nwcorner = b.nwcorner AND a.secorner = b.secorner " \
                              "UNION ALL " \
                              "SELECT b.codepoint, b.glyph, b.nwcorner, b.necorner, b.swcorner, b.secorner, b.esecorner, radical.totalstrokes, '2' as direction " \
                              "FROM fourcornercode a, fourcornercode b, glyph c, glyph d, radical " \
                              "WHERE " \
                              "c.codepoint = '{0}' " \
                              "AND b.codepoint = radical.codepoint " \
                              "AND a.codepoint = c.codepoint " \
                              "AND b.codepoint = d.codepoint " \
                              "AND d.occurrence = 1 " \
                              "AND a.necorner = b.necorner AND a.nwcorner = b.nwcorner AND a.swcorner = b.swcorner " \
                              "UNION ALL " \
                              "SELECT b.codepoint, b.glyph, b.nwcorner, b.necorner, b.swcorner, b.secorner, b.esecorner, radical.totalstrokes, '3' as direction " \
                              "FROM fourcornercode a, fourcornercode b, glyph c, glyph d, radical " \
                              "WHERE " \
                              "c.codepoint = '{0}' " \
                              "AND b.codepoint = radical.codepoint " \
                              "AND a.codepoint = c.codepoint " \
                              "AND b.codepoint = d.codepoint " \
                              "AND d.occurrence = 1 " \
                              "AND a.secorner = b.secorner AND a.swcorner = b.swcorner AND a.nwcorner = b.nwcorner " \
                              "UNION ALL " \
                              "SELECT b.codepoint, b.glyph, b.nwcorner, b.necorner, b.swcorner, b.secorner, b.esecorner, radical.totalstrokes, '4' as direction " \
                              "FROM fourcornercode a, fourcornercode b, glyph c, glyph d, radical " \
                              "WHERE " \
                              "c.codepoint = '{0}' " \
                              "AND b.codepoint = radical.codepoint " \
                              "AND a.codepoint = c.codepoint " \
                              "AND b.codepoint = d.codepoint " \
                              "AND d.occurrence = 1 " \
                              "AND a.secorner = b.secorner AND a.swcorner = b.swcorner AND a.necorner = b.necorner " \
                              "ORDER BY direction, radical.totalstrokes, b.nwcorner, b.necorner, " \
                              "b.swcorner, b.secorner ".format(codepoint)
        cur.execute(fourcornercodeQuery)
        lines = cur.fetchall()
        lineDicts = []
        for line in lines:
            lineDict = {}
            lineDict["codepoint"], lineDict["glyph"], \
                    lineDict["nwcorner"], lineDict["necorner"], lineDict["swcorner"], lineDict["secorner"], lineDict["esecorner"], \
                    lineDict["totalstrokes"], lineDict["direction"] = line
            lineDicts.append(lineDict)
        return lineDicts

class Fourcornercode(models.Model):
    codepoint = models.TextField(blank=True)
    nwcorner = models.IntegerField(null=True, blank=True)
    necorner = models.IntegerField(null=True, blank=True)
    swcorner = models.IntegerField(null=True, blank=True)
    secorner = models.IntegerField(null=True, blank=True)
    esecorner = models.IntegerField(null=True, blank=True)
    objects = FourcornercodeManager()
    class Meta:
        db_table = 'fourcornercode'

    ######################
    #        Glyph       #
    ######################
    
class GlyphManager(models.Manager):

    # glyph()
    # Returns the glyph corresponding to the passed-in codepoint, together with
    # the dialect, Sinoxenic and historical readings, the radical,
    # the four corner code and the phonetic series of Wieger and Karlgren.

    # URL:      glyph/(U\+[\dABCDEF]{1,5})/
    # View:     glyph()
    # Template: glyph.html

    # Returns fields to be presented as the main page for each character.
    # A dictionary of dictionaries with lists as values (keys can have more than one value,
    # e.g. multiple readings of a character.
    
    def glyph(self,codepoint):
        cur = connection.cursor()
        glyphQuery = "SELECT 'glyph' AS field, glyph.glyph "\
                     "FROM glyph " \
                     "WHERE glyph.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'codepoint' AS field, glyph.codepoint "\
                     "FROM glyph " \
                     "WHERE glyph.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'mandarin' AS field, pinyin FROM mandarin " \
                     "WHERE mandarin.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'cantonese' AS field, reading FROM cantonese " \
                     "WHERE cantonese.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'japaneseon' AS field, reading FROM japaneseon " \
                     "WHERE japaneseon.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'korean' AS field, reading FROM korean " \
                     "WHERE korean.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'vietnamese' AS field, reading FROM vietnamese " \
                     "WHERE vietnamese.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'earlymandarin' AS field, reading FROM zhongyuanyinyun, earlymandarin " \
                     "WHERE zhongyuanyinyun.homophone = earlymandarin.id " \
                     "AND zhongyuanyinyun.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'lmc' AS field, lmc FROM " \
                     "(SELECT * FROM guangyun, gyhomophone, yunjing " \
                     "WHERE guangyun.homophone = gyhomophone.id " \
                     "AND gyhomophone.yunjing = yunjing.id "\
                     "AND guangyun.codepoint = '{0}') " \
                     "UNION ALL " \
                     "SELECT 'mcb' AS field, mcb FROM " \
                     "(SELECT * FROM guangyun, gyhomophone  " \
                     "WHERE guangyun.homophone = gyhomophone.id " \
                     "AND guangyun.codepoint = '{0}') " \
                     "UNION ALL " \
                     "SELECT 'emc' AS field, emc FROM " \
                     "(SELECT * FROM guangyun, gyhomophone  " \
                     "WHERE guangyun.homophone = gyhomophone.id " \
                     "AND guangyun.codepoint = '{0}') " \
                     "UNION ALL " \
                     "SELECT  'mck' AS field, mck FROM " \
                     "(SELECT * FROM guangyun, gyhomophone  " \
                     "WHERE guangyun.homophone = gyhomophone.id " \
                     "AND guangyun.codepoint = '{0}') " \
                     "UNION ALL " \
                     "SELECT  'baxter' AS field, baxter FROM gsr " \
                     "WHERE gsr.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'baxterfinal' AS field, baxterfinal FROM gsr " \
                     "WHERE gsr.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'pulleyblank' AS field, pulleyblank FROM gsr " \
                     "WHERE gsr.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'pulleyblankfinal' AS field, pulleyblankfinal FROM gsr " \
                     "WHERE gsr.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'karlgren' AS field, karlgren FROM gsr " \
                     "WHERE gsr.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'karlgrenfinal' AS field, karlgrenfinal FROM gsr " \
                     "WHERE gsr.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'radicalnumber' AS field, radicalnumber FROM radical " \
                     "WHERE radical.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'strokecount' AS field, strokecount FROM radical " \
                     "WHERE radical.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'nwcorner' AS field, nwcorner FROM fourcornercode " \
                     "WHERE fourcornercode.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'necorner' AS field, necorner FROM fourcornercode " \
                     "WHERE fourcornercode.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'swcorner' AS field, swcorner FROM fourcornercode " \
                     "WHERE fourcornercode.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'secorner' AS field, secorner FROM fourcornercode " \
                     "WHERE fourcornercode.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'esecorner' AS field, esecorner FROM fourcornercode " \
                     "WHERE fourcornercode.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'karlgrenseries' AS field, series FROM karlgren " \
                     "WHERE codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'wieger' AS field, phonetic FROM wieger " \
                     "WHERE wieger.codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'guangyun' AS field, COUNT (*) FROM guangyun " \
                     "WHERE  codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'yunjing' AS field, COUNT (*) FROM yunjing " \
                     "WHERE  codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'shijing' AS field, COUNT (*) FROM shijing " \
                     "WHERE  codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'gsr' AS field, COUNT (*) FROM gsr " \
                     "WHERE  codepoint = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'zhongyuanyinyun' AS field, COUNT (*) FROM zhongyuanyinyun " \
                     "WHERE codepoint = '{0}' ".format(codepoint)
        cur.execute(glyphQuery)
        glyphList = cur.fetchall()
        glyphDict = {'glyph': [], 'codepoint': [], 'mandarin': [], \
             'cantonese': [], 'japaneseon': [], 'korean': [], \
             'vietnamese': [], 'earlymandarin': [], 'lmc': [], \
             'emc': [], 'mcb': [], 'mck': [], 'baxter': [], \
             'baxterfinal': [], 'pulleyblank': [], 'pulleyblankfinal': [], \
             'karlgren': [], 'karlgrenfinal': [], \
             'radicalnumber': [], 'strokecount': [], 'nwcorner': [], \
             'necorner': [], 'swcorner': [], 'secorner': [], \
             'esecorner': [], 'karlgrenseries': [], 'wieger': [], \
             'guangyun': [], 'yunjing': [], 'shijing': [], 'gsr': [], 'zhongyuanyinyun': []}
        for line in glyphList:
            key = line[0]
            value = line[1]
            glyphDict[key].append(value)
        return glyphDict

    def search(self,glyph):
        cur = connection.cursor()
        glyphQuery = "SELECT 'glyph' AS field, glyph.glyph "\
                     "FROM glyph " \
                     "WHERE glyph.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'codepoint' AS field, glyph.codepoint "\
                     "FROM glyph " \
                     "WHERE glyph.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'mandarin' AS field, pinyin FROM mandarin " \
                     "WHERE mandarin.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'cantonese' AS field, reading FROM cantonese " \
                     "WHERE cantonese.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'japaneseon' AS field, reading FROM japaneseon " \
                     "WHERE japaneseon.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'korean' AS field, reading FROM korean " \
                     "WHERE korean.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'vietnamese' AS field, reading FROM vietnamese " \
                     "WHERE vietnamese.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'earlymandarin' AS field, reading FROM zhongyuanyinyun, earlymandarin " \
                     "WHERE zhongyuanyinyun.homophone = earlymandarin.id " \
                     "AND zhongyuanyinyun.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'lmc' AS field, lmc FROM " \
                     "(SELECT * FROM guangyun, gyhomophone, yunjing " \
                     "WHERE guangyun.homophone = gyhomophone.id " \
                     "AND gyhomophone.yunjing = yunjing.id "\
                     "AND guangyun.glyph = '{0}') " \
                     "UNION ALL " \
                     "SELECT 'mcb' AS field, mcb FROM " \
                     "(SELECT * FROM guangyun, gyhomophone  " \
                     "WHERE guangyun.homophone = gyhomophone.id " \
                     "AND guangyun.glyph = '{0}') " \
                     "UNION ALL " \
                     "SELECT 'emc' AS field, emc FROM " \
                     "(SELECT * FROM guangyun, gyhomophone  " \
                     "WHERE guangyun.homophone = gyhomophone.id " \
                     "AND guangyun.glyph = '{0}') " \
                     "UNION ALL " \
                     "SELECT  'mck' AS field, mck FROM " \
                     "(SELECT * FROM guangyun, gyhomophone  " \
                     "WHERE guangyun.homophone = gyhomophone.id " \
                     "AND guangyun.glyph = '{0}') " \
                     "UNION ALL " \
                     "SELECT  'baxter' AS field, baxter FROM gsr " \
                     "WHERE gsr.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'baxterfinal' AS field, baxterfinal FROM gsr " \
                     "WHERE gsr.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'pulleyblank' AS field, pulleyblank FROM gsr " \
                     "WHERE gsr.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'pulleyblankfinal' AS field, pulleyblankfinal FROM gsr " \
                     "WHERE gsr.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'karlgren' AS field, karlgren FROM gsr " \
                     "WHERE gsr.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'karlgrenfinal' AS field, karlgrenfinal FROM gsr " \
                     "WHERE gsr.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'radicalnumber' AS field, radicalnumber FROM radical " \
                     "WHERE radical.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'strokecount' AS field, strokecount FROM radical " \
                     "WHERE radical.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'nwcorner' AS field, nwcorner FROM fourcornercode " \
                     "WHERE fourcornercode.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'necorner' AS field, necorner FROM fourcornercode " \
                     "WHERE fourcornercode.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'swcorner' AS field, swcorner FROM fourcornercode " \
                     "WHERE fourcornercode.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'secorner' AS field, secorner FROM fourcornercode " \
                     "WHERE fourcornercode.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'esecorner' AS field, esecorner FROM fourcornercode " \
                     "WHERE fourcornercode.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'karlgrenseries' AS field, series FROM karlgren " \
                     "WHERE karlgren.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'wieger' AS field, phonetic FROM wieger " \
                     "WHERE wieger.glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT 'guangyun' AS field, COUNT (*) FROM guangyun " \
                     "WHERE  glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'shijing' AS field, COUNT (*) FROM shijing " \
                     "WHERE  glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'gsr' AS field, COUNT (*) FROM gsr " \
                     "WHERE  glyph = '{0}' " \
                     "UNION ALL " \
                     "SELECT  'zhongyuanyinyun' AS field, COUNT (*) FROM zhongyuanyinyun " \
                     "WHERE glyph = '{0}' ".format(glyph)
        cur.execute(glyphQuery)
        glyphList = cur.fetchall()
        glyphDict = {'glyph': [], 'codepoint': [], 'mandarin': [], \
             'cantonese': [], 'japaneseon': [], 'korean': [], \
             'vietnamese': [], 'earlymandarin': [], 'lmc': [], \
             'emc': [], 'mcb': [], 'mck': [], 'baxter': [], \
             'baxterfinal': [], 'pulleyblank': [], 'pulleyblankfinal': [], \
             'karlgren': [], 'karlgrenfinal': [], \
             'radicalnumber': [], 'strokecount': [], 'nwcorner': [], \
             'necorner': [], 'swcorner': [], 'secorner': [], \
             'esecorner': [], 'karlgrenseries': [], 'wieger': [], \
             'guangyun': [], 'shijing': [], 'gsr': [], 'zhongyuanyinyun': []}
        for line in glyphList:
            key = line[0]
            value = line[1]
            glyphDict[key].append(value)
        return glyphDict


class Glyph(models.Model):
    codepoint = models.TextField(unique=True, blank=True)
    glyph = models.TextField(blank=True)
    occurrence = models.IntegerField(null=True, blank=True)
    objects = GlyphManager()
    class Meta:
        db_table = 'glyph'

    ######################
    #         GSR        #
    ######################
    
class GsrManager(models.Manager):

    # gsrtextbyrhyme()
    # Returns the characters in Grammatica Serica Recensa with numberings
    # lying between the passed-in arguments, with readings in Early Middle
    # Chinese (Pulleyblank), Old Chinese (Pulleyblank) and Old Chinee (Baxter).
    # A result set corresponds to one Old Chinese final).

    # URL:      gsrtextbyrhyme/([0-9]{1,4})-([0-9]{1,4})/
    # View:     gsrtextbyrhyme()
    # Template: gsrtextbyrhyme.html

    # Returns fields to be presented like this:

    # 可    1a                        k‘aăˀ [k‑kw]álă [khw]ajʔ
    # 柯    1d                        kaă   [kw]ál    [kw]aj
    # glyph phoneticlabel,glyphlabel  emc   ocp       ocb
    
    def gsrtextbyrhyme(self,lower,upper):
        cur = connection.cursor()
        gsrTextByRhymeQuery = "SELECT gsr.id, gsr.codepoint, gsr.glyph, " \
                   "gsr.phonetic, " \
                   "gsr.phoneticlabel, gsr.glyphlabel, " \
                   "gsr.pulleyblank, gsr.baxter, gsr.karlgren, " \
                   "gyhomophone.emc, gyhomophone.mcb " \
                   "FROM gsr, gyhomophone " \
                   "WHERE gsr.gyhomophone = gyhomophone.id " \
                   "AND gsr.phonetic >= {0} " \
                   "AND gsr.phonetic <= {1} " \
                   "ORDER BY gsr.id".format(lower,upper)
        cur.execute(gsrTextByRhymeQuery)
        lines = cur.fetchall()
        lineDicts = []
        for line in lines:
            lineDict= {}
            lineDict["id"], lineDict["codepoint"], lineDict["glyph"], \
            lineDict["phonetic"], lineDict["phoneticlabel"], lineDict["glyphlabel"], \
            lineDict["ocp"], lineDict["ocb"], lineDict["ock"], \
            lineDict["emc"], lineDict["mcb"] = line
            lineDicts.append(lineDict)
        return lineDicts

    # ocb()
    # Returns all characters with the passed-in Old Chinese final (Baxter),
    # with the readings in Old Chinese (Baxter), Old Chinese (Pulleyblank),
    # Early Middle Chinese (Pulleyblank) and Middle Chinese (Baxter).
    
    # URL:      ocb/([a-zSɦNɨʔ]{1,9})/
    # View:     ocb()
    # Template: ocb.html

    # Returns fields to be presented like this:

    # 工	   [k]aŋɥ [kw]ong kowŋ kuwng
    # glyph ocp    ocb     emc  mcb

    # Returns a list of the codepoints, glyphs and readings in the input OC final.
    
    def ocb(self,final):
        cur = connection.cursor()
        ocbQuery = "SELECT gsr.codepoint, gsr.glyph, pulleyblank, baxter, baxterfinal, emc, mcb " \
                   "FROM gsr, guangyun, gyhomophone " \
                   "WHERE gsr.codepoint = guangyun.codepoint " \
                   "AND guangyun.homophone = gyhomophone.id " \
                   "AND baxterfinal = '{0}' ".format(final)
        cur.execute(ocbQuery)
        lines = cur.fetchall()
        ocbDicts = []
        for line in lines:
            ocbDict = {}
            ocbDict["codepoint"], ocbDict["glyph"], ocbDict["pulleyblank"], ocbDict["baxter"], \
                                  ocbDict["baxterfinal"], ocbDict["emc"], ocbDict["mcb"] = line
            ocbDicts.append(ocbDict)
        return ocbDicts                                                                                      

    # ocp()
    # Returns all characters with the passed-in Old Chinese final (Pulleyblank),
    # with the readings in Old Chinese (Baxter), Old Chinese (Pulleyblank),
    # Early Middle Chinese (Pulleyblank) and Middle Chinese (Baxter).
    
    # URL:      ocp/([a-zə́ə̀áà\(\)\:ŋɣɥ]{1,4}[ăʃ]{0,1})/
    # View:     ocp()
    # Template: ocp.html

    # Returns fields to be presented like this:

    # 工	   [k]aŋɥ [kw]ong kowŋ kuwng
    # glyph ocp    ocb     emc  mcb

    # Returns a list of the codepoints, glyphs and readings in the input OC final.
    
    def ocp(self,final):
        cur = connection.cursor()
        ocpQuery = "SELECT gsr.codepoint, gsr.glyph, pulleyblank, baxter, emc, mcb " \
                   "FROM gsr, guangyun, gyhomophone " \
                   "WHERE gsr.codepoint = guangyun.codepoint " \
                   "AND guangyun.homophone = gyhomophone.id " \
                   "AND pulleyblankfinal = '{0}' ".format(final)
        cur.execute(ocpQuery)
        lines = cur.fetchall()
        ocpDicts = []
        for line in lines:
            ocpDict = {}
            ocpDict["codepoint"], ocpDict["glyph"], ocpDict["pulleyblank"], ocpDict["baxter"], ocpDict["emc"], ocpDict["mcb"] = line
            ocpDicts.append(ocpDict)
        return ocpDicts                                                                                      
        
    # ock()
    # Returns all characters with the passed-in Old Chinese final (Karlgren),
    # with the readings in Old Chinese (Baxter), Old Chinese (Pulleyblank),
    # Old Chinese (Karlgren), Middle Chinese (Karlgren)
    # Early Middle Chinese (Pulleyblank) and Middle Chinese (Baxter).
    
    # URL:      ocp/([a-zə́ə̀áà\(\)\:ŋɣɥ]{1,4}[ăʃ]{0,1})/
    # View:     ocp()
    # Template: ocp.html

    # Returns fields to be presented like this:

    # 工	   [k]aŋɥ [kw]ong kowŋ kuwng
    # glyph ocp    ocb     emc  mcb

    # Returns a list of the codepoints, glyphs and readings in the input OC final.
    
    def ock(self,final):
        cur = connection.cursor()
        ocpQuery = "SELECT gsr.codepoint, gsr.glyph, pulleyblank, baxter, karlgren, " \
                   "emc, mcb, mck " \
                   "FROM gsr, guangyun, gyhomophone " \
                   "WHERE gsr.codepoint = guangyun.codepoint " \
                   "AND guangyun.homophone = gyhomophone.id " \
                   "AND karlgrenfinal = '{0}' ".format(final)
        cur.execute(ocpQuery)
        lines = cur.fetchall()
        ockDicts = []
        for line in lines:
            ockDict = {}
            ockDict["codepoint"], ockDict["glyph"], ockDict["pulleyblank"], ockDict["baxter"], \
                                  ockDict["karlgren"],ockDict["emc"], ockDict["mcb"], ockDict["mck"] = line
            ockDicts.append(ockDict)
        return ockDicts                                                                                      
        
    # concordance()
    # Returns the text of the GSR phonetics containing the passed-in character.
  
    # URL:      gsrconcordance/(U\+[\dABCDEF]{1,5})/
    # View:     gsrconcordance()
    # Template: gsrconcordance.html

    # A GSR concordance lookup.
    # Returns fields to be displayed like this:
    #
    # 1175a	                 東

    # phoneticlabel + glyphlabel glyph
    #
    # Returns a list, not a dictionary of dictionaries to preserve ordering.
    # LIMIT 1 because the database contains a row for each reading of a glyph.

    def concordance(self,codepoint):
        cur = connection.cursor()
        concordanceQuery = "SELECT a.glyph, b.id, b.codepoint, b.glyph, " \
                           "b.phonetic, b.phoneticlabel, b.glyphlabel " \
                           "FROM (SELECT * FROM gsr WHERE codepoint = '{0}' LIMIT 1) a, gsr b " \
                           "WHERE a.phonetic = b.phonetic ".format(codepoint)
        cur.execute(concordanceQuery)
        lines = cur.fetchall()
        gsrDicts = []
        for line in lines:
            gsrDict = {}
            gsrDict["key"], gsrDict["id"], gsrDict["codepoint"], gsrDict["glyph"], \
                gsrDict["phonetic"], gsrDict["phoneticlabel"], gsrDict["glyphlabel"] = line
            gsrDicts.append(gsrDict)
        return gsrDicts


class Gsr(models.Model):
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    phoneticlabel = models.TextField(blank=True)
    glyphlabel = models.TextField(blank=True)
    phonetic = models.IntegerField(null=True, blank=True)
    pulleyblank = models.TextField(blank=True)
    baxter = models.TextField(blank=True)
    objects = GsrManager()
    class Meta:
        db_table = 'gsr'

class Gsrphonetic(models.Model):
    rhyme = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'gsrphonetic'

class Gsrrhyme(models.Model):
    name = models.TextField(blank=True)
    pulleyblank = models.TextField(blank=True)
    baxter = models.TextField(blank=True)
    karlgren = models.TextField(blank=True)
    class Meta:
        db_table = 'gsrrhyme'

    ######################
    #     Guangyun       #
    ######################
    
class GuangyunManager(models.Manager):

    # lmc()
    # Returns all characters with the passed-in Late Middle Chinese reading (Pulleyblank),
    # with the readings in Early Mandarin (Pulleyblank), Early Middle Chinese (Pulleyblank),
    # Middle Chinese (Baxter), Middle Chinese (Karlgren), Old Chinese (Pulleyblank) and
    # Old Chinese (Baxter).

    # URL:      lmc/([a-zʔʂɦŋʋŗȥăǝ]{1,7}[´`]{0,1)/
    # View:     lmc()
    # Template: lmc.html

    # Returns fields to be presented like this:
    # 東    tuŋ tǝwŋ towŋ tuwng tung1 [kj]aŋɥ [t]ong
    # glyph em  lmc  emc  mcb   mck   ocp     ocb

    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # A dictionary of dictionaries, so lines appear in no particular order.

    def lmc(self,reading):
        cur = connection.cursor()
        lmcQuery = "SELECT * FROM " \
                    "(SELECT lmc.codepoint, lmc.glyph, em.reading " \
                    "AS reading, 'em' AS period " \
                    "FROM (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id " \
                    "AND gyhomophone.yunjing = yunjing.id) lmc " \
                    "LEFT JOIN (SELECT * FROM zhongyuanyinyun, earlymandarin " \
                    "WHERE zhongyuanyinyun.homophone = earlymandarin.id) em " \
                    "ON lmc.codepoint = em.codepoint " \
                    "WHERE lmc.lmc = '{0}' " \
                    "UNION ALL " \
                    "SELECT lmc.codepoint, lmc.glyph, lmc.emc " \
                    "AS reading, 'emc' AS period " \
                    "FROM (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id " \
                    "AND gyhomophone.yunjing = yunjing.id) lmc " \
                    "WHERE lmc.lmc = '{0}' " \
                    "UNION ALL " \
                    "SELECT lmc.codepoint, lmc.glyph, lmc.mcb " \
                    "AS reading, 'mcb' AS period " \
                    "FROM (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id " \
                    "AND gyhomophone.yunjing = yunjing.id) lmc " \
                    "WHERE lmc.lmc = '{0}' " \
                    "UNION ALL " \
                    "SELECT lmc.codepoint, lmc.glyph, lmc.mck " \
                    "AS reading, 'mck' AS period " \
                    "FROM (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id " \
                    "AND gyhomophone.yunjing = yunjing.id) lmc " \
                    "WHERE lmc.lmc = '{0}' " \
                    "UNION ALL SELECT lmc.codepoint, lmc.glyph, gsr.pulleyblank " \
                    "AS reading, 'ocp' AS period " \
                    "FROM (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id " \
                    "AND gyhomophone.yunjing = yunjing.id) lmc " \
                    "LEFT JOIN gsr ON lmc.codepoint = gsr.codepoint " \
                    "WHERE lmc.lmc = '{0}' " \
                    "UNION ALL SELECT lmc.codepoint, lmc.glyph, gsr.baxter " \
                    "AS reading, 'ocb' AS period " \
                    "FROM (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id " \
                    "AND gyhomophone.yunjing = yunjing.id) lmc " \
                    "LEFT JOIN gsr ON lmc.codepoint = gsr.codepoint " \
                    "WHERE lmc.lmc = '{0}' ) AS readings , glyph " \
                    "WHERE readings.codepoint = glyph.codepoint " \
                    "AND glyph.occurrence = 1 " \
                    "ORDER BY readings.glyph, readings.period, readings.reading".format(reading)
        cur.execute(lmcQuery)
        lmcList = cur.fetchall()
        lmcDict = {}
        for line in lmcList:
            codepoint = line[0]
            glyph = line[1]
            periodReading = line[2]
            period = line[3]
            if not lmcDict.has_key(codepoint):
                lmcDict[codepoint] = {"glyph": glyph, "lmc": reading, period: [periodReading]}
            elif not lmcDict[codepoint].has_key(period):
                lmcDict[codepoint][period] = [periodReading]
            else:
                lmcDict[codepoint][period].append(periodReading)
        return lmcDict

    # emc()
    # Returns all characters with the passed-in Early Middle Chinese reading (Pulleyblank),
    # with the readings in Early Mandarin (Pulleyblank), Late Middle Chinese (Pulleyblank),
    # Middle Chinese (Baxter), Middle Chinese (Karlgren), Old Chinese (Pulleyblank) and
    # Old Chinese (Baxter).

    # URL:      emc/([a-zʔɕʂʐʑɲŋɣ‘ăǝɛɔɨ]{1,7}[ˀʰ]{0,1})/
    # View:     emc()
    # Template: emc.html

    # Returns fields to be presented like this:
    # 東    tuŋ tǝwŋ towŋ tuwng tung1 [kj]aŋɥ [t]ong
    # glyph em  lmc  emc  mcb   mck   ocp     ocb

    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # A dictionary of dictionaries, so lines appear in no particular order.

    def emc(self,reading):
        cur = connection.cursor()
        emcQuery = "SELECT * FROM " \
        "(SELECT emc.codepoint, emc.glyph, em.reading " \
        "AS reading, 'em' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN (SELECT * FROM zhongyuanyinyun, earlymandarin " \
        "WHERE zhongyuanyinyun.homophone = earlymandarin.id) em " \
        "ON emc.codepoint = em.codepoint " \
        "WHERE emc.emc = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, emc.lmc " \
        "AS reading, 'lmc' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone, yunjing " \
        "WHERE guangyun.homophone = gyhomophone.id " \
        "AND gyhomophone.yunjing = yunjing.id) emc " \
        "WHERE emc.emc = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, emc.mcb " \
        "AS reading, 'mcb' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "WHERE emc.emc = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, emc.mck " \
        "AS reading, 'mck' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "WHERE emc.emc = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, gsr.pulleyblank " \
        "AS reading, 'ocp' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN gsr ON emc.codepoint = gsr.codepoint " \
        "WHERE emc.emc = '{0}' " \
        "UNION ALL SELECT emc.codepoint, emc.glyph, gsr.baxter " \
        "AS reading, 'ocb' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN gsr ON emc.codepoint = gsr.codepoint " \
        "WHERE emc.emc = '{0}' " \
        "UNION ALL SELECT emc.codepoint, emc.glyph, gsr.karlgren " \
        "AS reading, 'ock' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN gsr ON emc.codepoint = gsr.codepoint " \
        "WHERE emc.emc = '{0}' ) AS readings , glyph " \
        "WHERE readings.codepoint = glyph.codepoint " \
        "AND glyph.occurrence = 1 " \
        "ORDER BY readings.glyph, readings.period, readings.reading".format(reading)
        cur.execute(emcQuery)
        emcList = cur.fetchall()
        emcDict = {}
        for line in emcList:
            codepoint = line[0]
            glyph = line[1]
            periodReading = line[2]
            period = line[3]
            if not emcDict.has_key(codepoint):
                emcDict[codepoint] = {"glyph": glyph, "emc": reading, period: [periodReading]}
            elif not emcDict[codepoint].has_key(period):
                emcDict[codepoint][period] = [periodReading]
            else:
                emcDict[codepoint][period].append(periodReading)
        return emcDict

    # mcb()
    # Returns all characters with the passed-in Middle Chinese reading (Baxter),
    # with the readings in Early Mandarin (Pulleyblank), Late Middle Chinese (Pulleyblank),
    # Early Middle Chinese (Pulleyblank), Middle Chinese (Karlgren), Old Chinese (Pulleyblank) and
    # Old Chinese (Baxter).

    # URL:      mcb/([a-zæɛɨ]{1,8}[XH])/
    # View:     mcb()
    # Template: mcb.html

    # Returns fields to be presented like this:
    # 東    tuŋ tǝwŋ towŋ tuwng tung1 [kj]aŋɥ [t]ong
    # glyph em  lmc  emc  mcb   mck   ocp     ocb

    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # A dictionary of dictionaries, so lines appear in no particular order.

    def mcb(self,reading):
        cur = connection.cursor()
        mcbQuery = "SELECT * FROM " \
        "(SELECT emc.codepoint, emc.glyph, em.reading " \
        "AS reading, 'em' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN " \
        "(SELECT * FROM zhongyuanyinyun, earlymandarin " \
        "WHERE zhongyuanyinyun.homophone = earlymandarin.id) em " \
        "ON emc.codepoint = em.codepoint " \
        "WHERE emc.mcb = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, emc.lmc " \
        "AS reading, 'lmc' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone, yunjing " \
        "WHERE guangyun.homophone = gyhomophone.id " \
        "AND gyhomophone.yunjing = yunjing.id) emc " \
        "WHERE emc.mcb = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, emc.mcb " \
        "AS reading, 'mcb' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "WHERE emc.mcb = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, emc.mck " \
        "AS reading, 'mck' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "WHERE emc.mcb = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, emc.emc " \
        "AS reading, 'emc' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN gsr ON emc.codepoint = gsr.codepoint " \
        "WHERE emc.mcb = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, gsr.baxter " \
        "AS reading, 'ocb' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN gsr ON emc.codepoint = gsr.codepoint " \
        "WHERE emc.mcb = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, gsr.pulleyblank " \
        "AS reading, 'ocp' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN gsr ON emc.codepoint = gsr.codepoint " \
        "WHERE emc.mcb = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, gsr.karlgren " \
        "AS reading, 'ock' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN gsr ON emc.codepoint = gsr.codepoint " \
        "WHERE emc.mcb = '{0}' ) AS readings , glyph " \
        "WHERE readings.codepoint = glyph.codepoint " \
        "AND glyph.occurrence = 1 " \
        "ORDER BY readings.glyph, readings.period, readings.reading".format(reading)
        cur.execute(mcbQuery)
        mcbList = cur.fetchall()
        mcbDict = {}
        for line in mcbList:
            codepoint = line[0]
            glyph = line[1]
            reading = line[2]
            period = line[3]
            if not mcbDict.has_key(codepoint):
                mcbDict[codepoint] = {"glyph": glyph, period: [reading]}
            elif not mcbDict[codepoint].has_key(period):
                mcbDict[codepoint][period] = [reading]
            else:
                mcbDict[codepoint][period].append(reading)
        return mcbDict
        cur.execute(mcbQuery)
        mcbList = cur.fetchall()
        mcbDict = {}
        for line in mcbList:
            codepoint = line[0]
            glyph = line[1]
            reading = line[2]
            period = line[3]
            if not mcbDict.has_key(codepoint):
                mcbDict[codepoint] = {"glyph": glyph, period: [reading]}
            elif not mcbDict[codepoint].has_key(period):
                mcbDict[codepoint][period] = [reading]
            else:
                mcbDict[codepoint][period].append(reading)
        return mcbDict

    # mck()
    # Returns all characters with the passed-in Middle Chinese reading (Karlgren),
    # with the readings in Early Mandarin (Pulleyblank), Late Middle Chinese (Pulleyblank),
    # Early Middle Chinese (Pulleyblank), Middle Chinese (Baxter), Old Chinese (Pulleyblank) and
    # Old Chinese (Baxter).

    # URL:      mcb/([a-zæɛɨ]{1,8}[XH])/
    # View:     mcb()
    # Template: mcb.html

    # Returns fields to be presented like this:
    # 東    tuŋ tǝwŋ towŋ tuwng tung1 [kj]aŋɥ [t]ong
    # glyph em  lmc  emc  mcb   mck   ocp     ocb

    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # A dictionary of dictionaries, so lines appear in no particular order.

    def mck(self,reading):
        cur = connection.cursor()
        mckQuery = "SELECT * FROM " \
        "(SELECT emc.codepoint, emc.glyph, em.reading " \
        "AS reading, 'em' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN " \
        "(SELECT * FROM zhongyuanyinyun, earlymandarin " \
        "WHERE zhongyuanyinyun.homophone = earlymandarin.id) em " \
        "ON emc.codepoint = em.codepoint " \
        "WHERE emc.mck = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, emc.lmc " \
        "AS reading, 'lmc' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone, yunjing " \
        "WHERE guangyun.homophone = gyhomophone.id " \
        "AND gyhomophone.yunjing = yunjing.id) emc " \
        "WHERE emc.mck = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, emc.mcb " \
        "AS reading, 'mcb' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "WHERE emc.mck = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, emc.mck " \
        "AS reading, 'mck' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "WHERE emc.mck = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, emc.emc " \
        "AS reading, 'emc' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN gsr ON emc.codepoint = gsr.codepoint " \
        "WHERE emc.mck = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, gsr.baxter " \
        "AS reading, 'ocb' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN gsr ON emc.codepoint = gsr.codepoint " \
        "WHERE emc.mck = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, gsr.pulleyblank " \
        "AS reading, 'ocp' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN gsr ON emc.codepoint = gsr.codepoint " \
        "WHERE emc.mck = '{0}' " \
        "UNION ALL " \
        "SELECT emc.codepoint, emc.glyph, gsr.karlgren " \
        "AS reading, 'ock' AS period " \
        "FROM (SELECT * FROM guangyun, gyhomophone " \
        "WHERE guangyun.homophone = gyhomophone.id ) emc " \
        "LEFT JOIN gsr ON emc.codepoint = gsr.codepoint " \
        "WHERE emc.mck = '{0}' ) AS readings , glyph " \
        "WHERE readings.codepoint = glyph.codepoint " \
        "AND glyph.occurrence = 1 " \
        "ORDER BY readings.glyph, readings.period, readings.reading".format(reading)
        cur.execute(mckQuery)
        mckList = cur.fetchall()
        mckDict = {}
        for line in mckList:
            codepoint = line[0]
            glyph = line[1]
            reading = line[2]
            period = line[3]
            if not mckDict.has_key(codepoint):
                mckDict[codepoint] = {"glyph": glyph, period: [reading]}
            elif not mckDict[codepoint].has_key(period):
                mckDict[codepoint][period] = [reading]
            else:
                mckDict[codepoint][period].append(reading)
        return mckDict

    # guangyuntextbyfinal()
    # Returns all characters with the passed-in Guangyun final, with the readings in
    # Early Middle Chinese (Pulleyblank), Middle Chinese (Baxter) and Middle Chinese
    # (Karlgren).

    # URL:      guangyuntextbyfinal/([0-9]{1,3})/
    # View:     guangyuntextbyfinal()
    # Template: guangyuntextbyfinal.html

    # Returns fields to be presented like this:
    
    # 東         弟一          獨用
    # finalglyph sectionlabel tongyong
    #
    # towŋ tuwng tung1 東德紅	   	東 菄 鶇 䍶 𠍀 倲 𩜍 𢘐 涷 蝀 凍 鯟 𢔅 崠 埬 𧓕 䰤
    # emc  mcb   mck   fanqie           glyphs		
    
    def guangyuntextbyfinal(self,final):
        guangyunTextByFinalQuery = "SELECT guangyun.glyph, guangyun.codepoint, guangyun.homophone, " \
                     "gyhomophone.final, gyhomophone.number, " \
                     "gyhomophone.initialfanqiecodepoint, gyhomophone.finalfanqiecodepoint, " \
                     "gyhomophone.initialfanqieglyph, gyhomophone.finalfanqieglyph, " \
                     "gyhomophone.emc, gyhomophone.mcb, gyhomophone.mck, " \
                     "gyfinal.number, gyfinal.type, " \
                     "gyfinal.finalglyph, gyfinal.sectionlabel, gyfinal.tongyong " \
                     "FROM guangyun, gyhomophone, gyfinal " \
                     "WHERE gyhomophone.id = guangyun.homophone AND " \
                     "gyhomophone.final = gyfinal.id AND gyfinal.number = {0} ".format(final)
        cur = connection.cursor()
        cur.execute(guangyunTextByFinalQuery)
        lines = cur.fetchall()
        lineDicts = []
        for line in lines:
            lineDict = {}
            lineDict["glyph"], lineDict["codepoint"], lineDict["homophoneid"], \
            lineDict["final"], lineDict["homophonenumber"], \
            lineDict["initialfanqiecodepoint"], lineDict["finalfanqiecodepoint"], \
            lineDict["initialfanqieglyph"], lineDict["finalfanqieglyph"], \
            lineDict["emc"], lineDict["mcb"], lineDict["mck"], \
            lineDict["finalnumber"], lineDict["finaltype"], \
            lineDict["finalglyph"], lineDict["sectionlabel"], lineDict["tongyong"] = line
            lineDicts.append(lineDict)
        return lineDicts

    # concordance()
    # Returns the text of the Guanyun homophones containing the passed-in character.
  
    # URL:      guangyunconcordance/(U\+[\dABCDEF]{1,5})/
    # View:     guangyunconcordance()
    # Template: guangyunconcordance.html

    # A Guangyun concordance lookup.
    # Returns fields to be displayed like this:
    #
    # 東         弟一          獨用     東德紅	                       東菄鶇䍶𠍀倲𩜍𢘐涷蝀凍鯟𢔅崠埬𧓕䰤

    # finalglyph sectionlabel tongyong glyph initialfanqie finalfanqie glyphs
    #
    # Returns a list, not a dictionary of dictionaries to preserve ordering.

    def concordance(self,codepoint):
        cur = connection.cursor()
        concordanceQuery = "SELECT b.codepoint, b.glyph, b.homophonenumber, " \
                           "b.initialfanqie, b.finalfanqie, b.homophone, b.finalnumber, " \
                           "b.finalglyph, b.sectionlabel, b.tongyong, b.tonenumber " \
                           "FROM (SELECT  a1.codepoint AS codepoint, a2.id AS homophone " \
                           "FROM guangyun AS a1, gyhomophone AS a2, gyfinal AS a3, gytone AS a4 " \
                           "WHERE a1.homophone = a2.id " \
                           "AND a2.final = a3.id " \
                           "AND a3.tone = a4.id) a, " \
                           "(SELECT  b1.id AS id, b1.codepoint AS codepoint, b1.glyph AS glyph, " \
                           "b2.number AS homophonenumber, b2.initialfanqieglyph AS initialfanqie, " \
                           "b2.finalfanqieglyph AS finalfanqie, b2.id AS homophone, "\
                           "b3.id AS final, b3.number AS finalnumber, " \
                           "b3.finalglyph AS finalglyph, " \
                           "b3.sectionlabel AS sectionlabel, b3.tongyong AS tongyong, b4.number AS tonenumber " \
                           "FROM guangyun AS b1, gyhomophone AS b2, gyfinal AS b3, gytone AS b4 " \
                           "WHERE b1.homophone = b2.id " \
                           "AND b2.final = b3.id " \
                           "AND b3.tone = b4.id) b "\
                           "WHERE a.codepoint = '{0}' " \
                           "AND a.homophone = b.homophone ".format(codepoint)
        cur.execute(concordanceQuery)
        lines = cur.fetchall()
        guangyunDicts = []
        for line in lines:
            guangyunDict = {}
            guangyunDict["codepoint"], guangyunDict["glyph"], guangyunDict["homophonenumber"], \
                                       guangyunDict["initialfanqie"], guangyunDict["finalfanqie"], \
                                       guangyunDict["homophone"], guangyunDict["finalnumber"], \
                                       guangyunDict["finalglyph"], \
                                       guangyunDict["sectionlabel"], guangyunDict["tongyong"], \
                                       guangyunDict["tonenumber"] = line
            guangyunDicts.append(guangyunDict)                               
        return guangyunDicts

class Guangyun(models.Model):
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    homophone = models.IntegerField(null=True, blank=True)
    objects = GuangyunManager()
    class Meta:
        db_table = 'guangyun'

class Gyfinal(models.Model):
    number = models.TextField(blank=True)
    type = models.TextField(blank=True)
    tone = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'gyfinal'

class Gyhomophone(models.Model):
    number = models.TextField(blank=True)
    initialfanqiecodepoint = models.TextField(blank=True)
    initialfanqieglyph = models.TextField(blank=True)
    finalfanqiecodepoint = models.TextField(blank=True)
    finalfanqieglyph = models.TextField(blank=True)
    final = models.IntegerField(null=True, blank=True)
    yunjing = models.IntegerField(null=True, blank=True)
    yunjingtype = models.IntegerField(null=True, blank=True)
    emc = models.TextField(blank=True)
    mcb = models.TextField(blank=True)
    mck = models.TextField(blank=True)
    class Meta:
        db_table = 'gyhomophone'

class Gytone(models.Model):
    number = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'gytone'

    ######################
    #     Japanese       #
    ######################
    
class JapaneseonManager(models.Manager):

    # japanese()
    # Returns all characters with the passed-in Japanese 'on' reading, with
    # the readings in Late Middle Chinese (Pulleyblank), Early Middle Chinese
    # (Pulleyblank), Middle Chinee (Baxter) and Middle Chinese (Karlgren).

    # URL:      japanese/([a-z]+)/
    # View:     japanese()
    # Template: japanese.html

    # Returns fields to be presented like this:
    # 東    tou      tǝwŋ towŋ tuwng tung1
    # glyph japanese lmc  emc  mcb   mck   

    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # A dictionary of dictionaries, so lines appear in no particular order.
    
    def japanese(self,reading):
        cur = connection.cursor()
        japaneseOnQuery = "SELECT * FROM " \
                    "(" \
                    "SELECT japaneseon.codepoint, japaneseon.glyph, mc.lmc AS reading, 'lmc' AS period FROM " \
                    "japaneseon " \
                    "LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc " \
                    "ON japaneseon.glyph = mc.glyph WHERE japaneseon.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT japaneseon.codepoint, japaneseon.glyph, mc.emc AS reading, 'emc' AS period FROM " \
                    "japaneseon LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON japaneseon.codepoint = mc.codepoint WHERE japaneseon.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT japaneseon.codepoint, japaneseon.glyph, mc.mcb AS reading, 'mcb' AS period FROM " \
                    "japaneseon " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON japaneseon.codepoint = mc.codepoint WHERE japaneseon.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT japaneseon.codepoint, japaneseon.glyph, mc.mck AS reading, 'mck' AS period FROM " \
                    "japaneseon " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON japaneseon.codepoint = mc.codepoint WHERE japaneseon.reading = '{0}' " \
                    ") AS readings , glyph " \
                    "WHERE readings.codepoint = glyph.codepoint AND glyph.occurrence = 1 " \
                    "ORDER BY readings.glyph, readings.period, readings.reading ".format(reading)
        cur.execute(japaneseOnQuery)
        japaneseList = cur.fetchall()
        japaneseDict = {}
        for line in japaneseList:
            codepoint = line[0]
            glyph = line[1]
            if not japaneseDict.has_key(codepoint):
                japaneseDict[codepoint] = {"glyph": glyph, \
                                           "japanese": reading, "lmc": [], \
                                           "emc": [], "mcb": [], "mck": []} 
        for line in japaneseList:
            codepoint = line[0]
            periodReading = line[2]
            period = line[3]
            japaneseDict[codepoint][period].append(periodReading)
        return japaneseDict

    # initial()
    # Returns all Japanese syllables having the passed-in letter as initial.
    
    # URL:      japaneseinitial/([A-Z])/
    # View:     japaneseinitial()
    # Template: japaneseinitial.html
    
    # Returns e.g [{'reading': 'aka', 'first': 'a', 'second': 'k'},
    #               'reading': 'aku', 'first': 'a', 'second': 'k'}...]
    # so that e.g. aka, aku can be displayed together.
    # A list, not a dictionary of dictionaries to preserve the ordering.
    
    def initial(self,initial):
        cur = connection.cursor()
        initialQuery = "SELECT DISTINCT japaneseon.reading, japaneseon.initial, japaneseon.second FROM japaneseon, glyph " +\
                       "WHERE japaneseon.codepoint = glyph.codepoint " +\
                       "AND japaneseon.initial = '{0}' AND glyph.occurrence = 1 " \
                       "ORDER BY japaneseon.initial, japaneseon.second, japaneseon.reading ".format(initial)
        cur.execute(initialQuery)
        lines = cur.fetchall()
        japaneseInitialList = []
        for line in lines:
            reading, initial, second = line
            japaneseInitialList.append({"reading": reading, "initial": initial, "second": second})        
        return japaneseInitialList
    
class Japaneseon(models.Model):
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    reading = models.TextField(blank=True)
    initial = models.TextField(blank=True)
    objects = JapaneseonManager()
    class Meta:
        db_table = 'japaneseon'

    ######################
    #     Karlgren       #
    ######################
    
class KarlgrenManager(models.Manager):

    # karlgren()
    # Returns all characters in the passed-in phonetic series in Karlgren's
    # Analytic Dictionary, with the readings in Mandarin, Early Mandarin (Pulleyblank),
    # Late Middle Chinese (Pulleyblank), Early Middle Chinese (Pulleyblank), Middle
    # Chinese (Baxter), Middle Chinese (Karlgren), Old Chinese (Pulleyblank) and Old
    # Chinese (Baxter).
    
    # URL:      karlgren/([0-9]{1,4})/
    # View:     karlgren()
    # Template: karlgren.html

    # Returns fields to be presented like this:
    # 東    dōng     tuŋ dung1     tǝwŋ towŋ tuwng tung1 [kj]aŋɥ [t]ong
    # glyph mandarin em  cantonese lmc  emc  mcb   mck   ocp     ocb

    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # Returns a list of dictionaries to preserve the ordering.

    def karlgren(self,series):
        cur = connection.cursor()
        karlgrenQuery = "SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, " \
                    "mandarin.pinyin, '0 mandarin' AS dialect FROM " \
                    "karlgren, mandarin " \
                    "WHERE karlgren.codepoint = mandarin.codepoint " \
                    "AND karlgren.series = '{0}' " \
                    "UNION ALL " \
                    "SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, " \
                    "cantonese.reading, '1 cantonese' AS dialect FROM " \
                    "karlgren, cantonese " \
                    "WHERE karlgren.codepoint = cantonese.codepoint " \
                    "AND karlgren.series = '{0}' " \
                    "UNION ALL " \
                    "SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, " \
                    "em.reading, '2 em' AS dialect FROM " \
                    "karlgren LEFT JOIN " \
                    "(SELECT * FROM zhongyuanyinyun, earlymandarin " \
                    "WHERE zhongyuanyinyun.homophone = earlymandarin.id) em " \
                    "WHERE karlgren.codepoint = em.codepoint " \
                    "AND karlgren.series = '{0}' " \
                    "UNION ALL " \
                    "SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, " \
                    "mc.lmc, '3 lmc' AS dialect FROM " \
                    "karlgren LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc " \
                    "WHERE karlgren.codepoint = mc.codepoint AND karlgren.series = '{0}' " \
                    "UNION ALL " \
                    "SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, " \
                    "mc.emc, '4 emc' AS dialect FROM " \
                    "karlgren LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "WHERE karlgren.codepoint = mc.codepoint AND karlgren.series = '{0}' " \
                    "UNION ALL " \
                    "SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, " \
                    "mc.mcb, '5 mcb' AS dialect FROM " \
                    "karlgren LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "WHERE karlgren.codepoint = mc.codepoint AND karlgren.series = '{0}' " \
                    "UNION ALL " \
                    "SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, " \
                    "mc.mck, '6 mck' AS dialect FROM " \
                    "karlgren LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "WHERE karlgren.codepoint = mc.codepoint AND karlgren.series = '{0}' " \
                    "UNION ALL " \
                    "SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, " \
                    "gsr.pulleyblank, '7 ocp' AS dialect FROM " \
                    "karlgren, gsr " \
                    "WHERE karlgren.codepoint = gsr.codepoint " \
                    "AND karlgren.series = '{0}' " \
                    "UNION ALL " \
                    "SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, " \
                    "gsr.baxter, '8 ocb' AS dialect FROM " \
                    "karlgren, gsr " \
                    "WHERE karlgren.codepoint = gsr.codepoint " \
                    "AND karlgren.series = '{0}' " \
                    "ORDER BY karlgren.id, dialect" \
                    " ".format(series)
        cur.execute(karlgrenQuery)
        karlgrenList = cur.fetchall()
        karlgrenDicts = []
        codepoint, glyph = karlgrenList[0][0], karlgrenList[0][1]
        karlgrenDict = {"codepoint": codepoint, "glyph": glyph, "mandarin": [], "cantonese": [], \
                                           "em": [], \
                                           "lmc": [], "emc": [], "mcb": [], "mck": [], \
                                           "ocp": [], "ocb": []}
        for line in karlgrenList:
            codepoint, glyph, id, reading, dialect = line
            dialect = dialect[2:]
            if not karlgrenDict["codepoint"] == codepoint:
                karlgrenDicts.append(karlgrenDict)
                karlgrenDict = {"codepoint": codepoint, "glyph": glyph, "mandarin": [], "cantonese": [], \
                                           "em": [], \
                                           "lmc": [], "emc": [], "mcb": [], "mck": [], \
                                           "ocp": [], "ocb": []}
            karlgrenDict[dialect].append(reading)
        karlgrenDicts.append(karlgrenDict)
        return karlgrenDicts

class Karlgren(models.Model):
    series = models.IntegerField(blank=True)
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    type = models.TextField(blank=True)
    objects = KarlgrenManager()
    class Meta:
        db_table = 'karlgren'

    ######################
    #       Korean       #
    ######################
    
class KoreanManager(models.Manager):

    # korean()
    # Returns all characters with the passed-in Korean reading, with
    # the readings in Late Middle Chinese (Pulleyblank), Early Middle Chinese
    # (Pulleyblank), Middle Chinee (Baxter) and Middle Chinese (Karlgren).

    # URL:      korean/([a-z]+)/
    # View:     korean()
    # Template: korean.html

    # Returns fields to be presented like this:
    # 東    tong   tǝwŋ towŋ tuwng tung1
    # glyph korean lmc  emc  mcb   mck   

    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # A dictionary of dictionaries, so lines appear in no particular order.

    def korean(self,reading):
        cur = connection.cursor()
        koreanQuery = "SELECT * FROM " \
                    "(" \
                    "SELECT korean.codepoint, korean.glyph, mc.lmc AS reading, 'lmc' AS period FROM " \
                    "korean " \
                    "LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc " \
                    "ON korean.glyph = mc.glyph WHERE korean.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT korean.codepoint, korean.glyph, mc.emc AS reading, 'emc' AS period FROM " \
                    "korean LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON korean.codepoint = mc.codepoint WHERE korean.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT korean.codepoint, korean.glyph, mc.mcb AS reading, 'mcb' AS period FROM " \
                    "korean " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON korean.codepoint = mc.codepoint WHERE korean.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT korean.codepoint, korean.glyph, mc.mck AS reading, 'mck' AS period FROM " \
                    "korean " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON korean.codepoint = mc.codepoint WHERE korean.reading = '{0}' " \
                    ") AS readings , glyph " \
                    "WHERE readings.codepoint = glyph.codepoint AND glyph.occurrence = 1 " \
                    "ORDER BY readings.glyph, readings.period, readings.reading ".format(reading)
        cur.execute(koreanQuery)
        koreanList = cur.fetchall()
        koreanDict = {}
        for line in koreanList:
            codepoint = line[0]
            glyph = line[1]
            if not koreanDict.has_key(codepoint):
                koreanDict[codepoint] = {"glyph": glyph, \
                                           "korean": reading, "lmc": [], \
                                           "emc": [], "mcb": [], "mck": [], \
                                           "ocp": [], "ocb": []} 
        for line in koreanList:
            codepoint = line[0]
            periodReading = line[2]
            period = line[3]
            koreanDict[codepoint][period].append(periodReading)
        return koreanDict

    # initial()
    # Returns all Korean syllables having the passed-in letter as initial.

    # URL:      koreaninitial/([A-Z])/
    # View:     koreaninitial()
    # Template: koreaninitial.html
    
    # Returns e.g [{'reading': 'an', 'first': 'a', 'second': 'n'},
    #               'reading': 'ang', 'first': 'a', 'second': 'n'}...]
    # so that e.g. an, ang can be displayed together.
    # A list, not a dictionary of dictionaries to preserve the ordering.
    
    def initial(self,initial):
        cur = connection.cursor()
        initialQuery = "SELECT DISTINCT reading FROM korean, glyph " +\
                       "WHERE korean.codepoint = glyph.codepoint " +\
                       "AND korean.initial = '{0}' AND glyph.occurrence = 1 ".format(initial)
        initialQuery = "SELECT DISTINCT korean.reading, korean.initial, korean.second FROM korean, glyph " +\
                       "WHERE korean.codepoint = glyph.codepoint " +\
                       "AND korean.initial = '{0}' AND glyph.occurrence = 1 " \
                       "ORDER BY korean.initial, korean.second, korean.reading ".format(initial)
        cur.execute(initialQuery)
        lines = cur.fetchall()
        koreanInitialList = []
        for line in lines:
            reading, initial, second = line
            koreanInitialList.append({"reading": reading, "initial": initial, "second": second})        
        return koreanInitialList
    
class Korean(models.Model):
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    reading = models.TextField(blank=True)
    initial = models.TextField(blank=True)
    objects = KoreanManager()
    class Meta:
        db_table = 'korean'

    # Late Middle Chinese readings are in Guangyun

    ######################
    #     Mandarin       #
    ######################
    
class MandarinManager(models.Manager):
    def glyphs(self,reading):
        cur = connection.cursor()
        mandarinGlyphsQuery = "SELECT glyph " \
                                "FROM mandarin " \
                                "WHERE mandarin.reading = '{0}' ".format(reading)
        cur.execute(mandarinGlyphsQuery)
        return cur.fetchall()

    # mandarin()
    # Returns all characters with the passed-in Mandarin reading, with the readings in 
    # Early Mandarin (Pulleyblank), Late Middle Chinese (Pulleyblank), Early Middle Chinese (Pulleyblank),
    # Middle Chinese (Baxter), Old Chinese (Pulleyblank) and Old Chinese (Baxter).

    # URL:      mandarin/([a-zāáǎàēéěèīíǐìōóǒòūúǔùüǖǘǚǜ]{1,6})/
    # View:     mandarin()
    # Template: mandarin.html

    # Returns fields to be presented like this:
    # 東    dōng     tuŋ tǝwŋ towŋ tuwng tung1 [kj]aŋɥ [t]ong
    # glyph mandarin em  lmc  emc  mcb   mck   ocp     ocb

    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # A dictionary of dictionaries, so lines appear in no particular order.

    def mandarin(self,reading):
        cur = connection.cursor()
        mandarinQuery = "SELECT * FROM " \
                    "(" \
                    "SELECT mandarin.codepoint, mandarin.glyph, em.reading AS reading, 'em' AS period FROM " \
                    "mandarin LEFT JOIN " \
                    "(SELECT * FROM zhongyuanyinyun, earlymandarin " \
                    "WHERE zhongyuanyinyun.homophone = earlymandarin.id) em " \
                    "ON mandarin.codepoint = em.codepoint WHERE mandarin.pinyin = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, mc.lmc AS reading, 'lmc' AS period FROM " \
                    "mandarin " \
                    "LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc " \
                    "ON mandarin.glyph = mc.glyph WHERE mandarin.pinyin = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, mc.emc AS reading, 'emc' AS period FROM " \
                    "mandarin LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON mandarin.codepoint = mc.codepoint WHERE mandarin.pinyin = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, mc.mcb AS reading, 'mcb' AS period FROM " \
                    "mandarin " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON mandarin.codepoint = mc.codepoint WHERE mandarin.pinyin = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, mc.mck AS reading, 'mck' AS period FROM " \
                    "mandarin " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON mandarin.codepoint = mc.codepoint WHERE mandarin.pinyin = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, gsr.pulleyblank AS reading, 'ocp' AS period FROM " \
                    "mandarin " \
                    "LEFT JOIN gsr " \
                    "ON mandarin.codepoint = gsr.codepoint WHERE mandarin.pinyin = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, gsr.baxter AS reading, 'ocb' AS period FROM " \
                    "mandarin " \
                    "LEFT JOIN gsr " \
                    "ON mandarin.codepoint = gsr.codepoint WHERE mandarin.pinyin = '{0}' " \
                    ") AS readings , glyph " \
                    "WHERE readings.codepoint = glyph.codepoint AND glyph.occurrence = 1 " \
                    "ORDER BY readings.glyph, readings.period, readings.reading ".format(reading)
        cur.execute(mandarinQuery)
        mandarinList = cur.fetchall()
        mandarinDict = {}
        for line in mandarinList:
            codepoint = line[0]
            glyph = line[1]
            if not mandarinDict.has_key(codepoint):
                mandarinDict[codepoint] = {"glyph": glyph, \
                                           "mandarin": reading, "em": [], "lmc": [], \
                                           "emc": [], "mcb": [], "mck": [], \
                                           "ocp": [], "ocb": []} 
        for line in mandarinList:
            codepoint = line[0]
            periodReading = line[2]
            period = line[3]
            mandarinDict[codepoint][period].append(periodReading)
        return mandarinDict

    # mandarintoneless()
    # Returns all characters with the passed-in Mandarin reading in whatever tone, with the readings in 
    # Early Mandarin (Pulleyblank), Late Middle Chinese (Pulleyblank), Early Middle Chinese (Pulleyblank),
    # Middle Chinese (Baxter), Old Chinese (Pulleyblank) and Old Chinese (Baxter).

    # URL:      mandarintoneless/([a-z]{1,6})/
    # View:     mandarintoneless()
    # Template: mandarintoneless.html

    # Returns fields to be presented like this:
    # 東    dōng     tuŋ tǝwŋ towŋ tuwng tung1 [kj]aŋɥ [t]ong
    # glyph mandarin em  lmc  emc  mcb   mck   ocp     ocb

    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # The postprocessing attempts to order the characters into those having a first tone reading,
    # those having no first tone reading but a second tone reading etc and returns a list ordered
    # accordingly.

    def mandarintoneless(self,toneless):
        cur = connection.cursor()
        mandarinQuery = "SELECT * FROM " \
                    "(" \
                    "SELECT mandarin.codepoint, mandarin.glyph, mandarin.tone, mandarin.pinyin AS reading, 'mandarin' AS period FROM " \
                    "mandarin " \
                    "WHERE mandarin.toneless = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, mandarin.tone, em.reading AS reading, 'em' AS period FROM " \
                    "mandarin LEFT JOIN " \
                    "(SELECT * FROM zhongyuanyinyun, earlymandarin " \
                    "WHERE zhongyuanyinyun.homophone = earlymandarin.id) em " \
                    "ON mandarin.codepoint = em.codepoint WHERE mandarin.toneless = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, mandarin.tone, mc.lmc AS reading, 'lmc' AS period FROM " \
                    "mandarin " \
                    "LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc " \
                    "ON mandarin.glyph = mc.glyph WHERE mandarin.toneless = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, mandarin.tone, mc.emc AS reading, 'emc' AS period FROM " \
                    "mandarin LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON mandarin.codepoint = mc.codepoint WHERE mandarin.toneless = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, mandarin.tone, mc.mcb AS reading,'mcb' AS period FROM " \
                    "mandarin " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON mandarin.codepoint = mc.codepoint WHERE mandarin.toneless = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, mandarin.tone, mc.mck AS reading, 'mck' AS period FROM " \
                    "mandarin " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON mandarin.codepoint = mc.codepoint WHERE mandarin.toneless = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, mandarin.tone, gsr.pulleyblank AS reading, 'ocp' AS period FROM " \
                    "mandarin " \
                    "LEFT JOIN gsr " \
                    "ON mandarin.codepoint = gsr.codepoint WHERE mandarin.toneless = '{0}' " \
                    "UNION ALL " \
                    "SELECT mandarin.codepoint, mandarin.glyph, mandarin.tone, gsr.baxter AS reading, 'ocb' AS period FROM " \
                    "mandarin " \
                    "LEFT JOIN gsr " \
                    "ON mandarin.codepoint = gsr.codepoint WHERE mandarin.toneless = '{0}' " \
                    ") AS readings , glyph " \
                    "WHERE readings.codepoint = glyph.codepoint AND glyph.occurrence = 1 " \
                    "ORDER BY readings.glyph, readings.tone, readings.period, readings.reading ".format(toneless)
        cur.execute(mandarinQuery)
        lines = cur.fetchall()
        mandarinDict = {}
        for line in lines:
            codepoint = line[0]
            glyph = line[1]
            tone = line[2]
            periodReading = line[3]
            period = line[4]
            if not mandarinDict.has_key(codepoint):
                mandarinDict[codepoint] = {}
                mandarinDict[codepoint]["glyph"] = glyph
                mandarinDict[codepoint]["tone"] = tone
                mandarinDict[codepoint]["mandarin"] = []
                mandarinDict[codepoint]["em"] = []
                mandarinDict[codepoint][ "lmc"] = []
                mandarinDict[codepoint]["emc"] = []
                mandarinDict[codepoint]["mcb"] = []
                mandarinDict[codepoint]["mck"] = []
                mandarinDict[codepoint]["ocp"] = []
                mandarinDict[codepoint]["ocb"] = []
            mandarinDict[codepoint][period].append(periodReading)
        mandarinLines = []
        for codepoint in mandarinDict.keys():
            tone = mandarinDict[codepoint]["tone"]
            mandarinLines.append([tone,codepoint,mandarinDict[codepoint]])
        mandarinLines.sort()
        return mandarinLines

    # initial()
    # Returns all Mandarin syllables having the passed-in letter as initial.

    # URL:      mandarininitial/([A-Z])/
    # View:     mandarininitial()
    # Template: mandarininitial.html
    
    # Returns e.g [{'pinyin': 'ā', 'toneless': 'a'},
    #               'pinyin': 'á', 'toneless': 'a'}...]
    # so that e.g. ā á ǎ à a can be displayed together.
    # A list, not a dictionary of dictionaries to preserve the ordering.
    
    def initial(self,initial):
        cur = connection.cursor()
        initialQuery = "SELECT DISTINCT mandarin.pinyin, mandarin.toneless FROM mandarin, glyph " +\
                       "WHERE mandarin.codepoint = glyph.codepoint " +\
                       "AND mandarin.initial = '{0}' AND glyph.occurrence = 1 " \
                       "ORDER BY mandarin.toneless, mandarin.tone, mandarin.pinyin ".format(initial)
        cur.execute(initialQuery)
        lines = cur.fetchall()
        mandarinInitialList = []
        for line in lines:
            pinyin, toneless = line
            mandarinInitialList.append({"pinyin": pinyin,"toneless": toneless})        
        return mandarinInitialList
    
class Mandarin(models.Model):
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    reading = models.TextField(blank=True)
    pinyin = models.TextField(blank=True)
    initial = models.TextField(blank=True)
    objects = MandarinManager()
    class Meta:
        db_table = 'mandarin'

    # Middle Chinese readings are in Guangyun

    # Old Chinese readings are in Grammata Serica Recensa

    ######################
    #     Radicals       #
    ######################
    
class RadicalManager(models.Manager):

    # radical()
    # Returns all characters having the passed-in radical, ordered by stroke count.

    # URL:      radical/([0-9]{1,3})/
    # View:     radical()
    # Template: radical.html

    # Returns fields to be presented like this:
    # 1           未末本札朮术𣎵 
    # strokecount glyphs

    # A list, not a dictionary, of dictionaries to preserve the ordering.

    def radical(self,radicalnumber):
        cur = connection.cursor()
        radicalQuery = "SELECT glyph.codepoint, glyph.glyph, radical.radicalnumber, radical.strokecount FROM radical, glyph " \
                    "WHERE radical.codepoint = glyph.codepoint " \
                    "AND glyph.occurrence = 1 AND radical.radicalnumber = {0} " \
                    "ORDER BY radical.radicalnumber, radical.strokecount ".format(radicalnumber)
        cur.execute(radicalQuery)
        lines = cur.fetchall()
        lineDicts = []
        for line in lines:
            lineDict = {}
            lineDict["codepoint"], lineDict["glyph"], lineDict["radicalnumber"], lineDict["strokecount"] = line
            lineDicts.append(lineDict)
        return lineDicts

    # The page radicallist.html is flat HTML.
            

class Radical(models.Model):
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    radicalnumber = models.IntegerField(null=True, blank=True)
    strokecount = models.IntegerField(null=True, blank=True)
    objects = RadicalManager()
    class Meta:
        db_table = 'radical'

    ######################
    #       Shijing      #
    ######################
    
class ShijingManager(models.Manager):

    # shijingtextbybook()
    # Returns the text of the book of Shijing numbered with the passed-in number, with
    # the rhymes as identified by Duan Yucai.

    # URL:      shijingtextbybook/([0-9]{1,2})/
    # View:     shijingtextbybook()
    # Template: shijingtextbybook.html

    # Returns fields to be presented like this:
    # 國風一            周南一之一
    # parttitle        booktitle

    # 關關   1.1        關 關 雎 鳩       鳩 A
    # title ode.stanza glyphs            glyph (if isrhyme) rhymeset
    
    def shijingtextbybook(self,book):
        cur = connection.cursor()
        shijingTextByBookQuery = "SELECT " \
                    "shijing.id, shijing.codepoint, shijing.glyph, " \
                    "shijing.line, shijing.isrhyme, " \
                    "shijingline.rhymeset, shijingline.stanza, " \
                    "shijingstanza.number, shijingstanza.ode, " \
                    "shijingode.number, " \
                    "shijingode.title, shijingbook.title, shijingbook.number, shijingpart.title " \
                    "FROM shijing, shijingline, shijingstanza, shijingode, shijingbook, shijingpart " \
                    "WHERE shijingbook.number = '{0}' " \
                    "AND shijing.line = shijingline.id " \
                    "AND shijingline.stanza = shijingstanza.id " \
                    "AND shijingstanza.ode = shijingode.id " \
                    "AND shijingode.book = shijingbook.id " \
                    "AND shijingbook.part = shijingpart.id " \
                    "ORDER BY shijing.id ".format(book)
        cur.execute(shijingTextByBookQuery)
        lines = cur.fetchall()
        # Creating dictionaries which represent lines of glyphs in Shijing, e.g. 關 關 雎 鳩 gets one dictionary.
        # Four lists hold glyphs, codepoints, rhyme glyphs, rhymesets.
        lineDicts = []
        lineDict = {}
        line = lines[0]
        # First glyph of first line of Shijing.
        shijingId, codepoint, glyph, shijingLine, isRhyme, rhymeset, stanza,  \
                stanzanumber, ode, odenumber, odetitle, booktitle,     \
                booknumber, parttitle =                                \
        line[0], line[1], line[2], line[3], line[4], line[5], line[6], \
                line[7], line[8], line[9], line[10], line[11],         \
                line[12], line[13]
        lineDict["shijingid"], lineDict["glyphs"],         \
            lineDict["line"], lineDict["stanza"], lineDict["stanzanumber"],        \
            lineDict["ode"], lineDict["odenumber"], lineDict["odetitle"],          \
            lineDict["booktitle"], lineDict["booknumber"], lineDict["parttitle"] = \
            shijingId, [[codepoint, glyph]], shijingLine, stanza, stanzanumber,    \
            ode, odenumber, odetitle, booktitle,  booknumber, parttitle
        if isRhyme == 1:
            lineDict["rhymes"] = [glyph]
            lineDict["rhymesets"] = [rhymeset]
        else:
            lineDict["rhymes"] = []
            lineDict["rhymesets"] = []
        # The rest of the glyphs.
        for line in lines[1:]:
            shijingId, codepoint, glyph, isRhyme, rhymeset, stanza, \
                    stanzanumber, ode, odenumber, odetitle, booktitle,    \
                    booknumber, parttitle =                               \
            line[0], line[1], line[2], line[4], line[5], line[6], \
                    line[7], line[8], line[9], line[10], line[11],        \
                    line[12], line[13]
            # When a new line of Shijing begins.
            if not line[3] == shijingLine:
                shijingLine = line[3]
                # Append the old line to the list.
                lineDicts.append(lineDict)
                lineDict = {}
                lineDict["shijingid"], lineDict["glyphs"],                          \
                    lineDict["line"], lineDict["isrhyme"], lineDict["rhymeset"], lineDict["stanza"],        \
                    lineDict["stanzanumber"], lineDict["ode"], lineDict["odenumber"], lineDict["odetitle"], \
                    lineDict["booktitle"], lineDict["booknumber"], lineDict["parttitle"] =                  \
                    shijingId, [[codepoint, glyph]], shijingLine, isRhyme, rhymeset, stanza, stanzanumber,  \
                    ode, odenumber, odetitle, booktitle,  booknumber, parttitle
                if isRhyme == 1:
                    lineDict["rhymes"] = [glyph]
                    lineDict["rhymesets"] = [rhymeset]
                else:
                    lineDict["rhymes"] = []
                    lineDict["rhymesets"] = []
            # When still in the same line of Shijing
            else:
                lineDict["shijingid"],      \
                lineDict["line"], lineDict["stanza"], lineDict["stanzanumber"],        \
                lineDict["ode"], lineDict["odenumber"], lineDict["odetitle"],          \
                lineDict["booktitle"], lineDict["booknumber"], lineDict["parttitle"] = \
                shijingId, shijingLine, stanza,stanzanumber, ode,                      \
                odenumber, odetitle, booktitle,  booknumber, parttitle
                lineDict["glyphs"].append([codepoint,glyph])
                if isRhyme == 1 and glyph not in lineDict["rhymes"]:
                    lineDict["rhymes"].append(glyph)
                    lineDict["rhymesets"].append(rhymeset)
        # Append last dictionary.
        lineDicts.append(lineDict)
        return lineDicts

    # concordance()
    # Returns the text of the lines of Shijing containing the passed-in character.

    # URL:      shijingconcordance/(U\+[\dABCDEF]{1,5})/
    # View:     shijingconcordance()
    # Template: shijingconcordance.html

    # A Shijing concordance lookup.
    # Returns fields to be displayed like this:
    #
    # 國風一     召南一之二 小星      1            三五在東
    # parttitle booktitle odetitle stanzanumber glyphs
    #
    # Returns a list, not a dictionary of dictionaries to preserve ordering.

    def concordance(self,glyph):
        cur = connection.cursor()
        # A cross join of two cross joins of shijing, shijingline, shijingstanza, shijingode, shijingpart
        # and shijingbook. Returns all characters occurring in a line containing the input character.
        # Uses AS to ensure unique field names.
        concordanceQuery = "SELECT b.id, b.codepoint, b.glyph, " \
                           "b.line, b.isrhyme, b.rhymeset, b.stanza, " \
                           "b.stanzanumber, b.ode, b.odenumber, " \
                           "b.odetitle, b.parttitle, b.booktitle, b.booknumber, b.parttitle " \
                     "FROM (SELECT  a1.id AS id, a1.codepoint AS codepoint, a1.isrhyme AS isrhyme, a1.line AS line " \
                     "FROM shijing a1, shijingline a2, shijingstanza a3, shijingode a4, shijingbook a5, shijingpart a6 " \
                     "WHERE a1.line = a2.id " \
                     "AND a2.stanza = a3.id " \
                     "AND a3.ode = a4.id " \
                     "AND a4.book = a5.id " \
                     "AND a5.part = a6.id) a, " \
                     "(SELECT  b1.id AS id, b1.codepoint AS codepoint, b1.glyph AS glyph, b1.line AS line, " \
                     "b1.isrhyme AS isrhyme, b2.rhymeset AS rhymeset, " \
                     "b2.stanza AS stanza, b3.number AS stanzanumber, b3.ode AS ode, b4.number AS odenumber, " \
                     "b4.title AS odetitle, b5.number AS booknumber, " \
                     "b5.title AS booktitle, b6.title AS parttitle " \
                     "FROM shijing b1, shijingline b2, shijingstanza b3, shijingode b4, " \
                     "shijingbook b5, shijingpart b6 " \
                     "WHERE b1.line = b2.id " \
                     "AND b2.stanza = b3.id " \
                     "AND b3.ode = b4.id " \
                     "AND b4.book = b5.id " \
                     "AND b5.part = b6.id) b " \
                     "WHERE a.codepoint = '{0}' " \
                     "AND a.isrhyme = 1 " \
                     "AND a.line = b.line " \
                     "ORDER BY a.id, b.id ".format(glyph)
        cur.execute(concordanceQuery)
        lines = cur.fetchall()
        # Creating dictionaries which represent lines of glyphs in Shijing, e.g. 關 關 雎 鳩 gets one dictionary.
        # Four lists hold glyphs, codepoints, rhyme glyphs, rhymesets.
        lineDicts = []
        lineDict = {}
        line = lines[0]
        # First glyph of first line of Shijing.
        shijingId, codepoint, glyph, shijingLine, isRhyme, rhymeset, stanza,  \
                stanzanumber, ode, odenumber, odetitle, booktitle,     \
                booknumber, parttitle =                                \
        line[0], line[1], line[2], line[3], line[4], line[5], line[6], \
                line[7], line[8], line[9], line[10], line[11],         \
                line[12], line[13]
        lineDict["shijingid"], lineDict["glyphs"],         \
            lineDict["line"], lineDict["stanza"], lineDict["stanzanumber"],        \
            lineDict["ode"], lineDict["odenumber"], lineDict["odetitle"],          \
            lineDict["booktitle"], lineDict["booknumber"], lineDict["parttitle"] = \
            shijingId, [[codepoint, glyph]], shijingLine, stanza, stanzanumber,    \
            ode, odenumber, odetitle, booktitle,  booknumber, parttitle
        if isRhyme == 1:
            lineDict["rhymes"] = [glyph]
            lineDict["rhymesets"] = [rhymeset]
        else:
            lineDict["rhymes"] = []
            lineDict["rhymesets"] = []
        # The rest of the glyphs.
        for line in lines[1:]:
            shijingId, codepoint, glyph, isRhyme, rhymeset, stanza, \
                    stanzanumber, ode, odenumber, odetitle, booktitle,    \
                    booknumber, parttitle =                               \
            line[0], line[1], line[2], line[4], line[5], line[6], \
                    line[7], line[8], line[9], line[10], line[11],        \
                    line[12], line[13]
            # When a new line of Shijing begins.
            if not line[3] == shijingLine:
                shijingLine = line[3]
                # Append the old line to the list.
                lineDicts.append(lineDict)
                lineDict = {}
                lineDict["shijingid"], lineDict["glyphs"],                          \
                    lineDict["line"], lineDict["isrhyme"], lineDict["rhymeset"], lineDict["stanza"],        \
                    lineDict["stanzanumber"], lineDict["ode"], lineDict["odenumber"], lineDict["odetitle"], \
                    lineDict["booktitle"], lineDict["booknumber"], lineDict["parttitle"] =                  \
                    shijingId, [[codepoint, glyph]], shijingLine, isRhyme, rhymeset, stanza, stanzanumber,  \
                    ode, odenumber, odetitle, booktitle,  booknumber, parttitle
                if isRhyme == 1:
                    lineDict["rhymes"] = [glyph]
                    lineDict["rhymesets"] = [rhymeset]
                else:
                    lineDict["rhymes"] = []
                    lineDict["rhymesets"] = []
            # When still in the same line of Shijing
            else:
                lineDict["shijingid"],      \
                lineDict["line"], lineDict["stanza"], lineDict["stanzanumber"],        \
                lineDict["ode"], lineDict["odenumber"], lineDict["odetitle"],          \
                lineDict["booktitle"], lineDict["booknumber"], lineDict["parttitle"] = \
                shijingId, shijingLine, stanza,stanzanumber, ode,                      \
                odenumber, odetitle, booktitle,  booknumber, parttitle
                lineDict["glyphs"].append([codepoint,glyph])
                if isRhyme == 1 and glyph not in lineDict["rhymes"]:
                    lineDict["rhymes"].append(glyph)
                    lineDict["rhymesets"].append(rhymeset)
        # Append last dictionary.
        lineDicts.append(lineDict)
        return lineDicts

class Shijing(models.Model):
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    isrhyme = models.IntegerField(null=True, blank=True)
    line = models.IntegerField(null=True, blank=True)
    objects = ShijingManager()
    class Meta:
        db_table = 'shijing'

class Shijingbook(models.Model):
    title = models.TextField(blank=True)
    part = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'shijingbook'

class Shijingline(models.Model):
    rhymeset = models.TextField(blank=True)
    duanrhyme = models.TextField(blank=True)
    stanza = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'shijingline'

class Shijingode(models.Model):
    title = models.TextField(blank=True)
    book = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'shijingode'

class Shijingpart(models.Model):
    title = models.TextField(blank=True)
    class Meta:
        db_table = 'shijingpart'

class Shijingstanza(models.Model):
    number = models.TextField(blank=True)
    ode = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'shijingstanza'

    ######################
    #    Vietnamese      #
    ######################
    
class VietnameseManager(models.Manager):

    # vietnamese()
    # Returns all characters with the passed-in Vietnamese reading, with
    # the readings in Late Middle Chinese (Pulleyblank), Early Middle Chinese
    # (Pulleyblank), Middle Chinee (Baxter) and Middle Chinese (Karlgren).

    # URL:      vietnamese/([a-zđăâêôơưàằầèềìòồờùừỳảẳẩẻểỉỏổởủửỷãẵẫẽễĩõỗỡũữỹáắấéếíóốớúứýạặậẹệịọộợụựỵ]+)/
    # View:     vietnamese()
    # Template: vietnamese.html

    # Returns fields to be presented like this:
    # 東    đông       tǝwŋ towŋ tuwng tung1
    # glyph vietnamese lmc  emc  mcb   mck   

    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # A dictionary of dictionaries, so lines appear in no particular order.
    
    def vietnamese(self,reading):
        cur = connection.cursor()
        vietnameseQuery = "SELECT * FROM " \
                    "(" \
                    "SELECT vietnamese.codepoint, vietnamese.glyph, mc.lmc AS reading, 'lmc' AS period FROM " \
                    "vietnamese " \
                    "LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc " \
                    "ON vietnamese.glyph = mc.glyph WHERE vietnamese.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT vietnamese.codepoint, vietnamese.glyph, mc.emc AS reading, 'emc' AS period FROM " \
                    "vietnamese LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON vietnamese.codepoint = mc.codepoint WHERE vietnamese.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT vietnamese.codepoint, vietnamese.glyph, mc.mcb AS reading, 'mcb' AS period FROM " \
                    "vietnamese " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON vietnamese.codepoint = mc.codepoint WHERE vietnamese.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT vietnamese.codepoint, vietnamese.glyph, mc.mck AS reading, 'mck' AS period FROM " \
                    "vietnamese " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON vietnamese.codepoint = mc.codepoint WHERE vietnamese.reading = '{0}' " \
                    ") AS readings , glyph " \
                    "WHERE readings.codepoint = glyph.codepoint AND glyph.occurrence = 1 " \
                    "ORDER BY readings.glyph, readings.period, readings.reading ".format(reading)
        cur.execute(vietnameseQuery)
        vietnameseList = cur.fetchall()
        vietnameseDict = {}
        for line in vietnameseList:
            codepoint = line[0]
            glyph = line[1]
            if not vietnameseDict.has_key(codepoint):
                vietnameseDict[codepoint] = {"glyph": glyph, \
                                           "vietnamese": reading, "lmc": [], \
                                           "emc": [], "mcb": [], "mck": [], \
                                           "ocp": [], "ocb": []} 
        for line in vietnameseList:
            codepoint = line[0]
            periodReading = line[2]
            period = line[3]
            vietnameseDict[codepoint][period].append(periodReading)
        return vietnameseDict

    # initial()
    # Returns all Vietnamese syllables having the passed-in letter as initial.

    # URL:      vietnameseinitial/([A-ZĐ])/
    # View:     vietnameseinitial()
    # Template: vietnameseinitial.html
    
    # Returns e.g [{'reading': 'ác', 'first': 'a', 'second': 'c'},
    #               'reading': 'ách', 'first': 'a', 'second': 'c'}...]
    # so that e.g. ác ách ạc can be displayed together.
    # A list, not a dictionary of dictionaries to preserve the ordering.
    
    def initial(self,initial):
        cur = connection.cursor()
        initialQuery = "SELECT DISTINCT vietnamese.reading, vietnamese.initial, vietnamese.second FROM vietnamese, glyph " +\
                       "WHERE vietnamese.codepoint = glyph.codepoint " +\
                       "AND vietnamese.initial = '{0}' AND glyph.occurrence = 1 " \
                       "ORDER BY vietnamese.initial, vietnamese.second, vietnamese.reading ".format(initial)
        cur.execute(initialQuery)
        lines = cur.fetchall()
        vietnameseInitialList = []
        for line in lines:
            reading, initial, second = line
            vietnameseInitialList.append({"reading": reading, "initial": initial, "second": second})        
        return vietnameseInitialList
    
class Vietnamese(models.Model):
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    reading = models.TextField(blank=True)
    initial = models.TextField(blank=True)
    objects = VietnameseManager()
    class Meta:
        db_table = 'vietnamese'

    ######################
    #       Wieger      #
    ######################
    
class WiegerManager(models.Manager):

    # wieger()
    # Returns all characters in the passed-in phonetic series in Wieger's
    # Chinese Characters, with the readings in Mandarin, Early Mandarin (Pulleyblank),
    # Late Middle Chinese (Pulleyblank), Early Middle Chinese (Pulleyblank), Middle
    # Chinese (Baxter), Middle Chinese (Karlgren), Old Chinese (Pulleyblank) and Old
    # Chinese (Baxter).

    # URL:      wieger/([0-9]{1,3})/
    # View:     wieger()
    # Template: wieger.html

    # Returns fields to be presented like this:
    # 東    dōng     tuŋ dung1     tǝwŋ towŋ tuwng tung1 [kj]aŋɥ [t]ong
    # glyph mandarin em  cantonese lmc  emc  mcb   mck   ocp     ocb

    # Returns a list of dictionaries to preserve the ordering.

    def wieger(self,series):
        cur = connection.cursor()
        wiegerQuery = "SELECT wieger.codepoint, wieger.glyph, wieger.id, " \
                    "mandarin.pinyin, '0 mandarin' AS dialect FROM " \
                    "wieger, mandarin " \
                    "WHERE wieger.codepoint = mandarin.codepoint " \
                    "AND wieger.phonetic = '{0}' " \
                    "UNION ALL " \
                    "SELECT wieger.codepoint, wieger.glyph, wieger.id, " \
                    "cantonese.reading, '1 cantonese' AS dialect FROM " \
                    "wieger, cantonese " \
                    "WHERE wieger.codepoint = cantonese.codepoint " \
                    "AND wieger.phonetic = '{0}' " \
                    "UNION ALL " \
                    "SELECT wieger.codepoint, wieger.glyph, wieger.id, " \
                    "em.reading, '2 em' AS dialect FROM " \
                    "wieger LEFT JOIN " \
                    "(SELECT * FROM zhongyuanyinyun, earlymandarin " \
                    "WHERE zhongyuanyinyun.homophone = earlymandarin.id) em " \
                    "WHERE wieger.codepoint = em.codepoint " \
                    "AND wieger.phonetic = '{0}' " \
                    "UNION ALL " \
                    "SELECT wieger.codepoint, wieger.glyph, wieger.id, " \
                    "mc.lmc, '3 lmc' AS dialect FROM " \
                    "wieger LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc " \
                    "WHERE wieger.codepoint = mc.codepoint AND wieger.phonetic = '{0}' " \
                    "UNION ALL " \
                    "SELECT wieger.codepoint, wieger.glyph, wieger.id, " \
                    "mc.emc, '4 emc' AS dialect FROM " \
                    "wieger LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "WHERE wieger.codepoint = mc.codepoint AND wieger.phonetic = '{0}' " \
                    "UNION ALL " \
                    "SELECT wieger.codepoint, wieger.glyph, wieger.id, " \
                    "mc.mcb, '5 mcb' AS dialect FROM " \
                    "wieger LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "WHERE wieger.codepoint = mc.codepoint AND wieger.phonetic = '{0}' " \
                    "UNION ALL " \
                    "SELECT wieger.codepoint, wieger.glyph, wieger.id, " \
                    "mc.mck, '6 mck' AS dialect FROM " \
                    "wieger LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "WHERE wieger.codepoint = mc.codepoint AND wieger.phonetic = '{0}' " \
                    "UNION ALL " \
                    "SELECT wieger.codepoint, wieger.glyph, wieger.id, " \
                    "gsr.pulleyblank, '7 ocp' AS dialect FROM " \
                    "wieger, gsr " \
                    "WHERE wieger.codepoint = gsr.codepoint " \
                    "AND wieger.phonetic = '{0}' " \
                    "UNION ALL " \
                    "SELECT wieger.codepoint, wieger.glyph, wieger.id, " \
                    "gsr.baxter, '8 ocb' AS dialect FROM " \
                    "wieger, gsr " \
                    "WHERE wieger.codepoint = gsr.codepoint " \
                    "AND wieger.phonetic = '{0}' " \
                    "ORDER BY wieger.id, dialect" \
                    " ".format(series)
        cur.execute(wiegerQuery)
        wiegerList = cur.fetchall()
        wiegerDicts = []
        codepoint, glyph = wiegerList[0][0], wiegerList[0][1]
        wiegerDict = {"codepoint": codepoint, "glyph": glyph, "mandarin": [], "cantonese": [], \
                                           "em": [], \
                                           "lmc": [], "emc": [], "mcb": [], "mck": [], \
                                           "ocp": [], "ocb": []}
        for line in wiegerList:
            codepoint, glyph, id, reading, dialect = line
            dialect = dialect[2:]
            if not wiegerDict["codepoint"] == codepoint:
                wiegerDicts.append(wiegerDict)
                wiegerDict = {"codepoint": codepoint, "glyph": glyph, "mandarin": [], "cantonese": [], \
                                           "em": [], \
                                           "lmc": [], "emc": [], "mcb": [], "mck": [], \
                                           "ocp": [], "ocb": []}
            wiegerDict[dialect].append(reading)
        wiegerDicts.append(wiegerDict)
        return wiegerDicts

class Wieger(models.Model):
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    phonetic = models.IntegerField(blank=True)
    type = models.TextField(blank=True)
    objects = WiegerManager()
    class Meta:
        db_table = 'wieger'

class Yjrhyme(models.Model):
    kaihe = models.TextField(blank=True)
    neiwai = models.TextField(blank=True)
    she = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'yjrhyme'

    ######################
    #       Yunjing      #
    ######################
    
class YunjingManager(models.Manager):

    # yunjingtextbyrhyme()
    # Returns the Yunjing table numbered by the passed-in number.

    # URL:      yunjingtextbyrhyme/([0-9]{1,2})/
    # View:     yunjingtextbyrhyme()
    # Template: yunjingtextbyrhyme.html

    # Selects the contents of a single page of Yunjing containing one rhyme.
    # Formatting is performed in templates and CSS.
    
    def yunjingtextbyrhyme(self,rhyme):
        yunjingPageQuery = "SELECT a.id, a.codepoint, a.glyph, a.initial, a.phonation, a.articulation, " \
                    "a.grade, a.tone, a.line, a.lmc, a.rhyme, a.guangyun, " \
                    "b.rhymelabel, b.rusheng, b.fanqie, b.gradekeys1, b.gradekeys2, b.gradekeys3, b.gradekeys4 " \
                    "FROM yunjing a, " \
                    "yjrhyme b " \
                    "WHERE rhyme = '{0}' " \
                    "AND a.rhyme = b.id ".format(rhyme)
        cur = connection.cursor()
        cur.execute(yunjingPageQuery)
        lines = cur.fetchall()
        lineDicts = []
        leftLineDicts = []
        rightLineDicts = []
        for line in lines:
            lineDict = {}
            lineDict["id"], lineDict["codepoint"], lineDict["glyph"], \
            lineDict["initial"], lineDict["phonation"], lineDict["articulation"], \
            lineDict["grade"], lineDict["tone"], lineDict["line"], \
            lineDict["lmc"], lineDict["rhyme"], lineDict["guangyun"], \
            lineDict["rhymelabel"], lineDict["rusheng"], lineDict["fanqie"], \
            lineDict["gradekeys1"], lineDict["gradekeys2"], lineDict["gradekeys3"], lineDict["gradekeys4"] = line
            if lineDict["initial"] > 12:
                leftLineDicts.append(lineDict)
            else:
                rightLineDicts.append(lineDict)
        lineDicts = {"title":u"Yunjing","left":tuple(leftLineDicts),"right":tuple(rightLineDicts)}
        return lineDicts

    def concordance(self,codepoint):
        yunjingConcordanceQuery = "SELECT a1.codepoint, a1.glyph, a1.homophone, " \
                                  "a2.yunjing, " \
                                  "a3.number, a3.rhyme, a3.finalglyph, a3.tongyong, a3.sectionlabel, " \
                                  "a4.number, " \
                                  "b1.id, b1.line, b1.codepoint, b1.glyph, " \
                                  "b1.rhyme, b1.tone, b1.grade, b1.initial, b1.lmc, " \
                                  "b2.id, b2.codepoint, b2.glyph, b2.rhyme, b2.tone, " \
                                  "b2.grade, b2.initial, " \
                                  "b3.rhymelabel, b3.rusheng, b3.fanqie, " \
                                  "b3.gradekeys1, b3.gradekeys2, b3.gradekeys3, b3.gradekeys4 " \
                                  "FROM (SELECT codepoint, glyph, homophone " \
                                  "FROM guangyun ) a1, " \
                                  "(SELECT id, number, final, yunjing " \
                                  " FROM gyhomophone ) a2, " \
                                  "(SELECT id, number, tone, rhyme, finalglyph, tongyong, sectionlabel " \
                                  " FROM gyfinal ) a3, " \
                                  "(SELECT id, number " \
                                  " FROM gytone ) a4, " \
                                  "(SELECT id, line, codepoint, glyph, rhyme, tone, grade, initial, lmc " \
                                  " FROM yunjing) b1,  " \
                                  "(SELECT id, line, codepoint, glyph, rhyme, tone, grade, initial " \
                                  " FROM yunjing) b2, " \
                                  "(SELECT id, rhymelabel, rusheng, fanqie, " \
                                  " gradekeys1, gradekeys2, gradekeys3, gradekeys4 " \
                                  " FROM yjrhyme ) b3 " \
                                  "WHERE a1.codepoint =  '{0}' " \
                                  "AND a1.homophone = a2.id " \
                                  "AND a2.final = a3.id " \
                                  "AND a3.tone = a4.id " \
                                  "AND b2.id = a2.yunjing " \
                                  "AND b2.rhyme = b1.rhyme " \
                                  "AND b2.rhyme = b3.id " \
                                  "ORDER BY a1.homophone, b3.id, b2.id, b1.id".format(codepoint)
                                  
        cur = connection.cursor()
        cur.execute(yunjingConcordanceQuery)
        lines = cur.fetchall()
        leftLineDicts = []
        rightLineDicts = []
        for line in lines:
            yunjingDict = {}
            yunjingDict["guangyuncodepoint"], yunjingDict["guangyunglyph"], \
                yunjingDict["guangyunhomophone"], yunjingDict["guangyuntoyunjing"], \
                yunjingDict["guangyunfinalnumber"], yunjingDict["guangyunrhyme"], \
                yunjingDict["guangyunfinalglyph"], yunjingDict["guangyuntongyong"], \
                yunjingDict["guangyunsectionlabel"], yunjingDict["yunjinghomophone"], \
                yunjingDict["yunjingid"], yunjingDict["yunjingline"], yunjingDict["yunjingcodepoint"], \
                yunjingDict["yunjingglyph"], yunjingDict["yunjingrhyme"], \
                yunjingDict["yunjingtone"], yunjingDict["yunjinggrade"], \
                yunjingDict["yunjinginitial"], yunjingDict["lmc"], \
                yunjingDict["yunjinghomophoneid"], yunjingDict["yunjinghomophonecodepoint"], \
                yunjingDict["yunjinghomophoneglyph"], yunjingDict["yunjinghomophonerhyme"], \
                yunjingDict["yunjinghomophonetone"], yunjingDict["yunjinghomophonegrade"], \
                yunjingDict["yunjinghomophoneinitial"], yunjingDict["rhymelabel"], \
                yunjingDict["rusheng"], yunjingDict["fanqie"], \
                yunjingDict["gradekeys1"], yunjingDict["gradekeys2"], \
                yunjingDict["gradekeys3"], yunjingDict["gradekeys4"] = line
            if yunjingDict["yunjinginitial"] > 12:
                leftLineDicts.append(yunjingDict)
            else:
                rightLineDicts.append(yunjingDict)
        yunjingDicts = {"title":u"Yunjing","left":tuple(leftLineDicts),"right":tuple(rightLineDicts)}
        return yunjingDicts       

class Yunjing(models.Model):
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    initial = models.IntegerField(null=True, blank=True)
    phonation = models.IntegerField(null=True, blank=True)
    articulation = models.IntegerField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    tone = models.IntegerField(null=True, blank=True)
    line = models.IntegerField(null=True, blank=True)
    lmc = models.TextField(blank=True)
    rhyme = models.IntegerField(null=True, blank=True)
    guangyun = models.IntegerField(null=True, blank=True)
    objects = YunjingManager()
    class Meta:
        db_table = 'yunjing'


    ######################
    #  Zhongyuanyinyun   #
    ######################
    
class ZhongyuanyinyunManager(models.Manager):

    # em()
    # Returns all characters with the passed-in Early Mandarin reading (Pulleyblank), with the readings in 
    # Late Middle Chinese (Pulleyblank), Early Middle Chinese (Pulleyblank),
    # Middle Chinese (Baxter), Middle Chinese (Karlgren), Old Chinese (Pulleyblank) and Old Chinese (Baxter).

    # URL:      em/([a-zʂŋʋă‘]{1,7}[´ˇ`]{0,1})/
    # View:     em()
    # Template: em.html

    # Returns fields to be presented like this:
    # 東    tuŋ tǝwŋ towŋ tuwng tung1 [kj]aŋɥ [t]ong
    # glyph em  lmc  emc  mcb   mck   ocp     ocb

    # The reason for the use of UNION ALL rather than a cross join in the query
    # is that a character may have a single reading in one dialect 
    # and multiple readings in another.
    
    # A dictionary of dictionaries, so lines appear in no particular order.
    
    def em(self,reading):
        cur = connection.cursor()
        zhongyuanyinyunQuery = "SELECT * FROM " \
                    "(" \
                    "SELECT em.codepoint, em.glyph, mc.lmc AS reading, 'lmc' AS period FROM " \
                    "(SELECT * FROM zhongyuanyinyun, earlymandarin WHERE zhongyuanyinyun.homophone = earlymandarin.id) em " \
                    "LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing " \
                    "WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc " \
                    "ON em.glyph = mc.glyph WHERE em.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT em.codepoint, em.glyph, mc.emc AS reading, 'emc' AS period FROM " \
                    "(SELECT * FROM zhongyuanyinyun, earlymandarin WHERE zhongyuanyinyun.homophone = earlymandarin.id) em " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON em.codepoint = mc.codepoint WHERE em.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT em.codepoint, em.glyph, mc.mcb AS reading, 'mcb' AS period FROM " \
                    "(SELECT * FROM zhongyuanyinyun, earlymandarin WHERE zhongyuanyinyun.homophone = earlymandarin.id) em  " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON em.codepoint = mc.codepoint WHERE em.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT em.codepoint, em.glyph, mc.mck AS reading, 'mck' AS period FROM " \
                    "(SELECT * FROM zhongyuanyinyun, earlymandarin WHERE zhongyuanyinyun.homophone = earlymandarin.id) em  " \
                    "LEFT JOIN " \
                    "(SELECT * FROM guangyun, gyhomophone " \
                    "WHERE guangyun.homophone = gyhomophone.id) mc " \
                    "ON em.codepoint = mc.codepoint WHERE em.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT em.codepoint, em.glyph, gsr.pulleyblank AS reading, 'ocp' AS period FROM " \
                    "(SELECT * FROM zhongyuanyinyun, earlymandarin WHERE zhongyuanyinyun.homophone = earlymandarin.id) em  " \
                    "LEFT JOIN gsr " \
                    "ON em.codepoint = gsr.codepoint WHERE em.reading = '{0}' " \
                    "UNION ALL " \
                    "SELECT em.codepoint, em.glyph, gsr.baxter AS reading, 'ocb' AS period FROM " \
                    "(SELECT * FROM zhongyuanyinyun, earlymandarin WHERE zhongyuanyinyun.homophone = earlymandarin.id) em  " \
                    "LEFT JOIN gsr " \
                    "ON em.codepoint = gsr.codepoint WHERE em.reading = '{0}' " \
                    ") AS readings , glyph " \
                    "WHERE readings.codepoint = glyph.codepoint AND glyph.occurrence = 1 " \
                    "ORDER BY readings.glyph, readings.period, readings.reading ".format(reading)
        cur.execute(zhongyuanyinyunQuery)
        zhongyuanyinyunList = cur.fetchall()
        zhongyuanyinyunDict = {}
        for line in zhongyuanyinyunList:
            codepoint = line[0]
            glyph = line[1]
            periodreading = line[2]
            period = line[3]
            if not zhongyuanyinyunDict.has_key(codepoint):
                zhongyuanyinyunDict[codepoint] = {"glyph": glyph, "em": reading, period: [periodreading]}
            elif not zhongyuanyinyunDict[codepoint].has_key(period):
                zhongyuanyinyunDict[codepoint][period] = [periodreading]
            else:
                zhongyuanyinyunDict[codepoint][period].append(reading)
        return zhongyuanyinyunDict

    # concordance()
    # Returns the text of the Zhongyuan Yinyun homophones containing the passed-in character.

    # URL:      zhongyuanyinyunconcordance/(U\+[\dABCDEF]{1,5})/
    # View:     zhongyuanyinyunconcordance()
    # Template: zhongyuanyinyunconcordance.html

    # A Zhongyuan Yinyun concordance lookup.
    # Returns fields to be displayed like this:
    #
    # 東鍾   平聲陰  1	      tuŋ      東冬

    # rhyme final   homophone reading glyphs
    #
    # Returns a list, not a dictionary of dictionaries to preserve ordering.

    def concordance(self,codepoint):
        cur = connection.cursor()
        linesQuery = "SELECT b.codepoint, b.glyph, b.reading, b.annotation, b.homophonenumber, " \
                     "b.finallabel, b.rhymelabel, b.rhyme " \
                     "FROM " \
                     "(SELECT a1.codepoint AS codepoint, a1.homophone AS homophone " \
                     " FROM zhongyuanyinyun AS a1, earlymandarin AS a2 " \
                     " WHERE a1.homophone = a2.id) a, " \
                     "(SELECT b1.id AS id, b1.codepoint AS codepoint, b1.glyph AS glyph, " \
                     " b1.homophone AS homophone, b1.annotation AS annotation, " \
                     " b2.reading AS reading, " \
                     " b3.id AS homophoneid, b3.number AS homophonenumber, " \
                     " b4.label AS finallabel, b5.number AS rhyme, b5.label AS rhymelabel " \
                     " FROM zhongyuanyinyun AS b1, earlymandarin AS b2, zyhomophone AS b3, zyfinal AS b4, zyrhyme AS b5 " \
                     " WHERE b1.homophone = b2.id AND b1.homophone = b3.id AND b3.final = b4.id AND b4.rhyme = b5.id) b " \
                     "WHERE a.codepoint = '{0}' " \
                     "AND a.homophone = b.homophone ".format(codepoint)
        cur.execute(linesQuery)
        lines = cur.fetchall()
        zhongyuanyinyunDicts = []
        for line in lines:
            zhongyuanyinyunDict = {}
            zhongyuanyinyunDict["codepoint"], zhongyuanyinyunDict["glyph"], \
                zhongyuanyinyunDict["reading"], zhongyuanyinyunDict["annotation"], \
                zhongyuanyinyunDict["homophone"],zhongyuanyinyunDict["final"], \
                zhongyuanyinyunDict["rhymelabel"], zhongyuanyinyunDict["rhyme"] = line
            zhongyuanyinyunDicts.append(zhongyuanyinyunDict)
        return zhongyuanyinyunDicts

    # textbyrhyme()
    # Returns all characters with the passed-in Zhongyuan Yinyun rhyme, with the readings in
    # Early Mandarin (Pulleyblank).

    # URL:      zhongyuanyinyuntextbyrhyme/([0-9]{1,2})/
    # View:     zhongyuanyinyuntextbyrhyme()
    # Template: zhongyuanyinyuntextbyrhyme.html

    # returns fields to be presented like this:
    # 東鍾          平聲陰
    # rhymelabel    finallabel
    # ...
    # xuŋ	烘 叿 [入聲] 轟 薨
    # reading   glyphs and annotations

    def textbyrhyme(self,rhyme):
        rhymeQuery = "SELECT * " \
                    "FROM (SELECT zhongyuanyinyun.codepoint, zhongyuanyinyun.glyph, " \
                    "zhongyuanyinyun.annotation, earlymandarin.reading, " \
                    "zyhomophone.id, zyhomophone.number, zyfinal.rhyme, zyfinal.label, " \
                    "zyrhyme.label AS label1 " \
                    "FROM zhongyuanyinyun, earlymandarin, zyhomophone, zyfinal, zyrhyme " \
                    "WHERE zhongyuanyinyun.homophone = earlymandarin.id " \
                    "AND zhongyuanyinyun.homophone = zyhomophone.id " \
                    "AND zyhomophone.final = zyfinal.id " \
                    "AND zyrhyme.id = zyfinal.rhyme " \
                    "AND zyrhyme.number = '{0}') ".format(rhyme)
        cur = connection.cursor()
        cur.execute(rhymeQuery)
        finals = cur.fetchall()
        lineDicts = []
        for line in finals:
            lineDict = {}
            lineDict["codepoint"], lineDict["glyph"], lineDict["annotation"], lineDict["earlymandarin"], \
            lineDict["homophoneid"], lineDict["homophone"], lineDict["final"], lineDict["finallabel"], \
            lineDict["rhymelabel"] = line
            lineDicts.append(lineDict)
        return lineDicts
    
class Zhongyuanyinyun(models.Model):
    codepoint = models.TextField(blank=True)
    glyph = models.TextField(blank=True)
    homophone = models.IntegerField(null=True, blank=True)
    annotation = models.TextField(blank=True)
    objects = ZhongyuanyinyunManager()
    class Meta:
        db_table = 'zhongyuanyinyun'

class Zyfinal(models.Model):
    number = models.TextField(blank=True)
    tonenumber = models.TextField(blank=True)
    toneletter = models.TextField(blank=True)
    label = models.TextField(blank=True)
    rhyme = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'zyfinal'

class Zyhomophone(models.Model):
    number = models.TextField(blank=True)
    final = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'zyhomophone'

class Zyrhyme(models.Model):
    number = models.TextField(blank=True)
    label = models.TextField(blank=True)
    class Meta:
        db_table = 'zyrhyme'

