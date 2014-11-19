#-*- coding: utf-8 -*-

#write the result of the query in a csv file

from act.models import Act
from django.conf import settings
import csv
from  common import *

#count=False and variable=True: count the sum of all the values taken by a variable
    #e.g.: sum of all the values taken by duree_variable=1000 -> res=1000
#count=False and variable=False: count the number of occurences of items matching a set of criteria defined by filter_vars
    #e.g.: number of acts with a duree_variable greater than 0=5 -> res=5

#count=True and variable=True -> average computation: count the sum of all the values taken by a variable AND its number of occurences
    #e.g.: sum of all the values taken by duree_variable=1000, number of occurences of duree_variable=5 -> res=[1000, 5]
#count=True and variable=False -> percentage computation: count the number of occurences of items matching a set of criteria (defined by check_vars_act and check_vars_act_ids) AMONG the number of occurences of items matching the set of criteria (defined by filter_vars)
    #e.g.: number of occurences of duree_variable among the acts with no_unique_type=COD=5, number of acts with no_unique_type=COD=15 -> res=[5, 15]



#WRITE RESULTS IN CS FILE

path=settings.PROJECT_ROOT+'/statistics/management/commands/queries.csv'
#~ writer=csv.writer(open(path, 'w'), delimiter=";")
writer=csv.writer(open(path, 'w'))


nb_acts=Act.objects.filter(validated=2).count()
writer.writerow(["Les requêtes suivantes sont recueillies à partir des "+ str(nb_acts)+ " actes validés."])
writer.writerow(["En présence de la variable secteur, chaque acte peut être compté jusqu'à 4 fois (une fois pour chaque secteur)."])
writer.writerow([""])



def write_res(question, res):
    writer.writerow([question])
    writer.writerow([res])
    writer.writerow("")
    print res
    print ""


def write_cs(question, res, res_2=None, count=True, percent=100, query=""):
    #res_2: need to sum 2 variables before computing average (q100: average votes_for_1 + votes_for_2) or percentage (q95: nb_point_a and nb_point_b)
    writer.writerow([question])
    writer.writerow(get_cs_list())
    row=[]
    for cs in get_cs_list():
        if count:
            if res[cs][0]==0:
                temp=0
            else:
                if res_2==None:
                    temp=round(float(res[cs][0])*percent/res[cs][1], 3)
                else:
                    #average votes_for_1 + votes_for_2
                    temp=round(float(res[cs][0]+res_2[cs][0])*percent/(res[cs][1]+res_2[cs][1]), 3)
        else:
            if res[cs]==0:
                temp=0
            else:
                if query=="pt_b_a":
                    #percentage nb_point_b regarding nb_point_a)
                    temp=round(float(res[cs])*percent/(res[cs]+res_2[cs]), 3)
                else:
                    temp=res[cs]
        row.append(temp)
    writer.writerow(row)
    writer.writerow("")
    print ""


def write_year(question, res, res_2=None, count=True, percent=100, bj=False, query=""):
    #res_2: need to sum 2 variables before computing average (q100: votes_for_1 and votes_for_2) or percentage (q95: nb_point_a and nb_point_b)
    writer.writerow([question])
    row=[]
    if not bj:
        writer.writerow(get_years_list())
        for year in get_years_list():
            #compute avg or percentage (two variables: total and number)
            if count:
                if res[year][0]==0:
                    temp=0
                else:
                    #indice de contrainte legislative -> nombre mots total * nb actes et non nombre mots total / nb actes
                    if query=="nb_mots":
                        res[year][1]=float(1)/res[year][1]
                    if res_2==None:
                        temp=round(float(res[year][0])*percent/res[year][1], 3)
                    else:
                        #average votes_for_1 + votes_for_2
                        temp=round(float(res[year][0]+res_2[year][0])*percent/(res[year][1]+res_2[year][1]), 3)
            else:
                if query=="pt_b_a":
                    #percentage nb_point_b regarding nb_point_a)
                    temp=round(float(res[year])*percent/(res[year]+res_2[year]), 3)
                else:
                    #no avg to compute
                    temp=res[year]
            row.append(temp)
        writer.writerow(row)
    else:
        #nb=2, display two lines with two variables
        writer.writerow(get_years_list_zero())
        for nb in range(2):
            if nb==0:
                row=["Une BJ"]
            else:
                row=["Plusieurs BJ"]

            for year in get_years_list():
                if res[year][nb]==0:
                    temp=0
                else:
                    total=res[year][0]+res[year][1]
                    temp=round(float(res[year][nb])*100/total, 3)
                row.append(temp)
            writer.writerow(row)

    writer.writerow("")
    print ""


def write_month(question, res, count=True, percent=1, query=""):
    writer.writerow([question])
    writer.writerow(months_list)
    row=[]
    for month in months_list:
        if not count:
            res_month=res[month]
        else:
            if res[month][0]==0:
                res_month=0
            else:
                #indice de contrainte legislative -> nombre mots total * nb actes et non nombre mots total / nb actes
                if query=="nb_mots":
                    res[month][1]=float(1)/res[month][1]
                res_month=round(float(res[month][0])*percent/res[month][1],3)
        row.append(res_month)

    writer.writerow(row)
    writer.writerow("")
    print ""


