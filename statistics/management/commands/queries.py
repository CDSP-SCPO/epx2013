#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.db import models
from act.models import Act, PartyFamily
from act_ids.models import ActIds
from django.db.models import Count
import csv
from django.conf import settings
from collections import OrderedDict
import datetime


#year and code sectoriel lists
years_list=[str(n) for n in range(1996, 2013)]
years_list_zero=list(years_list)
years_list_zero.insert(0, "")
#~ cs_1=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
cs_1=[str(n) for n in range(1, 21)]
for index in range(len(cs_1)):
    if len(cs_1[index])==1:
        cs_1[index]="0"+cs_1[index]
cs_2=["05.20", "15.10", "19.20", "19.30"]
cs_list=cs_1+cs_2

#write results in file
path=settings.PROJECT_ROOT+'/statistics/management/commands/queries.csv'
writer=csv.writer(open(path, 'w'))


def q1():
    #proportion d’actes avec plusieurs codes sectoriels
    question="proportion d’actes avec plusieurs codes sectoriels"
    print question

    cs=Act.objects.filter(validated=2, code_sect_1__isnull = False, code_sect_2__isnull = False).count()
    print "cs", cs
    nb_acts=Act.objects.filter(validated=2).count()
    print "nb_acts", nb_acts
    res=round(float(cs)/nb_acts,3)
    print "res", res

    writer.writerow([question])
    writer.writerow([res])
    writer.writerow("")
    print ""


def q2():
    #ventilation par domaines
    question="ventilation par domaines"
    print question
    res={}
    for secteur in cs_list:
        res[secteur]=0

    for act in Act.objects.filter(validated=2, code_sect_1__isnull=False):
        cs=act.code_sect_1.code_sect
        if cs[:5] in cs_2:
            res[cs[:5]]+=1
        elif cs[:2] in cs_1:
            res[cs[:2]]+=1
    print "res", res

    writer.writerow([question])
    writer.writerow(cs_list)
    temp=[]
    for cs in cs_list:
        temp.append(res[cs])
    writer.writerow(temp)
    writer.writerow("")
    print ""


def q3():
    #TODO
    #Frequence de la concordance Com/rapporteur/presidence du Conseil pour les 3 grandes familles (PPE ,PSE, ALDE)
    question="Frequence de la concordance Com/rapporteur/presidence du Conseil pour les 3 grandes familles (PPE ,PSE, ALDE)"
    print question

    writer.writerow([question])
    writer.writerow("")
    print ""


def q4():
    #TODO
    #Frequence de la concordance PE/Conseil
    question="Frequence de la concordance PE/Conseil"
    print question

    writer.writerow([question])
    writer.writerow("")
    print ""


def q5():
    #TODO
    #Fréquence de la concordance Commission/Conseil
    question="Frequence de la concordance Commission/Conseil"
    print question

    writer.writerow([question])
    writer.writerow("")
    print ""


def q6():
    #TODO
    #Frequence de la concordance Commission/PE
    question="Frequence de la concordance Commission/PE"
    print question


    writer.writerow([question])
    writer.writerow("")
    print ""


def q7():
    #duree moyenne des actes adoptes en 1e et en 2e lecture
    #1/ DureeTotaleDepuisPropCom lorsque NoUniqueType=COD ET NombreLectures=1.
    #2/ DureeTotaleDepuisPropCom lorsque NoUniqueType=COD ET NombreLectures=2
    question="duree moyenne des actes adoptes en 1e et en 2e lecture"
    print question
    res_1=0
    res_2=0

    #first lecture
    lec_1=ActIds.objects.filter(act__validated=2, no_unique_type="COD", act__nb_lectures=1)
    for lec in lec_1:
        res_1+=lec.act.duree_tot_depuis_prop_com
    res_1=round(float(res_1)/lec_1.count(), 3)
    print "res_1", res_1

    #second lecture
    lec_2=ActIds.objects.filter(act__validated=2, no_unique_type="COD", act__nb_lectures=2)
    for lec in lec_2:
        res_2+=lec.act.duree_tot_depuis_prop_com
    res_2=round(float(res_2)/lec_2.count(), 3)
    print "res_2", res_2

    question="DureeTotaleDepuisPropCom lorsque NoUniqueType=COD ET NombreLectures=1"
    writer.writerow([question])
    writer.writerow([res_1])
    writer.writerow("")
    question="DureeTotaleDepuisPropCom lorsque NoUniqueType=COD ET NombreLectures=2"
    writer.writerow([question])
    writer.writerow([res_2])
    writer.writerow("")
    print ""


