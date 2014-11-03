#-*- coding: utf-8 -*-

#common functions used by init, get and write functions

from django.db import models
from act_ids.models import ActIds
from datetime import datetime


def get_cs_list():
    cs_list=[str(n) for n in range(1, 21)]
    for index in range(len(cs_list)):
        if len(cs_list[index])==1:
            cs_list[index]="0"+cs_list[index]
    return cs_list


def get_years_list():
 return [str(n) for n in range(1996, 2014)]


def get_years_list_zero():
    years_list_zero=list(get_years_list())
    years_list_zero.insert(0, "")
    return years_list_zero


def get_months_list():
    return [str(n) for n in range(1, 13)]


def get_validated_acts(Model, filter_vars):
    val="validated"
    annee="releve_annee__lte"
    if Model==ActIds:
        filter_vars["src"]="index"
        val="act__"+val
        annee="act__"+annee
    filter_vars[val]=2
    #do not use validated acts of 2014
    filter_vars[annee]= 2013
    return filter_vars


def str_to_date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()


def get_periodes():
    periodes_list=("pré-élargissement (1/1/96 - 30/6/99)","pré-élargissement (1/7/99 - 30/04/04)","post-élargissement (1/5/04 - 31/1/09)","post-Lisbonne (1/2/09 - 31/12/12)","crise (15/9/08 - 31/12/12)")
    nb_periodes=len(periodes_list)
    periodes=[None]*nb_periodes
    periodes[0]=(str_to_date("1996-1-1"), str_to_date("1999-6-30"))
    periodes[1]=(str_to_date("1999-7-1"), str_to_date("2004-4-30"))
    periodes[2]=(str_to_date("2004-5-1"), str_to_date("2009-1-31"))
    periodes[3]=(str_to_date("2009-2-1"), str_to_date("2012-12-31"))
    periodes[4]=(str_to_date("2008-09-15"), str_to_date("2012-12-31"))
    # Post-Lisbonne : 01/02/2009 – 31/12/2013
    # Crise : 15-09_2008 (Faillite Lehman Brothers) -31/12/2013
    return periodes
