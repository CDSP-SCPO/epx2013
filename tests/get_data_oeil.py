#-*- coding: utf-8 -*-
#for accents between comments inside this file
"""
get data from Oeil (data for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
import urllib



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
        if key_events_soup.find(text=re.compile("Act adopted by Council after Parliament's 1st reading"))>0:
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



def get_data_oeil(soup, idsDataDic):
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

    #<table style="margin:0;" width="100%" id="key_players">
    soup_key_players=soup.find("table", {"id": "key_players"})
    #<div id="keyEvents" class="ep_borderbox">
    soup_key_events=soup.find("div", {"id": "keyEvents"})

    #nb_lectures
    fields['nb_lectures']=get_nb_lectures(soup_key_events, idsDataDic["suite_2e_lecture_pe"])
    print "nb_lectures:", fields['nb_lectures']

    #commission
    fields['commission'], searched_text=get_commission(soup_key_players, "COD", fields['nb_lectures'])
    print "commission:", fields['commission']


    return fields
