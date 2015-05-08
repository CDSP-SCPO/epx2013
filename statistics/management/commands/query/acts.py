#-*- coding: utf-8 -*-

#queries about the number of acts or percent of acts


#import general steps common to each query
from  common import *
from  ..init import *
from  ..get import *
from  ..write import *



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


def q2(factors=factors, periods=None):
    #Nombre d'actes
    init_question="Nombre d'actes"

    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)

    #for each factor
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res=init(factor, count=False)
        res=get(factor, res, periods=periods, count=False)
        write(factor, question, res, periods=periods, count=False)


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




def q57(cs="all", name="ALL"):
    if cs=="all":
        question="pourcentage d'actes avec plusieurs bases juridiques dans la production législative, par année"
        percent=1
        count=True
    else:
        question="pourcentage d'actes avec au moins un code sectoriel="+name+" dans la production législative, par année"
        percent=100
        count=False
    print question
    res=init_year()

    for act in Act.objects.filter(validated=2):
        if act.base_j.strip()!="":
            year=str(act.releve_annee)
            if cs=="all":
                nb_bj=act.base_j.count(';')
                #if more than one BJ, assignate to "many BJ" catageory
                if nb_bj>0:
                    nb_bj=1
                res[year][nb_bj]+=1
            else:
                res[year][1]+=1
                for nb in range(1,5):
                    code_sect=getattr(act, "code_sect_"+str(nb))
                    if code_sect is not None and get_cs(code_sect.code_sect)==cs:
                        res[year][0]+=1
                        break

    print "res", res

    write_year(question, res, count=count, percent=percent)


def nb_bj_cs(cs, name, variable, type_var, question):
    question=question+" en fonction du nombre de bases juridiques et du secteur"
    print question
    #first line: 1 BJ; second line: many BJ
    #first column: only one cs (13); second column: all cs
    res=[[0,0], [0,0]]

    for act in Act.objects.filter(validated=2):
        ok=False
        if type_var=="bool" and getattr(act, variable)==True:
            ok=True
        elif type_var=="int" and getattr(act, variable)>0:
            ok=True

        if ok:
            if act.base_j.strip()!="":
                nb_bj=act.base_j.count(';')
                #if more than one BJ, assignate to "many BJ" catageory
                if nb_bj>0:
                    nb_bj=1
                    res[nb_bj][1]+=1
                else:
                    #only one BJ
                    res[nb_bj][1]+=1

                #for specific cs in parameter
                for nb in range(1,5):
                    code_sect=getattr(act, "code_sect_"+str(nb))
                    if code_sect is not None and get_cs(code_sect.code_sect)==cs:
                        res[nb_bj][0]+=1
                        break

    print "res", res

    writer.writerow([question])
    writer.writerow(["", "CS="+name, "Tous les CS"])
    writer.writerow(["Une BJ", res[0][0], res[0][1]])
    writer.writerow(["Plusieurs BJ", res[1][0], res[1][1]])
    writer.writerow("")
    print ""


def q60():
    question="Nombre de discussions en point b"
    nb_bj_cs("13", "Marché intérieur", "nb_point_b", "int", question)


def q61():
    question="Nombre d'actes avec un vote public"
    nb_bj_cs("13", "Marché intérieur", "vote_public", "bool", question)


