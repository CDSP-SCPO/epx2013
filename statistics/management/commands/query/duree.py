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


def q78(cs=None):
    question="DureeTotaleDepuisTransCons moyenne, par période"
    Model=Act
    variable="duree_tot_depuis_trans_cons"
    filter_vars_acts={variable+"__gt": 1}
    res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts)

    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel : "+cs[1]+")"
        list_acts_cs=get_list_acts_cs(cs[0], Model=Model)
        res=get_by_period_cs(list_acts_cs, res, Model, filter_vars, filter_total, avg_variable=variable)
    else:
        res=get_by_period(res, Model, filter_vars, filter_total, avg_variable=variable)

    write_periods(question, res, percent=1)


def q96(factor="everything"):
    #Durée de la procédure (= Moyenne DureeTotaleDepuisTransCons ET DureeProcedureDepuisTransCons) par année, par secteur, par année et par secteur
    #1/pour tous les actes 2/VotePublic=Y 3/VotePublic=N 4/AdoptCSRegleVote=U 5/AdoptCSRegleVote=V 6/VotePublic=Y et AdoptCSRegleVote=U 7/ VotePublic=Y et AdoptCSRegleVote=V
    filters=(
        ("", {}),
        (" avec VotePublic=Y", {"vote_public": True}),
        (" avec VotePublic=N", {"vote_public": False}),
        (" avec AdoptCSRegleVote=U", {"adopt_cs_regle_vote": "U"}),
        (" avec AdoptCSRegleVote=V", {"adopt_cs_regle_vote": "V"}),
        (" avec VotePublic=Y et AdoptCSRegleVote=U", {"vote_public": True, "adopt_cs_regle_vote": "U"}),
        (" avec VotePublic=Y et AdoptCSRegleVote=V", {"vote_public": True, "adopt_cs_regle_vote": "V"})
    )
    variables=(("duree_tot_depuis_trans_cons", "DureeTotaleDepuisTransCons"), ("duree_proc_depuis_trans_cons", "DureeProcedureDepuisTransCons"))
    filter_vars={variables[0][0]+"__gt": 1, variables[1][0]+"__gt": 1}
    init_question="Durée moyenne (" + variables[0][1] + "+" + variables[1][1]+ ")"

    if factor=="csyear":
        #get by cs and by year only (for specific cs)
        analyses, nb_figures_cs=get_specific_cs()

    for filt in filters:
        filter_vars_temp=filter_vars.copy()
        #update filter
        filter_vars_temp.update(filt[1])
        
        for analysis, question in analyses:
            question=init_question+filt[0]+question
            
            res_1=init(analysis)
            res_2=init(analysis)
            res_1=get(analysis, res_1, variable=variables[0][0], filter_vars_acts=filter_vars_temp, nb_figures_cs=nb_figures_cs)
            res_2=get(analysis, res_2, variable=variables[1][0], filter_vars_acts=filter_vars_temp, nb_figures_cs=nb_figures_cs)
            write(analysis, question, res_1, res_2=res_2, percent=1, query="1+2")
        
        
def q110(factors=factors, periods=None, nb_figures_cs=2):
    #Durée Moyenne DureeTotaleDepuisTransCons
    #1/pour tous les actes 2/VotePublic=Y 3/VotePublic=N 4/AdoptCSRegleVote=U 5/AdoptCSRegleVote=V 6/VotePublic=Y et AdoptCSRegleVote=U 7/ VotePublic=Y et AdoptCSRegleVote=V
    
    #get parameters specific to the question
    factors_question, filter_vars_acts=get_parameters_question(factors, periods)
    
    filters=(
        ("", {}),
        #~ (" avec VotePublic=Y", {"vote_public": True}),
        #~ (" avec VotePublic=N", {"vote_public": False}),
        #~ (" avec AdoptCSRegleVote=U", {"adopt_cs_regle_vote": "U"}),
        #~ (" avec AdoptCSRegleVote=V", {"adopt_cs_regle_vote": "V"}),
        #~ (" avec VotePublic=Y et AdoptCSRegleVote=U", {"vote_public": True, "adopt_cs_regle_vote": "U"}),
        #~ (" avec VotePublic=Y et AdoptCSRegleVote=V", {"vote_public": True, "adopt_cs_regle_vote": "V"})
    )
    variable=("duree_tot_depuis_trans_cons", "DureeTotaleDepuisTransCons")
    filter_vars_acts.update({variable[0]+"__gt": 1})
    init_question=variable[1] + " moyenne"

    for filt in filters:
        filter_vars_temp=filter_vars_acts.copy()
        #update filter
        filter_vars_temp.update(filt[1])
        
        for factor, question in factors_question.iteritems():
            question=init_question+filt[0]+question
            res=init(factor)
            res=get(factor, res, variable=variable[0], filter_vars_acts=filter_vars_temp, nb_figures_cs=nb_figures_cs)
            write(factor, question, res, percent=1)


def q118(factors=factors, periods=None, nb_figures_cs=2):
    #DureeTotaleDepuisTransCons quand NbPointsB = 0,1,2,3 ou plus
    var="nb_point_b"
    variable="duree_tot_depuis_trans_cons"
    filters=(
        ({var: 0}, "exactement zéro point B"),
        ({var: 1}, "exactement un point B"),
        ({var: 2}, "exactement deux points B"),
        ({var+"__gt": 2}, "plus de deux points B"),
    )
    
    #get parameters specific to the question
    factors_question, filter_vars_acts=get_parameters_question(factors, periods)
    
    init_question="DureeTotaleDepuisTransCons moyenne pour les actes avec "

    for filt in filters:
        filter_vars_acts_temp=filter_vars_acts.copy()
        #update filter
        filter_vars_acts_temp.update(filt[0])
        init_question_2=init_question+filt[1]

        for factor, question in factors_question.iteritems():
            question=init_question_2+question

            if factor=="periods":
                res=[]
                for period in periods:
                    filter_vars_acts_temp_2=filter_vars_acts_temp.copy()
                    filter_vars_acts_temp_2.update(filter_periods_question(filter_vars_acts_temp_2, period))
                    res.append(init(factor))
                    res[-1]=get(factor, res[-1], variable=variable, filter_vars_acts=filter_vars_acts_temp_2, nb_figures_cs=nb_figures_cs)
            else:
                res=init(factor)
                res=get(factor, res, variable=variable, filter_vars_acts=filter_vars_acts_temp, nb_figures_cs=nb_figures_cs)
                
            write(factor, question, res, percent=1, periods=periods)


def q128(factors=factors, periods=None):
    #Durée de la procédure (= Moyenne DureeTotaleDepuisTransCons ET DureeProcedureDepuisTransCons)
    init_question="Durée moyenne de la procédure (= Moyenne DureeTotaleDepuisTransCons + DureeProcedureDepuisTransCons)"
    variables=("duree_tot_depuis_trans_cons", "duree_proc_depuis_trans_cons")
    filter_vars_acts={variables[0]+"__gt": 1, variables[1]+"__gt": 1}
    #get the factors specific to the question
    factors_question=get_factors_question(factors)

    #for each factor
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res_1=init(factor)
        res_2=init(factor)
        res_1=get(factor, res_1, variable=variables[0], filter_vars_acts=filter_vars_acts, periods=periods)
        res_2=get(factor, res_2, variable=variables[1], filter_vars_acts=filter_vars_acts, periods=periods)
        write(factor, question, res_1, res_2=res_2, percent=1, periods=periods, query="1+2")
