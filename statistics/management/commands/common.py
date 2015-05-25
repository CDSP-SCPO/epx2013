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


################################### FACTORS ####################################

def get_css(min_cs=1, max_cs=20):
    """
    FUNCTION
    #get all the different possible cs for the analysis (from 1 to 20 by default)
    PARAMETERS
    min_cs: smallest cs to use for the analysis (number between 1 and 20) [int]
    max_cs: biggest cs to use for the analysis (number between 1 and 20) [int]
    RETURN
    css: all the possible cs for the analysis [list of strings]
    """
    css=[str(n) for n in range(min_cs, (max_cs+1))]
    #add extra leading zero for cs with only one figure ("1"->"01")
    for index in range(len(css)):
        if len(css[index])==1:
            css[index]="0"+css[index]
    return css


def get_years(min_year, max_year):
    """
    FUNCTION
    #get all the different possible years for the analysis (currently from 1996 to 2014)
    PARAMETERS
    min_year: first validated year [int]
    max_year: last validated year to analyse (currently 2013) [int]
    RETURN
    years: all the possible years for the analysis [list of strings]
    """
    return [str(n) for n in range(min_year, max_year+1)]
    

def get_act_types():
    """
    FUNCTION
    get the act_type factor (type_acte variable)
    PARAMETERS
    None
    RETURN
    act_type: all the different types of acts to analyze together [list of lists of strings]
    """
    return [["CS DVE", "DVE"], ["CS DEC CAD", "CS DEC", "DEC", "DEC W/O ADD", "CS DEC W/O ADD"], ["CS REG", "REG"]]


def get_act_types_keys():
    """
    FUNCTION
    get the act_type keys for the act_type factor
    PARAMETERS
    None
    RETURN
    act_type_keys: keys for the types of acts[list of strings]
    """
    return ["DVE", "DEC", "REG"]


def get_periods(periods):
    """
    FUNCTION
    get the periods to use (for the periods analysis only)
    PARAMETERS
    periods: list of periods to analyse [tuple of tuples of strings]
    RETURN
    periods: periods to use [list of tuples of strings]
    """
    new_periods=[] 
    for period in periods:
        new_periods.append(("Période "+ period[0] + " - " + period[1], fr_to_us_date(period[0]), fr_to_us_date(period[1])))
    return new_periods


def get_nb_periods(factor, periods):
    """
    FUNCTION
    get the number of periods (for the periods analysis only)
    PARAMETERS
    factor: factor of the analysis [string]
    periods: periods to use [list of tuples of strings]
    RETURN
    nb_periods: number of periods of the analysis [int]
    """
    #get the number of periods (1 if there is no period)
    nb_periods=1
     #if analysis by period
    if factor=="periods":
        nb_periods=len(periods)
    return nb_periods


def get_months():
    """
    FUNCTION
    #get all the different possible months for the analysis (from 1 to 12)
    PARAMETERS
    None
    RETURN
    months: all the possible months for the analysis [list of strings]
    """
    return [str(n) for n in range(1, 13)]


def get_countries():
    """
    FUNCTION
    #get all the different possible countries for the analysis (currently 28 countries, see act_country)
    PARAMETERS
    None
    RETURN
    countries: all the possible countries for the analysis [list of strings]
    """
    return Country.objects.values_list("country_code", flat=True)


################################ END OF FACTORS ################################


def add_blank(list_var):
    """
    FUNCTION
    #add an empty space at the first position of the years or cs list; used in the header of the result table in the csv file 
    PARAMETERS
    list_var: list of cs or years [cs]
    RETURN
    list_with_blank: list of cs or years with an empty item in first position [list of strings]
    """
    list_with_blank=list(list_var)
    list_with_blank.insert(0, "")
    return list_with_blank

    
def str_to_date(string):
    """
    FUNCTION
    transform a us string date to a date in French format
    PARAMETERS
    string: us date to transform [string]
    RETURN
    string: date in the French format [date]
    """
    return datetime.strptime(string, '%Y-%m-%d').date()


def fr_to_us_date(date_fr):
    """
    FUNCTION
    transform a fr string date to a us string date
    PARAMETERS
    date_fr: fr string date to transform [string]
    RETURN
    date_us: us string date [string]
    """
    #DD/MM/YYYY to YYYY-MM-DD
    year=date_fr[-4:]
    month=date_fr[3:5]
    day=date_fr[:2]
    date_us=year+"-"+month+"-"+day
    #~ print "date us"
    #~ print date_us
    return date_us


def get_include_filter(Model, filter_vars_acts={}, filter_vars_acts_ids={}):
    """
    FUNCTION
    prepare the filter dictionary in order to get all the validated acts that are needed for the analysis
    PARAMETERS
    Model: model to use for the analysis [Model object]
    filter_vars_acts: filtering criteria from the Act model [dictionary]
    filter_vars_acts_ids: filtering criteria from the ActIds model [dictionary]
    RETURN
    filter_vars: filter dictionary to use for the analysis [dictionary]
    """
    filter_vars={}
    filter_vars_acts["validated"]=2
    #do not use validated acts of 2014
    filter_vars_acts["releve_annee__lte"]= max_year
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
    

