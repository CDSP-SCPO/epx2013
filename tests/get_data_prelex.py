#-*- coding: utf-8 -*-
#for accents between comments inside this file
"""
get data from Prelex (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup

def get_adopt_com_table(soup):
    """
    FUNCTION
    get the html content of the table tag "Adoption by Commission" from the prelex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    RETURN
    html content of the table "Adoption by Commission" [BeautifulSoup object]
    """
    try:
        return soup.find("b", text=re.compile("Adoption by Commission")).find_parent('table')
    except:
        print "no table called 'Adoption by Commission' (prelex)"
        return None


def get_jointly_resps(soup):
    """
    FUNCTION
    get the names of the jointly responsible persons (dg_2 and resp_2 or resp_3 from the prelex url
    PARAMETERS
    soup: prelex url content [BeautifulSoup object]
    RETURN
    names of jointly responsible persons (dg_2 and resp_2 or resp_3 ) [list of strings]
    """
    dg_2=resp_2=None
    try:
        #~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=191926
        jointly_resps=soup.find_all("td", text="Jointly responsible")

        temp=jointly_resps[0].find_next('td').get_text().strip()
        #no dg_2 for some acts
         #http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=199093
        if len(jointly_resps)==1:
            resp_2=temp
        else:
            #dg_2
            dg_2=temp
            #resp_2 or 3
            resp_2=jointly_resps[1].find_next('td').get_text().strip()

    except Exception, e:
        print "no dg_2 or resp_2", e

    return dg_2, resp_2

#in front of "Jointly responsible"
#can be Null



def get_data_prelex(soup, act_ids):
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

    #jointly responsible persons (dg_2 and resp_2 or resp_3)
    dg_2, resp_2=get_jointly_resps(soup_adopt_com_table)
    print "dg_2", dg_2
    print "resp_2", resp_2


    #~ return fields
    return fields
