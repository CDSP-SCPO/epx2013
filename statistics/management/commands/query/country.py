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
       

#NEW VERSION, periods does not work
def q114(factors=factors_list, periods=None):
    #1/pourcentage de AdoptCSContre et 2/pourcentage de AdoptCSAbs pour chaque Etat membre, par périodes
    variables=(("adopt_cs_abs", "AdoptCSAbs"), ("adopt_cs_contre", "AdoptCSContre"))
    variable="country"
    init_question="Pourcentage de "

    #get parameters specific to the question
    factors_question, filter_vars_acts=get_parameters_question(factors, periods)
    
    for var in variables:
        init_question_2=""
        if var[0]=="adopt_cs_contre":
            filter_vars_acts={"adopt_cs_regle_vote": "V"}
            init_question_2=", parmi les actes avec AdoptCSRegleVote=V"
            
        #~ exclude_vars_acts={var[0]: None}

        for factor, question in factors_question.iteritems():
            question=init_question+var[1]+"=Y"+init_question_2+question

            if factor=="periods":
                res=[]
                res_total=[]
                #~ for period in periods:
                    #~ filter_vars_acts_temp=filter_periods_question(filter_vars_acts, period)
                    #~ temp=init(factor, count=False, total=True)
                    #~ res.append(temp[0])
                    #~ res_total.append(temp[1])
                    #~ print "res_total", res_total
                    #~ temp=get(factor, res[-1], count=False, filter_vars_acts=filter_vars_acts_temp, nb_figures_cs=nb_figures_cs, res_total=res_total[-1], adopt_var=var[0])
                    #~ res[-1]=temp[0]
                    #~ res_total[-1]=temp[1]
                #~ write(factor, question, res, count=False, res_total=res_total, periods=periods)
            else:
                #~ pass
                res, res_total=init(factor, count=False, total=True)
                res, res_total=get(factor, res, count=False, filter_vars_acts=filter_vars_acts, nb_figures_cs=nb_figures_cs, res_total=res_total, adopt_var=var[0])
                write(factor, question, res, count=False, res_total=res_total)


#OLD version
def q114():
    #1/pourcentage de AdoptCSContre et 2/pourcentage de AdoptCSAbs pour chaque Etat membre, par périodes
    variables=(("adopt_cs_abs", "AdoptCSAbs"), ("adopt_cs_contre", "AdoptCSContre"))
    #~ variables=(("adopt_cs_abs", "AdoptCSAbs"),)
    filter_vars_acts={}
    variable="country"

    for var in variables:
        init_question="Pourcentage d'états membres parmi les actes avec "+var[1]+"=Y"
        if var[0]=="adopt_cs_contre":
            filter_vars_acts={"adopt_cs_regle_vote": "V"}
            init_question+=" et AdoptCSRegleVote=V"
        exclude_vars_acts={var[0]: None}

        #all the acts
        analysis=(variable, ", par état membre")
        question=init_question+analysis[1]
        res, res_total=init(analysis[0], total=True)
        res, res_total=get(analysis[0], res, count=False, filter_vars_acts=filter_vars_acts, exclude_vars_acts=exclude_vars_acts, res_total=res_total, adopt_var=var[0])
        write(analysis[0], question, res, count=False, res_total=res_total)
#~ 
        #~ #by period
        question=init_question+", par état membre et par période"
        res, filter_vars, filter_total, res_total=init_periods(filter_vars_acts=filter_vars_acts, query=variable)
        res, res_total=get_by_period(res, filter_vars, filter_total, exclude_vars_acts=exclude_vars_acts, res_total=res_total, adopt_cs=var[0], query=variable)
        write_periods(question, res, count=False, res_total=res_total, query=variable)
