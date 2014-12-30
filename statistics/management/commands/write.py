#-*- coding: utf-8 -*-

#write the result of the query in a csv file

from act.models import Act
from django.conf import settings
import csv
from  common import *


#count is False
    #shows a number of occurences or a sum: res[year/cs] contains only one value -> res[year/cs]=value -> final result=value
#count is True
    #average or percent computation: res[year/cs] contains two values (the second value is a count, a number of occurences) -> res[year/cs]=[val1, val2] -> final result=val1/val2
#res_2 is not None
    #need to sum 2 variables before computing average (q100: average votes_for_1 + votes_for_2) or percentage (q95: nb_point_a and nb_point_b)



#WRITE RESULTS IN CS FILE

path=settings.PROJECT_ROOT+'/statistics/management/commands/queries.csv'
#~ writer=csv.writer(open(path, 'w'), delimiter=";")
writer=csv.writer(open(path, 'w'))


nb_acts=Act.objects.filter(validated=2).count()
writer.writerow(["Les requêtes suivantes sont recueillies à partir des "+ str(nb_acts)+ " actes validés."])
writer.writerow(["En présence de la variable secteur, chaque acte peut être compté jusqu'à 4 fois (une fois pour chaque secteur)."])
writer.writerow([""])


def compute(res, res_2, count, percent, query, res_total=None):
    res_final=0
    num=0
    denom=1

    #~ print "res_total", res_total

    #only one value in res -> sum
    if not count:
        #if num=0 -> 0
        if res>0:
            if query=="pt_b_a":
                #percentage nb_point_b regarding nb_point_a)
                num=res
                denom=res+res_2
            #normal query
            else:
                num=res
                if res_total>0:
                    denom=res_total
            
    #count=True -> two values in res, either for an average or for a percentage computation
    else:
        #if num or denom=0 -> 0
        if res[0]>0:
            if query=="nb_mots":
                num=res[0]
                #indice de contrainte legislative -> nombre mots total * nb actes et non nombre mots total / nb actes
                denom=float(1)/res[1]
            #q105: average EPComAmdtAdopt + EPAmdtAdopt
            elif query=="1+2":
                num=res[0]+res_2[0]
                denom=res[1]+res_2[1]
            #normal query
            else:
                num=res[0]
                denom=res[1]

    #~ print "num", num
    #~ print "denom", denom

    #final computation
    res_final=round(float(num)*percent/denom, 3)

    return res_final


def write_all(res, res_2, count, percent, query):
    res_final=compute(res, res_2, count, percent, query)
    writer.writerow([res_final])


def write_year_cs_country(factor, res, res_2, count, percent, query, res_total, periods):
    row=[]
    res_2_temp=None
    res_total_temp=res_total

    if factor=="periods":
        list_var=range(len(res))
    if factor=="year":
        list_var=years_list
    elif factor=="cs":
        list_var=cs_list
    elif factor=="country":
        list_var=countries_list

    #header: every period
    if factor=="periods":
        header=[]
        for period in periods:
            header.append("Période du "+us_to_fr_date(period[0])+ " au "+us_to_fr_date(period[1]))
        writer.writerow(header)
    else:
        writer.writerow(list_var)
        
    for var in list_var:
        if res_2 is not None:
            res_2_temp=res_2[var]
        if factor=="periods" and res_total is not None:
            res_total_temp=res_total[var]
        res_final=compute(res[var], res_2_temp, count, percent, query, res_total_temp)
        row.append(res_final)
    writer.writerow(row)


def write_csyear(res, res_2, count, percent, query):
    writer.writerow(years_list_zero)
    res_2_temp=None
    
    for cs in cs_list:
        row=[cs]
        for year in years_list:
            if res_2 is not None:
                res_2_temp=res_2[cs][year]
            res_final=compute(res[cs][year], res_2_temp, count, percent, query)
            row.append(res_final)
        writer.writerow(row)
    

def write(factor, question, res, res_2=None, count=True, percent=100, query=None , res_total=None, periods=None):
    #res_2: need to sum 2 variables before computing average (q100: votes_for_1 and votes_for_2) or percentage (q95: nb_point_a and nb_point_b)
    print question
    writer.writerow([question])

    if factor=="all":
        write_all(res, res_2, count, percent, query)

    elif factor in ["periods", "year", "cs", "country"]:
        write_year_cs_country(factor, res, res_2, count, percent, query, res_total, periods)

    elif factor=="csyear":
      write_csyear(res, res_2, count, percent, query)
        
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


#OLD, NOT TO USE ANYMORE
def compute_periods(row, res, res_2, count, percent, query, res_total):
    res_2_temp=None
    
    if query=="country":
        for country in countries_list:
            if res_2 is not None:
                res_2_temp=res_2[country]
            res_final=compute(res[country], res_2_temp, count, percent, query, res_total=res_total)
            row.append(res_final)

        writer.writerow(row)

    #normal query, by period only
    else:
        res_final=compute(res, res_2, count, percent, query)
        row.append(res_final)
        writer.writerow(row)

#~ 
#~ #OLD, NOT TO USE ANYMORE
def write_periods(question, res, percent=100, res_2=None, count=True, res_total=None, query=None):
    print question
    writer.writerow([question])
    res_2_temp=None

    if query=="country":
         writer.writerow(countries_list_zero)

    for index in range(nb_periods):
        row=[periods[index][0]]
        if res_2 is not None:
            res_2_temp=res_2[index]
        compute_periods(row, res[index], res_2_temp, count, percent, query, res_total[index])
        
    writer.writerow("")
    print ""
