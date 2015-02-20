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



def init_temp(count, empty_dic, empty_list):
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
    res=0
    res_total=0
    if count:
        res=[0,0]

    return res, res_total


def init_country():
    res_total=0
    res={}
    #for each country
    for country in countries_list:
        res[country]=0

    #~ print "init_country", res
    return res, res_total


def init_year(count, total, empty_dic, empty_list):
    res={}
    for year in years_list:
        if empty_dic:
            #list of persons, key: pers object; value: nb of occurences
            temp=dict({})
        elif empty_list:
            temp=list([])
        elif count:
            temp=[0,0]
        else:
            temp=0
        res[year]=temp
        if empty_dic and total:
            res[year]["total"]=0
            
    return res
    

def init_cs(count, total, empty_dic, empty_list):
    res={}
    for cs in css:
        res[cs]=init_temp(count, empty_dic, empty_list)
        if empty_dic and total:
            res[cs]["total"]=0
    return res


def init_csyear(count, total, empty_dic, empty_list, amdt):
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
    

def init(factor, count=True, total=False, amdt=False, empty_list=False, empty_dic=False):
    #use total=True to compute the percentage of each cell compared to the total of the year
    #titles_list: initialize empty list
    res_total=None

    if factor in ["all", "periods"]:
        res, res_total=init_all(count)

    elif factor=="country":
        res, res_total=init_country()
            
    elif factor=="year":
        res=init_year(count, total, empty_dic, empty_list)
        
    elif factor=="cs":
        res=init_cs(count, total, empty_dic, empty_list)

    elif factor=="csyear":
        res=init_csyear(count, total, empty_dic, empty_list, amdt)

    if total:
        return res, res_total
    return res


def init_month(count=True):
    res={}
    for month in months_list:
        if count:
            temp=[0,0]
        else:
            temp=0
        res[month]=temp
    return res
