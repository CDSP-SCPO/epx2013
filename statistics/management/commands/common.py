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


def get_cs_list(min_cs=1, max_cs=20):
    #get all the different possible cs -> cs header to be written in the csv file
    cs_list=[str(n) for n in range(min_cs, (max_cs+1))]
    #add extra leading zero for cs with only one figure ("1"->"01")
    for index in range(len(cs_list)):
        if len(cs_list[index])==1:
            cs_list[index]="0"+cs_list[index]
    return cs_list


def get_years_list(last_validated_year):
    return [str(n) for n in range(1996, last_validated_year+1)]


def add_blank(list_var):
    list_with_blank=list(list_var)
    list_with_blank.insert(0, "")
    return list_with_blank


def get_months_list():
    return [str(n) for n in range(1, 13)]


def get_countries_list():
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


def get_nb_periods(factor):
    #get the number of periods (1 if there is no period)
    nb_periods=1
     #if analysis by period
    if factor=="periods":
        nb_periods=len(periods)
    return nb_periods
        

def get_periods():
    periods=[]
    ##2014-07-24, 2014-11-12
    #~ periods.append(("pré-élargissement\n(1/1/96 - 30/6/99)", str_to_date("1996-1-1"), str_to_date("1999-6-30")))
    #~ periods.append(("pré-élargissement\n(1/7/99 - 30/04/04)", str_to_date("1999-7-1"), str_to_date("2004-4-30")))
    #~ periods.append(("post-élargissement\n(1/5/04 - 30/11/09)", str_to_date("2004-5-1"), str_to_date("2009-11-30")))
    #~ periods.append(("post-Lisbonne \n(1/12/09 - 31/12/13)", str_to_date("2009-12-1"), str_to_date("2013-12-31")))
    #~ periods.append(("crise\n(15/9/08 - 31/12/13)", str_to_date("2008-09-15"), str_to_date("2013-12-31")))
    # Crise : 15-09_2008 (Faillite Lehman Brothers) -31/12/2013

    #2014-12-4
    periods.append(("Santer\n(1/1/96 - 15/9/99)", str_to_date("1996-1-1"), str_to_date("1999-9-15")))
    periods.append(("Prodi\n(16/9/99 - 30/4/2004)", str_to_date("1999-9-16"), str_to_date("2004-4-30")))
    periods.append(("Post-élargissement\n(1/5/04 - 14/09/08)", str_to_date("2004-5-1"), str_to_date("2008-9-14")))
    periods.append(("Post-crise\n(15/9/08 - 31/12/13)", str_to_date("2008-09-15"), str_to_date("2013-12-31")))
#~ 
    #~ #2014-12-18
    #~ periods.append(("Période 01/01/1996 - 31/10/1999", str_to_date("1996-1-1"), str_to_date("1999-10-31")))
    #~ periods.append(("Période 01/11/1999 - 31/10/2004", str_to_date("1999-11-1"), str_to_date("2004-10-31")))
    #~ periods.append(("Période 01/11/2004 - 31/10/2009", str_to_date("2004-11-1"), str_to_date("2009-10-31")))
    #~ periods.append(("Période 01/11/2009 - 31/12/2013", str_to_date("2009-11-1"), str_to_date("2013-12-31")))
    
    return periods


def get_factors_list():
    factors=["all", "year", "cs", "csyear"]


def get_factors():
    #store factors in an ordered dictionary: key=factor (e.g. "cs"), value=question (e.g. ", by cs")
    factors=OrderedDict({})
    factors["all"]=", pour la période 1996-"+str(last_validated_year)
    factors["periods"]=", par période"
    factors["year"]=", par année"
    factors["cs"]=", par secteur"
    factors["csyear"]=", par secteur et par année"
    factors["country"]=", par état membre"
    return factors
    

def get_factors_question(factors_list):
    #get factors specific to the question
    factors_question=OrderedDict({})
    for factor in factors_list:
        factors_question[factor]=factors[factor]
    return factors_question



### GLOBAL VARIABLES ###

#last validated year
last_validated_year=2013
#there is up to 4 code sectoriels for one act
nb_cs=4
#nb rapporteurs
nb_rapp=5
#nb resp_propos
nb_resp=3

cs_list=get_cs_list()
#number of figures to use to get all the different cs -> if nb=2 then cs=01.xx.xx.xx ... 20.xx.xx.xx, if nb=5 then cs=01.10.xx.xx ... 20.90.xx.xx
nb_figures_cs=2

#TO COMMENT OUT
#for specific queries
cs_list=["10"]

years_list=get_years_list(last_validated_year)
years_list_zero=add_blank(years_list)
months_list=get_months_list()
#list of countries
countries_list=get_countries_list()
countries_list_zero=add_blank(countries_list)
periods=get_periods()
nb_periods=len(periods)

#list of factors (variables to study)
factors=get_factors()
factors_list=get_factors_list()
