#-*- coding: utf-8 -*-
#for accents between comments inside this file
"""
get data from Prelex (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup


def get_adopt_conseil(soup, suite_2e_lecture_pe, split_propos, nb_lectures):
    """
    FUNCTION
    get the adopt_conseil variable from the prelex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    suite_2e_lecture_pe: suite_2e_lecture_pe variable [boolean]
    split_propos: split_propos variable [boolean]
    nb_lectures: nb_lectures variable [int]
    RETURN
    adopt_conseil: adopt_conseil variable [date]
    """
    adopt_conseil=None
    # if there is no  2d Lecture at PE
    if suite_2e_lecture_pe==False:
        acts=["Formal adoption by Council", "Adoption common position", "Council approval 1st rdg"]
        for act in acts:
            try:
                adopt_conseil=soup.find("a", text=re.compile(act)).find_next('br').next.strip()
                break
            except:
                print "pb", act
    # if Suite2LecturePE=Y and split_propos=N
    elif split_propos==False:
        if nb_lectures==2:
            try:
                #~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=156619
                date_table_soup=soup.find("b", text="EP opinion 2nd rdg").find_parent("table")
                #check table contains "Approval without amendment"
                approval=date_table_soup.find(text="Approval without amendment")
                #check next table title is "Signature by EP and Council"
                next_table_title=date_table_soup.find_next("table").find(text="Signature by EP and Council")
                #if conditions are met, then get the date
                adopt_conseil=date_table_soup.find("b").get_text()
            except:
                print "pb AdoptionConseil (case split_propos==0)"
        elif nb_lectures==3:
            #~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=137644
            date_table_soup=soup.find("b", text="Council decision at 3rd rdg").find_parent("table")
            #check next table title is "Signature by EP and Council"
            next_table_title=date_table_soup.find_next("table").find(text="Signature by EP and Council")
            #if conditions are met, then get the date
            adopt_conseil=date_table_soup.find("b").get_text()
            #~ return soup.find("a", text=re.compile("Council decision at 3rd rdg")).find_next('br').next.strip()

    #transform dates to the iso format (YYYY-MM-DD)
    if adopt_conseil!=None:
        adopt_conseil=date_string_to_iso(adopt_conseil)
    return adopt_conseil

#~ date in front of "Formal adoption by Council" or "Adoption common position" or "Council approval 1st rdg"
#not Null
#~ AAAA-MM-JJ format

#~ quand Suite2LecturePE=Y ET quand ProposSplittee=N and nb_lectures=2. Dans ce cas, la date AdoptionConseil=la date qui se trouve en face de la ligne « EP Opinion 2nd rdg » (vérifier qu’à la ligne qui suit dans le même carré, on trouve « Approval without amendment » et que le titre du carré qui suit est bien « Signature by EP and Council »
#~ Exemple : http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=156619

#~ quand Suite2LecturePE=Y ET quand ProposSplittee=N and nb_lectures=3 -> date in front of Council decision at 3rd rdg (vérifier que le titre du carré qui suit est bien « Signature by EP and Council »)
#~ Example: http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=137644

# if Suite2LecturePE=Y and split_propos=Y -> to fill manually



def get_nb_lectures(soup, no_unique_type, split_propos):
    """
    FUNCTION
    get the nb_lectures variable from the prelex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    no_unique_type: no_unique_type variable [string]
    split_propos: split_propos variable [boolean]
    RETURN
    nb_lectures variable [int]
    """
    if no_unique_type!="COD":
        return None

    #proposition not splited
    if split_propos==False:
        if soup.find(text=re.compile('EP opinion 3rd rdg'))>0 or soup.find(text=re.compile('EP decision 3rd rdg'))>0 or soup.find(text=re.compile('EP decision on 3rd rdg'))>0:
            return 3
        if soup.find(text=re.compile('EP opinion 2nd rdg'))>0:
            return 2
        if soup.find(text=re.compile('EP opinion 1st rdg'))>0:
            return 1
        return 0

    #proposition is splited
    if soup.find(text=re.compile('EP: position, 3rd reading'))>0 or soup.find(text=re.compile('EP: decision, 3rd reading'))>0 or soup.find(text=re.compile('EP: legislative resolution, 3rd reading'))>0:
        return 3
    if soup.find(text=re.compile('EP: position, 2nd reading'))>0:
        return 2
    if soup.find(text=re.compile('EP: position, 1st reading'))>0:
        return 1
    return 0

#Possible values
#1, 2, 3 ou NULL
#~ NULL if NoUniqueType !=COD
#~ if NoUniqueType=COD and if the proposition is not splitted:
    #~ if page contains "EP opinion 3rd rdg" or "EP decision 3rd rdg" -> nombreLectures=3
    #~ if page contains "EP opinion 2nd rdg" -> nombreLectures=2
    #~ if page contains "EP opinion 1st rdg" -> nombreLectures=1
    #~ otherwise error
#~ if NoUniqueType=COD and if the proposition is splitted:
    #~ if page contains "EP: position, 3rd reading" or "EP: decision, 3rd reading" or "EP: legislative resolution, 3rd reading" -> nombreLectures=3
    #~ if page contains "EP: position, 2nd reading" -> nombreLectures=2
    #~ if page contains "EP: position, 1st reading" -> nombreLectures=1
    #~ otherwise error




def get_data_prelex(soup, act_ids, act):
    """
    FUNCTION
    get all the data from the prelex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    act_ids: act ids instance [model instance]
    act: instance of the data of the act [Act model instance]
    RETURN
    fields: retrieved data from prelex [dictionary]
    dgs_temp: list of dg names [list of strings]
    resp_names: list of resp names [list of strings]
    """
    fields={}

    #extract Adoption by Commission table (html content)
    soup_adopt_com_table=get_adopt_com_table(soup)

    #nb_lectures -> ALREADY IN OEIL -> used only for adopt_conseil!
    fields['nb_lectures']=get_nb_lectures(soup, act_ids.no_unique_type, act.split_propos)
    #~ print "nb_lectures:", fields['nb_lectures']

    #adopt_conseil
    fields['adopt_conseil']=get_adopt_conseil(soup, act.suite_2e_lecture_pe, act.split_propos, fields['nb_lectures'])
    print "adopt_conseil:", fields['adopt_conseil']


    #~ return fields
    return fields, dgs_temp, resp_names
