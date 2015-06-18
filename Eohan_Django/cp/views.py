# Create your views here.
from django.template.loader import get_template
from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection
from django.core.urlresolvers import reverse
from django.conf import settings

from models import *

##import pickle, codecs
##
### Get codepoints to glyphs.
### Needed to validate input to Search.
##
##f=codecs.open("codepointToGlyphDict.py","rb")
##codepointToGlyphDict = pickle.load(f)
##f.close()

def cantonese(request,reading):
    cantoneseDict = Cantonese.objects.cantonese(reading)
    return render(request,'cantonese.html',{'cantonese':cantoneseDict,'title':u"Cantonese"})

def cantoneseinitial(request,initial):
    cantoneseinitial = Cantonese.objects.initial(initial)
    return render(request,'cantoneseinitial.html',{'cantoneseinitial':cantoneseinitial,'title':u"Cantonese " + initial})

def em(request,reading):
    earlymandarin = Zhongyuanyinyun.objects.em(reading)
    return render(request,'earlymandarin.html',{'earlymandarin':earlymandarin,'title':u"Early Mandarin"})

def emc(request,reading):
    emc = Guangyun.objects.emc(reading)
    return render(request,'emc.html',{'emc':emc,'title':u"Guangyun"})
       
def fourcornercode(request,codepoint):
    fourcornercode = Fourcornercode.objects.fourcornercode(codepoint)
    return render(request,'fourcornercode.html',{'fourcornercode':fourcornercode,'title':u"Four Corner Code"})
       
def glyph(request,codepoint):
    glyph = Glyph.objects.glyph(codepoint)
    return render(request,'glyph.html',
                  {'glyph':glyph,'title':glyph["glyph"][0]})

def gsrconcordance(request,codepoint):
    gsrconcordance = Gsr.objects.concordance(codepoint)
    return render(request,'gsrconcordance.html',{'gsrconcordance':gsrconcordance,'title':u"Grammata Serica Recensa"})
    
def gsrtextbyrhyme(request,lower,upper):
    lower = int(lower)-1
    upper = int(upper)-1
    gsr = Gsr.objects.gsrtextbyrhyme(lower,upper)
    return render(request,'gsrtextbyrhyme.html',{'gsr':gsr,'title':u"Grammata Serica Recensa"})

def guangyunconcordance(request,codepoint):
    guangyunconcordance = Guangyun.objects.concordance(codepoint)
    return render(request,'guangyunconcordance.html',{'guangyunconcordance':guangyunconcordance,'title':u"Guangyun"})

def guangyuntextbyfinal(request,final):
    guangyuntextbyfinal = Guangyun.objects.guangyuntextbyfinal(final)
    return render(request,'guangyuntextbyfinal.html',{'guangyuntextbyfinal':guangyuntextbyfinal,'title':u"Guangyun"})

def japanese(request,reading):
    japanese = Japaneseon.objects.japanese(reading)
    return render(request,'japanese.html',{'japanese':japanese,'title':u"Japanese"})

def japaneseinitial(request,initial):
    japaneseinitial = Japaneseon.objects.initial(initial)
    return render(request,'japaneseinitial.html',{'japaneseinitial':japaneseinitial,'title':u"Japanese " + initial})

def karlgren(request,series):
    karlgren = Karlgren.objects.karlgren(series)
    return render(request,'karlgren.html',{'karlgren':karlgren,'title':u"Karlgren: Analytic Dictionary"})
   
def korean(request,reading):
    korean = Korean.objects.korean(reading)
    return render(request,'korean.html',{'korean':korean,'title':u"Korean"})

def koreaninitial(request,initial):
    koreaninitial = Korean.objects.initial(initial)
    return render(request,'koreaninitial.html',{'koreaninitial':koreaninitial,'title':u"Korean " + initial})

def lmc(request,reading):
    lmc = Guangyun.objects.lmc(reading)
    return render(request,'lmc.html',{'lmc':lmc,'title':u"Late Middle Chinese"})

def main(request):
    return render(request,'main.html',{'main':{},'title':u"Eohan"})

def mandarin(request,reading):
    mandarin = Mandarin.objects.mandarin(reading)
    return render(request,'mandarin.html',{'mandarin':mandarin,'title':u"Mandarin"})

def mandarintoneless(request,reading):
    mandarintoneless = Mandarin.objects.mandarintoneless(reading)
    return render(request,'mandarintoneless.html',{'mandarintoneless':mandarintoneless,'title':u"Mandarin"})