def q62(cs, name):
    question="Pourcentages d'actes NoUniqueType=COD adoptés en 1ère lecture en fonction du nombre de base juridiques et du code sectoriel"
    print question
    #first line: 1 BJ; second line: many BJ
    #first column: only one cs (13); second column: all cs
    #first zero: nb acts; second_zero: total
    res=[[[0,0],[0,0]], [[0,0],[0,0]]]
    #~ count=0

    for act_ids in ActIds.objects.filter(act__validated=2, src="index"):
        act=act_ids.act
        if act.base_j.strip()!="":
            nb_bj=act.base_j.count(';')
            #if more than one BJ, assignate to "many BJ" catageory
            if nb_bj>0:
                nb_bj=1

            #for specific cs in parameter
            nb_cs=1
            for nb in range(1,5):
                code_sect=getattr(act, "code_sect_"+str(nb))
                if code_sect!=None and get_cs(code_sect.code_sect)==cs:
                    nb_cs=0
                    break

            #count total
            res[nb_bj][nb_cs][1]+=1
            if nb_cs==0:
                #if the act has a code sectoriel="13", it has to be counted for the "all cs" column too
                res[nb_bj][1][1]+=1

            #count number of acts
            if act_ids.no_unique_type=="COD" and act.nb_lectures==1:
                res[nb_bj][nb_cs][0]+=1
                if nb_cs==0:
                    #if the act has a code sectoriel="13", it has to be counted for the "all cs" column too
                    res[nb_bj][1][0]+=1

    print "res", res
    #~ print "count", count

    writer.writerow([question])
    writer.writerow(["", "CS="+name, "Tous les CS"])
    for nb_bj in range(2):
        if nb_bj==0:
            row=["Une BJ"]
        else:
            row=["Plusieurs BJ"]
        for nb_cs in range(2):
            if res[nb_bj][nb_cs][0]==0:
                temp=0
            else:
                temp=round(float(res[nb_bj][nb_cs][0])*100/res[nb_bj][nb_cs][1], 3)
            row.append(temp)
        writer.writerow(row)
    writer.writerow("")
    print ""


def q71(factors=factors, periods=None):
    #actes pour lesquels ProposOrigine="COM" et ComProc="Written procedure"
    init_question="Pourcentage d'actes provenant de la Commission et adoptés par procédure écrite"
    check_vars_acts={"com_proc": "Written procedure"}
    check_vars_acts_ids={"propos_origine": "COM"}
    #get the factors specific to the question
    factors_question=get_factors_question(factors)

    #for each factor
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res=init(factor)
        res=get(factor, res, Model=ActIds, check_vars_acts=check_vars_acts, check_vars_acts_ids=check_vars_acts_ids, periods=periods)
        write(factor, question, res, periods=periods)


def q72(cs=None):
    question="Pourcentage d'actes avec au moins un point A, par période"
    Model=Act
    filter_vars_acts={"nb_point_a__gte": 1}
    res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts)

    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel : "+cs[1]+")"
        list_acts_cs=get_list_acts_cs(cs[0], Model=Model)
        res=get_by_period_cs(list_acts_cs, res, Model, filter_vars, filter_total)
    else:
        res=get_by_period(res, Model, filter_vars, filter_total)

    write_periods(question, res)


def q74(factors=factors, periods=None):
    init_question="Pourcentage d'actes adoptés en 1ère lecture parmi les actes de codécision"
    filter_vars_acts_ids={"no_unique_type": "COD"}
    check_vars_acts={"nb_lectures": 1}
    #get the factors specific to the question
    factors_question=get_factors_question(factors)

    #for each factor
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res=init(factor)
        res=get(factor, res, Model=ActIds, filter_vars_acts_ids=filter_vars_acts_ids, check_vars_acts=check_vars_acts, periods=periods)
        write(factor, question, res, periods=periods)


def q77(factors=factors, periods=None):
    #get the factors specific to the question
    factors_question=get_factors_question(factors)
    
    Model=Act
    filter_vars_acts={"adopt_cs_regle_vote": "V"}
    filter_var_acts_vote=filter_vars_acts.copy()
    filter_var_acts_vote["vote_public"]=True

    #~ question="Pourcentage d’actes adoptés avec un vote public, parmi les actes avec une majorité qualifiée lors de l'adoption au conseil, par période"
    #~ res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_var_acts_vote, filter_total_acts=filter_total_acts)
    #~ #filter by specific cs
    #~ if cs is not None:
        #~ question+=" (code sectoriel : "+cs[1]+")"
        #~ res=get_by_period_cs(list_acts_cs, res, Model, filter_vars, filter_total)
    #~ else:
        #~ res=get_by_period(res, Model, filter_vars, filter_total)
    #~ write_periods(question, res)
