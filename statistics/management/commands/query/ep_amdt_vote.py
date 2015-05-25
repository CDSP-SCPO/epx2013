#-*- coding: utf-8 -*-

#queries about the amdt variables

#import general steps common to each query
from  ..init import *
from  ..get import *
from  ..write import *



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


def q100(factors=factors, periods=None, nb_figures_cs=2):
    #1/Moyenne EPVotesFor1-2, 3/Moyenne EPVotesAgst1-2, 5/Moyenne EPVotesAbs1-2, par année, par secteur, par année et par secteur
    variables=(("votes_for_", "EPVotesFor"), ("votes_agst_", "EPVotesAgst"), ("votes_abs_", "EPVotesAbs"))
    
    #get parameters specific to the question
    factors_question, filter_vars_acts=get_parameters_question(factors, periods)

    for var in variables:
        #the two variables cannot be null or equal to zero at the same time
        exclude_vars_acts={var[0]+"1": 0, var[0]+"2": 0}
        init_question="Nombre moyen de "+var[1]+"1-2"

        for factor, question in factors_question.iteritems():
            question=init_question+question
            res=init(factor)
            res=get(factor, res, variable=var[0]+"1", variable_2=var[0]+"2", filter_vars_acts=filter_vars_acts, exclude_vars_acts=exclude_vars_acts, nb_figures_cs=nb_figures_cs)
            write(factor, question, res, percent=1)


def q100_periods(cs=None):
    #1/Moyenne EPVotesFor1-2, 2/Moyenne EPVotesAgst1-2, 3/Moyenne EPVotesAbs1-2, suivant différentes périodes
    variables={"votes_for_": "EPVotesFor", "votes_agst_": "EPVotesAgst", "votes_abs_": "EPVotesAbs"}
    res_vars={}
    nb=2
    Model=Act
    if cs is not None:
        list_acts_cs=get_list_acts_cs(cs[0], Model=Model)

    for key, value in variables.iteritems():
        question="Nombre moyen de "+value+"1-2, par période"
        filter_vars_acts={key+"1__gt": 0, key+"2__gt": 0}
        res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts)

        #filter by specific cs
        if cs is not None:
            question+=" (code sectoriel : "+cs[1]+")"

        for index in range(1, nb+1):
            i=str(index)
            res_vars["res_"+i]=list(res)

            if cs is not None:
                res_vars["res_"+i]=get_by_period_cs(list_acts_cs, res_vars["res_"+i], Model, filter_vars, filter_total, avg_variable=key+i)
            else:
                res_vars["res_"+i]=get_by_period(res_vars["res_"+i], Model, filter_vars, filter_total, avg_variable=key+i)

        write_periods(question, res_vars["res_1"], percent=1, res_2=res_vars["res_2"])


def q105(factors=factors, periods=None):
    #1/ Moyenne EPComAmdtAdopt + EPAmdtAdopt, 2/ Moyenne EPComAmdtTabled + EPAmdtTabled
    #par année, par secteur, par année et par secteur
    variables=(
        (("com_amdt_adopt", "EPComAmdtAdopt"), ("amdt_adopt", "EPAmdtAdopt")),
        (("com_amdt_tabled", "EPComAmdtTabled"), ("amdt_tabled", "EPAmdtTabled"))
    )
    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)

    for variable in variables:
        filter_vars={variable[0][0]+"__gt": 0, variable[1][0]+"__gt": 0}
        init_question="Nombre moyen de "+variable[0][1]+"+"+variable[1][1]
        
        for factor, question in factors_question.iteritems():
            question=init_question+question
            
            res_1=init(factor)
            res_2=init(factor)
            res_1=get(factor, res_1, variable=variable[0][0], filter_vars_acts=filter_vars, periods=periods)
            res_2=get(factor, res_2, variable=variable[1][0], filter_vars_acts=filter_vars, periods=periods)
            write(factor, question, res_1, res_2=res_2, percent=1, query="1+2", periods=periods)


def q106(factors=factors, periods=None):
    #Nombre moyen (EPComAmdtAdopt+EPAmdtAdopt) / Nombre moyen (EPComAmdtTabled+EPAmdtTabled)

    filters=(
        ("", {}),
        (" sans point B et sans vote public", {"nb_point_b": 0, "vote_public": False}),
        (" avec au moins un point B et avec vote public", {"nb_point_b__gt": 0, "vote_public": True})
    )
    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)
    
    num_vars=("amdt_adopt", "com_amdt_adopt")
    num_names=("EPAmdtAdopt", "EPComAmdtAdopt")
    denom_vars=("amdt_tabled", "com_amdt_tabled")
    denom_names=("EPAmdtTabled", "EPComAmdtTabled")

    filter_vars_acts={num_vars[0]+"__gt": 0, num_vars[1]+"__gt": 0, denom_vars[0]+"__gt": 0, denom_vars[1]+"__gt": 0}
    init_question="Nombre moyen (" + num_names[0] + "+" +num_names[1]+") /  ("+denom_names[0] + "+" +denom_names[1]+")"

    for filt in filters:
        filter_vars_temp=filter_vars_acts.copy()
        #update filter
        filter_vars_temp.update(filt[1])
        
        for factor, question in factors_question.iteritems():
            question=init_question+filt[0]+question
            res=init(factor)
            res=get(factor, res, num_vars=num_vars, denom_vars=denom_vars, filter_vars_acts=filter_vars_temp, operation="+", periods=periods)
            write(factor, question, res, percent=1, periods=periods)