def mandarininitial(request,initial):
    mandarininitial = Mandarin.objects.initial(initial)
    return render(request,'mandarininitial.html',{'mandarininitial':mandarininitial,'title':u"Mandarin " + initial})

def mcb(request,reading):
    mcb = Guangyun.objects.mcb(reading)
    return render(request,'mcb.html',{'mcb':mcb,'title':u"Middle Chinese (Baxter)"})
             
def mck(request,reading):
    mck = Guangyun.objects.mck(reading)
    return render(request,'mck.html',{'mck':mck,'title':u"Middle Chinese (Karlgren)"})
             
def ocb(request,final):
    ocb = Gsr.objects.ocb(final)
    return render(request,'ocb.html',{'ocb':ocb,'title':u"Old Chinese (Baxter)"})

def ock(request,final):
    ock = Gsr.objects.ock(final)
    return render(request,'ock.html',{'ock':ock,'title':u"Old Chinese (Karlgren)"})

def ocp(request,final):
    ocp = Gsr.objects.ocp(final)
    return render(request,'ocp.html',{'ocp':ocp,'title':u"Old Chinese (Pulleyblank)"})

def radical(request,radicalnumber):
    radical = Radical.objects.radical(int(radicalnumber))
    return render(request,'radical.html',{'radical':radical,'title':u"Radical " + radicalnumber})

def radicallist(request):
    #radicallist = Radical.objects.radicallist()
    return render(request,'radicallist.html')

def search(request):
    glyph = request.GET["q"][0]
    # Validate input: probably not the best way.
    if len(glyph) < 2:
        search = Glyph.objects.search(glyph)
        return render(request,'glyph.html',
                      {'glyph':search,'title':glyph})
    else:
        return render(request,'main.html',{'main':{},'title':u"Eohan"})

def shijingconcordance(request,codepoint):
    shijingconcordance = Shijing.objects.concordance(codepoint)
    return render(request,'shijingconcordance.html',
                  {'shijingconcordance':shijingconcordance,'title':"Shijing"})

def shijingtextbybook(request,book):
    shijingtextbybook = Shijing.objects.shijingtextbybook(book)
    return render(request,'shijingtextbybook.html',{'shijingtextbybook':shijingtextbybook,'title':u"Shijing"})

def vietnamese(request,reading):
    vietnamese = Vietnamese.objects.vietnamese(reading)
    return render(request,'vietnamese.html',{'vietnamese':vietnamese,'title':u"Vietnamese"})

def vietnameseinitial(request,initial):
    vietnameseinitial = Vietnamese.objects.initial(initial)
    return render(request,'vietnameseinitial.html',{'vietnameseinitial':vietnameseinitial,'title':u"Vietnamese " + initial})

def wieger(request,phonetic):
    wieger = Wieger.objects.wieger(phonetic)
    return render(request,'wieger.html',{'wieger':wieger,'title':u"Wieger Phonetic Series"})
   
def yunjingconcordance(request,codepoint):
    yunjingconcordance = Yunjing.objects.concordance(codepoint)
    return render(request,'yunjingconcordance.html',{'yunjingconcordance':yunjingconcordance,'title':u"Yunjing"})

def yunjingtextbyrhyme(request,rhyme):
    yunjingtextbyrhyme = Yunjing.objects.yunjingtextbyrhyme(rhyme)
    return render(request,'yunjingtextbyrhyme.html',{'yunjingtextbyrhyme':yunjingtextbyrhyme,'title':u"Yunjing"})

def zhongyuanyinyunconcordance(request,codepoint):
    zhongyuanyinyunconcordance = Zhongyuanyinyun.objects.concordance(codepoint)
    return render(request,'zhongyuanyinyunconcordance.html',{'zhongyuanyinyunconcordance':zhongyuanyinyunconcordance,'title':u"Zhongyuan Yinyun"})

def zhongyuanyinyuntextbyrhyme(request,rhyme):
    zhongyuanyinyuntextbyrhyme = Zhongyuanyinyun.objects.textbyrhyme(rhyme)
    return render(request,'zhongyuanyinyuntextbyrhyme.html',{'zhongyuanyinyuntextbyrhyme':zhongyuanyinyuntextbyrhyme,'title':u"Zhongyuan Yinyun"})

