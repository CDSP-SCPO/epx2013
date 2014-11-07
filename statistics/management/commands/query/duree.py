#-*- coding: utf-8 -*-

#queries about the duration variables (duree_tot_depuis_prop_com and duree_tot_depuis_trans_cons)

#import general steps common to each query
from  ..init import *
from  ..get import *
from  ..write import *


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


def q14():
    #durée moyenne des actes adoptés en 1e et en 2e lecture
    question="durée DureeTotaleDepuisPropCom moyenne des actes NoUniqueType=COD adoptés en 1ère et 2ème lecture par année"
    print question
    nb_lec=2
    res=init_year_nb_lec()
    res=get_year_nb_lec(res, variable="duree_tot_depuis_prop_com")
    write_year_nb_lec(question, res)


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


def concordance_annee(resp_group, rapp_group, percent=100, variable=1):

    if variable!=1:
        question="DureeTotaleDepuisPropCom moyenne des actes pour lesquels il y a concordance des PartyFamilyResp et GroupePolitiqueRapporteur ("+resp_group+")"
    else:
        if resp_group=="any" and rapp_group=="any":
            question="Pourcentage discordance PartyFamilyRappPE1 et PartyFamilyRespPropos1, par année"
        else:
            question="Concordance PartyFamilyResp et GroupePolitiqueRapporteur ("+resp_group+") : Pourcentage par année"
    print question
    res={}
    for year in years_list:
        res[year]=[0,0]
        
    for act in Act.objects.filter(validated=2):
        if variable==1:
            res[year][1]+=1
            
        year=str(act.releve_annee)

        #count any political family for the rapp1 and resp1 (different only)
        if resp_group=="any" and rapp_group=="any":
            rapp=act.rapp_1
            resp=act.resp_1
            if rapp!=None and resp!=None:
                rapp_pf=PartyFamily.objects.get(country=rapp.country, party=rapp.party).party_family.strip().encode("utf-8")
                resp_pf=PartyFamily.objects.get(country=resp.country, party=resp.party).party_family.strip().encode("utf-8")
                if rapp_pf!=resp_pf:
                    res[year][0]+=1

        else:
            #count political families in parameter for all rapps and resps (same only)
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
                            if variable==1:
                                res[year][0]+=1
                            else:
                                res[year][0]+=getattr(act, variable)
                                res[year][1]+=1
                            same=True
                            break
        
    print "res"
    print res
    #duree moyenne
    for year in years_list:
        if res[year][0]!=0:
            res[year][0]=round(float(res[year][0])*percent/res[year][1], 3)

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

    
def q28():
    #durée moyenne d’adoption par secteur, en fonction de l'année
    question="DureeTotaleDepuisPropCom moyenne par secteur, en fonction de l'année"
    print question
    res=init_cs_year()
    res=get_by_cs_year(res, variable="duree_tot_depuis_prop_com")
    write_cs_year(question, res, percent=1)


def q30():
    #durée moyenne des actes adoptés en 1e et en 2e lecture
    question="durée DureeTotaleDepuisPropCom moyenne des actes NoUniqueType=COD adoptés en 1ère et 2ème lecture par secteur, en fonction de l'année (1ère lecture / 2ème lecture)"
    print question
    nb_lec=2
    res=init_cs_year_nb_lec()
    res=get_by_cs_year_nb_lec(res, variable="duree_tot_depuis_prop_com")
    write_cs_year_nb_lec(question, res)


def q36():
    #DureeTotaleDepuisPropCom lorsque VotePublic=Y
    question="DureeTotaleDepuisPropCom lorsque VotePublic=Y par secteur et par année"
    print question
    res=init_cs_year()
    
    for act in Act.objects.filter(validated=2, vote_public=True, duree_tot_depuis_prop_com__isnull=False):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)
                res[cs][str(act.releve_annee)][1]+=1
                res[cs][str(act.releve_annee)][0]+=act.duree_tot_depuis_prop_com
    print "res", res

    write_cs_year(question, res)


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
    res=init_cs_year()

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

    write_cs_year(question, res)
    

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
    res=init_cs_year()

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

    write_cs_year(question, res)