def get_include_filter_periods(Model, period, filter_vars):
    """
    FUNCTION
    update the filter dictionary for the periods analysis
    PARAMETERS
    Model: model to use for the analysis [Model object]
    period: period to use as filtering criteria [string]
    filter_vars: filter dictionary to to update [dictionary]
    RETURN
    filter_vars: updated filter dictionary [dictionary]
    """
    gte="adopt_conseil__gte"
    lte="adopt_conseil__lte"
    if Model!=Act:
        gte="act__"+gte
        lte="act__"+lte
    filter_vars[gte]=str_to_date(period[1])
    filter_vars[lte]=str_to_date(period[2])
    return filter_vars


def get_exclude_filter(Model, factor, exclude_vars_acts={}, exclude_vars_acts_ids={}):
    """
    FUNCTION
    prepare the exclude filter dictionary in order to exclude all the acts not wanted for the analysis
    PARAMETERS
    Model: model to use for the analysis [Model object]
    factor: factor of the analysis [string]
    exclude_vars_acts: exclude filtering criteria from the Act model [dictionary]
    exclude_vars_acts_ids: exclude filtering criteria from the ActIds model [dictionary]
    RETURN
    exclude_filter_vars: exclude filter dictionary to use for the analysis [dictionary]
    """
    exclude_filter_vars={}

    #exclude blank and null type_act
    if factor=="act_type":
        exclude_vars_acts["type_acte__exact"]=u''
        exclude_vars_acts["type_acte__isnull"]=True

    #the filter will be on the Act model
    if Model==Act:
        exclude_filter_vars.update(exclude_vars_acts)
    #the filter will be on the ActIds/MinAttend model
    else:
        for key, value in exclude_vars_acts.iteritems():
            exclude_filter_vars["act__"+key]=value
        exclude_filter_vars.update(exclude_vars_acts_ids)

    #~ print "exclude_filter_vars", exclude_filter_vars
    return exclude_filter_vars
    

def get_factors():
    """
    FUNCTION
    get the list of factors of the query
    PARAMETERS
    None
    RETURN
    factors: factors of the query [list of strings]
    """
    factors=["all", "year", "cs", "csyear", "act_type"]
    return factors


def get_factors_dic():
    """
    FUNCTION
    store all the possible factors in an ordered dictionary, with key=factor (e.g. "csyear") and value=question (e.g. ", by cs and by year")
    PARAMETERS
    None
    RETURN
    factors: ordered dictionary of all the possible factors [OrderedDict]
    """
    factors=OrderedDict({})
    factors["all"]=", pour la période 1996-"+str(max_year)
    factors["periods"]=", par période"
    factors["year"]=", par année"
    factors["cs"]=", par secteur"
    factors["csyear"]=", par secteur et par année"
    factors["act_type"]=", par type d'acte"
    factors["country"]=", par état membre"
    return factors
    

def get_factors_question(factors):
    """
    FUNCTION
    get an ordered dictionary of the factors of the query
    PARAMETERS
    factors: list of factors of the query [list of strings]
    RETURN
    factors_question: ordered dictionary of the factors of the query [OrderedDict]
    """
    factors_question=OrderedDict({})
    for factor in factors:
        factors_question[factor]=factors_dic[factor]
    return factors_question


def prepare_query(factors, periods):
    """
    FUNCTION
    get the factors of the query and update the list of periods
    PARAMETERS
    factors: list of factors of the query [list of strings]
    periods: periods to use in the French format [tuple of tuples of strings]
    RETURN
    factors_question: ordered dictionary of the factors of the query [OrderedDict]
    periods: periods to use in the American format [list of tuples of strings]
    """
    #get the factors specific to the question
    factors_question=get_factors_question(factors)
    #update periods
    if periods is not None:
        periods=get_periods(periods)
    return factors_question, periods
    

### GLOBAL VARIABLES ###

#min and max year
min_year=1996
max_year=2014
#there is up to 4 code sectoriels for one act
nb_css=4
#number of dgs
nb_dgs=3
#nb rapporteurs
nb_rapps=5
#nb resp_propos
nb_resps=3

#list of cs to look for
css=get_css()
#list of years
years_list=get_years(min_year, max_year)
#SPECIFIC QUERY, TO REMOVE
#~ years_list=get_years(2006, 2013)
years_list_zero=add_blank(years_list)
#list of months
months_list=get_months()
#list of countries
countries_list=get_countries()
countries_list_zero=add_blank(countries_list)
#list of types of acts
act_types=get_act_types()
#keys
act_types_keys=get_act_types_keys()

#list of factors (variables to study)
factors=get_factors()
#from the list of factors, get an ordered dic with factors as keys ("csyear") and questions as values ("by cs and by year")
factors_dic=get_factors_dic()