def write_cs_year(question, res, res_2=None, count=True, percent=100, total_year=False, amdt=False, query=""):
    #res_2: need to sum 2 variables before computing average (q100: votes_for_1 and votes_for_2) or percentage (q95: nb_point_a and nb_point_b)
    writer.writerow([question])
    writer.writerow(get_years_list_zero())
    for cs in get_cs_list():
        row=[cs]
        for year in get_years_list():
            if total_year:
                if amdt:
                    #display sum of each year for amdt
                    temp=res[cs][year][0]
                else:
                    if res[cs][year]==0:
                        temp=0
                    else:
                        temp=round(float(res[cs][year])*percent/total_year[year],3)
            else:
                if not count:
                    if res[cs][year]==0:
                        temp=0
                    elif query=="pt_b_a":
                        #percentage nb_point_b regarding nb_point_a)
                        temp=round(float(res[cs][year])*percent/(res[cs][year]+res_2[cs][year]), 3)
                    else:
                        temp=res[cs][year]
                else:
                    if res[cs][year][0]==0:
                        temp=0
                    else:
                        #indice de contrainte legislative -> nombre mots total * nb actes et non nombre mots total / nb actes
                        if query=="nb_mots":
                            res[cs][year][1]=float(1)/res[cs][year][1]
                        if res_2==None:
                            temp=round(float(res[cs][year][0])*percent/res[cs][year][1],3)
                        else:
                            #average votes_for_1 + votes_for_2
                            temp=round(float(res[cs][year][0]+res_2[cs][year][0])*percent/(res[cs][year][1]+res_2[cs][year][1]), 3)
            row.append(temp)
        writer.writerow(row)
    #write sum each column
    if amdt:
        row=["Total"]
        for year in get_years_list():
            row.append(total_year[year])
        writer.writerow(row)
    writer.writerow("")
    print ""


def write_list_pers(question, the_list, element, res, pers_type):
    #crosses cs OR year
    #element: cs OR year
    writer.writerow([question])
    for value in the_list:
        writer.writerow("")
        writer.writerow([element+" "+value])
        if pers_type=="resp":
            writer.writerow(["RespPropos", "PartyFamily", "NationRespPropos", "nb"])
            for resp in res[value]:
                try:
                    country=resp.country
                    pf=PartyFamily.objects.get(country=country, party=resp.party).party_family.encode("utf-8")
                    name=resp.name.encode("utf-8")
                    writer.writerow([name, pf, country.country_code, res[value][resp]])
                except Exception, e:
                    print "pb encoding resp", e
        else:
            writer.writerow(["RapporteursPE", "GroupRapporteurPE", "nb"])
            for rapp in res[value]:
                try:
                    name=rapp.name.encode("utf-8")
                    party=rapp.party.party.encode("utf-8")
                    writer.writerow([name, party, res[value][rapp]])
                except Exception, e:
                    print "pb encoding rapp", e
    writer.writerow("")
    print ""


def write_list_pers_cs_year(question, res, pers_type):
    writer.writerow([question])
    for cs in get_cs_list():
        writer.writerow("")
        writer.writerow(["CS "+cs])
        for year in get_years_list():
            writer.writerow(["YEAR "+year])
            if pers_type=="resp":
                writer.writerow(["RespPropos", "PartyFamily", "NationRespPropos", "nb"])
                for resp in res[cs][year]:
                    try:
                        country=resp.country
                        pf=PartyFamily.objects.get(country=country, party=resp.party).party_family.encode("utf-8")
                        name=resp.name.encode("utf-8")
                        writer.writerow([name, pf, country.country_code, res[cs][year][resp]])
                    except Exception, e:
                        print "pb encoding resp", e
            else:
                writer.writerow(["RapporteursPE", "GroupRapporteurPE", "nb"])
                for rapp in res[cs][year]:
                    try:
                        name=rapp.name.encode("utf-8")
                        party=rapp.party.party.encode("utf-8")
                        writer.writerow([name, party, res[cs][year][rapp]])
                    except Exception, e:
                        print "pb encoding rapp", e
        writer.writerow("")
    writer.writerow("")
    print ""


def write_percent_pers(question, the_list, element, res, pers_type, var="Party Family"):
    #crosses cs OR year
    #element: cs OR year
    writer.writerow([question])
    for value in the_list:
        writer.writerow("")
        writer.writerow([element+" "+value])
        writer.writerow([var+" "+pers_type, "percentage"])
        for stat in res[value]:
            if stat!="total":
                if res[value][stat]==0:
                    res_stat=0
                else:
                    res_stat=round(float(res[value][stat])*100/res[value]["total"],3)
                writer.writerow([stat, res_stat])
    writer.writerow("")
    print ""


def write_percent_pers_cs_year(question, res, pers_type, var="Party Family"):
    writer.writerow([question])
    for cs in get_cs_list():
        writer.writerow("")
        writer.writerow(["CS "+cs])
        for year in get_years_list():
            writer.writerow(["YEAR "+year])
            writer.writerow([var+" "+pers_type, "percentage"])
            for stat in res[cs][year]:
                if stat!="total":
                    if res[cs][year][stat]==0:
                        res_stat=0
                    else:
                        res_stat=round(float(res[cs][year][stat])*100/res[cs][year]["total"],3)
                    writer.writerow([stat, res_stat])

        writer.writerow("")
    writer.writerow("")
    print ""


def write_periods(question, res, periods, nb_periods, percent=100, res_2=None, nb=False):
    print question
    print "res:", res
    writer.writerow([question])

    header=[]
    for period in periods:
        header.append(period[0])
    writer.writerow(header)

    row=[]
    for index in range(nb_periods):
        if res[index][0]==0:
            temp=0
        #no percentage, display the number of occurences only
        elif nb:
            temp=res[index][0]
        elif res_2 is None:
            temp=round(float(res[index][0])*percent/res[index][1], 3)
        else:
            #average votes_for_1 + votes_for_2
            temp=round(float(res[index][0]+res_2[index][0])*percent/(res[index][1]+res_2[index][1]), 3)
        row.append(temp)
    writer.writerow(row)
    writer.writerow("")
    print ""
