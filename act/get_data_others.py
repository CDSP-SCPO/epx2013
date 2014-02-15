#-*- coding: utf-8 -*-
#for accents between comments inside this file
"""
get government composition from the file Composition politique gvts nationaux 93-12.csv (NationGvtPoliticalComposition) and opal variables
"""
from act.models import GvtCompo, Country, NP, MinAttend
from import_app.models import ImportNP, ImportMinAttend
from bs4 import BeautifulSoup
import re



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
    date=None
    if act.adopt_conseil!=None:
        date=act.adopt_conseil
    elif act.sign_pecs!=None:
        #if no adopt_conseil, take sign_pecs
        date=act.sign_pecs
    elif act_ids.propos_origine in ["EM", "CONS", "BCE", "CJUE"]:
        date=act.date_doc

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



def link_act_min_attend(act):
    """
    FUNCTION
    fill the assocation table which links an act and a country to its minister's attendance
    PARAMETERS
    act: instance of an act [Act model instance]
    RETURN
    min_attend_dic: min_attend variables [dictionary]
    """
    min_attend_dic={}
    #retrieve all the rows of the act from the ImportMinAttend table
    min_attends=ImportMinAttend.objects.filter(releve_annee=act.releve_annee, releve_mois=act.releve_mois, no_ordre=act.no_ordre)
    #for each country and each verbatim fill the association
    for min_attend in min_attends:
        #store data in a dictionary
        country=min_attend.country
        #initialization
        if country not in min_attend_dic:
            min_attend_dic[country]=""
        min_attend_dic[country]+=min_attend.ind_status+"; "

        try:
            MinAttend.objects.create(act=act, country=Country.objects.get(pk=min_attend.country), verbatim=min_attend.verbatim, ind_status=min_attend.ind_status)
        except Exception, e:
            print "min_attend already exists!", e

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
    #display gvt_compo variables
    for gvt_compo in act.gvt_compo.all():
        print "gvt_compo_country:", gvt_compo.country.country_code
        partys=""
        for party in gvt_compo.party.all():
            partys+=party.party+"; "
        print "gvt_compo_partys:", partys[:-2]

    #link the act with the min_attend variables  and return those variables in a special format to make their display easier in the template
    fields["min_attend"]=link_act_min_attend(act)
     #display min_attend variables
    for min_attend in MinAttend.objects.all():
        print "min_attend_act:", min_attend.act.releve_annee, min_attend.act.releve_mois, min_attend.act.no_ordre
        print "min_attend_country:", min_attend.country.country_code
        print "min_attend_verbatim:", min_attend.verbatim
        print "min_attend_ind_status:", min_attend.ind_status

    #link the act with the opal variables and return opal variables in a special format to make their display easier in the template
    fields["opal"]=link_get_act_opal(act_ids, act)

    return fields
