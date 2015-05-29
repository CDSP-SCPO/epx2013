#-*- coding: utf-8 -*-

from act.models import Act, Country
#initiate dictionary that will contain the result of a query
from common import *


#count=False and variable=True: count the sum of all the values taken by a variable
    #e.g.: sum of all the values taken by duree_variable=1000 -> res=1000
#count=False and variable=False: count the number of occurences of items matching a set of criteria defined by filter_vars
    #e.g.: number of acts with a duree_variable greater than 0=5 -> res=5

#count=True and variable=True -> average computation: count the sum of all the values taken by a variable AND its number of occurences
    #e.g.: sum of all the values taken by duree_variable=1000, number of occurences of duree_variable=5 -> res=[1000, 5]
#count=True and variable=False -> percentage computation: count the number of occurences of items matching a set of criteria (defined by check_vars_act and check_vars_act_ids) AMONG the number of occurences of items matching the set of criteria (defined by filter_vars)
    #e.g.: number of occurences of duree_variable among the acts with no_unique_type=COD=5, number of acts with no_unique_type=COD=15 -> res=[5, 15]



def init_temp(count, empty_dic=None, empty_list=None):
    """
    FUNCTION
    initialize the data structure of the subfactor of the analysis (if year is the factor, a specific year is a subfactor, e.g. 1996)
    PARAMETERS
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    empty_dic: TO BE TESTED AND REMOVED IF NOT NEEDED ANYMORE
    empty_list: TO BE TESTED AND REMOVED IF NOT NEEDED ANYMORE
    RETURN
    temp: data structure of the subfactor of the analysis [int, dictionary, list or list of lists]
    """
    if empty_dic:
        #list of persons, key: pers object; value: nb of occurences
        temp=dict({})
    elif empty_list:
        temp=list([])
    elif count:
        temp=[0,0]
    else:
        temp=0
    return temp


def init_all(count):
    """
    FUNCTION
    initialize the data structure that is going to store the results of the "all" analysis
    PARAMETERS
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    RETURN
    res: data structure that is going to store all the results of the analysis [dictionary]
    res_total: data structure that is going to store the total of each row / column (row / column analysis) [dictionary]
    """
    res=0
    res_total=0
    if count:
        res=[0,0]

    return res, res_total


def init_period(count, periods):
    res=OrderedDict({})
    for period in periods:
        res[period[0]]=init_temp(count)
    return res
    

def init_country(count):
    """
    FUNCTION
    initialize the data structure that is going to store the results of the "country" analysis
    PARAMETERS
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    None
    RETURN
    res: data structure that is going to store all the results of the analysis [dictionary]
    res_total: data structure that is going to store the total of each row / column (row / column analysis) [dictionary]
    """
    res_total=0
    res={}
    #for each country
    for country in countries_list:
        if count:
            res[country]=[0,0]
        else:
            res[country]=0

    #~ print "init_country", res
    return res, res_total


def init_cs(count, total, empty_dic, empty_list):
    """
    FUNCTION
    initialize the data structure that is going to store the results of the "cs" analysis
    PARAMETERS
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    total: used for percentage computation, True if need to compute the total number of occurences of a row / column (row / column analysis); False otherwise (cell analysis) [boolean]
    empty_dic: TO BE TESTED AND REMOVED IF NOT NEEDED ANYMORE
    empty_list: TO BE TESTED AND REMOVED IF NOT NEEDED ANYMORE
    RETURN
    res: data structure that is going to store all the results of the analysis [dictionary]
    """
    res={}
    for cs in css:
        res[cs]=init_temp(count, empty_dic, empty_list)
        if empty_dic and total:
            res[cs]["total"]=0
    return res


def init_year(count, total, empty_dic, empty_list):
    """
    FUNCTION
    initialize the data structure that is going to store the results of the "year" analysis
    PARAMETERS
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    total: used for percentage computation, True if need to compute the total number of occurences of a row / column (row / column analysis); False otherwise (cell analysis) [boolean]
    empty_dic: TO BE TESTED AND REMOVED IF NOT NEEDED ANYMORE
    empty_list: TO BE TESTED AND REMOVED IF NOT NEEDED ANYMORE
    RETURN
    res: data structure that is going to store all the results of the analysis [dictionary]
    res_total: data structure that is going to store the total of each row / column (row / column analysis) [dictionary]
    """
    res={}
    for year in years_list:
        res[year]=init_temp(count, empty_dic, empty_list)
        if empty_dic and total:
            res[year]["total"]=0
            
    return res


