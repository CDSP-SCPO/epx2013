#-*- coding: utf-8 -*-

#write the result of the query in a csv file

from act.models import Act
from django.conf import settings
import csv
from common import *
#variables name
import act_ids.var_name_ids as var_name_ids
import act.var_name_data as var_name_data


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


nb_acts=Act.objects.filter(validated=2, releve_annee__lte=max_year).count()
writer.writerow(["Les requêtes suivantes sont recueillies à partir des "+ str(nb_acts)+ " actes validés sur la période 1996-"+str(max_year)+"."])
writer.writerow(["En présence de la variable secteur, chaque acte peut être compté jusqu'à 4 fois (une fois pour chaque secteur)."])
writer.writerow([""])


def compute(res, res_2, count, percent, query, res_total=None):
    """
    FUNCTION
    compute the final result of a subfactor (specific cs, year or cross of specific cs and year)
    PARAMETERS
    res: result dictionary [dictionary]
    res_2: result dictionary of a second variable if any (average computation) [dictionary]
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    percent: percentage rate to use (by default 100% for percentage computation and 1 for other computations) [int]
    query: name of the specific query to realize [string]
    res_total: result dictionary of the total of each row / column (row / column analysis) [dictionary]
    RETURN
    acts: list of the fields of acts matching searching criteria [list of ints or integers]
    """
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
                #~ print "normal query count=True"
                num=res[0]
                denom=res[1]

    #~ print "num", num
    #~ print "denom", denom

    #final computation
    #~ print percent
    res_final=round(float(num)*percent/denom, 3)

    return res_final


def write_all(res, res_2, count, percent, query):
    """
    FUNCTION
    write the results table of the query in a csv file (all analysis)
    PARAMETERS
    res: result dictionary [dictionary]
    res_2: result dictionary of the second variable if any (average computation) [dictionary]
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    percent: percentage rate to use (by default 100% for percentage computation and 1 for other computations) [int]
    query: name of the specific query to realize [string]
    RETURN
    None
    """
    res_final=compute(res, res_2, count, percent, query)
    writer.writerow([res_final])


def write_cs_year_country_periods(factor, res, res_2, count, percent, query, res_total, periods):
    """
    FUNCTION
    write the results table of the query in a csv file (year, cs, country or periods analysis)
    PARAMETERS
    factor: factor of the analysis [string]
    res: result dictionary [dictionary]
    res_2: result dictionary of the second variable if any (average computation) [dictionary]
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    percent: percentage rate to use (by default 100% for percentage computation and 1 for other computations) [int]
    query: name of the specific query to realize [string]
    res_total: result dictionary of the total of each row / column (row / column analysis) [dictionary]
    periods: periods to use for the periods analysis [tuple of tuples of strings]
    RETURN
    None
    """
    row=[]
    res_2_temp=None
    res_total_temp=res_total

    if factor=="year":
        list_var=years_list
    elif factor=="cs":
        list_var=css
    elif factor=="country":
        list_var=countries_list
    elif factor=="periods":
        list_var=range(len(res))

    #header: every period
    if factor=="periods":
        header=[]
        for period in periods:
            header.append(period[0])
        writer.writerow(header)
    else:
        writer.writerow(list_var)
        
    for var in list_var:
        #~ print var
        if res_2 is not None:
            res_2_temp=res_2[var]

        if res_total is not None:
            if factor=="periods":
                res_total_temp=res_total[var]
            #~ else:
                #~ res_total_temp=res_total[0]
        res_final=compute(res[var], res_2_temp, count, percent, query, res_total_temp)
        row.append(res_final)
    writer.writerow(row)


def write_csyear(res, res_2, count, percent, query):
    """
    FUNCTION
    write the results table of the query in a csv file (csyear analysis)
    PARAMETERS
    res: result dictionary [dictionary]
    res_2: result dictionary of the second variable if any (average computation) [dictionary]
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    percent: percentage rate to use (by default 100% for percentage computation and 1 for other computations) [int]
    query: name of the specific query to realize [string]
    RETURN
    None
    """
    writer.writerow(years_list_zero)
    res_2_temp=None
    
    for cs in css:
        row=[cs]
        for year in years_list:
            if res_2 is not None:
                res_2_temp=res_2[cs][year]
            res_final=compute(res[cs][year], res_2_temp, count, percent, query)
            row.append(res_final)
        writer.writerow(row)


def write_act_type(res, res_2, count, percent, query):
    """
    FUNCTION
    write the results table of the query in a csv file (act_type analysis)
    PARAMETERS
    res: result dictionary [dictionary]
    res_2: result dictionary of the second variable if any (average computation) [dictionary]
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    percent: percentage rate to use (by default 100% for percentage computation and 1 for other computations) [int]
    query: name of the specific query to realize [string]
    RETURN
    None
    """
    writer.writerow(act_types)
    res_2_temp=None
    row=[]
    
    for key in act_types_keys:
        if res_2 is not None:
            res_2_temp=res_2[key]
        res_final=compute(res[key], res_2_temp, count, percent, query)
        row.append(res_final)
        
    writer.writerow(row)