def q8():
    #durée moyenne entre transmission au conseil et adoption pour les actes qui ont donné lieu à un vote public
    question="DureeTotaleDepuisTransCons lorsque VotePublic=Y"
    print question
    res=0

    acts=Act.objects.filter(validated=2, vote_public=True, duree_tot_depuis_trans_cons__isnull=False)
    for act in acts:
        res+=act.duree_tot_depuis_trans_cons
    res=round(float(res)/acts.count(), 3)
    print "res", res

    writer.writerow([question])
    writer.writerow([res])
    writer.writerow("")
    print ""


def q9():
    #Nombre d'actes legislatifs adoptes par annee
    question="production legislative par annee"
    print question
    res=[]

    for year in years_list:
        res.append(Act.objects.filter(validated=2, releve_annee=year).count())
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list_zero)
    writer.writerow(res)
    writer.writerow("")
    print ""


def q10():
    #production legislative par domaine et par année
    question="production legislative par domaine et par année"
    print question
    res={}
    for secteur in cs_list:
        res[secteur]={}
        for year in years_list:
            res[secteur][year]=0

    for act in Act.objects.filter(validated=2, code_sect_1__isnull=False):
        cs=act.code_sect_1.code_sect
        if cs[:5] in cs_2:
            res[cs[:5]][str(act.releve_annee)]+=1
        elif cs[:2] in cs_1:
            res[cs[:2]][str(act.releve_annee)]+=1
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list_zero)
    for cs in cs_list:
        row=[]
        row.append(cs)
        for year in years_list:
            row.append(res[cs][year])
        writer.writerow(row)
    writer.writerow("")
    print ""


def q11():
    #pourcentage de propositions modifiées par la Commission par annee
    question="pourcentage de propositions modifiees par la Commission par année"
    print question
    res={}
    for year in years_list:
        res[year]=[0,0]

    for act in Act.objects.filter(validated=2):
        res[str(act.releve_annee)][1]+=1
        if act.modif_propos:
            res[str(act.releve_annee)][0]+=1
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list)
    row=[]
    for year in years_list:
        if res[year][0]==0:
            res_year=0
        else:
            res_year=round(float(res[year][0])*100/res[year][1],3)
        row.append(res_year)
    writer.writerow(row)
    writer.writerow("")
    print ""


def q12():
    #durée moyenne d’adoption
    question="DureeTotaleDepuisPropCom en moyenne par année"
    print question
    res={}
    for year in years_list:
        res[year]=[0,0]

    for act in Act.objects.filter(validated=2, duree_tot_depuis_prop_com__isnull=False):
        res[str(act.releve_annee)][1]+=1
        if act.modif_propos:
            res[str(act.releve_annee)][0]+=act.duree_tot_depuis_prop_com
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list)
    row=[]
    for year in years_list:
        if res[year][0]==0:
            res_year=0
        else:
            res_year=round(float(res[year][0])/res[year][1],3)
        row.append(res_year)
    writer.writerow(row)
    writer.writerow("")
    print ""


def q13():
    #Pourcentage d'actes NoUniqueType=COD adoptés en 1ère et 2ème lecture.
    question="Pourcentage d'actes NoUniqueType=COD adoptés en 1ère et 2ème lecture par année"
    print question
    res_1={}
    res_2={}
    total={}
    for year in years_list:
        res_1[year]=0
        res_2[year]=0
        total[year]=0

    for act in ActIds.objects.filter(act__validated=2,  no_unique_type="COD", act__nb_lectures__isnull=False):
        year=str(act.act.releve_annee)
        total[year]+=1
        if act.act.nb_lectures==1:
            res_1[year]+=1
        elif act.act.nb_lectures==2:
            res_2[year]+=1
    print "res_1", res_1
    print "res_2", res_2
    print "total", total

    writer.writerow([question])
    writer.writerow(years_list_zero)
    row_1=["nb_lec=1"]
    row_2=["nb_lec=2"]
    for year in years_list:
        if res_1[year]==0:
            res_year=0
        else:
            res_year=round(float(res_1[year])*100/total[year],3)
        row_1.append(res_year)

        if res_2[year]==0:
            res_year=0
        else:
            res_year=round(float(res_2[year])*100/total[year],3)
        row_2.append(res_year)

    writer.writerow(row_1)
    writer.writerow(row_2)
    writer.writerow("")
    print ""


