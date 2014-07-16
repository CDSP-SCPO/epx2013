#-*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.db import models
from act.models import Act, MinAttend, Status, NP, PartyFamily, Country
from act_ids.models import ActIds
from django.db.models import Count
import csv
from django.conf import settings
from collections import OrderedDict
import datetime

#display decimals with comma
#DOES NOT WORK
import locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
#~ print locale.getlocale()
#~ print locale.format("%10.2f", 0.123) 


#year and code sectoriel lists
countries=Country.objects.values_list("country_code", flat=True)
years_list=[str(n) for n in range(1996, 2013)]
years_list_zero=list(years_list)
years_list_zero.insert(0, "")
cs_list=[str(n) for n in range(1, 21)]
for index in range(len(cs_list)):
    if len(cs_list[index])==1:
        cs_list[index]="0"+cs_list[index]

#write results in file
path=settings.PROJECT_ROOT+'/statistics/management/commands/queries.csv'
#~ writer=csv.writer(open(path, 'w'), delimiter=";")
writer=csv.writer(open(path, 'w'))


def get_cs(cs):
    if cs[:2] in cs_list:
        cs=cs[:2]
    else:
        cs=None
    return cs



def init_year():
    res={}
    for year in years_list:
        res[year]=[0,0]
    return res


def init_res():
    res={}
    for cs in cs_list:
        res[cs]=[0,0]
    return res


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


def init_cs_year(nb=1, total=False, amdt=False):
    #use nb=2 to compute the percentage for each cell
    #use total=True to compute the percentage of each cell compared to the total of the year
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
                if amdt==True:
                    total_year[year]=0
                else:
                    total_year[year]=temp
            res[secteur][year]=temp
            #ATTENTION! If nb=2 and total=True, the same list temp=[0,0] is used for total_year and res -> MUST USE A COPY OF THE LIST
            
    if total:
        return res, total_year
    return res


def init_cs_year_nb_lec(nb_lec=2, total=False):
    res={}
    total_year={}
    for cs in cs_list:
        res[cs]={}
        for year in years_list:
            res[cs][year]={}
            for i in range(1, nb_lec+1):
                res[cs][year][i]=0
    if total:
        for year in years_list:
            total_year[year]=[0]*nb_lec
        return res, total_year
    else:
        return res



def get_by_year(res, variable):
    for act in Act.objects.filter(validated=2):
        field=getattr(act, variable)
        if field != None:
            year=str(act.releve_annee)
            res[year][0]+=field
            res[year][1]+=1
    print "res", res
    return res


def get_by_cs(res, variable):
    for act in Act.objects.filter(validated=2):
        field=getattr(act, variable)
        if field != None:
            for nb in range(1,5):
                code_sect=getattr(act, "code_sect_"+str(nb))
                if code_sect!=None:
                    cs=get_cs(code_sect.code_sect)
                    res[cs][0]+=field
                    res[cs][1]+=1
    print "res", res
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
                res[year][nb_lec]+=temp
        #take into account nb_lec=3
        if total_year!=False:
            total_year[year]+=1
    print "res", res
    if not total_year:
        return res
    print "total", total_year
    return res, total_year
    

def get_by_cs_year(res, variable=1, total_year=False):
    for act in Act.objects.filter(validated=2):
        field=getattr(act, variable)
        if variable==1 or field!=None:
            for nb in range(1,5):
                code_sect=getattr(act, "code_sect_"+str(nb))
                if code_sect!=None:
                    cs=get_cs(code_sect.code_sect)
                    year=str(act.releve_annee)
                    res[cs][year][1]+=1
                    value=1
                    if variable!=1:
                        value=field
                    res[cs][year][0]+=value
                    if total_year:
                        #~ print "total_year", total_year
                        total_year[year]+=value
    print "res", res
    if total_year:
        return res, total_year
    return res


def get_by_cs_year_nb_lec(res, total_year=False, variable=1):
    for act in ActIds.objects.filter(src="index", act__validated=2,  no_unique_type="COD", act__nb_lectures__isnull=False):
        year=str(act.act.releve_annee)
        nb_lec=act.act.nb_lectures
        if nb_lec<3 and nb_lec>0 :
            
            for nb in range(1,5):
                code_sect=getattr(act.act, "code_sect_"+str(nb))
                if code_sect!=None:
                    cs=get_cs(code_sect.code_sect)
            
                    if variable!=1:
                        temp=getattr(act.act, variable)
                    else:
                        temp=1
                    if not total_year:
                        #~ print "nb_lec", nb_lec
                        #~ print "res", res
                        res[cs][year][nb_lec]+=1
                    else:
                        total_year[year][nb_lec]+=1
                        res[cs][year][nb_lec]+=temp
    print "res", res
    if not total_year:
        return res
    print "total", total_year
    return res, total_year