#~ 
    #~ question="Pourcentage d’actes adoptés avec avec opposition d'exactement un état, parmi les actes avec une majorité qualifiée lors de l'adoption au conseil, par période"
    #~ res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts, filter_total_acts=filter_total_acts)
    #~ #filter by specific cs
    #~ if cs is not None:
        #~ question+=" (code sectoriel : "+cs[1]+")"
        #~ res=get_by_period_cs(list_acts_cs, res, Model, filter_vars, filter_total, adopt_cs={"nb_countries": 1})
    #~ else:
        #~ res=get_by_period(res, Model, filter_vars, filter_total, adopt_cs={"nb_countries": 1})
    #~ write_periods(question, res)

    for factor, question in factors_question.iteritems():
        question="Pourcentage d’actes adoptés avec opposition d'au moins deux états, parmi les actes avec une majorité qualifiée lors de l'adoption au conseil"+question
        res=init(factor)
        res=get(factor, res, Model=Model, filter_vars_acts=filter_vars_acts, adopt_var="adopt_cs_contre", query=2, periods=periods)
        write(factor, question, res, periods=periods)

    #~ question="Pourcentage d’actes adoptés avec abstention d'au moins un état, parmi les actes avec une majorité qualifiée lors de l'adoption au conseil, par période"
    #~ res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts, filter_total_acts=filter_total_acts)
    #~ #filter by specific cs
    #~ if cs is not None:
        #~ question+=" (code sectoriel : "+cs[1]+")"
        #~ res=get_by_period_cs(list_acts_cs, res, Model, filter_vars, filter_total, exclude_vars={"adopt_cs_abs": None})
    #~ else:
        #~ res=get_by_period(res, Model, filter_vars, filter_total, exclude_vars={"adopt_cs_abs": None})
    #~ write_periods(question, res)


def q79(cs=None):
    question="Pourcentage d’actes adoptés en 2ème lecture parmi les actes de codécision, par période"
    Model=ActIds
    filter_total_act_ids={"no_unique_type": "COD"}
    filter_vars_acts={"nb_lectures": 2}
    filter_vars_acts_ids=filter_total_act_ids.copy()
    res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts, filter_vars_acts_ids=filter_vars_acts_ids, filter_total_acts_ids=filter_total_act_ids)

    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel : "+cs[1]+")"
        list_acts_cs=get_list_acts_cs(cs[0], Model=Model)
        res=get_by_period_cs(list_acts_cs, res, Model, filter_vars, filter_total)
    else:
        res=get_by_period(res, Model, filter_vars, filter_total)

    write_periods(question, res)


def q80(cs=None):
    question="Pourcentage d’actes avec au moins un point B, par période"
    Model=Act
    filter_vars_acts={"nb_point_b__gte": 1}
    filter_total_acts={"nb_point_b__isnull": False}
    res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts, filter_total_acts=filter_total_acts)

    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel : "+cs[1]+")"
        list_acts_cs=get_list_acts_cs(cs[0], Model=Model)
        res=get_by_period_cs(list_acts_cs, res, Model, filter_vars, filter_total)
    else:
        res=get_by_period(res, Model, filter_vars, filter_total)

    write_periods(question, res)


def liste_titre_actes_cs(cs, cs_list):
    question="Liste des actes dont un des 4 codes sectoriels commence par "+cs
    print question
    year_min=1996
    year_max=2012
    res=init_cs_year(titles_list=True)

    for act in Act.objects.filter(validated=2, releve_annee__gte=year_min, releve_annee__lte=year_max):
        #loop over the 4 possible cs
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect is not None:
                cs_act=get_cs(code_sect.code_sect)
                if cs_act==cs:
                    year=str(act.releve_annee)
                    res[cs][year].append([act.releve_annee, act.releve_mois, act.no_ordre, act.titre_rmc.encode("utf-8")])
                    break

    #~ print "res"
    #~ print res

    writer.writerow("")
    writer.writerow([question])

    writer.writerow(["CS "+cs])
    for year in years_list:
        if res[cs][year]:
            writer.writerow(["YEAR "+year])
            for act in res[cs][year]:
                writer.writerow(act)


def q82():
    #Liste des actes avec leur titre pour la période 1996-2012 lorsque l’un des 4 codes sectoriels comprend le code suivant (2 premiers chiffres)
    css=["19", "15", "03", "13", "05"]
    for cs in css:
        liste_titre_actes_cs(cs, css)
    writer.writerow("")
    print ""