def q14():
    #durée moyenne des actes adoptés en 1e et en 2e lecture
    question="durée DureeTotaleDepuisPropCom moyenne des actes NoUniqueType=COD adoptés en 1ère et 2ème lecture par année"
    print question
    res_1={}
    res_2={}
    total={}
    for year in years_list:
        res_1[year]=0
        res_2[year]=0
        total[year]=0

    for act in ActIds.objects.filter(act__validated=2,  no_unique_type="COD", act__nb_lectures__isnull=False):
        year=str(act.act.releve_annee)
        total[year]+=1
        if act.act.nb_lectures==1:
            res_1[year]+=act.act.duree_tot_depuis_prop_com
        elif act.act.nb_lectures==2:
            res_2[year]+=act.act.duree_tot_depuis_prop_com
    print "res_1", res_1
    print "res_2", res_2
    print "total", total

    writer.writerow([question])
    writer.writerow(years_list_zero)
    row_1=["nb_lec=1"]
    row_2=["nb_lec=2"]
    for year in years_list:
        if res_1[year]==0:
            res_year=0
        else:
            res_year=round(float(res_1[year])/total[year],3)
        row_1.append(res_year)

        if res_2[year]==0:
            res_year=0
        else:
            res_year=round(float(res_2[year])/total[year],3)
        row_2.append(res_year)

    writer.writerow(row_1)
    writer.writerow(row_2)
    writer.writerow("")
    print ""


def q15():
    #DureeTotaleDepuisTransCons lorsque VotePublic=Y
    question="DureeTotaleDepuisTransCons lorsque VotePublic=Y par année"
    print question
    res={}
    for year in years_list:
        res[year]=[0,0]

    for act in Act.objects.filter(validated=2, vote_public=True, duree_tot_depuis_trans_cons__isnull=False):
        year=str(act.releve_annee)
        res[year][1]+=1
        res[year][0]+=act.duree_tot_depuis_trans_cons
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list)
    row=[]
    for year in years_list:
        if res[year][1]==0:
            res_year=0
        else:
            res_year=round(float(res[year][0])/res[year][1],3)
        row.append(res_year)
    writer.writerow(row)
    writer.writerow("")
    print ""


def q16():
    #nombre moyen de EPComAmdtTabled, EPComAmdtAdopt, EPAmdtTabled, EPAmdtAdopt
    question="nombre moyen de EPComAmdtTabled, EPComAmdtAdopt, EPAmdtTabled, EPAmdtAdopt par année"
    print question
    amdts={}
    amdts["EPComAmdtTabled"]="com_amdt_tabled"
    amdts["EPComAmdtAdopt"]="com_amdt_adopt"
    amdts["EPAmdtTabled"]="amdt_tabled"
    amdts["EPAmdtAdopt"]="amdt_adopt"
    res={}
    for amdt in amdts:
        res[amdt]={}
        for year in years_list:
            res[amdt][year]=[0,0]

    for act in Act.objects.filter(validated=2):
        year=str(act.releve_annee)
        for amdt in amdts:
            if getattr(act, amdts[amdt])!=None:
                res[amdt][year][1]+=1
                res[amdt][year][0]+=getattr(act, amdts[amdt])
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list_zero)
    for amdt in amdts:
        row=[amdt]
        for year in years_list:
            if res[amdt][year][1]==0:
                res_year=0
            else:
                res_year=round(float(res[amdt][year][0])/res[amdt][year][1],3)
            row.append(res_year)
        writer.writerow(row)
    writer.writerow("")
    print ""


def q17():
    #votes par année
    question="votes par année"
    print question
    res={}
    for year in years_list:
        res[year]= 0

    for act in Act.objects.filter(validated=2, vote_public=True):
        year=str(act.releve_annee)
        res[year]+=1
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list)
    row=[]
    for year in years_list:
        row.append(res[year])
    writer.writerow(row)
    writer.writerow("")
    print ""


