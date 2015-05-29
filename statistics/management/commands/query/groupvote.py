#-*- coding: utf-8 -*-

#queries about the group vote variables


#import general steps common to each query
from  common import *
from  ..init import *
from  ..get import *
from  ..write import *



def q138(factors=factors, periods=None):
    #1/Cohésion moyenne pour chaque Groupe PE 2/Moyenne vote « oui » pour chaque groupe PE 3/Moyenne vote « non » pour chaque groupe PE 4/Moyenne vote « abstention » pour chaque groupe PE 5/Moyenne « present » pour chaque groupe PE 6/Moyenne « absent » pour chaque groupe PE 7/Moyenne « non voters » pour chaque groupe PE
    init_question="Moyenne du champ "
    variables=(
        (0, '"vote oui"'),
        (1, '"vote non"'),
        (2, '"vote abstention"'),
        (3, '"present"'),
        (4, '"absent"'),
        (5, '"non voters"'),
        (7, '"cohesion"')
    )
    
    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)

    for variable in variables:

        for factor, question in factors_question.iteritems():
            question=init_question+variable[1]+question
            res=init(factor, periods=periods)
            res=get(factor, res, periods=periods, groupvote_var_index=variable[0])
            write(factor, question, res, percent=1, periods=periods)


def q139(factors=factors, periods=None):
    #% d’actes avec une majorité de votes "For" (ALDE >= 66, Greens >= 29, GUE >= 27, IND >= 15, NI >= 20, PPE >= 192, PSE >= 145, UEN >= 29)
    init_question='Pourcentage d’actes avec une majorité de '
    variables=(
        (0, '"vote oui"'),
    )
    
    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)

    for variable in variables:

        for factor, question in factors_question.iteritems():
            question=init_question+variable[1]+" (ALDE >= 66, Greens >= 29, GUE >= 27, IND >= 15, NI >= 20, PPE >= 192, PSE >= 145, UEN >= 29)"+question
            res=init(factor, periods=periods)
            res=get(factor, res, periods=periods, groupvote_var_index=variable[0], query="groupvote_majority")
            write(factor, question, res, periods=periods)
