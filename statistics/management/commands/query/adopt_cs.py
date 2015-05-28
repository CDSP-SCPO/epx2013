#-*- coding: utf-8 -*-

#queries about the adopt_cs variables

from django.db import models
from act.models import Act
#import general steps common to each query
from  common import *
from  ..init import *
from  ..get import *
from  ..write import *



def q19():
    #1/ %age AdoptCSContre=Y ET 1 EM.       2/%age AdoptCSContre=Y ET 2 EM.        3/%age AdoptCSContre=Y ET 3 EM

    question="pourcentage AdoptCSContre=Y (parmi les actes avec au moins un pays contre) ET 1/2/3 EM par année"
    print question
    res={}
    total_year={}
    nb_pays=3
    for nb in range(1, nb_pays+1):
        nb=str(nb)
        res[nb]={}
        for year in years_list:
            res[nb][year]=0
            total_year[year]=0

    for act in Act.objects.filter(validated=2):
        nb=len(act.adopt_cs_contre.all())
        year=str(act.releve_annee)
        if nb>0:
            total_year[year]+=1
            if nb<4:
                nb=str(nb)
                res[nb][year]+=1
            else:
                print "higher than 3"
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list_zero)
    row=[]
    for nb in range(1, nb_pays+1):
        nb=str(nb)
        row=[nb+" EM"]
        for year in years_list:
            if res[nb][year]==0:
                res_year=0
            else:
                res_year=round(float(res[nb][year])*100/total_year[year],3)
            row.append(res_year)
        writer.writerow(row)
    writer.writerow("")
    print ""


def percent_nb_em_adopt_cs(res, adopt_variable, regle_vote, nb_em):
    for act in Act.objects.filter(validated=2, adopt_cs_regle_vote=regle_vote):
        nb_contre=len(getattr(act, adopt_variable).all())
        if nb_contre>0:
            for nb in range(1,5):
                code_sect=getattr(act, "code_sect_"+str(nb))
                if code_sect!=None:
                    cs=get_cs(code_sect.code_sect)
                    year=str(act.releve_annee)
                    res[cs][year][1]+=1
                    if nb_contre==nb_em:
                        res[cs][year][0]+=1
    print "res", res
    return res


def q35(nb_em):
    #1/ %age AdoptCSContre=Y ET 1 EM.       2/%age AdoptCSContre=Y ET 2 EM.        3/%age AdoptCSContre=Y ET 3 EM
    question="pourcentage "+str(nb_em)+" EM (parmi les actes AdoptCSContre=Y et AdoptCSRegleVote=V du même secteur et de la même année) par secteur et par année"
    print question
    res=init_cs_year()
    res=percent_nb_em_adopt_cs(res, "adopt_cs_contre", "V", nb_em)
    write_cs_year(question, res)


def q44():
    question="pourcentage AdoptCSContre=Y (parmi les actes AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année"
    print question
    res=init_cs_year()
    res=percent_adopt_cs_year(res, "adopt_cs_contre", {"adopt_cs_regle_vote": "U"})
    write_cs_year(question, res)


def q45(nb_em):
    question="pourcentage "+str(nb_em)+" EM (parmi les actes AdoptCSContre=Y et AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année"
    print question
    res=init_cs_year()
    res=percent_nb_em_adopt_cs(res, "adopt_cs_contre", "U", nb_em)
    write_cs_year(question, res)


def q47(nb_em):
    question="pourcentage "+str(nb_em)+" EM (parmi les actes AdoptCSAbs=Y et AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année"
    print question
    res=init_cs_year()
    res=percent_nb_em_adopt_cs(res, "adopt_cs_abs", "U", nb_em)
    write_cs_year(question, res)


