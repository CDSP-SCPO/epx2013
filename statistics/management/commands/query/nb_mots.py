#-*- coding: utf-8 -*-

#queries about the nb_mots variable


#import general steps common to each query
from  common import *
from  ..init import *
from  ..get import *
from  ..write import *



def q54(factors=factors, periods=None):
    init_question="Nombre de mots moyen"
    variable="nb_mots"
    filter_vars_acts={variable+"__isnull": False}

    #get the factors specific to the question
    factors_question=get_factors_question(factors)

    #for each factor
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res=init(factor)
        res=get(factor, res, variable=variable, filter_vars_acts=filter_vars_acts, periods=periods)
        write(factor, question, res, percent=1, periods=periods)


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


def q83(factors=factors, nb_figures_cs=2):
    #Nb de mots x Nb d’actes, par année, par secteur, par année et par secteur
    init_question="Total nombre de mots * nombre d'actes"
    variable="nb_mots"

    #get parameters specific to the question
    factors_question, filter_vars_acts=get_parameters_question(factors, periods)

    filter_vars_acts.update({variable+"__isnull": False})
    
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res=init(factor)
        res=get(factor, res, variable=variable, filter_vars_acts=filter_vars_acts, nb_figures_cs=nb_figures_cs)
        write(factor, question, res, percent=1, query=variable)


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


def nb_mots_moyen_type_acte(factors, type_actes):
    init_question="Nombre de mots moyen pour les actes de type "+ str(type_actes)
    variable="nb_mots"
    #get parameters specific to the question
    factors_question, filter_vars_acts=get_parameters_question(factors, periods)

    filter_vars_acts.update({variable+"__isnull": False, "type_acte__in": type_actes})
    
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res=init(factor)
        res=get(factor, res, variable=variable, filter_vars_acts=filter_vars_acts)
        write(factor, question, res, percent=1)
        

def q116(factors=factors):
    type_actes=[["CS DVE", "DVE"], ["CS DEC CAD", "CS DEC", "DEC", "CS DEC W/O ADD"], ["CS REG", "REG"]]
    for type_acte in type_actes:
        nb_mots_moyen_type_acte(factors, type_acte)


def q123(factors=factors):
    #Nombre total de mots pour les actes de type...
    variable="nb_mots"
    filter_vars_acts={variable+"__isnull": False}
    #get the factors specific to the question
    factors_question=get_factors_question(factors)

    #CS DEC, CS DEC CAD, DEC, DEC W/O ADD, DEC W/ ADD
    type_actes=[["CS DVE", "DVE"], ["CS DEC CAD", "CS DEC", "DEC", "DEC W/O ADD", "CS DEC W/O ADD"], ["CS REG", "REG"]]

    #for each type
    for type_acte in type_actes:
        init_question="Nombre total de mots pour les actes de type "+str(type_acte)
        filter_vars_acts["type_acte__in"]=type_acte

        #for each factor
        for factor, question in factors_question.iteritems():
            question=init_question+question
            res=init(factor, count=False)
            res=get(factor, res, variable=variable, filter_vars_acts=filter_vars_acts, count=False)
            write(factor, question, res, count=False)


def q125(factors=factors):
    #Nombre de mots moyens pour les actes de type...
    variable="nb_mots"
    filter_vars_acts={variable+"__isnull": False}
    #get the factors specific to the question
    factors_question=get_factors_question(factors)

    #CS DEC, CS DEC CAD, DEC, DEC W/O ADD, DEC W/ ADD
    type_actes=[["CS DVE", "DVE"], ["CS DEC CAD", "CS DEC", "DEC", "DEC W/O ADD", "CS DEC W/O ADD"], ["CS REG", "REG"]]

    #for each type
    for type_acte in type_actes:
        init_question="Nombre de mots moyens pour les actes de type "+str(type_acte)
        filter_vars_acts["type_acte__in"]=type_acte

        #for each factor
        for factor, question in factors_question.iteritems():
            question=init_question+question
            res=init(factor)
            res=get(factor, res, variable=variable, filter_vars_acts=filter_vars_acts)
            write(factor, question, res, percent=1)
