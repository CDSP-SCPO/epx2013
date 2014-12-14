#-*- coding: utf-8 -*-

#queries about the adopt_cs variables

from django.db import models
from act.models import Act
#import general steps common to each query
from  common import *
from  ..init import *
from  ..get import *
from  ..write import *


def get_percent_adopt_all(res, adopt_variable, filter_vars={}):
    filter_vars=get_validated_acts(Act, filter_vars)
    for act in Act.objects.filter(**filter_vars):
        res[1]+=1
        #check if there is at least one country
        if getattr(act, adopt_variable).exists():
            res[0]+=1

    print "res", res
    return res

    
def get_percent_adopt_cs(res, adopt_variable, filter_vars={}):
    filter_vars=get_validated_acts(Act, filter_vars)
    for act in Act.objects.filter(**filter_vars):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
                res[cs][1]+=1
                #check if there is at least one country
                if getattr(act, adopt_variable).exists():
                    res[cs][0]+=1

    print "res", res
    return res


def get_percent_adopt_year(res, adopt_variable, filter_vars={}):
    filter_vars=get_validated_acts(Act, filter_vars)
    for act in Act.objects.filter(**filter_vars):
        year=str(act.releve_annee)
        res[year][1]+=1
        #check if there is at least one country
        if getattr(act, adopt_variable).exists():
            res[year][0]+=1

    print "res", res
    return res


def get_percent_adopt_cs_year(res, adopt_variable, filter_vars={}):
    filter_vars=get_validated_acts(Act, filter_vars)
    for act in Act.objects.filter(**filter_vars):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)
                res[cs][year][1]+=1
                #check if there is at least one country
                if getattr(act, adopt_variable).exists():
                    res[cs][year][0]+=1
    print "res", res
    return res


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


def q88():
    adopt_cs=(("adopt_cs_contre", "AdoptCSContre"), ("adopt_cs_abs", "AdoptCSAbs"))
    regle_vote=("U", "V")

    for regle in regle_vote:
        filter_regle={"adopt_cs_regle_vote": regle}
        for adopt in adopt_cs:
            init_question="pourcentage "+adopt[1]+"=Y, parmi les actes AdoptCSRegleVote="+regle+", "

            question=init_question+"pour tous les actes"
            res=init_all()
            res=get_percent_adopt_all(res, adopt[0], filter_vars=filter_regle)
            write_all(question, res)

            #~ #by cs
            #~ question=init_question+"par secteur"
            #~ res=init_cs()
            #~ res=get_percent_adopt_cs(res, adopt[0], filter_vars=filter_regle)
            #~ write_cs(question, res)
#~ 
            #~ #by year
            #~ question=init_question+"par année"
            #~ res=init_year()
            #~ res=get_percent_adopt_year(res, adopt[0], filter_vars=filter_regle)
            #~ write_year(question, res)
#~ 
            #~ #by cs and by year
            #~ question=init_question+"par secteur et par année"
            #~ res=init_cs_year()
            #~ res=get_percent_adopt_cs_year(res, adopt[0], filter_vars=filter_regle)
            #~ write_cs_year(question, res)


def q97():
    #1/Pourcentage de AdoptCSContre=Y, 2/Pourcentage de AdoptCSAbs=Y, par année, par secteur, par année et par secteur
    variables={"adopt_cs_contre": "AdoptCSContre", "adopt_cs_abs": "AdoptCSAbs"}

    for key, value in variables.iteritems():
        question="Pourcentage "+value+"=Y par secteur"
        print question
        res=init_cs()
        res=percent_adopt_cs(res, key)
        write_cs(question, res)

        question="Pourcentage "+value+"=Y par année"
        print question
        res=init_year()
        res=percent_adopt_year(res, key)
        write_year(question, res)

        question="Pourcentage "+value+"=Y (parmi les actes du même secteur et de la même année) par secteur et par année"
        print question
        res=init_cs_year()
        res=percent_adopt_cs_year(res, key)
        write_cs_year(question, res)

