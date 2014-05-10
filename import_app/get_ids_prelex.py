"""
get the ids from Prelex
"""
import urllib
import re
from bs4 import BeautifulSoup
import config_file as conf
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_url_prelex_propos(propos_origine, propos_annee, propos_chrono):
    """
    FUNCTION
    return the prelex url (with propos ids)
    PARAMETERS
    propos_origine: propos_origine variable [string]
    propos_annee: propos_annee variable [int]
    propos_chrono: propos_chrono variable [string]
    RETURN
    url: prelex url [string]
    """
    #http://prelex.europa.eu/liste_resultats.cfm?ReqId=0&CL=en&DocType=COM&DocYear=2005&DocNum=566
    #~ url="http://prelex.europa.eu/liste_resultats.cfm?ReqId=0&CL=en&DocType=PROPOSORIGINE&DocYear=PROPOSANNEE&DocNum=PROPOSCHRONO"
    url=conf.url_prelex_propos
    url=url.replace("PROPOSORIGINE", propos_origine, 1)
    url=url.replace("PROPOSANNEE", str(propos_annee), 1)
    url=url.replace("PROPOSCHRONO", propos_chrono, 1)
    return url


def get_url_prelex_no_unique(no_unique_type, no_unique_annee, no_unique_chrono):
    """
    FUNCTION
    return the prelex url (with oeil ids) (USEFUL if propos_chrono contains a dash)
    PARAMETERS
    propos_origine: propos_origine variable [string]
    propos_annee: propos_annee variable [int]
    propos_chrono: propos_chrono variable [string]
    RETURN
    url: prelex url [string]
    """
    #no_unique_chrono coded on 4 digits if numbers only and 5 if final character is a letter
    #propos_chrono coded on 4 digits
    if no_unique_chrono[-1].isdigit():
        no_unique_chrono_len=4
    else:
        no_unique_chrono_len=5

    while len(no_unique_chrono)!=no_unique_chrono_len:
        no_unique_chrono="0"+str(no_unique_chrono)

    #http://ec.europa.eu/prelex/liste_resultats.cfm?CL=en&ReqId=0&DocType=COD&DocYear=2005&DocNum=0223
    #~ url="http://ec.europa.eu/prelex/liste_resultats.cfm?CL=en&ReqId=0&DocType=NOUNIQUETYPE&DocYear=NOUNIQUEANNEE&DocNum=0NOUNIQUECHRONO"
    url=conf.url_prelex_no_unique
    url=url.replace("NOUNIQUETYPE", no_unique_type, 1)
    url=url.replace("NOUNIQUEANNEE", str(no_unique_annee), 1)
    url=url.replace("NOUNIQUECHRONO", no_unique_chrono, 1)
    return url

def get_url_prelex(dos_id):
    """
    FUNCTION
    return the prelex url (with dos_id) (USEFUL if propos_chrono contains a dash and there is no no_unique)
    PARAMETERS
    dos_id: dos_id variable [int]
    RETURN
    url: prelex url [string]
    """
    #http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=193517
    #~ url="http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=DOSSIERID"
    url=conf.url_prelex
    url=url.replace("DOSSIERID", str(dos_id), 1)
    return url


def get_url_content_prelex(url):
    """
    FUNCTION
    check if the prelex url exists and return its content
    PARAMETERS
    url: prelex url [string]
    RETURN
    content of the page if the url exists and false otherwise [BeautifulSoup object]
    """
    url_content=False
    try:
        #~ logger.debug("soup prelex to be processed")
        #~ soup=BeautifulSoup(urllib.urlopen(url))
        logger.debug("soup prelex to be processed with html5 library")
        soup=BeautifulSoup(urllib.urlopen(url), 'html5')
        if not (soup.find(text='This page does not exists') or soup.find(text=re.compile('The document is not available in PreLex'))):
            url_content=soup
    except:
        print "no url content for prelex"

    return url_content


