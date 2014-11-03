#-*- coding: utf-8 -*-

#queries about the amdt variables

#import general steps common to each query
from  ..init import *
from  ..get import *
from  ..write import *


def q16():
    #nombre moyen de EPComAmdtTabled, EPComAmdtAdopt, EPAmdtTabled, EPAmdtAdopt
    question="nombre moyen de EPComAmdtTabled, EPComAmdtAdopt, EPAmdtTabled, EPAmdtAdopt par année"
    print question
    amdts={}
    amdts["EPComAmdtTabled"]="com_amdt_tabled"
    amdts["EPComAmdtAdopt"]="com_amdt_adopt"
    amdts["EPAmdtTabled"]="amdt_tabled"
    amdts["EPAmdtAdopt"]="amdt_adopt"
    res={}
    for amdt in amdts:
        res[amdt]={}
        for year in years_list:
            res[amdt][year]=[0,0]

    for act in Act.objects.filter(validated=2):
        year=str(act.releve_annee)
        for amdt in amdts:
            if getattr(act, amdts[amdt])!=None:
                res[amdt][year][1]+=1
                res[amdt][year][0]+=getattr(act, amdts[amdt])
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list_zero)
    for amdt in amdts:
        row=[amdt]
        for year in years_list:
            if res[amdt][year][1]==0:
                res_year=0
            else:
                res_year=round(float(res[amdt][year][0])/res[amdt][year][1],3)
            row.append(res_year)
        writer.writerow(row)
    writer.writerow("")
    print ""




def q32(display_name, variable_name):
    #nombre moyen de EPComAmdtTabled, EPComAmdtAdopt, EPAmdtTabled, EPAmdtAdopt
    question="nombre moyen de " +display_name+ " par secteur, en fonction de l'année"
    print question
    res, total_year=init_cs_year(total=True, amdt=True)
    res, total_year=get_by_cs_year(res, variable=variable_name, total_year=total_year)
    write_cs_year(question, res, total_year=total_year, amdt=True)


    
def q75():
    question="Nombre moyen d’amendements déposés par la commission parlementaire du PE saisie au fond"
    filter_variables={"com_amdt_tabled__isnull": False}
    queries_periodes(question, Act, filter_variables=filter_variables, exclude_variables={"com_amdt_tabled": 0}, filter_total=filter_variables, avg_variable="com_amdt_tabled", percent=1)
    
    question="Nombre moyen d’amendements déposés au PE"
    filter_variables={"amdt_tabled__isnull": False}
    queries_periodes(question, Act, filter_variables=filter_variables, exclude_variables={"amdt_tabled": 0}, filter_total=filter_variables, avg_variable="amdt_tabled", percent=1)


def q99():
    #Nombre d’EPComAmdtAdopt, 2/Nombre d’EPComAmdtTabled, 3/Nombre d’EPAmdtAdopt, 4/Nombre d’EPAmdtTabled, par année, par secteur, par année et par secteur
    variables={"com_amdt_tabled": "EPComAmdtTabled", "com_amdt_adopt": "EPComAmdtAdopt", "amdt_tabled": "EPAmdtTabled", "amdt_adopt": "EPAmdtAdopt"}

    for key, value in variables.iteritems():
        filter_vars={key+"__isnull": False}
        
        question="Nombre total d'"+value+" par secteur"
        print question
        res=init_cs(count=False)
        res=get_by_cs(res, count=False, variable=key, filter_vars=filter_vars)
        write_cs(question, res, count=False)
#~ 
        question="Nombre total d'"+value+" par année"
        print question
        res=init_year(count=False)
        res=get_by_year(res, count=False, variable=key, filter_vars=filter_vars)
        write_year(question, res, count=False)

        question="Nombre total d'"+value+" par année et par secteur"
        print question
        res=init_cs_year(count=False)
        res=get_by_cs_year(res, count=False, variable=key, filter_vars=filter_vars)
        write_cs_year(question, res, count=False)


def q100():
    #1/Moyenne EPVotesFor1, 2/Moyenne EPVotesFor2, 3/Moyenne EPVotesAgst1, 4/Moyenne EPVotesAgst2, 5/Moyenne EPVotesAbs1, 6/Moyenne EPVotesAbs2, par année, par secteur, par année et par secteur
    variables={"votes_for_": "EPVotesFor", "votes_agst_": "EPVotesAgst", "votes_abs_": "EPVotesAbs"}
    res={}
    nb=2

    #TODO
    for key, value in variables.iteritems():
		filter_vars={key+"1__isnull": False, key+"2__isnull": False}
		#~ 
		question="Nombre moyen de "+value+"1-2 par secteur"
		print question
		for index in range(1, nb+1):
			i=str(index)
			res["res_"+i]=init_cs()
			res["res_"+i]=get_by_cs(res["res_"+i], variable=key+i, filter_vars=filter_vars)
		write_cs(question, res["res_1"], res_2=res["res_2"], percent=1)
		
		question="Nombre moyen de "+value+"1-2 par année"
		print question
		for index in range(1, nb+1):
			i=str(index)
			res["res_"+i]=init_year()
			res["res_"+i]=get_by_year(res["res_"+i], variable=key+i, filter_vars=filter_vars)
		write_year(question, res["res_1"], res_2=res["res_2"], percent=1)
		
		question="Nombre moyen de "+value+"1-2 par secteur et par année"
		print question
		for index in range(1, nb+1):
			i=str(index)
			res["res_"+i]=init_cs_year()
			res["res_"+i]=get_by_cs_year(res["res_"+i], variable=key+i, filter_vars=filter_vars)
		write_cs_year(question, res["res_1"], res_2=res["res_2"], percent=1)