#NOT USED
def q109():
    #1/ Moyenne EPVotesFor1/EPVotesFor2 2/ Moyenne EPVotesAgst1/EPVotesAgst2 3/ Moyenne EPVotesAbs1/EPVotesAbs2
    variables=(
        ("votes_for_", "EPVotesFor"),
        ("votes_agst_", "EPVotesAgst"),
        ("votes_abs_", "EPVotesAbs")
    )

    for var in variables:
        var1=var[0]+"1"
        var2=var[0]+"2"
        init_question="Nombre moyen de " + var[1] + "1 / " + var[1]+"2, "
        filter_vars={var1+"__gt": 0, var2+"__gt": 0}

        question=init_question+"par secteur"
        res=init_cs()
        res=get_by_cs_division(res, var1, var2, filter_vars=filter_vars)
        write_cs(question, res, percent=1)

        question=init_question+"par année"
        res=init_year()
        res=get_by_year_division(res, var1, var2, filter_vars=filter_vars)
        write_year(question, res, percent=1)

        question=init_question+"par secteur et par année"
        res=init_cs_year()
        res=get_by_cs_year_division(res, var1, var2, filter_vars=filter_vars)
        write_cs_year(question, res, percent=1)


def division(num_vars, num_names, denom_vars, denom_names, factor, operation=None):
    filter_vars={num_vars[0]+"__gt": 0, denom_vars[0]+"__gt": 0}
    init_question="Nombre moyen (" + num_names[0]
    
    #only one variable in the numerator and one in the denominator
    if len(num_vars)==1:
        init_question=init_question + "/" + denom_names[0] +")"
    else:
        #2 variables in the numerator and 2 in the denominator
        init_question=init_question +operation+num_names[1]+") /  ("+denom_names[0]+operation+denom_names[1]+")"

        filter_vars.update({num_vars[1]+"__gt": 0,  denom_vars[1]+"__gt": 0})

    if factor=="csyear":
        #get by cs and by year only (for specific cs)
        analyses, nb_figures_cs=get_specific_cs()


    for analysis, question in analyses:
        question=init_question+question
        res=init(analysis)
        res=get(analysis, res, num_vars=num_vars, denom_vars=denom_vars, filter_vars_acts=filter_vars, operation=operation, nb_figures_cs=nb_figures_cs)
        write(analysis, question, res, percent=1)


def q111(factor="everything"):
    #Nombre moyen de EPComAmdtAdopt / EPComAmdtTabled
    #pour tous les actes, par année, par secteur, par année et par secteur
    num_vars=("com_amdt_adopt",)
    num_names=("EPComAmdtAdopt",)
    denom_vars=("com_amdt_tabled",)
    denom_names=("EPComAmdtTabled",)
    division(num_vars, num_names, denom_vars, denom_names, factor)


def q112(factor="everything"):
    #Nombre moyen de EPAmdtAdopt / EPAmdtTabled
    #pour tous les actes, par année, par secteur, par année et par secteur
    num_vars=("amdt_adopt",)
    num_names=("EPAmdtAdopt",)
    denom_vars=("amdt_tabled",)
    denom_names=("EPAmdtTabled",)
    division(num_vars, num_names, denom_vars, denom_names, factor)


def q113(factor="everything"):
    #Nombre moyen de (EPAmdtAdopt - EPComAmdtAdopt) / (EPAmdtTabled - EPComAmdtTabled)
    #pour tous les actes, par année, par secteur, par année et par secteur
    num_vars=("amdt_adopt", "com_amdt_adopt")
    num_names=("EPAmdtAdopt", "EPComAmdtAdopt")
    denom_vars=("amdt_tabled", "com_amdt_tabled")
    denom_names=("EPAmdtTabled", "EPComAmdtTabled")
    division(num_vars, num_names, denom_vars, denom_names, factor, operation="-")


def q127(factors=factors, periods=None):
    #Nombre moyen de EPVotesFor1-2
    init_question="Nombre moyen de EPVotesFor1-2"
    variable="votes_for_"
    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)
    #the two variables cannot be null or equal to zero at the same time
    exclude_vars_acts={variable+"1": 0, variable+"2": 0}

    #for each factor
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res=init(factor)
        res=get(factor, res, variable=variable+"1", variable_2=variable+"2", exclude_vars_acts=exclude_vars_acts, periods=periods)
        write(factor, question, res, percent=1, periods=periods)
