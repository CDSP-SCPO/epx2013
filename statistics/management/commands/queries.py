#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.db import models
from act.models import Act, MinAttend, Status, NP
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


def get_cs(cs):
    if cs[:5] in cs_2:
        cs=cs[:5]
    elif cs[:2] in cs_1:
        cs=cs[:2]
    else:
        cs=None
    return cs




def init_year_nb_lec(nb_lec=2, total=False):
    res={}
    total_year={}
    for year in years_list:
        res[year]={}
        if total:
            total_year[year]=0
        for i in range(1, nb_lec+1):
            if total:
                temp=0
            else:
                temp=[0,0]
            res[year][i]=temp
    if total:
        return res, total_year
    return res


def init_cs_year(nb=1, total=False):
    res={}
    total_year={}
    for secteur in cs_list:
        res[secteur]={}
        for year in years_list:
            if nb==1:
                temp=0
            else:
                temp=[0,0]
            if total:
                total_year[year]=temp
            res[secteur][year]=temp
            
    if total:
        return res, total_year
    else:
        return res


def init_cs_year_nb_lec(nb_lec=2, total=False):
    res={}
    total_year={}
    for cs in cs_list:
        res[cs]={}
        for year in years_list:
            res[cs][year]={}
            for i in range(nb_lec):
                if total:
                    temp=0
                else:
                    temp=[0,0]
                res[cs][year][i]=temp
    if total:
        for year in years_list:
            total_year[year]=[0]*nb_lec
        return res, total_year
    else:
        return res




def get_year_nb_lec(res, total_year=False, variable=1):
    for act in ActIds.objects.filter(src="index", act__validated=2,  no_unique_type="COD", act__nb_lectures__isnull=False):
        year=str(act.act.releve_annee)
        nb_lec=act.act.nb_lectures
        if nb_lec<3:
            if variable!=1:
                temp=getattr(act.act, variable)
            else:
                temp=1
            if not total_year:
                res[year][nb_lec][1]+=1
                res[year][nb_lec][0]+=temp
            else:
                total_year[year]+=1
                res[year][nb_lec]+=temp
    print "res", res
    if not total_year:
        return res
    print "total", total_year
    return res, total_year


def get_cs_year(res, variable=1):
    for act in Act.objects.filter(validated=2):
        if variable==1 or getattr(act, variable)!=None:
            cs=get_cs(act.code_sect_1.code_sect)
            year=str(act.releve_annee)
            res[cs][year][1]+=1
            value=1
            if variable!=1:
                value=getattr(act, variable)
            res[cs][year][0]+=value
    print "res", res
    return res


def get_cs_year_nb_lec(res, total_year=False, variable=1):
    for act in ActIds.objects.filter(src="index", act__validated=2,  no_unique_type="COD", act__nb_lectures__isnull=False):
        year=str(act.act.releve_annee)
        nb_lec=act.act.nb_lectures
        if nb_lec<3:
            nb_lec=nb_lec-1
            cs=get_cs(act.act.code_sect_1.code_sect)
            if variable!=1:
                temp=getattr(act.act, variable)
            else:
                temp=1
            if not total_year:
                res[cs][year][nb_lec][1]+=1
                res[cs][year][nb_lec][0]+=temp
            else:
                total_year[year][nb_lec]+=1
                res[cs][year][nb_lec]+=temp
    print "res", res
    if not total_year:
        return res
    print "total", total_year
    return res, total_year




def write_year_nb_lec(question, res, total_year=False, nb_lec=2, percent=1):
    writer.writerow([question])
    writer.writerow(years_list_zero)
    for nb in range(1, nb_lec+1):
        row=["nb_lec="+str(nb)]
        for year in years_list:
            if not total_year:
                if res[year][nb][0]==0:
                    res_year=0
                else:
                    res_year=round(float(res[year][nb][0])*percent/res[year][nb][1],3)
            else:
                if res[year][nb]==0:
                    res_year=0
                else:
                    res_year=round(float(res[year][nb])*percent/total_year[year],3)
            row.append(res_year)
        writer.writerow(row)
    writer.writerow("")
    print ""


