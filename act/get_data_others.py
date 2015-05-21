#-*- coding: utf-8 -*-
#for accents between comments inside this file
"""
get external data: gvt_compo, opal and group_votes
"""
from act.models import GvtCompo, Country, NP, MinAttend, Verbatim, Status, PartyFamily
from import_app.models import ImportNP, ImportMinAttend, ImportGroupVotes
from bs4 import BeautifulSoup
import re
from django.forms.models import model_to_dict
from collections import OrderedDict
from common.config_file import nb_groups
from  act import var_name_data


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


def save_gvt_compo(act_ids, act):
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



def save_get_min_attend(act_ids):
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
                pass
                #~ print "min_attend already exists!", e

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



def save_get_opal(act_ids, act):
    """
    FUNCTION
    fill the table which links an act to its opal variables
    PARAMETERS
    act_ids: instance of the ids of the act [ActIds model instance]
    act: instance of the act [Act model instance]
    RETURN
    opal_dic: opal variables [OrderedDict]
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


def save_get_group_votes(act):
    """
    FUNCTION
    fill the table that links an act to its ep group votes variables (if not done already) and return them
    PARAMETERS
    act: instance of the act [Act model instance]
    RETURN
    group_votes_dic: group votes variables [dictionary of lists of strings]
    """
    #to be displayed in the template
    group_votes_dic=OrderedDict({})

    #alreay exists
    if act.group_vote_names not in [None, ""] :
        for i in range(nb_groups):
            row=str(i)
            votes=getattr(act, "group_vote_"+row).split(";")
            for j, vote_col in enumerate(votes):
                group_votes_dic["group_vote_"+row+"_"+str(j)]=vote_col
            
    #doesn't exist yet
    else:
        #Are there matches in the ImportGroupVotes table?
        group_votes=ImportGroupVotes.objects.filter(title=act.titre_en)

        if group_votes:
            group_vote_names=""
            for i, group_vote in enumerate(group_votes):
                row=str(i)
                votes=[group_vote.col_for, group_vote.col_against, group_vote.col_abstension, group_vote.col_present, group_vote.col_absent, group_vote.col_non_voters, group_vote.col_total_members, group_vote.col_cohesion]
                #remove None values
                field_value=';'.join(map(str, votes)).replace("None", "")
                setattr(act, "group_vote_"+row, field_value)
                #~ print "group_vote_"+row, field_value
                group_vote_names+=group_vote.group_name+";"
                #~ print str(act.__dict__)
                #~ act.save()

                #get the data to be displayed in the template
                for j, vote_col in enumerate(votes):
                    group_votes_dic["group_vote_"+row+"_"+str(j)]=vote_col

            #~ print "group_vote_names[:-1]", group_vote_names[:-1]
            act.group_vote_names=group_vote_names[:-1]
            print "group_vote_names", act.group_vote_names
            print "group_vote_3", act.group_vote_3
            act.save()

    return group_votes_dic


      

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
    save_gvt_compo(act_ids, act)

    #link the act with the group_votes variables
    fields["group_votes"]=save_get_group_votes(act)

    #get the gvts composition of the act
    fields["gvt_compo"]=get_gvt_compo(act_ids, act)

    #link the act with the min_attend variables  and return those variables in a special format to make their display easier in the template
    fields["min_attend"]=save_get_min_attend(act_ids)

    #link the act with the opal variables and return opal variables in a special format to make their display easier in the template
    fields["opal"]=save_get_opal(act_ids, act)

    return fields