def q77(factors=factors, periods=None):
    #1/Nombre de votes « contre » (AdoptCSContre=Y), règle V avec 1 EM 2/Nombre d’abstentions (AdoptCSAbs=Y), règle V avec 1 EM 3/Nombre de votes « contre » (AdoptCSContre=Y), règle V avec 2 EM 4/Nombre d’abstentions (AdoptCSAbs=Y), règle V avec 2 EM 5/Nombre d’abstentions (AdoptCSAbs=Y), règle V avec 3 EM 6/Nombre de votes « contre » (AdoptCSAbs=Y), règle V avec 3 EM
    init_question="Parmis les actes avec AdoptCSRegleVote=V, nombre d'actes avec "
    variables=(("adopt_cs_abs", "AdoptCSAbs"), ("adopt_cs_contre", "AdoptCSContre"))
    countries=(1,2,3)
    
    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)

    filter_vars_acts={"adopt_cs_regle_vote": "V"}

    for variable in variables:

        for country in countries:

            for factor, question in factors_question.iteritems():
                question=init_question+variable[1]+"=Y et "+str(country)+ " EM"+question
                res=init(factor, count=False)
                res=get(factor, res, count=False, filter_vars_acts=filter_vars_acts, adopt_var=variable[0], nb_adopt_var=country, periods=periods)
                write(factor, question, res, count=False, periods=periods)
    

def q97(factors=factors, periods=None):
    #1/Pourcentage "AdoptCSAbs"= Y parmi tous les actes 2/Pourcentage "AdoptCSContre"= Y parmi les actes avec AdoptCSRegleVote=V
    variables=(("adopt_cs_abs", "AdoptCSAbs"), ("adopt_cs_contre", "AdoptCSContre"))

    filters=(
        ({}, ""),
        ({"adopt_cs_regle_vote": "U"}, " parmi les actes avec AdoptCSRegleVote=U"),
        ({"adopt_cs_regle_vote": "V"}, " parmi les actes avec AdoptCSRegleVote=V")
    )

    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)

    for variable in variables:
        init_question="pourcentage "+variable[1]+"=Y"
       
        for filt in filters:
            filter_vars_acts=filt[0]
        
            for factor, question in factors_question.iteritems():
                question=init_question+filt[1]+question
                res=init(factor)
                res=get(factor, res, filter_vars_acts=filter_vars_acts, adopt_var=variable[0], periods=periods)
                write(factor, question, res, periods=periods)


def q135(factors=factors, periods=None):
    #1/Nombre de Votes « contre » (AdoptCSContre=Y) pour les actes avec au moins un point B et AdoptCSRegleVote=V 2/Nombre de Votes « contre » (AdoptCSContre=Y) pour les actes avec au moins un point B et AdoptCSRegleVote=U 3/Nombre de votes « abstention » (AdoptCSAbs=Y) pour les actes avec au moins un point B et AdoptCSRegleVote=V 4/Nombre de votes « abstention » (AdoptCSAbs=Y) pour les actes avec au moins un point B et AdoptCSRegleVote=U
    init_question="Parmi les actes avec au moins un point B, nombre d'actes avec "
    variables=(("adopt_cs_abs", "AdoptCSAbs"), ("adopt_cs_contre", "AdoptCSContre"))
    regle_votes=("U","V")
    #TEST
    #~ variables=(("adopt_cs_abs", "AdoptCSAbs"),)
    #~ regle_votes=("V",)
    
    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)

    filter_vars_acts={"nb_point_b__gt": 0}

    for variable in variables:

        for regle_vote in regle_votes:
            filter_vars_acts_temp=filter_vars_acts.copy()
            filter_vars_acts_temp["adopt_cs_regle_vote"]=regle_vote

            for factor, question in factors_question.iteritems():
                question=init_question+variable[1]+"=Y et AdoptCSRegleVote="+regle_vote+question
                res=init(factor, count=False)
                res=get(factor, res, count=False, filter_vars_acts=filter_vars_acts_temp, adopt_var=variable[0], periods=periods)
                write(factor, question, res, count=False, periods=periods)