def write_cs_year(question, res, total_year=False, percent=1, nb=1):
    writer.writerow([question])
    writer.writerow(years_list_zero)
    for cs in cs_list:
        row=[cs]
        for year in years_list:
            if total_year!=False:
                if res[cs][year]==0:
                    res_year=0
                else:
                    res_year=round(float(res[cs][year])*percent/total_year[year],3)
            else:
                if nb==1:
                    res_year=res[cs][year]
                elif nb==2:
                    if res[cs][year][0]==0:
                        res_year=0
                    else:
                        res_year=round(float(res[cs][year][0])*percent/res[cs][year][1],3)
            row.append(res_year)
        writer.writerow(row)
    writer.writerow("")
    print ""


def write_cs_year_nb_lec(question, res, total_year=False, nb_lec=2, percent=1):
    writer.writerow([question])
    writer.writerow(years_list_zero)
    for cs in cs_list:
        row=[cs]
        for year in years_list:
            res_year=""
            for nb in range(nb_lec):
                if not total_year:
                    if res[cs][year][nb][0]==0:
                        temp=0
                    else:
                        temp=round(float(res[cs][year][nb][0])*percent/res[cs][year][nb][1],3)
                else:
                    if res[cs][year][nb]==0:
                        temp=0
                    else:
                        temp=round(float(res[cs][year][nb])*percent/total_year[year][nb],3)
                res_year+=str(temp)+ " / "
            row.append(res_year[:-3])
        writer.writerow(row)
    writer.writerow("")
    print ""




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
        cs=get_cs(act.code_sect_1.code_sect)
        res[cs]+=1
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
    lec_1=ActIds.objects.filter(src="index", act__validated=2, no_unique_type="COD", act__nb_lectures=1)
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
    writer.writerow(years_list)
    writer.writerow(res)
    writer.writerow("")
    print ""


def q10():
    #production legislative par domaine et par année
    question="production legislative par domaine et par année"
    print question
    res=init_cs_year()

    for act in Act.objects.filter(validated=2, code_sect_1__isnull=False):
        cs=get_cs(act.code_sect_1.code_sect)
        res[cs][str(act.releve_annee)]+=1
    print "res", res

    write_cs_year(question, res)
   

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
    nb_lec=2
    res, total_year=init_year_nb_lec(total=True)

    res, total_year=get_year_nb_lec(res, total_year=total_year)
   
    write_year_nb_lec(question, res, total_year=total_year, percent=100)


def q14():
    #durée moyenne des actes adoptés en 1e et en 2e lecture
    question="durée DureeTotaleDepuisPropCom moyenne des actes NoUniqueType=COD adoptés en 1ère et 2ème lecture par année"
    print question
    nb_lec=2
    res=init_year_nb_lec()

    res=get_year_nb_lec(res, variable="duree_tot_depuis_prop_com")

    write_year_nb_lec(question, res)


def q15():
    #DureeTotaleDepuisTransCons lorsque VotePublic=Y
    question="DureeTotaleDepuisTransCons moyenne lorsque VotePublic=Y par année"
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
    #DureeTotaleDepuisPropCom lorsque VotePublic=Y
    question="DureeTotaleDepuisPropCom lorsque VotePublic=Y"
    print question
    res={}
    for year in years_list:
        res[year]=[0,0]

    for act in Act.objects.filter(validated=2, vote_public=True, duree_tot_depuis_prop_com__isnull=False):
        res[str(act.releve_annee)][1]+=1
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


def q21():
    #Nombre d’actes pour lesquels on a eu au moins une discussion en points B par année
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


