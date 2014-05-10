"""
get the ids from oeil
"""
import urllib2
import re
from bs4 import BeautifulSoup
import config_file as conf
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_url_oeil(no_unique_type, no_unique_annee, no_unique_chrono):
    """
    FUNCTION
    return the oeil url
    PARAMETERS
    no_unique_annee: no_unique_annee variable [int]
    no_unique_chrono: no_unique_chrono variable [string]
    no_unique_type: no_unique_type variable [string]
    RETURN
    url: url of the oeil page [string]
    """
    #no_unique_chrono coded on 4 digits if numbers only and 5 if final character is a letter
    #if empty
    if no_unique_chrono in [None, ""] :
        return None
    #if only digits
    if no_unique_chrono[-1].isdigit():
        no_unique_chrono_len=4
    else:
        no_unique_chrono_len=5

    while len(no_unique_chrono)!=no_unique_chrono_len:
        no_unique_chrono="0"+str(no_unique_chrono)

    #http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2005/0223(COD)
    #~ url="http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=NOUNIQUEANNEE/NOUNIQUECHRONO(NOUNIQUETYPE)"
    url=conf.url_oeil
    url=url.replace("NOUNIQUEANNEE", no_unique_annee, 1)
    url=url.replace("NOUNIQUECHRONO", no_unique_chrono, 1)
    url=url.replace("NOUNIQUETYPE", no_unique_type, 1)
    return url


def get_url_content_oeil(url):
    """
    FUNCTION
    check if the oeil url exists and return its content
    PARAMETERS
    url: oeil url [string]
    RETURN
    url_content: content of the page if the url exists and false otherwise [BeautifulSoup object]
    """
    url_content=False
    try:
        logger.debug(url)
        print "url", url
        logger.debug("html to be retrieved with urllib2 and a 10-second timeout")
        html=urllib2.urlopen(url, timeout=10).read()
        #~ print html
        print "html retrieved"
        logger.debug("first 300 html characters "+ html[:300])
        #~ logger.debug("soup oeil to be processed")
        #~ soup=BeautifulSoup(html)
        logger.debug("soup oeil to be processed with html5 library")
        soup=BeautifulSoup(html, 'html5')
        logger.debug("soup oeil retrieved :)")
        if not (soup.title.string=="Procedure File: ERROR"):
            logger.debug("soup oeil: no error :)")
            url_content=soup
    except Exception, e:
        logger.debug("no content for oeil url"+ str(e))
        print "no content for oeil url", e

    logger.debug("end get_url_content_oeil")
    return url_content


def get_no_celex(soup):
    """
    FUNCTION
    get act from oeil
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    no_celex [string]
    """
    try:
        #http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2005/0223(COD)
        act=soup.find("div", {"id": "final_act"}).find("a", {"class": "sumbutton"})["title"]
        return act.split(" ")[-1]
    except Exception, e:
        #~ print "get_no_celex exception", e
        try:
            #http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=1997/0309(SYN)
            act=soup.find("div", {"id": "final_act"}).find("a")["href"]
            index=act.rfind("=")
            return act[index+1:].strip()
        except Exception, e:
            #~ print "get_no_celex exception 2", e
            try:
                #http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=1997/0221(SYN)
                act=soup.find(text="Implementing legislative act").find_next("td").find("a").get_text()
                return act.strip()
            except Exception, e:
                #~ print "get_no_celex exception 3", e
                return None


def get_nos_unique(soup):
    """
    FUNCTION
    get oeil ids from oeil
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    no_unique_type, no_unique_annee and no_unique_chrono variables [string, int, string]
    """
    try:
        title=soup.title.string
        #~ print "title (oeil):", title
        #Procedure File: 2005/0223(COD)
        title=title.replace('Procedure File: ','').split("/")
        #~ print "new title (oeil):", title
        no_unique_annee=title[0]
        title=title[1].split("(")
        no_unique_chrono_temp=title[0]
        #we remove the 0s at the beginning
        index_start=0
        for character in no_unique_chrono_temp:
            if character=="0":
                index_start+=1
            else:
                break
        no_unique_chrono=no_unique_chrono_temp[index_start:]
        no_unique_type=title[1][:-1].upper()

        return no_unique_type, no_unique_annee, no_unique_chrono

    except:
        return None, None, None


def get_proposs(soup):
    """
    FUNCTION
    get prelex ids from oeil
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    propos_origine, propos_annee and propos_chrono variables [string, int, string]
    """
    #3 different kinds of acts -> 3 possibilities to retrieve prelex ids
    act_type=["Legislative proposal published", "Non-legislative basic document", "Supplementary legislative basic document", "Initial legislative proposal published"]
    for act in act_type:
        try:
            prelex=soup.find(text=act).find_parent().find_parent().find("td", {"class": "event_column_document"})
            #~ print "prelex (oeil):", prelex
            ids_prelex=prelex.get_text().strip()
            #~ print "ids_prelex (oeil):", ids_prelex

            if ids_prelex=="":
                ids_prelex=prelex.previous_sibling.strip()

            #~ print "prelexId (oeil):", ids_prelex
            ids_prelex=ids_prelex.split('(')
            propos_origine=ids_prelex[0].upper()
            ids_prelex=ids_prelex[1].split(')')
            propos_annee=ids_prelex[0]
            propos_chrono_temp=ids_prelex[1]
            #~ print "propos_chrono_temp (oeil):", propos_chrono_temp

            #remove trailing zeros
            index_start=0
            for character in propos_chrono_temp:
                if character=="0":
                    index_start+=1
                else:
                    break

            #if regex catches text after oeil ids, we delete it -> starts with '\r' or `'n'
            spaces=propos_chrono_temp.find('\r')
            index_end=spaces

            spaces=propos_chrono_temp.find('\n')
            if spaces!=-1 and (spaces<index_end or index_end==-1):
                index_end=spaces

            if index_end==-1:
                propos_chrono=propos_chrono_temp[index_start:]
            else:
                propos_chrono=propos_chrono_temp[index_start:index_end]
            break

        except:
            propos_origine=None
            propos_annee=None
            propos_chrono=None
            print "no prelex page (oeil)"

    return propos_origine, propos_annee, propos_chrono


def get_ids_oeil(soup):
    """
    FUNCTION
    get all the ids from the oeil url
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    fields: retrieved data from oeil [dictionary]
    """
    fields={}

    #eurlex id
    fields['no_celex']=get_no_celex(soup)
    print "no_celex:", fields['no_celex']

    #oeil ids
    fields['no_unique_type'], fields['no_unique_annee'], fields['no_unique_chrono']=get_nos_unique(soup)
    print "no_unique_type:", fields['no_unique_type']
    print "no_unique_annee:", fields['no_unique_annee']
    print "no_unique_chrono:", fields['no_unique_chrono']

    #prelex ids
    fields['propos_origine'], fields['propos_annee'], fields['propos_chrono']=get_proposs(soup)
    print "propos_origine:", fields['propos_origine']
    print "propos_annee:", fields['propos_annee']
    print "propos_chrono:", fields['propos_chrono']

    return fields