def write_year(question, res, nb_var=1):
    writer.writerow([question])
    row=[]
    if nb_var==1:
        #one line to display
        writer.writerow(years_list)
        for year in years_list:  
            if res[year][0]==0:
                temp=0
            else:
                temp=round(float(res[year][0])/res[year][1], 3) 
            row.append(temp)
        writer.writerow(row)
    else:
        #nb=2, display two lines with two variables
        writer.writerow(years_list_zero)
        for nb in range(nb_var):
            if nb==0:
                row=["1 BJ"]
            else:
                row=["Plusieurs BJ"]
            
            for year in years_list:
                if res[year][nb]==0:
                    temp=0
                else:
                    total=res[year][0]+res[year][1]
                    temp=round(float(res[year][nb])*100/total, 3) 
                row.append(temp)
            writer.writerow(row)
        
    writer.writerow("")
    print ""


def write_cs(question, res):
    writer.writerow([question])
    writer.writerow(cs_list)
    row=[]
    for cs in cs_list:    
        if res[cs][0]==0:
            temp=0
        else:
            temp=round(float(res[cs][0])/res[cs][1], 3)
        row.append(temp)
    writer.writerow(row)
    writer.writerow("")
    print ""


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


def write_cs_year(question, res, total_year=False, percent=1, nb=1, amdt=False):
    writer.writerow([question])
    writer.writerow(years_list_zero)
    for cs in cs_list:
        row=[cs]
        for year in years_list:
            if total_year:
                if amdt:
                    #display sum of each year for amdt
                    res_year=res[cs][year][0]
                else:
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
    #write sum each column
    if amdt:
        row=["Total"]
        for year in years_list:
            row.append(total_year[year])
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
            
            if not total_year:
                if res[cs][year][1]==0 and res[cs][year][2]==0:
                    res[cs][year][1]=0
                    res[cs][year][2]=0
                elif res[cs][year][1]==0:
                    res[cs][year][2]=100
                elif res[cs][year][2]==0:
                    res[cs][year][1]=100
                else:
                    #both 1st and 2 lecture are different from zero
                    total=res[cs][year][1]+res[cs][year][2]
                    res[cs][year][1]=round(float(res[cs][year][1])*percent/total,3)
                    res[cs][year][2]=round(float(res[cs][year][2])*percent/total,3)
                
            row.append(str(res[cs][year][1]) + "/" + str(res[cs][year][2]))
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

    for act in Act.objects.filter(validated=2):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
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
    

def concordance_generale(resp_group, rapp_group):
    question="Concordance PartyFamilyResp et GroupePolitiqueRapporteur ("+resp_group+") : Pourcentage sur la periode 1996-2012"
    print question
    
    res=[0,0]
    for act in Act.objects.filter(validated=2):
        res[1]+=1
        resps=[]
        rapps=[]
        
        for i in range(1, 3):
            i=str(i)
            resp=getattr(act, "resp_"+i)
            rapp=getattr(act, "rapp_"+i)
            if resp!=None:
                resps.append(resp)
            if rapp!=None:
                rapps.append(rapp)
        
        if (len(resps)>0) and (len(rapps)>0):
            same=False
            for resp in resps:
                if same:
                    break
                for rapp in rapps:
                    if PartyFamily.objects.get(country=resp.country, party=resp.party).party_family.strip()==resp_group and rapp.party.party.strip() in rapp_group:
                        res[0]+=1
                        same=True
                        break
    
    print "res"
    print res
    #duree moyenne
    res[0]=round(float(res[0])*100/res[1], 3)

    writer.writerow([question])
    writer.writerow([res[0]])
    writer.writerow("")
    print ""


def q3():
    #pourcentage des actes quand PartyFamilyResp1 OU PartyFamilyResp2='Social Democracy' ET GroupePolitiqueRapporteur1 OU GroupePolitiqueRapporteur2= 'Progressive Alliance of Socialists and Democrats' OU 'Party of European Socialists' OU 'Socialist Group in the European Parliament »
    concordance_generale("Social Democracy", ["Progressive Alliance of Socialists and Democrats", "Party of European Socialists", "Socialist Group in the European Parliament"])


def q4():
    #pourcentage des actes quand PartyFamilyResp1 OU PartyFamilyResp2='Conservative/Christian Democracy' ET GroupePolitiqueRapporteur1 OU GroupePolitiqueRapporteur2= 'Progressive Alliance of Socialists and Democrats' OU 'Party of European Socialists' OU 'Socialist Group in the European Parliament »
    concordance_generale("Conservative/Christian Democracy", [u"European People's Party (Christian Democrats)", u"EPP - European People's Party (Christian Democrats)", u"European People's Party (Christian Democrats) and European Democrats"])