def init_csyear(count, total, empty_dic, empty_list, amdt):
    """
    FUNCTION
    initialize the data structure that is going to store the results of the "csyear" analysis
    PARAMETERS
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    total: used for percentage computation, True if need to compute the total number of occurences of a row / column (row / column analysis); False otherwise (cell analysis) [boolean]
    empty_dic: TO BE TESTED AND REMOVED IF NOT NEEDED ANYMORE
    empty_list: TO BE TESTED AND REMOVED IF NOT NEEDED ANYMORE
    RETURN
    res: data structure that is going to store all the results of the analysis [dictionary]
    """
    res={}
    total_year={}
    for cs in css:
        res[cs]={}
        for year in years_list:
            temp=init_temp(count, empty_dic, empty_list)
            if total:
                if amdt==True:
                    total_year[year]=0
                else:
                    total_year[year]=temp
            res[cs][year]=temp
            if total and empty_dic:
                res[cs][year]["total"]=0

        #ATTENTION! If count=True and total=True, the same list temp=[0,0] is used for total_year and res -> MUST USE A COPY OF THE LIST
    return res


def init_act_type(count):
    """
    FUNCTION
    initialize the data structure that is going to store the results of the "act_type" analysis
    PARAMETERS
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    RETURN
    res: data structure that is going to store all the results of the analysis [dictionnary]
    """
    res={}
    for key in act_types_keys:
        res[key]=init_temp(count)
    #~ print "init", res
    return res


def init_country_year(count):
    res={}
    for country in countries_list:
        res[country]={}
        for year in years_list:
            res[country][year]=init_temp(count)
    return res


def init_country_period(count, periods):
    res={}
    for country in countries_list:
        res[country]={}
        for period in periods:
            res[country][period[0]]=init_temp(count)
    return res


def init_country_cs(count):
    res={}
    
    for country in countries_list:
        res[country]={}
        for cs in css:
            res[country][cs]=init_temp(count)

    return res


def init_country_acttype(count):
    res={}
    
    for country in countries_list:
        res[country]={}
        for key in act_types_keys:
            res[country][key]=init_temp(count)

    return res


def init_dg_year(count):
    res={}
    for dg in dg_list:
        res[dg]={}
        for year in years_list:
            res[dg][year]=init_temp(count)
    return res


def init_dg_period(count, periods):
    res={}
    for dg in dg_list:
        res[dg]={}
        for period in periods:
            res[dg][period[0]]=init_temp(count)
    return res


def init_dg_cs(count):
    res={}
    for dg in dg_list:
        res[dg]={}
        for cs in css:
            res[dg][cs]=init_temp(count)
    return res


def init_dg_acttype(count):
    res={}
    for dg in dg_list:
        res[dg]={}
        for key in act_types_keys:
            res[dg][key]=init_temp(count)
    return res
    

def init_resppf_year(count):
    res={}
    for pf in resppf_list:
        res[pf]={}
        for year in years_list:
            res[pf][year]=init_temp(count)

    res_total={}
    for year in years_list:
        res_total[year]=0
    
    return res, res_total


def init_resppf_period(count, periods):
    res={}
    for pf in resppf_list:
        res[pf]={}
        for period in periods:
            res[pf][period[0]]=init_temp(count)

    res_total={}
    for period in periods:
        res_total[period[0]]=0
    
    return res, res_total


def init_resppf_cs(count):
    res={}
    for pf in resppf_list:
        res[pf]={}
        for cs in css:
            res[pf][cs]=init_temp(count)
            
    res_total={}
    for cs in css:
        res_total[cs]=0
    
    return res, res_total


def init_resppf_acttype(count):
    res={}
    for pf in resppf_list:
        res[pf]={}
        for key in act_types_keys:
            res[pf][key]=init_temp(count)

    res_total={}
    for key in act_types_keys:
        res_total[key]=0
    
    return res, res_total


def init_perscountry_year(count):
    res={}
    for country in countries_list:
        res[country]={}
        for year in years_list:
            res[country][year]=init_temp(count)

    res_total={}
    for year in years_list:
        res_total[year]=0
    
    return res, res_total


def init_perscountry_period(count, periods):
    res={}
    for country in countries_list:
        res[country]={}
        for period in periods:
            res[country][period[0]]=init_temp(count)

    res_total={}
    for period in periods:
        res_total[period[0]]=0
    
    return res, res_total


def init_perscountry_cs(count):
    res={}
    for country in countries_list:
        res[country]={}
        for cs in css:
            res[country][cs]=init_temp(count)
            
    res_total={}
    for cs in css:
        res_total[cs]=0
    
    return res, res_total


def init_perscountry_acttype(count):
    res={}
    for country in countries_list:
        res[country]={}
        for key in act_types_keys:
            res[country][key]=init_temp(count)

    res_total={}
    for key in act_types_keys:
        res_total[key]=0
    
    return res, res_total
    

def init_rappgroup_year(count):
    res={}
    for group in rappgroup_list:
        res[group]={}
        for year in years_list:
            res[group][year]=init_temp(count)

    res_total={}
    for year in years_list:
        res_total[year]=0
    
    return res, res_total


def init_rappgroup_period(count, periods):
    res={}
    for group in rappgroup_list:
        res[group]={}
        for period in periods:
            res[group][period[0]]=init_temp(count)

    res_total={}
    for period in periods:
        res_total[period[0]]=0
    
    return res, res_total


def init_rappgroup_cs(count):
    res={}
    for group in rappgroup_list:
        res[group]={}
        for cs in css:
            res[group][cs]=init_temp(count)
            
    res_total={}
    for cs in css:
        res_total[cs]=0
    
    return res, res_total


