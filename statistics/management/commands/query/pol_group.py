#-*- coding: utf-8 -*-

#queries about the political group variables (RespPropos or Rapporteur)

#import general steps common to each query
from  common import *
from  ..init import *
from  ..get import *
from  ..write import *



def q137(factors=factors, periods=None):
    init_question="Répartition des RapporteurPE"
    
    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)
    count=False

    #for each factor
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res, res_total=init(factor, count=count, periods=periods)
        res, res_total=get(factor, res, res_total=res_total, count=count, periods=periods)
        write(factor, question, res, res_total=res_total, count=count, periods=periods)