def q58():
    #DureeTotaleDepuisPropCom moyenne des actes pour lesquels il y a concordance des PartyFamilyResp et GroupePolitiqueRapporteur ("Social Democracy")
    concordance_annee("Social Democracy", ["Progressive Alliance of Socialists and Democrats", "Party of European Socialists", "Socialist Group in the European Parliament"], percent=1, variable="duree_tot_depuis_prop_com")


def q59(cs, name):
    question="impact du nombre de bases juridiques sur la durée de la procédure"
    print question
    res_cs=[0,0]
    res_bj=[0,0]
    res_cs_bj=[0,0]

    for act in Act.objects.filter(validated=2, duree_tot_depuis_prop_com__isnull=False):
        ok=0
        #DureeTotDepuisPropCom moyenne pour les actes avec un code sectoriel Marché intérieur
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None and get_cs(code_sect.code_sect)==cs:
                res_cs[0]+=act.duree_tot_depuis_prop_com
                res_cs[1]+=1
                ok+=1
                break

        #DureeTotDepuisPropCom moyenne pour les actes avec plusieurs bases juridiques
        if act.base_j.count(';')>0:
            res_bj[0]+=act.duree_tot_depuis_prop_com
            res_bj[1]+=1
            ok+=1
        
        #DureeTotDepuisPropCom moyenne pour les actes avec plusieurs bases juridiques et un code sectoriel Marché intérieur
        if ok==2:
            res_cs_bj[0]+=act.duree_tot_depuis_prop_com
            res_cs_bj[1]+=1
        
    
    writer.writerow([question])

    #DureeTotDepuisPropCom moyenne pour les actes avec un code sectoriel Marché intérieur
    if res_cs[0]==0:
        temp=0
    else:
        temp=round(float(res_cs[0])/res_cs[1], 3) 
    writer.writerow(["DureeTotDepuisPropCom moyenne pour les actes avec un code sectoriel "+name, temp])
    
    #DureeTotDepuisPropCom moyenne pour les actes avec plusieurs bases juridiques
    if res_cs[0]==0:
        temp=0
    else:
        temp=round(float(res_bj[0])/res_bj[1], 3) 
    writer.writerow(["DureeTotDepuisPropCom moyenne pour les actes avec plusieurs bases juridiques", temp])
    
    #DureeTotDepuisPropCom moyenne pour les actes avec plusieurs bases juridiques et un code sectoriel Marché intérieur
    if res_cs[0]==0:
        temp=0
    else:
        temp=round(float(res_cs_bj[0])/res_cs_bj[1], 3) 
    writer.writerow(["DureeTotDepuisPropCom moyenne pour les actes avec plusieurs bases juridiques et un code sectoriel "+name, temp])
    
        
    writer.writerow("")
    print ""


def q78():
    question="Durée moyenne par acte"
    Model=Act
    filter_vars_acts={"duree_tot_depuis_prop_com__isnull": False}
    periods, nb_periods, res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts)
    res=get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total, avg_variable="duree_tot_depuis_prop_com")
    write_periods(question, res, periods, nb_periods, percent=1)


def q96():
    #Durée DureeTotaleDepuisTransCons moyenne 1/pour tous les actes, 2/quand VotePublic=Y ou 3/quand VotePublic= N, par année, par secteur, par année et par secteur
    variables={", pour tous les actes,": "", ", pour les actes avec VotePublic=Y,": ("vote_public",True) , ", pour les actes avec VotePublic=N,": ("vote_public",False)}
    variable="duree_tot_depuis_trans_cons"
    filter_vars={"validated": 2, variable+"__isnull": False}

    for key, value in variables.iteritems():
        #if not first query (for all the acts), then filter by vote_public
        if type(value) is not str:
            filter_vars[value[0]]=value[1]
        
        question="Durée DureeTotaleDepuisTransCons moyenne"+key+" par secteur"
        print question
        res=init_cs()
        res=get_by_cs(res, variable=variable, filter_vars=filter_vars)
        write_cs(question, res, percent=1)

        question="Durée DureeTotaleDepuisTransCons moyenne"+key+" par année"
        print question
        res=init_year()
        res=get_by_year(res, variable=variable, filter_vars=filter_vars)
        write_year(question, res, percent=1)

        question="Durée DureeTotaleDepuisTransCons moyenne"+key+" par année et par secteur"
        print question
        res=init_cs_year()
        res=get_by_cs_year(res, variable=variable, filter_vars=filter_vars)
        write_cs_year(question, res, percent=1)


    