def q22():
    #pourcentage de ministres presents (M) et de RP (CS ou CS_PR) par secteurs et par annee
    question="pourcentage de ministres presents (M) et de RP (CS ou CS_PR) par année"
    print question
    res={}
    total_year={}
    statuses={}
    statuses["M"]=0
    statuses["CS"]=1
    statuses["CS_PR"]=1
    for status in statuses:
        res[statuses[status]]={}
        for year in years_list:
            res[statuses[status]][year]=0
    for year in years_list:
        total_year[year]=0
  
    for act in MinAttend.objects.filter(act__validated=2):
        status=Status.objects.get(verbatim=act.verbatim, country=act.country).status
        if status not in ["NA", "AB"]:
            year=str(act.act.releve_annee)
            total_year[year]+=1
            res[statuses[status]][year]+=1
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list_zero)
    for index in range(2):
        if index==0:
            row=["M"]
        else:
            row=["RP"]
        for year in years_list:
            if res[index][year]==0:
                res_year=0
            else:
                res_year=round(float(res[index][year])*100/total_year[year],3)
            row.append(res_year)
        writer.writerow(row)
    writer.writerow("")
    print ""


def q23():
    #TODO
    #Frequence de la concordance Com/rapporteur/presidence du Conseil pour les 3 grandes familles (PPE ,PSE, ALDE)
    question="Frequence de la concordance Com/rapporteur/presidence du Conseil pour les 3 grandes familles (PPE ,PSE, ALDE) par année"
    print question

    writer.writerow([question])
    writer.writerow("")
    print ""


def q24():
    #TODO
    #Frequence de la concordance PE/Conseil
    question="Frequence de la concordance PE/Conseil par année"
    print question

    writer.writerow([question])
    writer.writerow("")
    print ""


def q25():
    #TODO
    #Fréquence de la concordance Commission/Conseil
    question="Frequence de la concordance Commission/Conseil par année"
    print question

    writer.writerow([question])
    writer.writerow("")
    print ""


def q26():
    #TODO
    #Frequence de la concordance Commission/PE
    question="Frequence de la concordance Commission/PE par année"
    print question

    writer.writerow([question])
    writer.writerow("")
    print ""


def q27():
    #pourcentage par annee de propositions modifiées par la Commission suivant le secteur
    question="pourcentage des propositions modifiées par la Commission par secteur, en fonction des années"
    print question
    res, total_year=init_cs_year(total=True)

    for act in Act.objects.filter(validated=2, code_sect_1__isnull=False):
        cs=get_cs(act.code_sect_1.code_sect)
        year=str(act.releve_annee)
        if act.modif_propos:
            total_year[year]+=1
            res[cs][year]+=1
    print "res", res

    write_cs_year(question, res, total_year=total_year, percent=100)

    
def q28():
    #durée moyenne d’adoption par secteur, en fonction de l'année
    question="DureeTotaleDepuisPropCom moyenne par secteur, en fonction de l'année"
    print question
    res=init_cs_year(nb=2)

    res=get_cs_year(res, variable="duree_tot_depuis_prop_com")
    
    write_cs_year(question, res, percent=1, nb=2)


def q29():
    #Pourcentage d'actes NoUniqueType=COD adoptés en 1ère et 2ème lecture.
    question="Pourcentage d'actes NoUniqueType=COD adoptés en 1ère et 2ème lecture par secteur, en fonction de l'année (1ère lecture / 2ème lecture)"
    print question
    nb_lec=2
    res, total_year=init_cs_year_nb_lec(total=True)

    res, total_year=get_cs_year_nb_lec(res, total_year=total_year)
   
    write_cs_year_nb_lec(question, res, total_year=total_year, percent=100)


def q30():
    #durée moyenne des actes adoptés en 1e et en 2e lecture
    question="durée DureeTotaleDepuisPropCom moyenne des actes NoUniqueType=COD adoptés en 1ère et 2ème lecture par secteur, en fonction de l'année (1ère lecture / 2ème lecture)"
    print question
    nb_lec=2
    res=init_cs_year_nb_lec()

    res=get_cs_year_nb_lec(res, variable="duree_tot_depuis_prop_com")

    write_cs_year_nb_lec(question, res)
    