def init_rappgroup_acttype(count):
    res={}
    for group in rappgroup_list:
        res[group]={}
        for key in act_types_keys:
            res[group][key]=init_temp(count)

    res_total={}
    for key in act_types_keys:
        res_total[key]=0
    
    return res, res_total

    
def init_groupvote_year(count):
    res={}
    for groupvote in groupvotes:
        res[groupvote]={}
        for year in years_list:
            temp=init_temp(count)
            res[groupvote][year]=temp

    #~ print "init groupvote", res
    return res


def init_groupvote_period(count, periods):
    res={}
    for groupvote in groupvotes:
        res[groupvote]=OrderedDict({})
        for period in periods:
            res[groupvote][period[0]]=init_temp(count)
    #~ print "init groupvote", res
    return res

    
def init_groupvote_cs(count):
    res={}
    
    for groupvote in groupvotes:
        res[groupvote]={}
        for cs in css:
            res[groupvote][cs]=init_temp(count)

    return res


def init_groupvote_acttype(count):
    res={}
    
    for groupvote in groupvotes:
        res[groupvote]={}
        for key in act_types_keys:
            res[groupvote][key]=init_temp(count)

    return res


def init_month(count=True):
    """
    FUNCTION
    initialize the data structure that is going to store the results of the month analysis
    PARAMETERS
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    RETURN
    res: data structure that is going to store all the results of the analysis [dictionary]
    """
    res={}
    for month in months_list:
        if count:
            temp=[0,0]
        else:
            temp=0
        res[month]=temp
    return res
    

def init(factor, count=True, total=False, amdt=False, empty_dic=False, empty_list=False, periods=None):
    """
    FUNCTION
    initialize the data structure that is going to store all the results of the analysis
    PARAMETERS
    factor: factor of the analysis [string]
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    total: used for percentage computation, True if need to compute the total number of occurences of a row / column (row / column analysis); False otherwise (cell analysis) [boolean]
    amdt: TO BE TESTED AND REMOVED IF NOT NEEDED ANYMORE
    empty_dic: TO BE TESTED AND REMOVED IF NOT NEEDED ANYMORE
    empty_list: TO BE TESTED AND REMOVED IF NOT NEEDED ANYMORE
    RETURN
    res: data structure that is going to store all the results of the analysis [dictionary]
    res_total: data structure that is going to store the total of each row / column (row / column analysis) [dictionary]
    """
    #titles_list: initialize empty list
    res_total=None

    if factor == "all":
        res, res_total=init_all(count)

    elif factor== "period":
        res=init_period(count, periods)

    elif factor=="country":
        res, res_total=init_country(count)

    elif factor=="cs":
        res=init_cs(count, total, empty_dic, empty_list)
                
    elif factor=="year":
        res=init_year(count, total, empty_dic, empty_list)

    elif factor=="csyear":
        res=init_csyear(count, total, empty_dic, empty_list, amdt)

    elif factor=="act_type":
        res=init_act_type(count)


    elif factor=="country_year":
        res=init_country_year(count)

    elif factor=="country_period":
        res=init_country_period(count, periods)

    elif factor=="country_cs":
        res=init_country_cs(count)

    elif factor=="country_acttype":
        res=init_country_acttype(count)
        

    elif factor=="dg_year":
        res=init_dg_year(count)

    elif factor=="dg_period":
        res=init_dg_period(count, periods)

    elif factor=="dg_cs":
        res=init_dg_cs(count)

    elif factor=="dg_acttype":
        res=init_dg_acttype(count)


    elif factor=="resppf_year":
        res, res_total=init_resppf_year(count)

    elif factor=="resppf_period":
        res, res_total=init_resppf_period(count, periods)

    elif factor=="resppf_cs":
        res, res_total=init_resppf_cs(count)

    elif factor=="resppf_acttype":
        res, res_total=init_resppf_acttype(count)


    elif factor=="perscountry_year":
        res, res_total=init_perscountry_year(count)

    elif factor=="perscountry_period":
        res, res_total=init_perscountry_period(count, periods)

    elif factor=="perscountry_cs":
        res, res_total=init_perscountry_cs(count)

    elif factor=="perscountry_acttype":
        res, res_total=init_perscountry_acttype(count)


    elif factor=="rappgroup_year":
        res, res_total=init_rappgroup_year(count)

    elif factor=="rappgroup_period":
        res, res_total=init_rappgroup_period(count, periods)

    elif factor=="rappgroup_cs":
        res, res_total=init_rappgroup_cs(count)

    elif factor=="rappgroup_acttype":
        res, res_total=init_rappgroup_acttype(count)
                

    elif factor=="groupvote_year":
        res=init_groupvote_year(count)

    elif factor=="groupvote_period":
        res=init_groupvote_period(count, periods)

    elif factor =="groupvote_cs":
        res=init_groupvote_cs(count)

    elif factor == "groupvote_acttype":
        res=init_groupvote_acttype(count)

    if res_total is not None:
        return res, res_total
    return res