def q7():
    #duree moyenne des actes adoptes en 1e et en 2e lecture
    #1/ DureeTotaleDepuisPropCom lorsque NoUniqueType=COD ET NombreLectures=1.
    #2/ DureeTotaleDepuisPropCom lorsque NoUniqueType=COD ET NombreLectures=2
    question="duree moyenne des actes adoptes en 1e et en 2e lecture"
    print question
    res_1=0
    res_2=0

    #first lecture
    lec_1=ActIds.objects.filter(src="index", act__validated=2, no_unique_type="COD", act__nb_lectures=1, act__duree_tot_depuis_prop_com__isnull=False)
    for lec in lec_1:
        res_1+=lec.act.duree_tot_depuis_prop_com
    res_1=round(float(res_1)/lec_1.count(), 3)
    print "res_1", res_1

    #second lecture
    lec_2=ActIds.objects.filter(src="index", act__validated=2, no_unique_type="COD", act__nb_lectures=2, act__duree_tot_depuis_prop_com__isnull=False)
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

    for act in Act.objects.filter(validated=2):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
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


def concordance_annee(resp_group, rapp_group):
    question="Concordance PartyFamilyResp et GroupePolitiqueRapporteur ("+resp_group+") : Pourcentage par année"
    print question
    res={}
    for year in years_list:
        res[year]=[0,0]
        
    for act in Act.objects.filter(validated=2):
        year=str(act.releve_annee)
        res[year][1]+=1
        resps=[]
        rapps=[]
        
        for i in range(1, 3):
            i=str(i)
            resp=getattr(act, "resp_"+i)
            rapp=getattr(act, "rapp_"+i)
            if resp!=None:
                resps.append(resp)
            if rapp!=None:
                rapps.append(rapp)
        
        if (len(resps)>0) and (len(rapps)>0):
            same=False
            for resp in resps:
                if same:
                    break
                for rapp in rapps:
                    if PartyFamily.objects.get(country=resp.country, party=resp.party).party_family.strip()==resp_group and rapp.party.party.strip() in rapp_group:
                        res[year][0]+=1
                        same=True
                        break
    
    print "res"
    print res
    #duree moyenne
    for year in years_list:
        if res[year][0]!=0:
            res[year][0]=round(float(res[year][0])*100/res[year][1], 3)

    writer.writerow([question])
    writer.writerow(years_list)
    row=[]
    for year in years_list:
        row.append(res[year][0])
    writer.writerow(row)
    writer.writerow("")
    print ""


def q23():
    #pourcentage des actes quand PartyFamilyResp1 OU PartyFamilyResp2='Social Democracy' ET GroupePolitiqueRapporteur1 OU GroupePolitiqueRapporteur2= 'Progressive Alliance of Socialists and Democrats' OU 'Party of European Socialists' OU 'Socialist Group in the European Parliament »
    concordance_annee("Social Democracy", ["Progressive Alliance of Socialists and Democrats", "Party of European Socialists", "Socialist Group in the European Parliament"])


def q24():
    #pourcentage des actes quand PartyFamilyResp1 OU PartyFamilyResp2='Conservative/Christian Democracy' ET GroupePolitiqueRapporteur1 OU GroupePolitiqueRapporteur2= 'Progressive Alliance of Socialists and Democrats' OU 'Party of European Socialists' OU 'Socialist Group in the European Parliament »
    concordance_annee("Conservative/Christian Democracy", [u"European People's Party (Christian Democrats)", u"EPP - European People's Party (Christian Democrats)", u"European People's Party (Christian Democrats) and European Democrats"])


def q27():
    #pourcentage par annee de propositions modifiées par la Commission suivant le secteur
    question="pourcentage des propositions modifiées par la Commission par secteur, en fonction de l'année"
    print question
    res, total_year=init_cs_year(total=True)

    for act in Act.objects.filter(validated=2):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
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
    res=get_by_cs_year(res, variable="duree_tot_depuis_prop_com")
    write_cs_year(question, res, percent=1, nb=2)


def q29():
    #Pourcentage d'actes NoUniqueType=COD adoptés en 1ère et 2ème lecture.
    question="Pourcentage d'actes NoUniqueType=COD adoptés en 1ère et 2ème lecture parmi les actes du même secteur et de la même année (% 1ère lecture / % 2ème lecture)"
    print question
    nb_lec=2
    res=init_cs_year_nb_lec()
    res=get_by_cs_year_nb_lec(res)
    write_cs_year_nb_lec(question, res, percent=100)


