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
            if code_sect is not None:
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
            if code_sect is not None:
                cs=get_cs(code_sect.code_sect)
                res[cs][str(act.releve_annee)]+=1
    print "res", res

    write_cs_year(question, res)



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
                if code_sect is not None:
                    total_year[year]+=1
                    cs=get_cs(code_sect.code_sect)
                    res[cs][year]+=1
    print "res", res

    write_cs_year(question, res, total_year=total_year, percent=100)



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
    #~ count=0

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
                        #~ if nb_bj==0:
                            #~ print act.releve_annee, act.releve_mois, act.no_ordre, act.nb_point_b, act.base_j, act.code_sect_1_id, act.code_sect_2_id, act.code_sect_3_id, act.code_sect_4_id, act.validated
                            #~ count+=1
                        break

    print "res", res
    #~ print "count", count

    writer.writerow([question])
    writer.writerow(["", "CS="+name, "Tous les CS"])
    writer.writerow(["Une BJ", res[0][0], res[0][1]])
    writer.writerow(["Plusieurs BJ", res[1][0], res[1][1]])
    writer.writerow("")
    print ""


def q61():
    question="Nombre d'actes avec un vote public"
    nb_bj_cs("13", "Marché intérieur", "vote_public", "bool", question)


def q71(cs=None):
    #actes pour lesquels ProposOrigine="COM" et ComProc="Written procedure"
    question="Pourcentage d'actes provenant de la Commission et adoptés par procédure écrite"
    Model=ActIds
    filter_vars_acts={"com_proc": "Written procedure"}
    filter_vars_acts_ids={"propos_origine": "COM"}
    periods, nb_periods, res, filter_vars, filter_total=init_periods(Model, filter_vars_acts, filter_vars_acts_ids=filter_vars_acts_ids)

    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel: "+cs[1]+")"
        list_acts_cs=get_list_acts_cs(cs[0], Model=Model)
        res=get_by_period_cs(list_acts_cs, periods, nb_periods, res, Model, filter_vars, filter_total)
    else:
        res=get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total)

    write_periods(question, res, periods, nb_periods)


def q72(cs=None):
    question="Pourcentage d'actes avec au moins un point A"
    Model=Act
    filter_vars_acts={"nb_point_a__gte": 1}
    periods, nb_periods, res, filter_vars, filter_total=init_periods(Model, filter_vars_acts)

    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel: "+cs[1]+")"
        list_acts_cs=get_list_acts_cs(cs[0], Model=Model)
        res=get_by_period_cs(list_acts_cs, periods, nb_periods, res, Model, filter_vars, filter_total)
    else:
        res=get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total)

    write_periods(question, res, periods, nb_periods)


def q74(cs=None):
    question="Pourcentage d'actes adoptés en 1ère lecture parmi les actes de codécision"
    Model=ActIds
    filter_total_act_ids={"no_unique_type": "COD"}
    filter_vars_acts={"nb_lectures": 1}
    filter_vars_acts_ids=filter_total_act_ids.copy()
    periods, nb_periods, res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts, filter_vars_acts_ids=filter_vars_acts_ids, filter_total_acts_ids=filter_total_act_ids)

    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel: "+cs[1]+")"
        list_acts_cs=get_list_acts_cs(cs[0], Model=Model)
        res=get_by_period_cs(list_acts_cs, periods, nb_periods, res, Model, filter_vars, filter_total)
    else:
        res=get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total)

    write_periods(question, res, periods, nb_periods)


def q77(cs=None):

    Model=Act
    filter_total_acts={"adopt_cs_regle_vote": "V"}
    filter_vars_acts=filter_total_acts.copy()
    filter_var_acts_vote=filter_total_acts.copy()
    filter_var_acts_vote["vote_public"]=True
    if cs is not None:
        list_acts_cs=get_list_acts_cs(cs[0], Model=Model)

    question="Pourcentage d’actes adoptés avec un vote public, parmi les actes avec une majorité qualifiée lors de l'adoption au conseil"
    periods, nb_periods, res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_var_acts_vote, filter_total_acts=filter_total_acts)
    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel: "+cs[1]+")"
        res=get_by_period_cs(list_acts_cs, periods, nb_periods, res, Model, filter_vars, filter_total)
    else:
        res=get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total)
    write_periods(question, res, periods, nb_periods)

    question="Pourcentage d’actes adoptés avec avec opposition d'exactement un état, parmi les actes avec une majorité qualifiée lors de l'adoption au conseil"
    periods, nb_periods, res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts, filter_total_acts=filter_total_acts)
    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel: "+cs[1]+")"
        res=get_by_period_cs(list_acts_cs, periods, nb_periods, res, Model, filter_vars, filter_total, adopt_cs={"nb_countries": 1})
    else:
        res=get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total, adopt_cs={"nb_countries": 1})
    write_periods(question, res, periods, nb_periods)

    question="Pourcentage d’actes adoptés avec opposition d'au moins deux états, parmi les actes avec une majorité qualifiée lors de l'adoption au conseil"
    periods, nb_periods, res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts, filter_total_acts=filter_total_acts)
    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel: "+cs[1]+")"
        res=get_by_period_cs(list_acts_cs, periods, nb_periods, res, Model, filter_vars, filter_total, adopt_cs={"nb_countries__gte": 2})
    else:
        res=get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total, adopt_cs={"nb_countries__gte": 2})
    write_periods(question, res, periods, nb_periods)

    question="Pourcentage d’actes adoptés avec abstention d'au moins un état, parmi les actes avec une majorité qualifiée lors de l'adoption au conseil"
    periods, nb_periods, res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts, filter_total_acts=filter_total_acts)
    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel: "+cs[1]+")"
        res=get_by_period_cs(list_acts_cs, periods, nb_periods, res, Model, filter_vars, filter_total, exclude_vars={"adopt_cs_abs": None})
    else:
        res=get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total, exclude_vars={"adopt_cs_abs": None})
    write_periods(question, res, periods, nb_periods)


def q79(cs=None):
    question="Pourcentage d’actes adoptés en 2ème lecture parmi les actes de codécision"
    Model=ActIds
    filter_total_act_ids={"no_unique_type": "COD"}
    filter_vars_acts={"nb_lectures": 2}
    filter_vars_acts_ids=filter_total_act_ids.copy()
    periods, nb_periods, res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts, filter_vars_acts_ids=filter_vars_acts_ids, filter_total_acts_ids=filter_total_act_ids)

    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel: "+cs[1]+")"
        list_acts_cs=get_list_acts_cs(cs[0], Model=Model)
        res=get_by_period_cs(list_acts_cs, periods, nb_periods, res, Model, filter_vars, filter_total)
    else:
        res=get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total)

    write_periods(question, res, periods, nb_periods)


def q80(cs=None):
    question="Pourcentage d’actes avec au moins un point B"
    Model=Act
    filter_vars_acts={"nb_point_b__gte": 1}
    periods, nb_periods, res, filter_vars, filter_total=init_periods(Model, filter_vars_acts=filter_vars_acts)

    #filter by specific cs
    if cs is not None:
        question+=" (code sectoriel: "+cs[1]+")"
        list_acts_cs=get_list_acts_cs(cs[0], Model=Model)
        res=get_by_period_cs(list_acts_cs, periods, nb_periods, res, Model, filter_vars, filter_total)
    else:
        res=get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total)

    write_periods(question, res, periods, nb_periods)



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