def get_no_celex(soup, no_celex):
    """
    FUNCTION
    get no_celex from prelex
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    RETURN
    no_celex_p: no_celex if found on prelex, None otherwise [string]
    """
    no_celex_p=None
    try:
        urls_eurlex=[text.get('href') for text in soup.find_all('a', {"href": re.compile("^(.)*uri=CELEX:[0-9](195[789]|19[6-9][0-9]|20[0-1][0-9])([dflryDFLRY]|PC)[0-9]{4}(\(0[1-9]\)|R\(0[1-9]\))?")})]
        for url_eurlex in urls_eurlex:
            #no_celex found!
            if url_eurlex.split(":")[2]==no_celex:
                no_celex_p=no_celex
                break
    except:
        print "no eurlex page (prelex)"

    return no_celex_p


def get_nos_unique(soup):
    """
    FUNCTION
    get oeil ids from prelex
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    RETURN
    no_unique_type, no_unique_annee and no_unique_chrono variables [string, int, string]
    """
    try:
        ids_oeil=soup.get_text()
        #~ print "oeil ids (prelex):", oldOeilUrl
        ids_oeil=ids_oeil.split("/")
        no_unique_type=ids_oeil[2].upper()
        no_unique_annee=ids_oeil[0]
        no_unique_chrono_temp=ids_oeil[1]
        #we remove the 0s at the beginning
        index_start=0
        for character in no_unique_chrono_temp:
            if character=="0":
                index_start+=1
            else:
                break
        no_unique_chrono=no_unique_chrono_temp[index_start:]

    except:
        no_unique_type=None
        no_unique_annee=None
        no_unique_chrono=None
        print "no oeil page (prelex)"

    return no_unique_type, no_unique_annee, no_unique_chrono


def get_dos_id(soup):
    """
    FUNCTION
    get prelex dos_id from prelex
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    RETURN
    dos_id [int]
    """
    try:
        dos_id=soup.find('a', {"href": re.compile("DosId=")})['href']
        return dos_id[(str(dos_id).rfind('=')+1):]
    except:
        print "problem on page (prelex)"
        return None


def get_proposs(soup):
    """
    FUNCTION
    get prelex ids from prelex
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    RETURN
    propos_origine, propos_annee and propos_chrono variables [string, int, string]
    """
    try:
        ids_prelex=soup.get_text()
        #~ print "prelex ids (prelex):", prelexId
        ids_prelex="".join(ids_prelex.split())
        ids_prelex=ids_prelex.split("(")
        propos_origine=ids_prelex[0]
        ids_prelex=ids_prelex[1].split(")")
        propos_annee=ids_prelex[0]
        propos_chrono_temp=ids_prelex[1]
        #we remove the 0s at the beginning
        index_start=0
        for character in propos_chrono_temp:
            if character=="0":
                index_start+=1
            else:
                break
        propos_chrono=propos_chrono_temp[index_start:]
        return propos_origine, propos_annee, propos_chrono

    except:
        return None, None, None


def get_ids_prelex(soup, no_celex):
    """
    FUNCTION
    get all the ids from the prelex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    no_celex: no_celex variable [string]
    RETURN
    fields: retrieved data from prelex [dictionary]
    """
    fields={}

    #eurlex id
    fields['no_celex']=get_no_celex(soup, no_celex)
    print "fields['no_celex']:", fields['no_celex']

    ids_oeil_prelex=soup.find_all('font', {'size': "-1"})

    #if there is no error on the page
    if ids_oeil_prelex!=[]:
        #oeil ids
        fields['no_unique_type'], fields['no_unique_annee'], fields['no_unique_chrono']=get_nos_unique(ids_oeil_prelex[1])
        print "no_unique_type:", fields['no_unique_type']
        print "no_unique_annee:", fields['no_unique_annee']
        print "no_unique_chrono:", fields['no_unique_chrono']

        #prelex dos_id
        fields['dos_id']=get_dos_id(soup)
        print "dos_id:", fields['dos_id']

        #prelex ids
        fields['propos_origine'], fields['propos_annee'], fields['propos_chrono']=get_proposs(ids_oeil_prelex[0])
        print "propos_origine:", fields['propos_origine']
        print "propos_annee:", fields['propos_annee']
        print "propos_chrono:", fields['propos_chrono']
    else:
        #if problems on page (just beginning with titles but nothing about the act)
        print "problem on page (prelex)"
        fields['url_exists']=False

    return fields