def q30():
    #durée moyenne des actes adoptés en 1e et en 2e lecture
    question="durée DureeTotaleDepuisPropCom moyenne des actes NoUniqueType=COD adoptés en 1ère et 2ème lecture par secteur, en fonction de l'année (1ère lecture / 2ème lecture)"
    print question
    nb_lec=2
    res=init_cs_year_nb_lec()
    res=get_by_cs_year_nb_lec(res, variable="duree_tot_depuis_prop_com")
    write_cs_year_nb_lec(question, res)
    

def q31():
    #DureeTotaleDepuisTransCons lorsque VotePublic=Y
    question="DureeTotaleDepuisTransCons moyenne lorsque VotePublic=Y par secteur, en fonction de l'année"
    print question
    res=init_cs_year(nb=2)

    for act in Act.objects.filter(validated=2, vote_public=True, duree_tot_depuis_trans_cons__isnull=False):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)
                res[cs][year][1]+=1
                res[cs][year][0]+=act.duree_tot_depuis_trans_cons
    print "res", res

    write_cs_year(question, res, nb=2)


def q32(display_name, variable_name):
    #nombre moyen de EPComAmdtTabled, EPComAmdtAdopt, EPAmdtTabled, EPAmdtAdopt
    question="nombre moyen de " +display_name+ " par secteur, en fonction de l'année"
    print question
    res, total_year=init_cs_year(nb=2, total=True, amdt=True)
    res, total_year=get_by_cs_year(res, variable=variable_name, total_year=total_year)
    write_cs_year(question, res, total_year=total_year, nb=2, amdt=True)


def q33():
    #votes par année
    question="votes par secteur, en fonction de l'année"
    print question
    res=init_cs_year()

    for act in Act.objects.filter(validated=2, vote_public=True):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)
                res[cs][year]+=1
    print "res", res

    write_cs_year(question, res)

def percent_adopt_cs(res, adopt_variable, regle_vote):
    for act in Act.objects.filter(validated=2, adopt_cs_regle_vote=regle_vote):
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

def q34():
    #pourcentage AdoptCSContre=Y
    question="pourcentage AdoptCSContre=Y (parmi les actes AdoptCSRegleVote=V du même secteur et de la même année) par secteur et par année"
    print question
    res=init_cs_year(nb=2)
    res=percent_adopt_cs(res, "adopt_cs_contre", "V")
    write_cs_year(question, res, percent=100, nb=2)
    


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
    res=init_cs_year(nb=2)
    res=percent_nb_em_adopt_cs(res, "adopt_cs_contre", "V", nb_em)
    write_cs_year(question, res, percent=100, nb=2)


def q36():
    #DureeTotaleDepuisPropCom lorsque VotePublic=Y
    question="DureeTotaleDepuisPropCom lorsque VotePublic=Y par secteur et par année"
    print question
    res=init_cs_year(nb=2)
    
    for act in Act.objects.filter(validated=2, vote_public=True, duree_tot_depuis_prop_com__isnull=False):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)
                res[cs][str(act.releve_annee)][1]+=1
                res[cs][str(act.releve_annee)][0]+=act.duree_tot_depuis_prop_com
    print "res", res

    write_cs_year(question, res, nb=2)
    

def q37():
    question="Pourcentage d’actes pour lesquels on a eu au moins une discussion en points B, en fonction de l'année, par secteur et par année"
    print question
    res, total_year=init_cs_year(total=True)
    print total_year

    for act in Act.objects.filter(validated=2, nb_point_b__isnull=False):
        if act.nb_point_b>0:
            year=str(act.releve_annee)
            #for each code sectoriel
            for nb in range(1,5):
                code_sect=getattr(act, "code_sect_"+str(nb))
                if code_sect!=None:
                    total_year[year]+=1
                    cs=get_cs(code_sect.code_sect)
                    res[cs][year]+=1
    print "res", res

    write_cs_year(question, res, total_year=total_year, percent=100)
    

