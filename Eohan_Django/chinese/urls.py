# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.static import *
from django.views.generic import RedirectView
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles import *

from cp.views import \
     cantonese, \
     cantoneseinitial, \
     em, \
     emc, \
     fourcornercode, \
     glyph, \
     gsrconcordance, \
     gsrtextbyrhyme, \
     guangyunconcordance, \
     guangyuntextbyfinal, \
     japanese, \
     japaneseinitial, \
     karlgren, \
     korean, \
     koreaninitial, \
     lmc, \
     main, \
     mandarin, \
     mandarininitial, \
     mandarintoneless, \
     mcb, \
     mck, \
     ocb, \
     ock, \
     ocp, \
     radical, \
     radicallist, \
     search, \
     shijingconcordance, \
     shijingtextbybook, \
     vietnamese, \
     vietnameseinitial, \
     wieger, \
     yunjingconcordance, \
     yunjingtextbyrhyme, \
     zhongyuanyinyunconcordance, \
     zhongyuanyinyuntextbyrhyme

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(ur'^$', 'chinese.views.home', name='home'),
    # url(ur'^chinese/', include('chinese.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(ur'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(ur'^admin/', include(admin.site.urls)),
    url(ur'^$',main),
    url(ur'^/$',main),
    url(ur'^cantonese/([a-z]{1,6}[1-6])/$',cantonese),
    url(ur'^cantoneseinitial/([A-Z])/$',cantoneseinitial),
    url(ur'^em/([a-zʂŋʋă‘]{1,7}[´ˇ`]{0,1})/$', em),
    url(ur'^emc/([a-zʔɕʂʐʑɲŋɣ‘ăǝɛɔɨ]{1,7}[ˀʰ]{0,1})$', emc),
    url(ur'^fourcornercode/(U\+[\dABCDEF]{1,5})/$',fourcornercode),
    url(ur'^glyph/(U\+[\dABCDEF]{1,5})/$', glyph),
    url(ur'^gsrconcordance/(U\+[\dABCDEF]{1,5})/$', gsrconcordance),
    url(ur'^gsrtextbyrhyme/([0-9]{1,4})-([0-9]{1,4})/$', gsrtextbyrhyme),
    url(ur'^guangyunconcordance/(U\+[\dABCDEF]{1,5})$', guangyunconcordance),
    url(ur'^guangyuntextbyfinal/([0-9]{1,3})$', guangyuntextbyfinal),
    url(ur'^japanese/([a-z]+)/$',japanese),
    url(ur'^japaneseinitial/([A-Z])/$',japaneseinitial),
    url(ur'^karlgren/([0-9]{1,4})/$',karlgren),
    url(ur'^korean/([a-z]+)/$',korean),
    url(ur'^koreaninitial/([A-Z])/$',koreaninitial),
    url(ur'^lmc/([a-zʔʂɦŋʋŗȥăǝ]{1,7}[´`]{0,1})/$',lmc),
    url(ur'^main/$',main),
    url(ur'^mandarin/([a-zāáǎàēéěèīíǐìōóǒòūúǔùüǖǘǚǜ]{1,6})/$',mandarin),
    url(ur'^mandarininitial/([A-Z])/$',mandarininitial),
    url(ur'^mandarintoneless/([a-zü]{1,6})/$',mandarintoneless),
    url(ur'^mcb/([a-zæɛɨ]{1,8}[XH]{0,1})/$',mcb),
    url(ur'^mck/([a-zậåăäaɒɛĕe̯ǝw‘ˑχɣˆṣẓńśź123]{1,9})/$',mck),
    url(ur'^ocb/([a-zSɦNɨʔ]{1,9})/$',ocb),
    url(ur'^ock/([a-zâaåăɛe̯ĕǝôọŏŭ‘χˆńṣẓˑ123]{1,9})/$',ock),
    url(ur'^ocp/([a-zə́ə̀áà\(\)\:ŋɣɥ]{1,4}[ăʃ]{0,1})/$',ocp),
    url(ur'^radical/([0-9]{1,3})/$',radical),
    url(ur'^radicallist/$',radicallist),
    #url(ur'^search/?q=(\p{Han})$',search),
    url(ur'^search/$',search),
    url(ur'^shijingconcordance/(U\+[\dABCDEF]{1,5})$', shijingconcordance),
    url(ur'^shijingtextbybook/([0-9]{1,2})$', shijingtextbybook),
    url(ur'^vietnamese/([a-zđăâêôơưàằầèềìòồờùừỳảẳẩẻểỉỏổởủửỷãẵẫẽễĩõỗỡũữỹáắấéếíóốớúứýạặậẹệịọộợụựỵ]+)/$',vietnamese),
    url(ur'^vietnameseinitial/([A-ZĐ])/$',vietnameseinitial),
    url(ur'^wieger/([0-9]{1,3})/$',wieger),
    url(ur'^yunjingconcordance/(U\+[\dABCDEF]{1,5})/$', yunjingconcordance),
    url(ur'^yunjingtextbyrhyme/([0-9]{1,2})$', yunjingtextbyrhyme),
    url(ur'^zhongyuanyinyunconcordance/(U\+[\dABCDEF]{1,5})/$', zhongyuanyinyunconcordance),
    url(ur'^zhongyuanyinyuntextbyrhyme/([0-9]{1,2})/$', zhongyuanyinyuntextbyrhyme),
)
