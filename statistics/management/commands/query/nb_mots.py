#-*- coding: utf-8 -*-

#queries about the nb_mots variable


#import general steps common to each query
from  common import *
from  ..init import *
from  ..get import *
from  ..write import *



def q54(factor="everything"):
    init_question="Nombre de mots moyen"
    variable="nb_mots"
    filter_vars={variable+"__isnull": False}

    if factor=="csyear":
        #get by cs and by year only (for specific cs)
        analyses, nb_figures_cs=get_specific_cs()
    
    for analysis, question in analyses:
        question=init_question+question
        
        res=init(analysis)
        res=get(analysis, res, variable=variable, filter_vars_acts=filter_vars, nb_figures_cs=nb_figures_cs)
        write(analysis, question, res, percent=1)


def nb_mots_type_acte(type_acte):
    question="Nombre de mots moyen pour les actes de type "+type_acte+", par année"
    print question
    res=init_year()
    res=get_by_year_variable(Act, res, {"validated": 2, "type_acte": type_acte}, "nb_mots")
    write_year(question, res)


def q63():
    type_actes=["CS DEC", "CS DVE", "CS REG", "DEC", "DVE", "REG", "CS DEC W/O ADD"]
    for type_acte in type_actes:
        nb_mots_type_acte(type_acte)


def nb_mots_type_acte_bis(type_actes):
    str_list=str(type_actes)
    question="Total nombre de mots * nombre d'actes de type "+str_list
    print question
    nb=0
    res=0
    for act in Act.objects.filter(validated=2, type_acte__in=type_actes, nb_mots__isnull=False):
        nb+=1
        res+=act.nb_mots
    res=res*nb
    write_res(question, res)

    question="Total nombre de mots * nombre d'actes de type "+str_list+", par année"
    print question
    res=init_year()
    res=get_by_year_variable(Act, res, {"validated": 2, "type_acte__in": type_actes, "nb_mots__isnull": False}, "nb_mots")
    write_year(question, res, query="nb_mots")


def q63_bis():
    type_actes=[["CS DVE", "DVE"], ["CS DEC CAD", "CS DEC", "DEC", "CS DEC W/O ADD"], ["CS REG", "REG"]]
    for type_acte in type_actes:
        nb_mots_type_acte_bis(type_acte)


def nb_mots_no_unique_type(no_unique_type):
    question="Nombre de mots moyen pour les actes de NoUniqueType "+no_unique_type+", par année"
    print question
    res=init_year()
    res=get_by_year_variable(ActIds, res, {"act__validated": 2, "src": "index", "no_unique_type": no_unique_type}, "nb_mots")
    write_year(question, res)


def q64():
    no_unique_types=["COD", "CNS", "SYN", "CS"]
    for no_unique_type in no_unique_types:
        nb_mots_no_unique_type(no_unique_type)


def nb_mots_no_unique_type_bis(key, no_unique_types):
    str_list=str(no_unique_types)
    nb=0
    res=0
    if key=="include":
        txt=" = "
        nb_actes=ActIds.objects.filter(act__validated=2, src="index", no_unique_type__in=no_unique_types, act__nb_mots__isnull=False)
        for act in ActIds.objects.filter(act__validated=2, src="index", no_unique_type__in=no_unique_types, act__nb_mots__isnull=False):
            nb+=1
            res+=act.act.nb_mots
    else:
        txt=" <> "
        nb_actes=ActIds.objects.filter(act__validated=2, src="index", act__nb_mots__isnull=False).exclude(no_unique_type__in=no_unique_types)
        for act in ActIds.objects.filter(act__validated=2, src="index", act__nb_mots__isnull=False).exclude(no_unique_type__in=no_unique_types):
            nb+=1
            res+=act.act.nb_mots

    question="Total nombre de mots * nombre d'actes de NoUniqueType"+txt+str_list
    print question


    res=res*nb
    write_res(question, res)

    res=init_year()
    question="Total nombre de mots * nombre d'actes de NoUniqueType"+txt+str_list+", par année"
    print question
    if key=="include":
        txt=" = "
        res=get_by_year_variable(ActIds, res, {"act__validated": 2, "src": "index", "no_unique_type__in": no_unique_types}, "nb_mots")
    else:
        txt=" <> "
        res=get_by_year_variable(ActIds, res, {"act__validated": 2, "src": "index"}, "nb_mots", exclude_vars={"no_unique_type__in": no_unique_types})

    write_year(question, res, query="nb_mots")


def q64_bis():
    no_unique_types={"include": ["COD"], "exclude": ["COD"]}
    for key, no_unique_type in no_unique_types.iteritems():
        nb_mots_no_unique_type_bis(key, no_unique_type)


def q83(factor="everything"):
    #Nb de mots x Nb d’actes, par année, par secteur, par année et par secteur
    init_question="Total nombre de mots * nombre d'actes"
    variable="nb_mots"
    filter_vars={variable+"__isnull": False}

    if factor=="csyear":
        #get by cs and by year only (for specific cs)
        analyses, nb_figures_cs=get_specific_cs()

    for analysis, question in analyses:
        question=init_question+question
        
        res=init(analysis)
        res=get(analysis, res, variable=variable, filter_vars_acts=filter_vars, nb_figures_cs=nb_figures_cs)
        write(analysis, question, res, percent=1, query=variable)


def nb_mots_2009(filter_vars={}, q=""):
    #Nb de mots x Nb d’actes par année, pour les secteurs
    question="Total nombre de mots * nombre d'actes de 2009, "+q+"par mois"
    print question
    res=init_month()
    res=get_by_month(res, "nb_mots", filter_vars=filter_vars)
    write_month(question, res, query="nb_mots")


def q90_mois():
    nb_mots_2009(filter_vars={"act__releve_annee": 2009})


def q90_mois_nut():
    nb_mots_2009(filter_vars={"act__releve_annee": 2009, "no_unique_type": "COD"}, q="pour les actes de NoUniqueType=COD, ")
