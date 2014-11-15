#-*- coding: utf-8 -*-

#queries about the nb_point_b variable

#import general steps common to each query
from  common import *
from  ..init import *
from  ..get import *
from  ..write import *


def q60():
    question="Nombre de discussions en point b"
    nb_bj_cs("13", "Marché intérieur", "nb_point_b", "int", question)



def q65():
    question="Nombre total de points B par année"
    print question
    res=init_year(count=False)
    res=get_by_year(res, count=False, variable="nb_point_b")
    write_year(question, res, count=False)


def q66():
    question="Nombre total de points B par secteur"
    print question
    res=init_cs(count=False)
    res=get_by_cs(res, count=False, variable="nb_point_b")
    write_cs(question, res, count=False)


def q67():
    question="Nombre total de points B par année et par secteur"
    print question
    res=init_cs_year()
    res=get_by_cs_year(res, count=False, variable="nb_point_b")
    write_cs_year(question, res)


def q68():
    question="Nombre total de points B pour les actes avec un vote public, par année"
    print question
    res=init_year(count=False)
    res=get_by_year(res, count=False, variable="nb_point_b", filter_variables={"vote_public": True})
    write_year(question, res, count=False)



def q69():
    question="Nombre total de points B pour les actes avec un vote public, par secteur"
    print question
    res=init_cs(count=False)
    res=get_by_cs(res, count=False, variable="nb_point_b", filter_variables={"vote_public": True})
    write_cs(question, res, count=False)



def q70():
    question="Nombre total de points B pour les actes avec un vote public, par année et par secteur"
    print question
    res=init_cs_year(count=False)
    res=get_by_cs_year(res, count=False, variable="nb_point_b", filter_variables={"vote_public": True})
    write_cs_year(question, res, count=False)


def q73(cs=None):
    question="Nombre moyen de points B"
    Model=Act
    filter_vars_acts={"nb_point_b__gte": 1}
    periods, nb_periods, res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts)

    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel: "+cs[1]+")"
        list_acts_cs=get_list_acts_cs(cs[0], Model=Model)
        res=get_by_period_cs(list_acts_cs, periods, nb_periods, res, Model, filter_vars, filter_total, avg_variable="nb_point_b")
    else:
        res=get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total, avg_variable="nb_point_b")

    write_periods(question, res, periods, nb_periods, percent=1)


def q95():
    #Pourcentage de points B par rapport aux points A, par année, par secteur, par année et par secteur
    filter_vars_b={"nb_point_b__isnull": False}
    filter_vars_a={"nb_point_a__isnull": False}
    initial_question="Pourcentage de NbPointB"

    question=initial_question+" par secteur"
    print question
    res_1=init_cs(count=False)
    res_2=init_cs(count=False)
    res_1=get_by_cs(res_1, count=False, variable="nb_point_b", filter_vars=filter_vars_b)
    res_2=get_by_cs(res_2, count=False, variable="nb_point_a", filter_vars=filter_vars_a)
    write_cs(question, res_1, res_2=res_2, count=False, query="pt_b_a")

    question=initial_question+" par année"
    print question
    res_1=init_year(count=False)
    res_2=init_year(count=False)
    res_1=get_by_year(res_1, count=False, variable="nb_point_b", filter_vars=filter_vars_b)
    res_2=get_by_year(res_2, count=False, variable="nb_point_a", filter_vars=filter_vars_a)
    write_year(question, res_1, res_2=res_2, count=False, query="pt_b_a")

    question=initial_question+" par secteur et par année"
    print question
    res_1=init_cs_year(count=False)
    res_2=init_cs_year(count=False)
    res_1=get_by_cs_year(res_1, count=False, variable="nb_point_b", filter_vars=filter_vars_b)
    res_2=get_by_cs_year(res_2, count=False, variable="nb_point_a", filter_vars=filter_vars_a)
    write_cs_year(question, res_1, res_2=res_2, count=False, query="pt_b_a")