def q31():
    #DureeTotaleDepuisTransCons lorsque VotePublic=Y
    question="DureeTotaleDepuisTransCons moyenne lorsque VotePublic=Y par secteur, en fonction de l'année"
    print question
    res=init_cs_year(nb=2)
    
    res=get_cs_year(res, variable="duree_tot_depuis_prop_com")

    for act in Act.objects.filter(validated=2, vote_public=True, duree_tot_depuis_trans_cons__isnull=False):
        cs=get_cs(act.code_sect_1.code_sect)
        year=str(act.releve_annee)
        res[cs][year][1]+=1
        res[cs][year][0]+=act.duree_tot_depuis_trans_cons
    print "res", res

    write_cs_year(question, res, nb=2)


def q32(display_name, variable_name):
    #nombre moyen de EPComAmdtTabled, EPComAmdtAdopt, EPAmdtTabled, EPAmdtAdopt
    question="nombre moyen de " +display_name+ " par secteur, en fonction de l'année"
    print question
    res=init_cs_year(nb=2)
    
    res=get_cs_year(res, variable=variable_name)

    write_cs_year(question, res, nb=2)


def q33():
    #votes par année
    question="votes par secteur, en fonction de l'année"
    print question
    res=init_cs_year()

    for act in Act.objects.filter(validated=2, vote_public=True):
        cs=get_cs(act.code_sect_1.code_sect)
        year=str(act.releve_annee)
        res[cs][year]+=1
    print "res", res

    write_cs_year(question, res)


def q34():
    #pourcentage AdoptCSContre=Y
    question="pourcentage AdoptCSContre=Y (parmi les actes du même secteur et de la même année) par secteur, en fonction de l'année"
    print question
    res=init_cs_year(nb=2)
    
    for act in Act.objects.filter(validated=2):
        cs=get_cs(act.code_sect_1.code_sect)
        year=str(act.releve_annee)
        res[cs][year][1]+=1
        #check if there is at least one country
        if act.adopt_cs_contre.exists():
            res[cs][year][0]+=1
    print "res", res

    write_cs_year(question, res, percent=100, nb=2)


def q35(nb_em):
    #1/ %age AdoptCSContre=Y ET 1 EM.       2/%age AdoptCSContre=Y ET 2 EM.        3/%age AdoptCSContre=Y ET 3 EM
    question="pourcentage AdoptCSContre=Y (parmi les actes du même secteur et de la même année) ET "+str(nb_em)+" EM par secteur, en fonction de l'année"
    print question
    res=init_cs_year(nb=2)

    for act in Act.objects.filter(validated=2):
        nb=len(act.adopt_cs_contre.all())
        if nb>0:
            cs=get_cs(act.code_sect_1.code_sect)
            year=str(act.releve_annee)
            res[cs][year][1]+=1
            if nb==nb_em:
                res[cs][year][0]+=1
    print "res", res

    write_cs_year(question, res, percent=100, nb=2)


def q36():
    #DureeTotaleDepuisPropCom lorsque VotePublic=Y
    question="DureeTotaleDepuisPropCom lorsque VotePublic=Y par secteur, en fonction de l'année"
    print question
    res=init_cs_year(nb=2)
    
    for act in Act.objects.filter(validated=2, vote_public=True, duree_tot_depuis_prop_com__isnull=False):
        cs=get_cs(act.code_sect_1.code_sect)
        year=str(act.releve_annee)
        res[cs][str(act.releve_annee)][1]+=1
        res[cs][str(act.releve_annee)][0]+=act.duree_tot_depuis_prop_com
    print "res", res

    write_cs_year(question, res, nb=2)
    

def q37():
    #Nombre d’actes pour lesquels on a eu au moins une discussion en points B par année
    question="Nombre d’actes pour lesquels on a eu au moins une discussion en points B par secteur, en fonction de l'année"
    print question
    res=init_cs_year()

    for act in Act.objects.filter(validated=2, nb_point_b__isnull=False):
        if act.nb_point_b>0:
            cs=get_cs(act.code_sect_1.code_sect)
            year=str(act.releve_annee)
            res[cs][year]+=1
    print "res", res

    write_cs_year(question, res)
    

