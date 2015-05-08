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
       

#does not work
def q114(factors=factors, periods=None):
    #1/pourcentage de AdoptCSContre et 2/pourcentage de AdoptCSAbs pour chaque Etat membre, par périodes
    variables=(("adopt_cs_abs", "AdoptCSAbs"), ("adopt_cs_contre", "AdoptCSContre"))
    init_question="Pourcentage de "

    #get the factors specific to the question
    factors_question=get_factors_question(factors)
    
    for var in variables:
        init_question_2=""
        filter_vars_acts={}
        if var[0]=="adopt_cs_contre":
            filter_vars_acts={"adopt_cs_regle_vote": "V"}
            init_question_2=", parmi les actes avec AdoptCSRegleVote=V"
            
        #~ exclude_vars_acts={var[0]: None}

        #for each factor
        for factor, question in factors_question.iteritems():
            question=init_question+var[1]+"=Y"+init_question_2+question
            res, res_total=init(factor, count=False, total=True)
            res, res_total=get(factor, res, count=False, filter_vars_acts=filter_vars_acts, res_total_init=res_total, adopt_var=var[0])
            write(factor, question, res, count=False, res_total=res_total)



def q126(factors=factors, periods=None):
    #Parmi les votes AdoptCSAbs=Y, pourcentage de chaque Etat membre
    init_question="Parmi les votes AdoptCSAbs=Y, pourcentage de votes de chaque Etat membre"
    #get the factors specific to the question
    factors_question=get_factors_question(factors)
    variable="adopt_cs_abs"
    exclude_vars_acts={variable: None}
    
    #for each factor
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res, res_total=init(factor, count=False, total=True)
        res, res_total=get(factor, res, exclude_vars_acts=exclude_vars_acts, count=False, res_total_init=res_total, adopt_var=variable)
        write(factor, question, res, count=False, res_total=res_total)