def q38():
    question="pourcentage de ministres presents (M) et de RP (CS ou CS_PR) selon le pays et l'année (premier chiffre : pourcentage de M  par rapport au pays et à l'année ; deuxième chiffre : pourcentage de CS ou CS_PR par rapport au pays et à l'année)"
    print question

    statuses={}
    statuses["M"]=0
    statuses["CS"]=1
    statuses["CS_PR"]=1
    res={}
    total_cell={}
    for country in countries:
        res[country]={}
        total_cell[country]={}
        for year in years_list:
            total_cell[country][year]=0
            res[country][year]=[0,0]

    for act in MinAttend.objects.filter(act__validated_attendance=True).exclude(act__releve_annee=2013):
        status=Status.objects.get(verbatim=act.verbatim, country=act.country).status
        country=act.country.country_code
        if status not in ["NA", "AB"]:
            year=str(act.act.releve_annee)
            total_cell[country][year]+=1
            res[country][year][statuses[status]]+=1
    print "res", res
    print "total_cell", total_cell

    writer.writerow([question])
    writer.writerow(years_list_zero)
    for country in countries:
        row=[country]
        for year in years_list:
            res_year=""
            for index in range(2):
                if res[country][year][index]==0:
                    temp=0
                else:
                    temp=round(float(res[country][year][index])*100/total_cell[country][year],3)
                res_year+=str(temp)+ " / "
            row.append(res_year[:-3])
        writer.writerow(row)
    writer.writerow("")
    print ""
    
    

def concordance_annee_secteur_abs(resp_group, rapp_group):
    #répartition pourcentage dans les secteurs (somme colonne différent 100%)
    question="Concordance PartyFamilyResp et GroupePolitiqueRapporteur ("+resp_group+") : Pourcentage par secteur en fonction de l'année"
    print question
    res, total_year=init_cs_year(total=True)
        
    for act in Act.objects.filter(validated=2):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)
                total_year[year]+=1
                resps=[]
                rapps=[]
                
                for i in range(1, 3):
                    i=str(i)
                    resp=getattr(act, "resp_"+i)
                    rapp=getattr(act, "rapp_"+i)
                    if resp!=None:
                        resps.append(resp)
                    if rapp!=None:
                        rapps.append(rapp)
                
                if (len(resps)>0) and (len(rapps)>0):
                    same=False
                    for resp in resps:
                        if same:
                            break
                        for rapp in rapps:
                            if PartyFamily.objects.get(country=resp.country, party=resp.party).party_family.strip()==resp_group and rapp.party.party.strip() in rapp_group:
                                res[cs][year]+=1
                                same=True
                                break
    
    print "res"
    print res
    
    write_cs_year(question, res, total_year=total_year, percent=100)
    


def concordance_annee_secteur(resp_group, rapp_group):
    #répartition pourcentage selon chaque année (somme colonne = 100%)
    question="Concordance PartyFamilyResp et GroupePolitiqueRapporteur ("+resp_group+") : Pourcentage par secteur en fonction de l'année"
    print question
    res, total_year=init_cs_year(total=True)
        
    for act in Act.objects.filter(validated=2):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)
                resps=[]
                rapps=[]
                
                for i in range(1, 3):
                    i=str(i)
                    resp=getattr(act, "resp_"+i)
                    rapp=getattr(act, "rapp_"+i)
                    if resp!=None:
                        resps.append(resp)
                    if rapp!=None:
                        rapps.append(rapp)
                
                if (len(resps)>0) and (len(rapps)>0):
                    same=False
                    for resp in resps:
                        if same:
                            break
                        for rapp in rapps:
                            if PartyFamily.objects.get(country=resp.country, party=resp.party).party_family.strip()==resp_group and rapp.party.party.strip() in rapp_group:
                                res[cs][year]+=1
                                total_year[year]+=1
                                same=True
                                break
    
    print "res"
    print res
    
    write_cs_year(question, res, percent=100, total_year=total_year)


def q39():
    #pourcentage des actes quand PartyFamilyResp1 OU PartyFamilyResp2='Social Democracy' ET GroupePolitiqueRapporteur1 OU GroupePolitiqueRapporteur2= 'Progressive Alliance of Socialists and Democrats' OU 'Party of European Socialists' OU 'Socialist Group in the European Parliament »
    concordance_annee_secteur("Social Democracy", ["Progressive Alliance of Socialists and Democrats", "Party of European Socialists", "Socialist Group in the European Parliament"])


def q40():
    #pourcentage des actes quand PartyFamilyResp1 OU PartyFamilyResp2='Conservative/Christian Democracy' ET GroupePolitiqueRapporteur1 OU GroupePolitiqueRapporteur2= 'Progressive Alliance of Socialists and Democrats' OU 'Party of European Socialists' OU 'Socialist Group in the European Parliament »
    concordance_annee_secteur("Conservative/Christian Democracy", [u"European People's Party (Christian Democrats)", u"EPP - European People's Party (Christian Democrats)", u"European People's Party (Christian Democrats) and European Democrats"])


def q43():
    #période 2010-2012 : %age d’actes ayant fait l’objet d’ interventions des parlements nationaux
    question="période 2010-2012 : Pourcentage d’actes ayant fait l’objet d'interventions des parlements nationaux"
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


