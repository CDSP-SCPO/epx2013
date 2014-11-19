#-*- coding: utf-8 -*-

#initiate dictionary that will contain the result of a query
from  common import *


#count=False and variable=True: count the sum of all the values taken by a variable
    #e.g.: sum of all the values taken by duree_variable=1000 -> res=1000
#count=False and variable=False: count the number of occurences of items matching a set of criteria defined by filter_vars
    #e.g.: number of acts with a duree_variable greater than 0=5 -> res=5

#count=True and variable=True -> average computation: count the sum of all the values taken by a variable AND its number of occurences
    #e.g.: sum of all the values taken by duree_variable=1000, number of occurences of duree_variable=5 -> res=[1000, 5]
#count=True and variable=False -> percentage computation: count the number of occurences of items matching a set of criteria (defined by check_vars_act and check_vars_act_ids) AMONG the number of occurences of items matching the set of criteria (defined by filter_vars)
    #e.g.: number of occurences of duree_variable among the acts with no_unique_type=COD=5, number of acts with no_unique_type=COD=15 -> res=[5, 15]




def init_cs(count=True, total=False, empty_list=False, empty_dic=False):
    res={}
    for cs in get_cs_list():
        if empty_dic:
            #list of persons, key: pers object; value: nb of occurences
            temp=dict({})
        elif empty_list:
            temp=list([])
        elif count:
            temp=[0,0]
        else:
            temp=0
        res[cs]=temp
        if empty_dic and total:
            res[cs]["total"]=0
    return res


def init_year(count=True, total=False, empty_list=False, empty_dic=False):
    #empty_dic: for list of persons
    res={}
    for year in get_years_list():
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


def init_month(count=True):
    res={}
    for month in months_list:
        if count:
            temp=[0,0]
        else:
            temp=0
        res[month]=temp
    return res


def init_cs_year(count=True, total=False, amdt=False, empty_list=False, empty_dic=False):
    #use total=True to compute the percentage of each cell compared to the total of the year
    #titles_list: initialize empty list
    res={}
    total_year={}
    for secteur in get_cs_list():
        res[secteur]={}
        for year in get_years_list():
            if empty_dic:
                #list of persons, key: pers object; value: nb of occurences
                temp=dict({})
            elif empty_list:
                temp=list([])
            elif count:
                temp=[0,0]
            else:
                temp=0

            if total:
                if amdt==True:
                    total_year[year]=0
                else:
                    total_year[year]=temp
            res[secteur][year]=temp
            if total and empty_dic:
                res[secteur][year]["total"]=0

            #ATTENTION! If count=True and total=True, the same list temp=[0,0] is used for total_year and res -> MUST USE A COPY OF THE LIST
    #~ print "res"
    #~ print res
    if total and not empty_dic:
        return res, total_year
    return res


def init_periods(Model, filter_vars_acts={}, filter_vars_acts_ids={}, filter_total_acts={}, filter_total_acts_ids={}):
    #~ periods=get_periods()
    #~ nb_periods=len(periods)
    res=[[0 for x in range(2)] for y in range(nb_periods)]
    filter_vars=get_validated_acts(Model, filter_vars_acts=filter_vars_acts, filter_vars_acts_ids=filter_vars_acts_ids)
    filter_total=get_validated_acts(Model, filter_vars_acts=filter_total_acts, filter_vars_acts_ids=filter_total_acts_ids)
    return res, filter_vars, filter_total