def q38():
    #pourcentage de ministres presents (M) et de RP (CS ou CS_PR) par secteurs et par annee
    question="pourcentage de ministres presents (M) et de RP (CS ou CS_PR) selon les secteurs, par année (premier chiffre : pourcentage de M dans l'année ; deuxième chiffre : pourcentage de CS ou CS_PR dans l'année)"
    print question
    res={}
    total_year={}
    statuses={}
    statuses["M"]=0
    statuses["CS"]=1
    statuses["CS_PR"]=1
    
    res, total_year=init_cs_year(nb=2, total=True)
  
    for act in MinAttend.objects.filter(act__validated=2):
        status=Status.objects.get(verbatim=act.verbatim, country=act.country).status
        if status not in ["NA", "AB"]:
            cs=get_cs(act.act.code_sect_1.code_sect)
            year=str(act.act.releve_annee)
            total_year[year][statuses[status]]+=1
            res[cs][year][statuses[status]]+=1
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list_zero)
    for cs in cs_list:
        row=[cs]
        for year in years_list:
            res_year=""
            for index in range(2):
                if res[cs][year][index]==0:
                    temp=0
                else:
                    temp=round(float(res[cs][year][index])*100/total_year[year][index],3)
                res_year+=str(temp)+ " / "
            row.append(res_year[:-3])
        writer.writerow(row)
    writer.writerow("")
    print ""


def q39():
    #TODO
    #Frequence de la concordance Com/rapporteur/presidence du Conseil pour les 3 grandes familles (PPE ,PSE, ALDE)
    question="Frequence de la concordance Com/rapporteur/presidence du Conseil pour les 3 grandes familles (PPE ,PSE, ALDE) par année"
    print question

    writer.writerow([question])
    writer.writerow("")
    print ""


def q40():
    #TODO
    #Frequence de la concordance PE/Conseil
    question="Frequence de la concordance PE/Conseil par année"
    print question

    writer.writerow([question])
    writer.writerow("")
    print ""


def q41():
    #TODO
    #Fréquence de la concordance Commission/Conseil
    question="Frequence de la concordance Commission/Conseil par année"
    print question

    writer.writerow([question])
    writer.writerow("")
    print ""


def q42():
    #TODO
    #Frequence de la concordance Commission/PE
    question="Frequence de la concordance Commission/PE par année"
    print question

    writer.writerow([question])
    writer.writerow("")
    print ""
    

def q43():
    #période 2010-2012 : %age d’actes ayant fait l’objet d’ interventions des parlements nationaux
    question="période 2010-2012 : %age d’actes ayant fait l’objet d’ interventions des parlements nationaux"
    print question
    res={}
    years_list_np=[n for n in range(2010, 2013)]
    for year in years_list_np:
        res[str(year)]=[0,0]
    
    for act in Act.objects.filter(validated=2, releve_annee__in=years_list_np):
        year=str(act.releve_annee)
        res[year][1]+=1
        if act.np_set.exists():
            res[year][0]+=1
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list_np)
    row=[]
    for year in years_list_np:
        year=str(year)
        if res[year][0]==0:
            res_year=0
        else:
            res_year=round(float(res[year][0])*100/res[year][1],3)
        row.append(res_year)
    writer.writerow(row)
    writer.writerow("")
    print ""
    
    
class Command(NoArgsCommand):
    def handle(self, **options):

        nb_acts=Act.objects.filter(validated=2).count()
        writer.writerow(["Les requêtes suivantes sont recueillies a partir des "+ str(nb_acts)+ " actes validés"])
        writer.writerow([""])

        #proportion d’actes avec plusieurs codes sectoriels
        q1()
        #~ #ventilation par domaines
        q2()
        #~ #Frequence de la concordance Com/rapporteur/presidence du Conseil pour les 3 grandes familles (PPE ,PSE, ALDE)
        q3()
        #~ #Frequence de la concordance PE/Conseil
        q4()
        #~ #Fréquence de la concordance Commission/Conseil
        q5()
        #~ #Frequence de la concordance Commission/PE
        q6()
        #~ #durée moyenne des actes adoptés en 1e et en 2e lecture
        q7()
        #~ #durée moyenne entre transmission au conseil et adoption pour les actes qui ont donné lieu à un vote public
        q8()