def q44():
    question="pourcentage AdoptCSContre=Y (parmi les actes AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année"
    print question
    res=init_cs_year(nb=2)
    res=percent_adopt_cs(res, "adopt_cs_contre", "U")
    write_cs_year(question, res, percent=100, nb=2)


def q45(nb_em):
    question="pourcentage "+str(nb_em)+" EM (parmi les actes AdoptCSContre=Y et AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année"
    print question
    res=init_cs_year(nb=2)
    res=percent_nb_em_adopt_cs(res, "adopt_cs_contre", "U", nb_em)
    write_cs_year(question, res, percent=100, nb=2)


def q46():
    question="pourcentage AdoptCSAbs=Y (parmi les actes AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année"
    print question
    res=init_cs_year(nb=2)
    res=percent_adopt_cs(res, "adopt_cs_abs", "U")
    write_cs_year(question, res, percent=100, nb=2)


def q47(nb_em):
    question="pourcentage "+str(nb_em)+" EM (parmi les actes AdoptCSAbs=Y et AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année"
    print question
    res=init_cs_year(nb=2)
    res=percent_nb_em_adopt_cs(res, "adopt_cs_abs", "U", nb_em)
    write_cs_year(question, res, percent=100, nb=2)


def q48():
    question="DureeTotaleDepuisTransCons moyenne pour les actes avec au moins une discussion en point B, par année"
    print question
    res={}
    for year in years_list:
        res[year]=[0,0]

    for act in Act.objects.filter(validated=2, nb_point_b__isnull=False, duree_tot_depuis_trans_cons__isnull=False):
        if act.nb_point_b>0:
            year=str(act.releve_annee)
            res[year][0]+=act.duree_tot_depuis_trans_cons
            res[year][1]+=1
        
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list)
    row=[]
    for year in years_list:    
        if res[year][0]==0:
            res_year=0
        else:
            res_year=round(float(res[year][0])/res[year][1], 3)
        row.append(res_year)
    writer.writerow(row)
    writer.writerow("")
    print ""
    

def q49():
    question="DureeTotaleDepuisTransCons moyenne pour les actes avec au moins une discussion en point B, par secteur"
    print question
    res={}
    for cs in cs_list:
        res[cs]=[0,0]

    for act in Act.objects.filter(validated=2, nb_point_b__isnull=False, duree_tot_depuis_trans_cons__isnull=False):
        if act.nb_point_b>0:
            for nb in range(1,5):
                code_sect=getattr(act, "code_sect_"+str(nb))
                if code_sect!=None:
                    cs=get_cs(code_sect.code_sect)
                    res[cs][0]+=act.duree_tot_depuis_trans_cons
                    res[cs][1]+=1
        
    print "res", res

    writer.writerow([question])
    writer.writerow(cs_list)
    row=[]
    for cs in cs_list:    
        if res[cs][0]==0:
            res_cs=0
        else:
            res_cs=round(float(res[cs][0])/res[cs][1], 3)
        row.append(res_cs)
    writer.writerow(row)
    writer.writerow("")
    print ""


def q50():
    question="DureeTotaleDepuisTransCons moyenne pour les actes avec au moins une discussion en point B, par secteur et par année"
    print question
    res=init_cs_year(nb=2)

    for act in Act.objects.filter(validated=2, nb_point_b__isnull=False, duree_tot_depuis_trans_cons__isnull=False):
        if act.nb_point_b>0:
            for nb in range(1,5):
                code_sect=getattr(act, "code_sect_"+str(nb))
                if code_sect!=None:
                    cs=get_cs(code_sect.code_sect)
                    year=str(act.releve_annee)
                    res[cs][year][0]+=act.duree_tot_depuis_trans_cons
                    res[cs][year][1]+=1
        
    print "res", res

    write_cs_year(question, res, nb=2)
    

    question="DureeTotaleDepuisTransCons moyenne pour les actes avec au moins une discussion en point B, par année"
    print question
    res={}
    for year in years_list:
        res[year]=[0,0]

    for act in Act.objects.filter(validated=2, nb_point_b__isnull=False, duree_tot_depuis_trans_cons__isnull=False):
        if act.nb_point_b>0:
            year=str(act.releve_annee)
            res[year][0]+=act.duree_tot_depuis_trans_cons
            res[year][1]+=1
        
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list)
    row=[]
    for year in years_list:    
        if res[year][0]==0:
            res_year=0
        else:
            res_year=round(float(res[year][0])/res[year][1], 3)
        row.append(res_year)
    writer.writerow(row)
    writer.writerow("")
    print ""


