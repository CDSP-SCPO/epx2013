#-*- coding: utf-8 -*-

#queries about the country variable


#import general steps common to each query
from  common import *
from  ..init import *
from  ..get import *
from  ..write import *



def q101():
    initial_question="Répartition des nationalités des RespPropos"
    nb_resp=3
    #~ #par secteur
    question=initial_question+", par secteur"
    print question
    res=init_cs(total=True, empty_dic=True)
    res=get_percent_pers_cs(res, "resp", nb_resp, var="country")
    write_percent_pers(question, get_cs_list(), "CS", res, "RespPropos", var="country")

    #~ #par année
    question=initial_question+", par année"
    print question
    res=init_year(total=True, empty_dic=True)
    res=get_percent_pers_year(res, "resp", nb_resp, var="country")
    write_percent_pers(question, get_years_list(), "YEAR", res, "RespPropos", var="country")

    #par secteur et par année
    question=initial_question+", par secteur et par année"
    print question
    res=init_cs_year(total=True, empty_dic=True)
    res=get_percent_pers_cs(res, "resp", nb_resp, var="country", year_var=True)
    write_percent_pers_cs_year(question, res, "RespPropos", var="country")


def q102():
    #a)NoUniqueType=COD et NbLectures=1
    #b)NoUniqueType=COD et NbLectures=2 ou 3
    nb_lec_list=((" et NbLectures=1", "act__nb_lectures"),(" et NbLectures=2 ou 3", "act__nb_lectures__gt"))
    initial_question="Répartition des nationalités des Rapporteurs, pour les actes NoUniqueType=COD"
    nb_rapp=5
    
    for nb_lec in nb_lec_list:
        #-> par secteur
        question=initial_question+nb_lec[0]+", par secteur"
        print question
        res=init_cs(total=True, empty_dic=True)
        res=get_percent_pers_cs(res, "rapp", nb_rapp, var="country", filter_vars={"no_unique_type": "COD", nb_lec[1]: 1})
        write_percent_pers(question, get_cs_list(), "CS", res, "RapporteurPE", var="country")
    
        #~ #-> par année
        question=initial_question+nb_lec[0]+", par année"
        print question
        res=init_year(total=True, empty_dic=True)
        res=get_percent_pers_year(res, "rapp", nb_rapp, var="country", filter_vars={"no_unique_type": "COD", nb_lec[1]: 1})
        write_percent_pers(question, get_years_list(), "YEAR", res, "RapporteurPE", var="country")
    
        #~ #-> par secteur et par année
        question=initial_question+nb_lec[0]+", par secteur et par année"
        print question
        res=init_cs_year(total=True, empty_dic=True)
        res=get_percent_pers_cs(res, "rapp", nb_rapp, var="country", year_var=True, filter_vars={"no_unique_type": "COD", nb_lec[1]: 1})
        write_percent_pers_cs_year(question, res, "RapporteurPE", var="country")


def q126(factors=factors, periods=None):
    #Parmi les votes AdoptCSAbs=Y, pourcentage de chaque Etat membre
    init_question="Parmi les votes AdoptCSAbs=Y, pourcentage de votes de chaque Etat membre"
    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)
    variable="adopt_cs_abs"
    exclude_vars_acts={variable: None}
    
    #for each factor
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res, res_total=init(factor, count=False, total=True)
        res, res_total=get(factor, res, exclude_vars_acts=exclude_vars_acts, count=False, res_total_init=res_total, adopt_var=variable)
        write(factor, question, res, count=False, res_total=res_total)


def q134(factors=factors, periods=None):
    #1/Nombre de Votes « contre » (AdoptCSContre=Y) pour chaque EM 2/Nombre de votes « abstentions » (AdoptCSAbs=Y) pour chaque EM
    init_question="Nombre de Parmi les votes AdoptCSAbs=Y, pourcentage de votes de chaque Etat membre"
    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)
    variables=(("adopt_cs_abs", "AdoptCSAbs"), ("adopt_cs_contre", "AdoptCSContre"))
    exclude_vars_acts={variable: None}
    
    #for each factor
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res, res_total=init(factor, count=False, total=True)
        res, res_total=get(factor, res, exclude_vars_acts=exclude_vars_acts, count=False, res_total_init=res_total, adopt_var=variable)
        write(factor, question, res, count=False, res_total=res_total)
