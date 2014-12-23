#-*- coding: utf-8 -*-

#queries about the party_family variable


#import general steps common to each query
from  common import *
from  ..init import *
from  ..get import *
from  ..write import *



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




def concordance_annee_secteur_abs(resp_group, rapp_group):
    #répartition pourcentage dans les secteurs (somme colonne différent 100%)
    question="Concordance PartyFamilyResp et GroupePolitiqueRapporteur ("+resp_group+") : Pourcentage par secteur et par année"

    print question
    res, total_year=init_cs_year()

    for act in Act.objects.filter(validated=2):
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)

                #count any political family for the rapp1 and resp1 (different only)
                if resp_group=="any" and rapp_group=="any":
                    rapp=act.rapp_1
                    resp=act.resp_1
                    if rapp!=None and resp!=None:
                        res[cs][year][1]+=1
                        rapp_pf=PartyFamily.objects.get(country=rapp.country, party=rapp.party).party_family.strip().encode("utf-8")
                        resp_pf=PartyFamily.objects.get(country=resp.country, party=resp.party).party_family.strip().encode("utf-8")
                        if rapp_pf!=resp_pf:
                            res[cs][year][0]+=1

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
                        res[cs][year][1]+=1
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

    write_cs_year(question, res)



def concordance_annee_secteur(resp_group, rapp_group):
    #répartition pourcentage selon chaque année (somme colonne = 100%)
    if resp_group=="any" and rapp_group=="any":
        question="Pourcentage discordance PartyFamilyRappPE1 et PartyFamilyRespPropos1, par secteur en fonction de l'année"
    else:
        question="Concordance PartyFamilyResp et GroupePolitiqueRapporteur ("+resp_group+") : Pourcentage par secteur en fonction de l'année"

    print question
    res, total_year=init_cs_year(total=True)

    for act in Act.objects.filter(validated=2):
        for nb in range(1,nb_cs+1):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)

                #count any political family for the rapp1 and resp1 (different only)
                if resp_group=="any" and rapp_group=="any":
                    rapp=act.rapp_1
                    resp=act.resp_1
                    if rapp!=None and resp!=None:
                        rapp_pf=PartyFamily.objects.get(country=rapp.country, party=rapp.party).party_family.strip().encode("utf-8")
                        resp_pf=PartyFamily.objects.get(country=resp.country, party=resp.party).party_family.strip().encode("utf-8")
                        if rapp_pf!=resp_pf:
                            res[cs][year]+=1
                            total_year[year]+=1

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


def q84(factor="everything"):
    #Pourcentage de discordance des familles politiques
    init_question="Pourcentage de discordance de PartyFamilyRappPE* et PartyFamilyRespPropos*"
    filter_vars={"rapp_1__isnull": False, "resp_1__isnull": False}

    if factor=="csyear":
        #get by cs and by year only (for specific cs)
        analyses, nb_figures_cs=get_specific_cs()

    for analysis, question in analyses:
        question=init_question+question
        res=init(analysis)
        res=get(analysis, res, filter_vars_acts=filter_vars, query="discordance", nb_figures_cs=nb_figures_cs)
        write(analysis, question, res)


def q93():
    initial_question="Pourcentage des familles politiques des RespPropos"
    #~ -> par secteur
    question=initial_question+", par secteur"
    print question
    res=init_cs(total=True, empty_dic=True)
    res=get_percent_pf_cs(res, "resp", 3)
    write_percent_pf(question, cs_list, "CS", res, "RespPropos")
#~
    #~ #-> par année
    question=initial_question+", par année"
    print question
    res=init_year(total=True, empty_dic=True)
    res=get_percent_pf_year(res, "resp", 3)
    write_percent_pf(question, years_list, "YEAR", res, "RespPropos")

    #~ #-> par secteur et par année
    question=initial_question+", par secteur et par année"
    print question
    res=init_cs_year(total=True, empty_dic=True)
    res=get_percent_pf_cs(res, "resp", 3, year_var=True)
    write_percent_pf_cs_year(question, res, "RespPropos")
    #~


def q94():
    initial_question="Pourcentage des familles politiques des Rapporteurs, pour les actes NoUniqueType=COD"

    #a)NoUniqueType=COD et NbLectures=1
    #b)NoUniqueType=COD et NbLectures=2 ou 3
    nb_lec_list=((" et NbLectures=1", "act__nb_lectures"),(" et NbLectures=2 ou 3", "act__nb_lectures__gt"))

    for nb_lec in nb_lec_list:
        #-> par secteur
        question=initial_question+nb_lec[0]+", par secteur"
        print question
        res=init_cs(empty_dic=True)
        res=get_percent_pf_cs(res, "rapp", 5, filter_variables={"no_unique_type": "COD", nb_lec[1]: 1})
        write_percent_pf(question, cs_list, "CS", res, "RapporteurPE")

        #~ #-> par année
        question=initial_question+nb_lec[0]+", par année"
        print question
        res=init_year(empty_dic=True)
        res=get_percent_pf_year(res, "rapp", 5, filter_variables={"no_unique_type": "COD", nb_lec[1]: 1})
        write_percent_pf(question, years_list, "YEAR", res, "RapporteurPE")

        #~ #-> par secteur et par année
        question=initial_question+nb_lec[0]+", par secteur et par année"
        print question
        res=init_cs_year(empty_dic=True)
        res=get_percent_pf_cs(res, "rapp", 5, year_var=True, filter_variables={"no_unique_type": "COD", nb_lec[1]: 1})
        write_percent_pf_cs_year(question, res, "RapporteurPE")