def q51(adopt_cs_regle_vote):
    question="DureeTotaleDepuisTransCons moyenne lorsque AdoptCSRegleVote="+adopt_cs_regle_vote+", par année"
    print question
    res={}
    for year in years_list:
        res[year]=[0,0]

    for act in Act.objects.filter(validated=2, adopt_cs_regle_vote=adopt_cs_regle_vote, duree_tot_depuis_trans_cons__isnull=False):
        if act.nb_point_b>0:
            year=str(act.releve_annee)
            res[year][0]+=act.duree_tot_depuis_trans_cons
            res[year][1]+=1
        
    print "res", res

    writer.writerow([question])
    writer.writerow(years_list)
    row=[]
    for year in years_list:    
        if res[year][0]==0:
            res_year=0
        else:
            res_year=round(float(res[year][0])/res[year][1], 3)
        row.append(res_year)
    writer.writerow(row)
    writer.writerow("")
    print ""
    

def q52(adopt_cs_regle_vote):
    question="DureeTotaleDepuisTransCons moyenne lorsque AdoptCSRegleVote="+adopt_cs_regle_vote+", par secteur"
    print question
    res={}
    for cs in cs_list:
        res[cs]=[0,0]

    for act in Act.objects.filter(validated=2, adopt_cs_regle_vote=adopt_cs_regle_vote, duree_tot_depuis_trans_cons__isnull=False):
        if act.nb_point_b>0:
            for nb in range(1,5):
                code_sect=getattr(act, "code_sect_"+str(nb))
                if code_sect!=None:
                    cs=get_cs(code_sect.code_sect)
                    res[cs][0]+=act.duree_tot_depuis_trans_cons
                    res[cs][1]+=1
        
    print "res", res

    writer.writerow([question])
    writer.writerow(cs_list)
    row=[]
    for cs in cs_list:    
        if res[cs][0]==0:
            res_cs=0
        else:
            res_cs=round(float(res[cs][0])/res[cs][1], 3)
        row.append(res_cs)
    writer.writerow(row)
    writer.writerow("")
    print ""


def q53(adopt_cs_regle_vote):
    question="DureeTotaleDepuisTransCons moyenne lorsque AdoptCSRegleVote="+adopt_cs_regle_vote+", par secteur et par année"
    print question
    res=init_cs_year(nb=2)

    for act in Act.objects.filter(validated=2, adopt_cs_regle_vote=adopt_cs_regle_vote, duree_tot_depuis_trans_cons__isnull=False):
        if act.nb_point_b>0:
            for nb in range(1,5):
                code_sect=getattr(act, "code_sect_"+str(nb))
                if code_sect!=None:
                    cs=get_cs(code_sect.code_sect)
                    year=str(act.releve_annee)
                    res[cs][year][0]+=act.duree_tot_depuis_trans_cons
                    res[cs][year][1]+=1
        
    print "res", res

    write_cs_year(question, res, nb=2)


def q54():
    question="Nombre de mots moyen des textes des actes, par année"
    print question
    res=init_year()
    res=get_by_year(res, variable="nb_mots")
    write_year(question, res)
    

def q55():
    question="Nombre de mots moyen des textes des actes, par secteur"
    print question
    res=init_cs()
    res=get_by_cs(res, variable="nb_mots")
    write_cs(question, res)
   

def q56():
    question="Nombre de mots moyen des textes des actes, par secteur et par année"
    print question
    res=init_cs_year(nb=2)
    res=get_by_cs_year(res, variable="nb_mots")
    write_cs_year(question, res, nb=2)


def q57():
    question="pourcentage d'actes avec plusieurs bases juridiques dans la production législative, par année"
    print question
    res=init_year()
    
    for act in Act.objects.filter(validated=2, base_j__isnull=False):
        if act.base_j.strip()!="":
            nb_bj=act.base_j.count(';')
            #if more than one BJ, assignate to "many BJ" catageory
            if nb_bj>0:
                nb_bj=1
            year=str(act.releve_annee)
            res[year][nb_bj]+=1
    print "res", res
    
    write_year(question, res, nb_var=2)
    
    
    

    
