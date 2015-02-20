#-*- coding: utf-8 -*-

#common functions used by init, get and write functions
from act.models import Country
from collections import OrderedDict


#For integer variables, if there is a zero value (0), the value must be:

#~ > - EPComAmdtTabled: discarded
#~ > - EPComAmdtAdopt: discarded
#~ > - EPAmdtTabled: discarded
#~ > - EPAmdtAdopt: discarded
#~ > - EPVotesFor1-2: discarded (except when sum 1-2 and at least one of the two is non null)
#~ > - EPVotesAgst1-2: discarded (except when sum 1-2 and at least one of the two is non null)
#~ > - EPVotesAbs1-2: discarded (except when sum 1-2 and at least one of the two is non null)

#~ > - NombreLectures: counted as 0
#~ > - NbPointB: counted as 0
#~ > - NbPointA: counted as 0
#~ > - DureeAdoptionTrans: counted as 0

#~ > - NombreMots: IMPOSSIBLE
#~ > - DureeProcedureDepuisPropCom: IMPOSSIBLE
#~ > - DureeTotaleDepuisPropCom: IMPOSSIBLE
#~ > - DureeProcedureDepuisTransCons: IMPOSSIBLE
#~ > - DureeTotaleDepuisTransCons: IMPOSSIBLE



#If asked about the Durée moyenne... -> take the DureeTotaleDepuisTransCons variable



from django.db import models
from act.models import Act, MinAttend
from act_ids.models import ActIds
from datetime import datetime


def get_css(min_cs=1, max_cs=20):
    #get all the different possible cs -> cs header to be written in the csv file
    css=[str(n) for n in range(min_cs, (max_cs+1))]
    #add extra leading zero for cs with only one figure ("1"->"01")
    for index in range(len(css)):
        if len(css[index])==1:
            css[index]="0"+css[index]
    return css


def get_years(last_validated_year):
    return [str(n) for n in range(1996, last_validated_year+1)]


def add_blank(list_var):
    list_with_blank=list(list_var)
    list_with_blank.insert(0, "")
    return list_with_blank


def get_months():
    return [str(n) for n in range(1, 13)]


def get_countries():
    return Country.objects.values_list("country_code", flat=True)


#transform a us string date to a date format
def str_to_date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()


#transform a fr string date to a us string date
def fr_to_us_date(date_fr):
    #DD/MM/YYYY to YYYY-MM-DD
    year=date_fr[-4:]
    month=date_fr[3:5]
    day=date_fr[:2]
    date_us=year+"-"+month+"-"+day
    #~ print "date us"
    #~ print date_us
    return date_us
    

#transform a us string date to a fr string date
#~ def us_to_fr_date(date_us):
    #~ #YYYY-MM-DD to DD/MM/YYYY
    #~ year=date_us[:4]
    #~ month=date_us[5:7]
    #~ day=date_us[8:10]
    #~ date_fr=day+"/"+month+"/"+year
    #~ return date_fr


def get_validated_acts(Model, filter_vars_acts={}, filter_vars_acts_ids={}):
    filter_vars={}
    filter_vars_acts["validated"]=2
    #do not use validated acts of 2014
    filter_vars_acts["releve_annee__lte"]= last_validated_year
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
    filter_vars[gte]=str_to_date(period[1])
    filter_vars[lte]=str_to_date(period[2])
    return filter_vars
        

def get_periods():
    #2014-12-4
    periods=(
        ("Période 01/01/1996 - 15/09/1999", fr_to_us_date("01/01/1996"), fr_to_us_date("15/09/1999")),
        ("Période 16/09/1999 - 30/04/2004", fr_to_us_date("16/09/1999"), fr_to_us_date("30/04/2004")),
        ("Période 01/05/2004 - 14/09/2008", fr_to_us_date("01/05/2004"), fr_to_us_date("14/09/2008")),
        ("Période 15/09/2008 - 31/12/2013", fr_to_us_date("15/09/2008"), fr_to_us_date("31/12/2013"))
    )
    return periods


def get_nb_periods(factor):
    #get the number of periods (1 if there is no period)
    nb_periods=1
     #if analysis by period
    if factor=="periods":
        nb_periods=len(periods)
    return nb_periods


def get_factors():
    factors=["all", "year", "cs", "csyear"]
    return factors


def get_factors_dic():
    #store factors in an ordered dictionary: key=factor (e.g. "cs"), value=question (e.g. ", by cs")
    factors=OrderedDict({})
    factors["all"]=", pour la période 1996-"+str(last_validated_year)
    factors["periods"]=", par période"
    factors["year"]=", par année"
    factors["cs"]=", par secteur"
    factors["csyear"]=", par secteur et par année"
    factors["country"]=", par état membre"
    return factors
    

def get_factors_question(factors):
    #get factors specific to the question
    factors_question=OrderedDict({})
    for factor in factors:
        factors_question[factor]=factors_dic[factor]
    return factors_question



### GLOBAL VARIABLES ###

#last validated year
last_validated_year=2013
#there is up to 4 code sectoriels for one act
nb_css=4
#nb rapporteurs
nb_rapps=5
#nb resp_propos
nb_resps=3
#list of cs to look for
css=get_css()

years_list=get_years(last_validated_year)
years_list_zero=add_blank(years_list)
months_list=get_months()
#list of countries
countries_list=get_countries()
countries_list_zero=add_blank(countries_list)
periods=get_periods()

#list of factors (variables to study)
factors=get_factors()
#from the list of factors, get an ordered dic with factors as keys ("csyear") and questions as values ("by cs and by year")
factors_dic=get_factors_dic()