def q18():
    #pourcentage AdoptCSContre=Y
    question="pourcentage AdoptCSContre=Y (parmi tous les actes) par année"
    print question
    res={}
    for year in years_list:
        res[year]= [0,0]

    for act in Act.objects.filter(validated=2):
        year=str(act.releve_annee)
        res[year][1]+=1
        #check if there is at least one country
        if act.adopt_cs_contre.exists():
            res[year][0]+=1
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list)
    row=[]

    for year in years_list:
        if res[year][1]==0:
            res_year=0
        else:
            res_year=round(float(res[year][0])*100/res[year][1],3)
        row.append(res_year)
    writer.writerow(row)
    writer.writerow("")
    print ""

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


def q20():
    #ombre d’actes pour lesquels on a eu au moins une discussion en points B par année
    question="Nombre d’actes pour lesquels on a eu au moins une discussion en points B par année"
    print question
    res={}
    for year in years_list:
        res[year]=0

    for act in Act.objects.filter(validated=2, nb_point_b__isnull=False):
        if act.nb_point_b>0:
            year=str(act.releve_annee)
            res[year]+=1
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list)
    row=[]
    for year in years_list:
        row.append(res[year])
    writer.writerow(row)
    writer.writerow("")
    print ""


def q21():
    #pourcentage de ministres presents (M) et de RP (CS ou CS_PR) par secteurs et par annee
    question="pourcentage de ministres presents (M) et de RP (CS ou CS_PR) par secteurs et par année"
    print question
    res={}
    for secteur in cs_list:
        res[secteur]={}
        for year in years_list:
            res[secteur][year]=0

    for act in Act.objects.filter(validated=2, code_sect_1__isnull=False):
        cs=act.code_sect_1.code_sect
        if cs[:5] in cs_2:
            res[cs[:5]][str(act.releve_annee)]+=1
        elif cs[:2] in cs_1:
            res[cs[:2]][str(act.releve_annee)]+=1
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list_zero)
    for cs in cs_list:
        row=[]
        row.append(cs)
        for year in years_list:
            row.append(res[cs][year])
        writer.writerow(row)
    writer.writerow("")
    print ""


class Command(NoArgsCommand):
    def handle(self, **options):

        nb_acts=Act.objects.filter(validated=2).count()
        writer.writerow(["Les requêtes suivantes sont recueillies a partir des "+ str(nb_acts)+ " actes validés"])
        writer.writerow([""])

        #proportion d’actes avec plusieurs codes sectoriels
        #~ q1()
        #ventilation par domaines
        #~ q2()
        #Frequence de la concordance Com/rapporteur/presidence du Conseil pour les 3 grandes familles (PPE ,PSE, ALDE)
        #~ q3()
        #Frequence de la concordance PE/Conseil
        #~ q4()
        #Fréquence de la concordance Commission/Conseil
        #~ q5()
        #Frequence de la concordance Commission/PE
        #~ q6()
        #durée moyenne des actes adoptés en 1e et en 2e lecture
        #~ q7()
        #durée moyenne entre transmission au conseil et adoption pour les actes qui ont donné lieu à un vote public
        #~ q8()


        #PAR ANNEE

        #production législative
        #~ q9()
        #ventilation par domaines
        #~ q10()
        #pourcentage de propositions modifiées par la Commission
        #~ q11()
        #~ #durée moyenne d’adoption
        #~ q12()
        #pourcentage d’actes adoptés en 1e et 2e lecture
        #~ q13()
        #durée moyenne des actes adoptés en 1e et en 2e lecture
        #~ q14()
        #durée moyenne entre transmission au conseil et adoption pour les actes qui ont donné lieu à un vote public
        #~ q15()
        #nombre moyen d’amendements déposés/adoptés
        #~ q16()
        #vote?
        #~ q17()
        #pourcentage AdoptCSContre=Y
        #~ q18()
        #~ #1/ %age AdoptCSContre=Y ET 1 EM.       2/%age AdoptCSContre=Y ET 2 EM.        3/%age AdoptCSContre=Y ET 3 EM
        #~ q19()
        #Durée moyenne des actes soumis à un vote
        #~ q20()
        #pourcentage de ministres presents (M) et de RP (CS ou CS_PR)? par annee ET par secteurs
        q21()

