#-*- coding: utf-8 -*-
#for accents between comments inside this file
"""
get data from Oeil (data for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
import urllib
from common.functions import date_string_to_iso
#save rapp
from common.db import save_get_field_and_fk
from act.models import Country, Person, Party
#logging
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_nb_lectures(soup, suite_2e_lecture_pe):
    """
    FUNCTION
    get the nb_lectures variable from the oeil url
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    suite_2e_lecture_pe: suite_2e_lecture_pe variable [boolean]
    RETURN
    nb_lectures [int]
    """
    try:
        #search in the key event table only
        key_events_soup=soup.find("a", {"class": "expand_button"}, text="Key events").find_next("table")

        #3d lecture
        if key_events_soup.find(text=re.compile('Decision by Council, 3rd rdg'))>0 or key_events_soup.find(text=re.compile('Decision by Council, 3rd reading'))>0:
            return 3

        #2d lecture
        #if suite_2e_lecture_pe=Yes
        if suite_2e_lecture_pe==True:
            pattern="Decision by Parliament, 2nd reading"
        #if suite_2e_lecture_pe=No
        else:
            pattern="Act approved by Council, 2nd reading"
        if key_events_soup.find(text=re.compile(pattern))>0:
            return 2

        #1st lecture
        if key_events_soup.find(text=re.compile("Act adopted by Council after Parliament's 1st reading"))>0 or key_events_soup.find(text=re.compile("Committee referral announced in Parliament, 1st reading/single reading"))>0:
            return 1

        return None
    except:
        print  "no nb_lectures!"
        return None

#possible values: 1, 2, 3 or NULL
#3: "Decision by Council, 3rd rdg ou reading"
#2: - Suite2LecturePE=Y, "Decision by Parliament 2nd reading".
#   - Suite2LecturePE=N, "Act approved by Council, 2nd reading"
#1: "Act adopted by Council after Parliament's 1st reading"


def get_commission(soup, no_unique_type, nb_lectures):
    """
    FUNCTION
    get the commission variable from the oeil url
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    no_unique_type: no_unique_type variable [string]
    nb_lectures: nb_lectures variable [int]
    RETURN
    commission
    searched_text: None, "Committee responsible" or "Former committee responsible" [string]
    """
    searched_text=commission=None
    try:
        if no_unique_type=="COD" and nb_lectures==3:
            commission=soup.find(text="Former committee responsible").find_next("acronym")
            searched_text="Former committee responsible"
            print searched_text
        else:
            commission=soup.find(text="Committee responsible").find_next("acronym")
            searched_text="Committee responsible"
    except Exception, e:
        print "no commission!", e

    if commission!=None:
        if commission.get_text()=="DELE":
            commission=commission.find_next("acronym").get_text()
        else:
            commission=commission.get_text()

    return commission, searched_text

#Acronym under "Committee responsible" or "Former committee responsible"
#can be NULL


#~ http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2005/0017(COD)
def get_vote_page(soup):
    """
    FUNCTION
    get the html page about votes from the oeil url
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    html page about votes [BeautifulSoup object]
    """
    try:
        link_votes=soup.find(text="Results of vote in Parliament").find_next("td").find("a")["href"]
        return BeautifulSoup(urllib.urlopen("http://www.europarl.europa.eu/"+link_votes))
    except:
        print "no vote page!"
        return None


def get_com_amdt_tabled(soup):
    """
    FUNCTION
    get the com_amdt_tabled variable from the vote page
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    com_amdt_tabled [int]
    """
    try:
        return soup.find(text="EP Committee").find_next('td').get_text()
    except:
        print "no com_amdt_tabled!"
        return None

#on vote page:
#Last table "Amendments adopted in plenary": EP Committee (row) and Tabled by (column)


def get_com_amdt_adopt(soup):
    """
    FUNCTION
    get the com_amdt_adopt variable from the vote page
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    com_amdt_adopt [int]
    """
    try:
        return soup.find(text="EP Committee").find_next('td').find_next('td').get_text()
    except:
        print "no com_amdt_adopt!"
        return None

#on vote page:
#Last table "Amendments adopted in plenary": EP Committee (row) and Adopted (column)


def get_amdt_tabled(soup):
    """
    FUNCTION
    get the amdt_tabled variable from the vote page
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    amdt_tabled [int]
    """
    try:
        return soup.find(text="Total").find_next('th').get_text()
    except:
        print "no amdt_tabled!"
        return None


def get_amdt_adopt(soup):
    """
    FUNCTION
    get the amdt_adopt variable from the vote page
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    amdt_adopt [int]
    """
    try:
        return soup.find(text="Total").find_next('th').find_next('th').get_text()
    except:
        print "no amdt_adopt!"
        return None


def get_vote_tables(soup):
    """
    FUNCTION
    get the two tables Final vote and final vote part two from the vote page
    PARAMETERS
    soup: vote page url content [BeautifulSoup object]
    RETURN
    vote_tables: the first and second table (empty if does not exist)  [list of BeautifulSoup objects]
    """
    #<td class="rowtitle">Final vote&nbsp;20/10/2010</td>
    #<td class="rowtitle">Final vote Part two</td>
    vote_tables=[None]*2
    try:
        vote_tables_temp=soup.find_all("td", {"class": "rowtitle"})
        vote_tables[0]=vote_tables_temp[0].find_next("table").find("table")
        vote_tables[1]=vote_tables_temp[1].find_next("table").find("table")
        return vote_tables
    except:
        return vote_tables


def get_vote(vote_table, vote):
    """
    FUNCTION
    get the vote variable For, Against or Abstentions from one of the two vote tables
    PARAMETERS
    vote_table: html content of the first or second vote table [BeautifulSoup object]
    vote="For", "Against" or "Abstentions" [string]
    RETURN
    votes_for_1, votes_agst_1, votes_abs_1, votes_for_2, votes_agst_2 or votes_abs_2 variable [int]
    """
    if vote_table!=None:
        return vote_table.find("p", text=vote).find_next("p").get_text()
    else:
        print "no vote variable!"
        return None


def get_rapps_html(soup, searched_text):
    """
    FUNCTION
    get the html content about rapporteurs from the oeil url
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    searched_text: "Committee responsible" or "Former committee responsible" [string]
    RETURN
    rapps: rapporteurs data [BeautifulSoup object]
    """
    rapps=[None]*5
    if searched_text!=None:
        try:
            #exclude shadow rapporteurs (parent: <div class="result_moredata shadow">)
            rapps_temp=[rapp for rapp in soup.find(text=searched_text).find_next("td", {"class": "players_rapporter_com "}).find_all("p", {"class": "players_content"}) if rapp.parent.name!="div"]
            for index in range(len(rapps_temp)):
                rapps[index]=rapps_temp[index]
        except Exception, e:
            print "pb rapps html", e
            pass

    return rapps



def get_rapps(rapps_html):
    """
    FUNCTION
    get rapporteurs data from the html content about rapporteurs
    PARAMETERS
    rapps_html: rapporteurs data (html format) [BeautifulSoup object]
    RETURN
    data: rapporteurs data object [dictionary of Person model objects]
    """
    data={}
    #for each rapporteur, get name, party and country
    for index in xrange(len(rapps_html)):
        num=str(index+1)
        #django adds "_id" to foreign keys field names
        data['rapp_'+num+"_id"]=None
        if rapps_html[index]!=None:
            field=[Person, "name", get_rapp(rapps_html[index])]
            fks=[]
            
            try:
                fks.append([Country, "country", get_country_instance(get_country(rapps_html[index])).pk])
            except Exception, e:
                print "exception get_rapps", e
                
            fks.append([Party, "party", get_party(rapps_html[index])])
            src="rapp"
            data['rapp_'+num+"_id"]=save_get_field_and_fk(field, fks, src)[0]

    return data


#external table
def get_country_instance(country):
    """
    FUNCTION
    get the instance of the country in parameter
    PARAMETERS
    country: name of the country [string]
    RETURN
    instance:instance of the country [Country instance]
    """
    instance=None
    try:
        #get the instance of the country
        instance=Country.objects.get(country=country)
    except:
        print "the country does not exist!"

    return instance


#external table
def get_country(rapp_data):
    """
    FUNCTION
    get the country from the rapporteur data in parameter
    PARAMETERS
    rapp_data: rapporteur data [BeautifulSoup object]
    RETURN
    country variable [string]
    """
    try:
        link=rapp_data.find("span", {"class": "players_rapporter_text"}).find("a")['href']
        link_deputy_soup=BeautifulSoup(urllib.urlopen(link))
        #return acronym of the country
        return(link_deputy_soup.find("li", {"class": "nationality"}).contents[0].strip())
    except:
        print "no country!"
        return None

#on the deputy's persononal page: country (next to the flag, next to the picture)
#can be NULL
#27 possible values (EU countries)


#external table
def get_party(rapp_data):
    """
    FUNCTION
    get the party from the rapporteur data in parameter
    PARAMETERS
    rapp_data: rapporteur data [BeautifulSoup object]
    RETURN
    party variable [string]
    """
    try:
        return rapp_data.find("span", {"class": "tiptip"})["title"]
    except:
        print "no party!"
        return None

#below "Rapporteur", before the name of the Rapporteur
#can be NULL


#external table
def get_rapp(rapp_data):
    """
    FUNCTION
    get the name from the rapporteur data in parameter
    PARAMETERS
    rapp_data: rapporteur data [BeautifulSoup object]
    RETURN
    rapp variable [string]
    """
    try:
        return rapp_data.find("span", {"class": "players_rapporter_text"}).get_text()
    except:
        print "no rapp!"
        return None

#below "Rapporteur", name of the Rapporteur
#can be NULL


def get_modif_propos(soup):
    """
    FUNCTION
    get the modif_propos variable from the oeil url
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    modif_propos variable [boolean]
    """
    try:
        modif_proposs=["Modified legislative proposal published", "Amended legislative proposal for reconsultation published", "Legislative proposal published"]
        for modifPropos in modif_proposs:
            if soup.find(text=re.compile(modifPropos))!=None:
                if modifPropos=="Legislative proposal published":
                    if soup.find(text=re.compile("Initial legislative proposal published"))==None:
                        return None
                return True
        return False
    except:
        print "no modif_propos!"
        return None

#In key events:
    #- if "Modified legislative proposal published" or "Amended legislative proposal for reconsultation published" -> Modif Propos=Y.
    #http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2002/0203%28CNS%29&l=en
    #http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2000/0062B%28CNS%29&l=en
    #- if "Legislative proposal published"
            #- if "Initial legislative proposal published" -> Modif Propos=Y.
            #http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2003/0059%28COD%29&l=en
            #- otherwise -> Modif Propos=NULL.
    #- otherwise -> Modif Propos=N (http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2005/0223(COD))


def get_sign_pecs(soup, no_unique_type):
    """
    FUNCTION
    get the sign_pecs variable from the oeil url
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    sign_pecs [date]
    """
    if no_unique_type=="COD" or no_unique_type=="ACI":
        try:
            sign_pecs=soup.find("td", text="Final act signed").find_previous("td").get_text()
            return date_string_to_iso(sign_pecs)
        except:
            return None

    return None

#date in front of "Final act signed"
#can be NULL
#only if NoUniqueType=COD or ACI


def get_dg_names(soup):
    """
    FUNCTION
    get the dg names from the oeil url
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    dg_names: list of dg names [list of strings]
    """
    dgs=[None]*2
    try:
        #view-source:http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2005/0223(COD) (2 dgs)
        #<td class="players_committee">
        soup=soup.find("td", {"class": "players_committee"})
        # <p class="players_content">
        dg_names=soup.find_all("p", {"class": "players_content"})
        #<p class="players_content"><a href="http://epp.eurostat.ec.europa.eu/portal/page/portal/eurostat/home" title="Eurostat" target="_blank">Eurostat</a></p>
        #<p class="players_content">Energy and Transport</p>
        for index, dg_name in enumerate(dg_names):
            try:
                #with link
                dgs[index]=dg_name.find("a").get_text().strip()
            except Exception, e:
                print "exception get_dg_names 1", e
                #without link
                dgs[index]=dg_name.get_text().strip()
    except Exception, e:
        print "exception get_dg_names 2", e

    return dgs


def get_resp_names(soup):
    """
    FUNCTION
    get the resp names from the oeil url
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    RETURN
    resp_names: list of resp names [list of strings]
    """
    resp_names=[None]*3
    try:
        #http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2007/0128(COD)
        #<td class="players_rapporter_com">
        soup=soup.find("td", {"class": "players_rapporter_com"})
        # <p class="players_content">
        resp_names=soup.find_all("p", {"class": "players_content"})
        #<p class="players_content">KYPRIANOU  Markos</p>
        resp_names=[resp_name.get_text().strip() for resp_name in resp_names]
        while len(resp_names)<3:
            resp_names.append(None)
    except Exception, e:
        print "exception get_resp_names", e

    return resp_names



def get_data_oeil(soup, act_ids, act=None):
    """
    FUNCTION
    get all data from the oeil url
    PARAMETERS
    soup: oeil url content [BeautifulSoup object]
    act_ids: act ids instance [ActIds model instance]
    RETURN
    fields: retrieved data from oeil [dictionary]
    dg_names: list of dg names [list of strings]
    resp_names: list of resp names [list of strings]
    """
    fields={}
    act=act_ids.act
    
    #<table style="margin:0;" width="100%" id="key_players">
    soup_key_players=soup.find("table", {"id": "key_players"})
    #<div id="keyEvents" class="ep_borderbox">
    soup_key_events=soup.find("div", {"id": "keyEvents"})

    #nb_lectures
    fields['nb_lectures']=get_nb_lectures(soup_key_events, act.suite_2e_lecture_pe)
    print "nb_lectures:", fields['nb_lectures']
    logger.debug("nb_lectures: "+ str(fields['nb_lectures']))

    #commission
    fields['commission'], searched_text=get_commission(soup_key_players, act_ids.no_unique_type, fields['nb_lectures'])
    print "commission:", fields['commission']
    logger.debug("commission: "+ str(fields['commission']))

    #html content of the votes page
    vote_page_soup=get_vote_page(soup_key_events)
    #~ print votesSectionSoup

    #com_amdt_tabled
    fields['com_amdt_tabled']=get_com_amdt_tabled(vote_page_soup)
    print "com_amdt_tabled:", fields['com_amdt_tabled']
    logger.debug("com_amdt_tabled: "+ str(fields['com_amdt_tabled']))

    #com_amdt_adopt
    fields['com_amdt_adopt']=get_com_amdt_adopt(vote_page_soup)
    print "com_amdt_adopt:", fields['com_amdt_adopt']
    logger.debug("com_amdt_adopt: "+ str(fields['com_amdt_adopt']))

    #amdt_tabled
    fields['amdt_tabled']=get_amdt_tabled(vote_page_soup)
    print "amdt_tabled:", fields['amdt_tabled']
    logger.debug("amdt_tabled: "+ str(fields['amdt_tabled']))

    #amdt_adopt
    fields['amdt_adopt']=get_amdt_adopt(vote_page_soup)
    print "amdt_adopt:", fields['amdt_adopt']
    logger.debug("amdt_adopt: "+ str(fields['amdt_adopt']))

    #html content of the 2 tables of vote (Final vote and Final vote part two):
    vote_tables=get_vote_tables(vote_page_soup)
    vote_table_1=vote_tables[0]
    vote_table_2=vote_tables[1]

    #votes_for_1
    fields['votes_for_1']=get_vote(vote_table_1, "For")
    print "votes_for_1:", fields['votes_for_1']
    logger.debug("votes_for_1: "+ str(fields['votes_for_1']))

    #votes_agst_1
    fields['votes_agst_1']=get_vote(vote_table_1, "Against")
    print "votes_agst_1:", fields['votes_agst_1']
    logger.debug("votes_agst_1: "+ str(fields['votes_agst_1']))

    #votes_abs_1
    fields['votes_abs_1']=get_vote(vote_table_1, "Abstentions")
    print "votes_abs_1:", fields['votes_abs_1']
    logger.debug("votes_abs_1: "+ str(fields['votes_abs_1']))

    #votes_for_2
    fields['votes_for_2']=get_vote(vote_table_2, "For")
    print "votes_for_2:", fields['votes_for_2']
    logger.debug("votes_for_2: "+ str(fields['votes_for_2']))

    #votes_agst_2
    fields['votes_agst_2']=get_vote(vote_table_2, "Against")
    print "votes_agst_2:", fields['votes_agst_2']
    logger.debug("votes_agst_2: "+ str(fields['votes_agst_2']))

    #votes_abs_2
    fields['votes_abs_2']=get_vote(vote_table_2, "Abstentions")
    print "votes_abs_2:", fields['votes_abs_2']
    logger.debug("votes_abs_2: "+ str(fields['votes_abs_2']))

    #rapporteurs
    rapps_html=get_rapps_html(soup_key_players, searched_text)
    rapps=get_rapps(rapps_html)
    #rapp variables (name, country, party)
    for rapp in rapps:
        if rapps[rapp]!=None:
            fields[rapp]=rapps[rapp]
            num=rapp[-4]
            print rapp+": ", rapps[rapp].name
            print 'country_'+num+": ", rapps[rapp].country.country_code
            print 'party_'+num+": ", rapps[rapp].party.party
            logger.debug("rapp: "+ rapps[rapp].name+", "+rapps[rapp].country.country_code+", "+rapps[rapp].party.party)

    #modif_propos
    fields['modif_propos']=get_modif_propos(soup_key_events)
    print "modif_propos:", fields['modif_propos']
    logger.debug("modif_propos: "+ fields['modif_propos'])

    #sign_pecs
    fields['sign_pecs']=get_sign_pecs(soup_key_events, act_ids.no_unique_type)
    print "sign_pecs:", fields['sign_pecs']
    logger.debug("sign_pecs: "+ sign_pecs)


    try:
        soup_dg_resp=soup_key_players.find("a", {"title": "European Commission"}).find_next("table")
    except Exception, e:
        print "exception soup_dg_resp", e
        soup_dg_resp=None

    #get dg names
    dg_names=get_dg_names(soup_dg_resp)
    print "dg_names:", dg_names
    logger.debug("dg_names: "+ dg_names)

    #get resp names
    resp_names=get_resp_names(soup_dg_resp)
    print "resp_names:", resp_names
    logger.debug("resp_names: "+ resp_names)

    print "NB LECTURES OEIL", fields["nb_lectures"]
    logger.debug("nb_lectures: "+ str(fields["nb_lectures"]))

    return fields, dg_names, resp_names
