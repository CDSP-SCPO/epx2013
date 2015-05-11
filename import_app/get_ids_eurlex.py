"""
get the ids from eurlex
"""
import urllib
import re
from bs4 import BeautifulSoup
from common import config_file as conf

#log file
import logging
logger = logging.getLogger(__name__)


def get_url_eurlex(no_celex, tab="ALL"):
    """
    FUNCTION
    return the eurlex url
    PARAMETERS
    no_celex: no_celex variable [string]
    tab: "ALL" used to retrieve info or "HIS" (PROCEDURE) used to retrieve ids [string]
    RETURN
    url: url of the eurlex page [string]
    """
    #http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32006R1921:EN:NOT
    #~ url_eurlex="http://new.eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:NOCELEX"
    #~ url_eurlex="http://new.eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:NOCELEX"
    url=conf.url_eurlex
    if tab=="HIS":
        url=url.replace("ALL", tab, 1)
    url=url.replace("NOCELEX", no_celex, 1)
    return url


def get_url_content_eurlex(url):
    """
    FUNCTION
    check if the eurlex url exists and return its content
    PARAMETERS
    url: eurlex url [string]
    RETURN
    url_content: content of the page if the url exists and false otherwise [BeautifulSoup object]
    """
    url_content=False
    try:
        #use html.parser to parse the page
        soup=BeautifulSoup(urllib.urlopen(url), "html.parser")
        #http://new.eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32006L1929
        if not(soup.find(text="The requested document does not exist.")):
            url_content=soup
    except:
        logger.debug("no content for eurlex url"+ str(e))
        print "no content for eurlex url"

    return url_content


def get_no_celex(soup):
    """
    FUNCTION
    get no_celex from eurlex
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    no_celex variable [string]
    """
    no_celex=None
    try:
        #<title>EUR-Lex - 32006R1921 - EN - EUR-Lex</title>
        no_celex=soup.title.string.split("-")[2].strip()
    except Exception, e:
        print "no no_celex", e

    return no_celex


def get_chrono(chrono):
    """
    FUNCTION
    remove the 0 at the beginning of the oeil no_chrono field
    PARAMETERS
    chrono: no_chrono variable [string]
    RETURN
    updated no_chrono [string]
    """
    index_start=0
    #we remove the 0s at the beginning
    for character in chrono:
        if character=="0":
            index_start+=1
        else:
            break
    chrono=chrono[index_start:]
    #remove space around bracket (44 - 07)
    chrono=chrono.replace(" ", "")
    #remove zero directly after dash (44-07 -> 44-7)
    index=chrono.find("-")
    if index!=-1 and chrono[index+1]=="0":
        chrono=chrono[:index+1]+chrono[index+2:]

    return chrono


def get_nos_unique(soup):
    """
    FUNCTION
    get oeil ids from eurlex
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    no_unique_type, no_unique_annee and no_unique_chrono variables [string, int, string]
    """
    exist=True
    #http://new.eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32006R1921
    try:
        url=soup.find(text="European Parliament - Legislative observatory").parent.parent['href']
        #~ print "old oeil url (eurlex):", url
        #http://www.europarl.europa.eu/oeil/FindByProcnum.do?lang=2&procnum=COD/2005/0223
        url=url[url.rfind('='):][1:].split("/")
        no_unique_type=url[0].upper()
        #~ print 'no_unique_type (eurlex):', no_unique_type
        no_unique_annee=url[1]
        #~ print 'no_unique_annee (eurlex):', no_unique_annee
        no_unique_chrono=url[2]
    except:
        try:
            #ALL TAB
            #<a href="./../../../procedure/EN/193517">COD(2005)0223</a>
            ids_oeil=soup.find(text="Procedure number:").find_next('a').get_text().strip()
            #~ print "ids_oeil (eurlex):", ids_oeil
            ids_oeil=ids_oeil.split("(")
            no_unique_type=ids_oeil[0].strip().upper()
            #~ print 'no_unique_type (eurlex):', no_unique_type
            ids_oeil=ids_oeil[1].split(")")
            no_unique_annee=ids_oeil[0]
            #~ print 'no_unique_annee (eurlex):', no_unique_annee
            no_unique_chrono=ids_oeil[1].strip()
        except:
            print "no oeil page (eurlex)"
            no_unique_type, no_unique_annee, no_unique_chrono=None, None, None
            exist=False

    if exist:
        no_unique_chrono=get_chrono(no_unique_chrono)

    return no_unique_type, no_unique_annee, no_unique_chrono


def get_proposs(soup):
    """
    FUNCTION
    get prelex ids from eurlex (prelex was the website of the European commission and was discontinued in late 2014)
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    propos_origine, propos_annee and propos_chrono variables [string, int, string]
    """
    try:
        #<strong>Procedure </strong><p><span>COM (2005) 566: Proposal for a Regulation of the European Parliament...</span>
        ids_prelex=soup.find("span").get_text().split(":")[0].strip()
        ids_prelex=ids_prelex.split("(")
        propos_origine=ids_prelex[0].strip().upper()
        if propos_origine=="COMMITTEE":
            propos_origine="COM"
        ids_prelex=ids_prelex[1].split(")")
        propos_annee=ids_prelex[0]
        propos_chrono=get_chrono(ids_prelex[1].strip())
    except Exception, e:
        print "no Internal reference", e
        propos_origine, propos_annee, propos_chrono=None, None, None

    return propos_origine, propos_annee, propos_chrono


def get_ids_eurlex(soup):
    """
    FUNCTION
    get all the ids from the eurlex url
    PARAMETERS
    soup: eurlex url content [BeautifulSoup object]
    RETURN
    fields: retrieved data from eurlex [ditionary]
    """
    fields={}

    #act
    fields['no_celex']=get_no_celex(soup)
    print "no_celex:", fields['no_celex']

    #<div class="tabContent tabContentForDocument">
    soup=soup.find("div", {"class": "tabContentForDocument"})

    #oeil ids
    fields['no_unique_type'], fields['no_unique_annee'], fields['no_unique_chrono']=get_nos_unique(soup)
    print 'no_unique_type:', fields['no_unique_type']
    print 'no_unique_annee:', fields['no_unique_annee']
    print 'no_unique_chrono:', fields['no_unique_chrono']

    #prelex ids
    fields['propos_origine'], fields['propos_annee'], fields['propos_chrono']=get_proposs(soup)
    print 'propos_origine:', fields['propos_origine']
    print 'propos_annee:', fields['propos_annee']
    print 'propos_chrono:', fields['propos_chrono']

    return fields