def q98(factors=factors, periods=None, nb_figures_cs=2):
    #Pourcentage d’actes adoptés avec NoUniqueType=COD 1/et NbLectures=1, 2/et NbLectures=2 ou 3, par année, par secteur, par année et par secteur

    #get parameters specific to the question
    factors_question, filter_vars_acts=get_parameters_question(factors, periods)
    
    #variables=(([1], "1ère lecture"), ([2, 3], "2ème ou 3ème lecture"))
    #2014-12-23
    variables=(([1], "1ère lecture"), ([2], "2ème lecture"), ([3], "3ème lecture"))
    filter_vars_acts.update({"nb_lectures__isnull": False})
    filter_vars_acts_ids={"no_unique_type": "COD"}
    init_question="Pourcentage d'actes adoptés en "

    for variable in variables:
        check_vars_acts={"nb_lectures__in": variable[0]}
    
        for factor, question in factors_question.iteritems():
            question=init_question+variable[1]+", parmi les actes NoUniqueType=COD"+question
            res=init(factor)
            res=get(factor, res, Model=ActIds, filter_vars_acts=filter_vars_acts, filter_vars_acts_ids=filter_vars_acts_ids, check_vars_acts=check_vars_acts, nb_figures_cs=nb_figures_cs)
            write(factor, question, res)
        

def q103():
    question="Nombre d'actes adoptés sans point B (la variable NbPointB est vide ou égale à zéro)"
    Model=Act
    #nb_point_b=None or nb_point_b=0
    exclude_vars_acts={"nb_point_b__gte": 1}
    periods, nb_periods, res, filter_vars, filter_total=init_periods(Model)
    res=get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total, exclude_vars=exclude_vars_acts)
    write_periods(question, res, periods, nb_periods, nb=True)


def q107(factors=factors, periods=None):
    #Pourcentage d'actes avec VotePublic=Y
    init_question="Pourcentage d'actes avec VotePublic=Y"
    check_vars_acts={"vote_public": True}
    #get the factors specific to the question
    factors_question=get_factors_question(factors)

    #for each factor
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res=init(factor)
        res=get(factor, res, check_vars_acts=check_vars_acts, periods=periods)
        write(factor, question, res, periods=periods)


def q108(factors=factors, periods=None, nb_figures_cs=2):
    #Pourcentage d'actes avec au moins un points B, exactement un point B, deux points B, plus de deux points B
    var="nb_point_b"
    filters=(
        ({var: 1}, "exactement un point B"),
        ({var+"__gte": 1}, "au moins un point B"),
        ({var: 2}, "exactement deux points B"),
        ({var+"__gt": 2}, "plus de deux points B")
    )
    
    #get parameters specific to the question
    factors_question=get_factors_question(factors)
    
    init_question="Pourcentage d'actes avec "
    filter_vars_acts.update({var+"__isnull": False})

    for filt in filters:
        check_vars_acts=filt[0]
        init_question_2=init_question+filt[1]

        for factor, question in factors_question.iteritems():
            question=init_question_2+question

            if factor=="periods":
                res=[]
                for period in periods:
                    filter_vars_acts_temp=filter_periods_question(filter_vars_acts, period)
                    res.append(init(factor))
                    res[-1]=get(factor, res[-1], filter_vars_acts=filter_vars_acts_temp, check_vars_acts=check_vars_acts, nb_figures_cs=nb_figures_cs)
            else:
                res=init(factor)
                res=get(factor, res, filter_vars_acts=filter_vars_acts, check_vars_acts=check_vars_acts, nb_figures_cs=nb_figures_cs)
                
            write(factor, question, res, periods=periods)
                

def q115(factor="everything"):
    #Pourcentage d'actes avec 1/CommissionPE= LIBE 2/CommissionPE= JURI par cs et par année
    variable=("commission", "CommissionPE")
    init_question="Pourcentage d'actes avec "+variable[1]+"="
    
    variables=("LIBE", "JURI")
    exclude_vars_acts={variable[0]+"__in": [""]}

    if factor=="csyear":
        #get by cs and by year only (for specific cs)
        analyses, nb_figures_cs=get_specific_cs()

    for var in variables:
        question_temp=init_question+var
        check_vars_acts={variable[0]: var}
        for analysis, question in analyses:
            question=question_temp+question
            
            res=init(analysis)
            res=get(analysis, res, exclude_vars_acts=exclude_vars_acts, check_vars_acts=check_vars_acts, nb_figures_cs=nb_figures_cs)
            write(analysis, question, res)


