#-*- coding: utf-8 -*-

#common functions used by init, get and write functions



#For integer variables, if there is a zero value (0), the value must be:

#~ > - EPComAndtTabled: discarded
#~ > - EPComAndtAdopt: discarded
#~ > - EPAmdtTabled: discarded
#~ > - EPAmdtAdopt: discarded
#~ > - EPVotesFor1-2: discarded
#~ > - EPVotesAgst1-2: discarded
#~ > - EPVotesAbs1-2: discarded

#~ > - NombreLectures: counted as 0
#~ > - NbPointB: counted as 0
#~ > - NbPointA: counted as 0
#~ > - DureeAdoptionTrans: counted as 0

#~ > - NombreMots: IMPOSSIBLE
#~ > - DureeProcedureDepuisPropCom: IMPOSSIBLE
#~ > - DureeTotaleDepuisPropCom: IMPOSSIBLE
#~ > - DureeProcedureDepuisTransCons: IMPOSSIBLE
#~ > - DureeTotaleDepuisTransCons: IMPOSSIBLE



from django.db import models
from act.models import Act, MinAttend
from act_ids.models import ActIds
from datetime import datetime


def get_cs_list(min_cs=1, max_cs=20):
    #get all the different possible cs -> cs header to be written in the csv file
    cs_list=[str(n) for n in range(min_cs, (max_cs+1))]
    #add extra leading zero for cs with only one figure ("1"->"01")
    for index in range(len(cs_list)):
        if len(cs_list[index])==1:
            cs_list[index]="0"+cs_list[index]
    return cs_list


def get_years_list():
 return [str(n) for n in range(1996, 2014)]


def get_years_list_zero(years_list):
    years_list_zero=list(years_list)
    years_list_zero.insert(0, "")
    return years_list_zero


def get_months_list():
    return [str(n) for n in range(1, 13)]



def get_validated_acts(Model, filter_vars_acts={}, filter_vars_acts_ids={}):
    filter_vars={}
    filter_vars_acts["validated"]=2
    #do not use validated acts of 2014
    filter_vars_acts["releve_annee__lte"]= 2013
    #TEST ONLY
    #~ filter_vars_acts["releve_annee__gte"]= 2009

    #the filter will be on the Act model
    if Model==Act:
        filter_vars.update(filter_vars_acts)
    #the filter will be on the ActIds/MinAttend model
    else:
        for key, value in filter_vars_acts.iteritems():
            filter_vars["act__"+key]=value
        filter_vars.update(filter_vars_acts_ids)
        if Model==ActIds:
            filter_vars["src"]="index"
        elif Model==MinAttend:
            filter_vars["act__validated_attendance"]=1

    return filter_vars


def get_validated_acts_periods(Model, period, filter_vars):
    gte="adopt_conseil__gte"
    lte="adopt_conseil__lte"
    if Model!=Act:
        gte="act__"+gte
        lte="act__"+lte
    filter_vars[gte]=period[1]
    filter_vars[lte]=period[2]
    return filter_vars


def str_to_date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()


def get_periods():
    periods=[]
    periods.append(("pré-élargissement (1/1/96 - 30/6/99)", str_to_date("1996-1-1"), str_to_date("1999-6-30")))
    periods.append(("pré-élargissement (1/7/99 - 30/04/04)", str_to_date("1999-7-1"), str_to_date("2004-4-30")))
    periods.append(("post-élargissement (1/5/04 - 30/11/09)", str_to_date("2004-5-1"), str_to_date("2009-11-30")))
    periods.append(("post-Lisbonne (1/12/09 - 31/12/13)", str_to_date("2009-12-1"), str_to_date("2013-12-31")))
    periods.append(("crise (15/9/08 - 31/12/13)", str_to_date("2008-09-15"), str_to_date("2013-12-31")))
    # Crise : 15-09_2008 (Faillite Lehman Brothers) -31/12/2013
    return periods




### VARIABLES ###
cs_list=get_cs_list()
years_list=get_years_list()
years_list_zero=get_years_list_zero(years_list)
months_list=get_months_list()
periods=get_periods()
nb_periods=len(periods)
#there is up to 4 code sectoriels for one act
nb_cs=4

