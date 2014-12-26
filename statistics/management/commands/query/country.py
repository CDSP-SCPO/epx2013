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
       

def q114():
    #1/pourcentage de AdoptCSContre et 2/pourcentage de AdoptCSAbs pour chaque Etat membre, par périodes
    variables=(("adopt_cs_abs", "AdoptCSAbs"), ("adopt_cs_contre", "AdoptCSContre"))
    init_question="Pour chaque Etat membre, pourcentage de "
    filter_vars_acts={}
    variable="country"

    for var in variables:
        if var[0]=="adopt_cs_contre":
            filter_vars_acts={"adopt_cs_regle_vote": "V"}
            init_question_2=", parmi les actes avec AdoptCSRegleVote=V"
        else:
            init_question_2=""
        #~ exclude_vars_acts={var[0]: None}

        #all the acts
        analysis=(variable, ", par pays")
        question=init_question+var[1]+init_question_2+analysis[1]
        res, res_total=init(analysis[0], total=True)
        res, res_total=get(analysis[0], res, count=False, filter_vars_acts=filter_vars_acts, res_total=res_total, adopt_var=var[0])
        write(analysis[0], question, res, count=False, res_total=res_total)

        #by period
        question=init_question+var[1]+init_question_2+", par période"
        res, filter_vars, filter_total, res_total=init_periods(filter_vars_acts=filter_vars_acts, query=variable)
        res, res_total=get_by_period(res, filter_vars, filter_total, res_total=res_total, adopt_cs=var[0], query=variable)
        write_periods(question, res, count=False, res_total=res_total, query=variable)

        
