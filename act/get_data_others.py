#-*- coding: utf-8 -*-
#for accents between comments inside this file
"""
get government composition from the file Composition politique gvts nationaux 93-12.csv (NationGvtPoliticalComposition) and opal variables
"""
from act.models import GvtCompo, Country, NP, MinAttend, Verbatim, Status, PartyFamily
from import_app.models import ImportNP, ImportMinAttend
from bs4 import BeautifulSoup
import re


def get_date(act_ids, act):
    """
    FUNCTION
    get the date to be used to get the governments composition
    PARAMETERS
    act_ids: instance of the ids of the act [ActIds model instance]
    act: instance of an act [Act model instance]
    RETURN
    date: date for the gvts composition [Date]
    """
    date=None
    if act.adopt_conseil!=None:
        date=act.adopt_conseil
    elif act.sign_pecs!=None:
        date=act.sign_pecs
    elif act_ids.propos_origine in ["EM", "CONS", "BCE", "CJUE"]:
        date=act.date_doc
    print "date gvt_compo", date
    return date


def link_act_gvt_compo(act_ids, act):
    """
    FUNCTION
    fill the assocation table which links an act to its governments composition
    PARAMETERS
    act_ids: instance of the ids of the act [ActIds model instance]
    act: instance of an act [Act model instance]
    RETURN
    None
    """
    #take the right date field
    date=get_date(act_ids, act)

    if date==None:
        return None

    #retrieve all the rows from GvtCompo for which start_date<adoptionConseil<end_date
    gvt_compos=GvtCompo.objects.filter(start_date__lte=date, end_date__gte=date)
    #fill the association
    for gvt_compo in gvt_compos:
        try:
            act.gvt_compo.add(gvt_compo)
        except Exception, e:
            print "gvt compo already exists!", e
    else:
        print "gvt compo: no matching date"



def get_gvt_compo(act_ids, act):
    """
    FUNCTION
    get all the governments composition of the given act
    PARAMETERS
    act_ids: instance of the ids of the act [ActIds model instance]
    act: instance of an act [Act model instance]
    RETURN
    gvt_compo_dic: governements composition [Dictionary]
    """
    gvt_compo_dic={}
    #take the right date field
    date=get_date(act_ids, act)

    if date!=None:
        #get all the rows from GvtCompo for which start_date<adoptionConseil<end_date
        gvt_compos=GvtCompo.objects.filter(start_date__lte=date, end_date__gte=date)

        #put the countries, parties and party families in a dictionary
        for gvt_compo in gvt_compos:
            country=gvt_compo.country
            country_code=country.country_code
            #initialization
            if country_code not in gvt_compo_dic:
                gvt_compo_dic[country_code]=""

            for party in gvt_compo.party.all():
                party_family=PartyFamily.objects.get(country=country, party=party).party_family
                gvt_compo_dic[country_code]+=party.party+" ("+party_family+"); "

        #remove last "; "
        for country in gvt_compo_dic:
            gvt_compo_dic[country]=gvt_compo_dic[country][:-2]
            
        else:
            print "gvt compo: no matching date"

    return gvt_compo_dic



def link_act_min_attend(act_ids):
    """
    FUNCTION
    fill the assocation table which links an act and a country to its minister's attendance
    PARAMETERS
    act_ids: instance of the ids of the act [ActIds model instance]
    RETURN
    min_attend_dic: min_attend variables [dictionary]
    """
    min_attend_dic={}
    #if the attendances of the act have been validated already
    if act_ids.act.validated_attendance:
        #retrieve all the rows of the act from the ImportMinAttend table
        min_attends=ImportMinAttend.objects.filter(no_celex=act_ids.no_celex)
        attendance=False
        #for each country and each verbatim fill the association
        for min_attend in min_attends:
            #get or create the verbatim with its status if it does not exist in the Vernatim model
            verbatim, created = Verbatim.objects.get_or_create(verbatim=min_attend.verbatim)
            #fill status table
            status, created = Status.objects.get_or_create(verbatim=verbatim, country=Country.objects.get(country_code=min_attend.country), status=min_attend.status)

            #store data in a dictionary
            country=min_attend.country
            #initialization
            if country not in min_attend_dic:
                min_attend_dic[country]=""
            min_attend_dic[country]+=min_attend.status+"; "

            try:
                MinAttend.objects.create(act=act_ids.act, country=Country.objects.get(pk=min_attend.country), verbatim=verbatim)
            except Exception, e:
                print "min_attend already exists!", e

            #check if there is at least one status different from AB and NA -> check if there are attendances for the act
            if min_attend.status not in ["AB", "NA"]:
                attendance=True
    
        #if no status different from AB or NA found, consider there is no attendance for this act and empty the dictionary
        if not attendance:
            min_attend_dic={}

        #remove last "; "
        for country in min_attend_dic:
            min_attend_dic[country]=min_attend_dic[country][:-2]

    return min_attend_dic



def link_get_act_opal(act_ids, act):
    """
    FUNCTION
    fill the table which links an act to its opal variables
    PARAMETERS
    act_ids: instance of the ids of the act [ActIds model instance]
    act: instance of the act [Act model instance]
    RETURN
    opal_dic: opal variables [dictionary]
    """
    opal_dic={}

    #Are there matches in the ImportOpal table?
    opals=ImportNP.objects.defer("no_celex").filter(no_celex=act_ids.no_celex)

    for opal in opals:
        #store data in a dictionary
        country=opal.np
        #initialization
        if country not in opal_dic:
            opal_dic[country]={"act_type": "", "act_date": "", "case_nb": ""}
        opal_dic[country]["act_type"]+=opal.act_type+"; "
        opal_dic[country]["act_date"]+=str(opal.act_date)+"; "
        opal_dic[country]["case_nb"]+=str(opal.case_nb)+"; "

        try:
            #save opal instances
            fields={"case_nb": opal.case_nb, "np": Country.objects.get(pk=opal.np), "act_type": opal.act_type, "act_date": opal.act_date , "act": act}
            NP.objects.create(**fields)
        except Exception, e:
            print "opal variables already saved!", e

    #remove last "; "
    for country in opal_dic:
        for field in opal_dic[country]:
            opal_dic[country][field]=opal_dic[country][field][:-2]

    #return opal variables in a special format to make their display easier in the template
    return opal_dic



def get_data_others(act_ids, act):
    """
    FUNCTION
    link the act to its government (gvt_compo), get the np variables (opal) and link the minister's attendance (min_attend)
    PARAMETERS
    act_ids: instance of the ids of the act [ActIds model instance]
    act: instance of the data of the act [Act model instance]
    RETURN
    opal variables [dictionary]
    """
    fields={}

    #link the act with the gvt_compo variables
    link_act_gvt_compo(act_ids, act)

    #get the gvts composition of the act
    fields["gvt_compo"]=get_gvt_compo(act_ids, act)

    #link the act with the min_attend variables  and return those variables in a special format to make their display easier in the template
    fields["min_attend"]=link_act_min_attend(act_ids)

    #link the act with the opal variables and return opal variables in a special format to make their display easier in the template
    fields["opal"]=link_get_act_opal(act_ids, act)

    return fields