def q119(factors=factors, periods=None, nb_figures_cs=2):
    #Pourcentage d'actes avec un vote public parmi les actes avec NbPointsB = 1,2,3 ou plus
    var="nb_point_b"
    filters=(
        ({var: 1}, "exactement un point B"),
        ({var: 2}, "exactement deux points B"),
        ({var+"__gt": 2}, "plus de deux points B")
    )
    
    #get parameters specific to the question
    factors_question, filter_vars_acts=get_parameters_question(factors, periods)
    
    init_question="Pourcentage d'actes avec un vote public, parmi les actes avec "
    check_vars_acts={"vote_public": True}

    for filt in filters:
        filter_vars_acts_temp=filter_vars_acts.copy()
        filter_vars_acts_temp.update(filt[0])
        init_question_2=init_question+filt[1]

        for factor, question in factors_question.iteritems():
            question=init_question_2+question

            if factor=="periods":
                res=[]
                for period in periods:
                    filter_vars_acts_temp_2=filter_vars_acts_temp.copy()
                    filter_vars_acts_temp_2.update(filter_periods_question(filter_vars_acts, period))
                    res.append(init(factor))
                    res[-1]=get(factor, res[-1], filter_vars_acts=filter_vars_acts_temp_2, check_vars_acts=check_vars_acts, nb_figures_cs=nb_figures_cs)
            else:
                res=init(factor)
                res=get(factor, res, filter_vars_acts=filter_vars_acts_temp, check_vars_acts=check_vars_acts, nb_figures_cs=nb_figures_cs)
                
            write(factor, question, res, periods=periods)


def list_acts(Model, search, cs, fields):
    if search=="cs":
        #List of acts with at least one code sectoriel "cs" -> display only the fields "fields"
        question="Liste des actes avec au moins un code sectoriel commençant par "+ cs +"."
    elif search=="bj":
        #List of acts with many bases juridiques -> for those acts, display only the fields "fields"
        question="Liste des actes avec plusieurs bases juridiques."
    acts=get_list_acts(Model, search, cs, fields)
    write_list_acts(question, acts, fields)


def q120():
    #Liste des actes pour lesquels au moins 1 CodeSect commence par 03 / 12 / 13 / 15
    list_acts(ActIds, "cs", "03", ["titre_rmc", "code_sect_1", "code_sect_2", "code_sect_3", "code_sect_4", "propos_origine", "resp_1", "resp_2", "resp_3", "cons_b", "cons_a"])
    list_acts(Act, "cs", "15", ["titre_rmc", "code_sect_1", "code_sect_2", "code_sect_3", "code_sect_4", "nb_point_b", "votes_for_1", "votes_for_2", "commission", "com_amdt_tabled", "com_amdt_adopt", "amdt_tabled", "amdt_adopt", "adopt_cs_contre", "adopt_cs_abs"])
    list_acts(Act, "cs", "12", ["titre_rmc", "code_sect_1", "code_sect_2", "code_sect_3", "code_sect_4", "nb_point_b", "votes_for_1", "votes_for_2", "commission", "com_amdt_tabled", "com_amdt_adopt", "amdt_tabled", "amdt_adopt", "adopt_cs_contre", "adopt_cs_abs"])
    list_acts(ActIds, "cs", "13", ["titre_rmc", "propos_origine", "dg_1", "dg_2", "commission", "votes_for_1", "votes_for_2", "votes_agst_1", "votes_agst_2", "votes_abs_1", "votes_abs_2", "adopt_cs_contre", "adopt_cs_abs", "np", "nb_mots", "duree_tot_depuis_trans_cons"])