def write(factor, question, res, res_2=None, count=True, percent=100, query=None, res_total=None, periods=None):
    """
    FUNCTION
    write the results table of the query in a csv file
    PARAMETERS
    question: text of the question of the query [string]
    res: result dictionary [dictionary]
    res_2: result dictionary of the second variable if any (average computation) [dictionary]
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    percent: percentage rate to use (by default 100% for percentage computation and 1 for other computations) [int]
    query: name of the specific query to realize [string]
    res_total: result dictionary of the total of each row / column (row / column analysis) [dictionary]
    periods: periods to use for the periods analysis [tuple of tuples of strings]
    RETURN
    None
    """
    #res_2: need to sum 2 variables before computing average (q100: votes_for_1 and votes_for_2) or percentage (q95: nb_point_a and nb_point_b)
    print question
    writer.writerow([question])

    #if we don't want to compute a percentage but count the number of occurences
    if not count and res_total is None:
        percent=1

    #only one period -> first element of the list
    if factor != "periods":
        res=res[0]
        if res_2 is not None:
            res_2=res_2[0]
        if res_total is not None:
            res_total=res_total[0]
    
    if factor=="all":
        write_all(res, res_2, count, percent, query)

    elif factor in ["cs", "year", "country", "periods"]:
        write_cs_year_country_periods(factor, res, res_2, count, percent, query, res_total, periods)

    elif factor=="csyear":
      write_csyear(res, res_2, count, percent, query)

    elif factor=="act_type":
        write_act_type(res, res_2, count, percent, query)
        
    writer.writerow("")
    print ""


#NOT UP-TO-DATE!!!
def write_month(question, res, count=True, percent=1, query=""):
    """
    FUNCTION
    write the results table of the query in a csv file (months analysis)
    PARAMETERS
    question: text of the question of the query [string]
    res: result dictionary [dictionary]
    count: True if need to count the number of occurences for percentage or average computation; False otherwise (used for simple count analysis) [boolean]
    percent: percentage rate to use (by default 100% for percentage computation and 1 for other computations) [int]
    query: name of the specific query to realize [string]
    RETURN
    None
    """
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
    """
    FUNCTION
    write the results table of queries that count the number of occurences of resp and rapp variables (cs or year analysis)
    PARAMETERS
    question: text of the question of the query [string]
    the_list: list of resp or rapp [list of Person instances]
    element: "CS" or "YEAR" [string]
    res: result dictionary [dictionary]
    pers_type: "rapp" or "resp" [string]
    RETURN
    None
    """
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
    """
    FUNCTION
    write the results table of queries that count the number of occurences of resp and rapp variables (csyear analysis)
    PARAMETERS
    question: text of the question of the query [string]
    res: result dictionary [dictionary]
    pers_type: "rapp" or "resp" [string]
    RETURN
    None
    """
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
    """
    FUNCTION
    write the results table of queries that show the country repartition of rapp or resp variables, for cs or year analysis (q101 and q102)
    PARAMETERS
    question: text of the question of the query [string]
    the_list: list of resp or rapp [list of Person instances]
    element: "CS" or "YEAR" [string]
    res: result dictionary [dictionary]
    pers_type: "rapp" or "resp" [string]
    var: variable to fetch (party family or country) [string]
    RETURN
    None
    """
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
    """
    FUNCTION
    write the results table of queries that show the country repartition of rapp or resp variables, for csyear analysis (q101 and q102)
    PARAMETERS
    question: text of the question of the query [string]
    res: result dictionary [dictionary]
    pers_type: "rapp" or "resp" [string]
    var: variable to fetch (party family or country) [string]
    RETURN
    None
    """
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


def write_list_acts(question, acts, fields):
    """
    FUNCTION
    write the results table of queries that list acts with specific fields (q120 and q121)
    PARAMETERS
    question: text of the question of the query [string]
    acts: acts to display [list of ints or strings]
    fields: field names to display [list of strings]
    RETURN
    None
    """
    print question
    writer.writerow([question])
    #write headers
    headers=[]
    #act ids
    act_ids=["releve_annee", "releve_mois", "no_ordre"]
    fields=act_ids+fields
    for field in fields:
        #ActIds
        if field=="propos_origine":
            headers.append(var_name_ids.var_name[field])
        #Act
        else:
            headers.append(var_name_data.var_name[field])
    writer.writerow(headers)

    #write acts
    for act in acts:
        writer.writerow(act)
            
    writer.writerow("")
    print ""


def write_list_acts_by_year_and_dg_or_resp(question, res):
    print question
    writer.writerow([question])
    writer.writerow("")

    #for each year
    for year in years_list:
        writer.writerow(["AdoptionProposOrigine="+year])
        writer.writerow("")

        #for each dg or resp
        for var in res[year]:
            writer.writerow([var])
            #for each act
            for titre in res[year][var]:
                writer.writerow([titre])  
            writer.writerow("")
            
        writer.writerow("")

    writer.writerow("")
    