class Command(NoArgsCommand):
    def handle(self, **options):

        nb_acts=Act.objects.filter(validated=2).count()
        writer.writerow(["Les requêtes suivantes sont recueillies a partir des "+ str(nb_acts)+ " actes validés"])
        writer.writerow([""])

        #proportion d’actes avec plusieurs codes sectoriels
        #~ q1()
        #ventilation par domaines
        #~ q2()
        #Concordance PartyFamilyResp et GroupePolitiqueRapporteur (Social Democracy): Pourcentage sur la periode 1996-2012
        #~ q3()
        #Concordance PartyFamilyResp et GroupePolitiqueRapporteur (Conservative/Christian Democracy): Pourcentage sur la periode 1996-2012
        #~ q4()
        #~ #durée moyenne des actes adoptés en 1e et en 2e lecture
        #~ q7()
        #~ #durée moyenne entre transmission au conseil et adoption pour les actes qui ont donné lieu à un vote public
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
        #Nombre d’actes pour lesquels on a eu au moins une discussion en points B
        #~ q21()
        #pourcentage de ministres presents (M) et de RP (CS ou CS_PR)? par annee
        #~ q22()
        #Concordance PartyFamilyResp et GroupePolitiqueRapporteur (Social Democracy): Pourcentage par année
        #~ q23()
        #Concordance PartyFamilyResp et GroupePolitiqueRapporteur (Conservative/Christian Democracy): Pourcentage par année
        #~ q24()


        #PAR SECTEUR ET PAR ANNEE

        #% age de propositions modifiées par la Commission
        #~ q27()
        #~ #durée moyenne d’adoption
        #~ q28()
        #~ #% age d’actes adoptés en 1e et 2e lecture
        #~ q29()
        #~ #durée moyenne des actes adoptés en 1e et en 2e lecture
        #~ q30()
        #~ #durée moyenne entre transmission au conseil et adoption pour les actes qui ont donné lieu à un vote public
        #~ q31()
        #~ #nombre moyen d’amendements déposés/adoptés
        #~ q32("EPComAmdtTabled", "com_amdt_tabled")
        #~ q32("EPComAmdtAdopt", "com_amdt_adopt")
        #~ q32("EPAmdtTabled", "amdt_tabled")
        #~ q32("EPAmdtAdopt", "amdt_adopt")
        #Vote?
        #~ q33()
        #%age de votes négatifs par Etat membre
        #~ q34()
        #% age de votes négatifs isolés, de 2 Etats, de 3 Etats
        #~ q35(1)
        #~ q35(2)
        #~ q35(3)
        #Durée moyenne des actes soumis à un vote
        #~ q36()
        #~ #Pourcentage d’actes pour lesquels on a eu au moins une discussion en points B
        #~ q37()
        #~ #pourcentage de ministres presents (M) et de RP (CS ou CS_PR)? par annee ET par secteurs
        #~ q38()
        #Concordance PartyFamilyResp et GroupePolitiqueRapporteur (Social Democracy): Pourcentage par année et par secteur
        #~ q39()
        #~ #Concordance PartyFamilyResp et GroupePolitiqueRapporteur (Conservative/Christian Democracy): Pourcentage par année et par secteur
        #~ q40()
        #~ 
        
        #période 2010-2012 : %age d’actes ayant fait l’objet d’ interventions des parlements nationaux
        #~ q43()
        
        #~ #pourcentage AdoptCSContre=Y (parmi les actes AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année
        #~ q44()
        #pourcentage 1/2/3 EM (parmi les actes AdoptCSContre=Y et AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année
        #~ q45(1)
        #~ q45(2)
        #~ q45(3)
         #pourcentage AdoptCSAbs=Y (parmi les actes AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année
        #~ q46()
        #~ #pourcentage 1/2/3 EM (parmi les actes AdoptCSAbs=Y et AdoptCSRegleVote=U du même secteur et de la même année) par secteur et par année
        #~ q47(1)
        #~ q47(2)
        #~ q47(3)
        #DureeTotaleDepuisTransCons moyenne pour actes avec au moins une discussion en point B par année
        #~ q48()
        #DureeTotaleDepuisTransCons moyenne pour actes avec au moins une discussion en point B par secteur
        #~ q49()
        #~ #DureeTotaleDepuisTransCons moyenne pour les actes avec au moins une discussion en point B, par secteur et par année
        #~ q50()
       #DureeTotaleDepuisTransCons moyenne lorsque AdoptCSRegleVote=U par année  
        #~ q51("U")
        #~ q51("V")
        #~ #DureeTotaleDepuisTransCons moyenne lorsque AdoptCSRegleVote=U par secteur
        #~ q52("U")
        #~ q52("V")
        #DureeTotaleDepuisTransCons moyenne lorsque AdoptCSRegleVote=U, par secteur et par année
        #~ q53("U")
        #~ q53("V")
        #Nombre de mots moyen des textes des actes, par année
        #~ q54()
        #~ #Nombre de mots moyen des textes des actes, par secteur
        #~ q55()
        #~ #Nombre de mots moyen des textes des actes, par secteur et par année
        #~ q56()
        
        q57()
        
        
        
        #29,32,34,35,37,38,44,..., end