#~ 
#~ 
        #~ #PAR ANNEE
#~ 
        #~ #production législative
        q9()
        #~ #ventilation par domaines
        q10()
        #~ #pourcentage de propositions modifiées par la Commission
        q11()
        #durée moyenne d’adoption
        q12()
        #~ #pourcentage d’actes adoptés en 1e et 2e lecture
        q13()
        #~ #durée moyenne des actes adoptés en 1e et en 2e lecture
        q14()
        #~ #durée moyenne entre transmission au conseil et adoption pour les actes qui ont donné lieu à un vote public
        q15()
        #~ #nombre moyen d’amendements déposés/adoptés
        q16()
        #~ #vote?
        q17()
        #~ #pourcentage AdoptCSContre=Y
        q18()
        #1/ %age AdoptCSContre=Y ET 1 EM.       2/%age AdoptCSContre=Y ET 2 EM.        3/%age AdoptCSContre=Y ET 3 EM
        q19()
        #~ #Durée moyenne des actes soumis à un vote
        q20()
        #~ #Nombre d’actes pour lesquels on a eu au moins une discussion en points B
        q21()
        #~ #pourcentage de ministres presents (M) et de RP (CS ou CS_PR)? par annee ET par secteurs
        q22()
         #~ #Frequence de la concordance Com/rapporteur/presidence du Conseil pour les 3 grandes familles (PPE ,PSE, ALDE)
        q23()
        #~ #Frequence de la concordance PE/Conseil
        q24()
        #~ #Fréquence de la concordance Commission/Conseil
        q25()
        #~ #Frequence de la concordance Commission/PE
        q26()
#~ 
#~ 
        #~ #PAR SECTEUR ET PAR ANNEE
#~ 
        #~ #% age de propositions modifiées par la Commission
        #~ #q27()
        #~ #durée moyenne d’adoption
        #~ #q28()
        #~ #% age d’actes adoptés en 1e et 2e lecture
        q29()
        #~ #durée moyenne des actes adoptés en 1e et en 2e lecture
        q30()
        #~ #durée moyenne entre transmission au conseil et adoption pour les actes qui ont donné lieu à un vote public
        q31()
        #~ #nombre moyen d’amendements déposés/adoptés
        q32("EPComAmdtTabled", "com_amdt_tabled")
        q32("EPComAmdtAdopt", "com_amdt_adopt")
        q32("EPAmdtTabled", "amdt_tabled")
        q32("EPAmdtAdopt", "amdt_adopt")
        #~ #Vote?
        #~ #q33()
        #~ #%age de votes négatifs par Etat membre
        q34()
        #~ #% age de votes négatifs isolés, de 2 Etats, de 3 Etats
        q35(1)
        q35(2)
        q35(3)
        #~ #Durée moyenne des actes soumis à un vote
        q36()
        #~ #Nombre d’actes pour lesquels on a eu au moins une discussion en points B
        q37()
        #~ #pourcentage de ministres presents (M) et de RP (CS ou CS_PR)? par annee ET par secteurs
        q38()
         #~ #Frequence de la concordance Com/rapporteur/presidence du Conseil pour les 3 grandes familles (PPE ,PSE, ALDE)
        q39()
        #~ #Frequence de la concordance PE/Conseil
        q40()
        #~ #Fréquence de la concordance Commission/Conseil
        q41()
        #~ #Frequence de la concordance Commission/PE
        q42()
        
        
        #période 2010-2012 : %age d’actes ayant fait l’objet d’ interventions des parlements nationaux
        q43()