def q121():
    #Liste des actes avec plusieurs bases juridiques
    list_acts(ActIds, "bj", "", ["titre_rmc", "base_j", "propos_origine", "dg_1", "dg_2", "commission", "votes_for_1", "votes_for_2", "votes_agst_1", "votes_agst_2", "votes_abs_1", "votes_abs_2", "adopt_cs_contre", "adopt_cs_abs", "np", "nb_mots", "duree_tot_depuis_trans_cons"])


def q122(factors=factors, periods=None):
    #Pourcentage d'actes avec au moins un EM sans statut 'M'

    #get the factors specific to the question
    factors_question=get_factors_question(factors)

    #~ init_question="Nombre d'actes avec au moins une présence de ministre (au moins un statut différent de 'NA' et 'AB')"
    #~ for factor, question in factors_question.iteritems():
        #~ question=init_question+question
        #~ res=init(factor, count=False)
        #~ res=get(factor, res, filter_vars_acts=filter_vars_acts, nb_figures_cs=nb_figures_cs, query="nb_attendances", count=False)
        #~ write(factor, question, res, count=False, percent=1)
    
    init_question="Pourcentage d'actes avec au moins un EM sans statut 'M' (et au moins un 'CS' ou 'CS_PR')"
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res=init(factor)
        res=get(factor, res, query="no_minister_percent", periods=periods)
        write(factor, question, res, periods=periods)

#~ 
    #~ init_question="Nombre d'actes avec au moins un EM sans statut 'M' (et au moins un 'CS' ou 'CS_PR')"
    #~ for factor, question in factors_question.iteritems():
        #~ question=init_question+question
        #~ res=init(factor, count=False)
        #~ res=get(factor, res, filter_vars_acts=filter_vars_acts, nb_figures_cs=nb_figures_cs, query="no_minister_nb_1", count=False)
        #~ write(factor, question, res, count=False, percent=1)

    #~ init_question="Nombre d'actes avec au moins deux EM sans statut 'M' (et au moins un 'CS' ou 'CS_PR')"
    #~ for factor, question in factors_question.iteritems():
        #~ question=init_question+question
        #~ res=init(factor, count=False)
        #~ res=get(factor, res, filter_vars_acts=filter_vars_acts, nb_figures_cs=nb_figures_cs, query="no_minister_nb_2", count=False)
        #~ write(factor, question, res, count=False, percent=1)


def q124(factors=factors, periods=None):
    #Nombre d'actes de type
    filter_vars_acts={}
    type_actes=[["CS DVE", "DVE"], ["CS DEC CAD", "CS DEC", "DEC", "DEC W/O ADD", "CS DEC W/O ADD"], ["CS REG", "REG"]]
    
    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)

    #for each type
    for type_acte in type_actes:
        init_question="Nombre d'actes de type "+str(type_acte)
        filter_vars_acts["type_acte__in"]=type_acte
        
        #for each factor
        for factor, question in factors_question.iteritems():
            question=init_question+question
            res=init(factor, count=False)
            res=get(factor, res, filter_vars_acts=filter_vars_acts, periods=periods, count=False)
            write(factor, question, res, periods=periods, count=False)


def list_dg_resp(var_name, nb):
    #init
    question="Liste des actes par annee et par "+var_name.upper()
    res=init(factor="year", empty_dic=True)

    #get
    res=get_list_acts_by_year_and_dg_or_resp(res, var_name, nb)

    #write
    write_list_acts_by_year_and_dg_or_resp(question, res)


def q129():
    #list of dgs
    list_dg_resp("dg", nb_dgs)
    #list of resps
    list_dg_resp("resp", nb_resps)


def q131(factors=factors, periods=None):
    #Nombre d’actes avec NoUniqueType=COD
    init_question="Nombre d’actes avec NoUniqueType=COD"
    filter_vars_acts_ids={"no_unique_type": "COD"}

    #get the factors specific to the question and update the periods (fr to us format)
    factors_question, periods=prepare_query(factors, periods)

    #for each factor
    for factor, question in factors_question.iteritems():
        question=init_question+question
        res=init(factor, count=False)
        res=get(factor, res, Model=ActIds, filter_vars_acts_ids=filter_vars_acts_ids, periods=periods, count=False)
        write(factor, question, res, periods=periods, count=False)
