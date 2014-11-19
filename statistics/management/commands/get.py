#-*- coding: utf-8 -*-

#get the corresponding data for each variable and put them in a dictionary
from django.db import models
from act.models import Act, MinAttend, Status, NP, PartyFamily
from act_ids.models import ActIds
from django.db.models import Count
from  common import *



#count=False and variable=True: count the sum of all the values taken by a variable
    #e.g.: sum of all the values taken by duree_variable=1000 -> res=1000
#count=False and variable=False: count the number of occurences of items matching a set of criteria defined by filter_vars
    #e.g.: number of acts with a duree_variable greater than 0=5 -> res=5

#count=True and variable=True -> average computation: count the sum of all the values taken by a variable AND its number of occurences
    #e.g.: sum of all the values taken by duree_variable=1000, number of occurences of duree_variable=5 -> res=[1000, 5]
#count=True and variable=False -> percentage computation: count the number of occurences of items matching a set of criteria (defined by check_vars_act and check_vars_act_ids) AMONG the number of occurences of items matching the set of criteria (defined by filter_vars)
    #e.g.: number of occurences of duree_variable among the acts with no_unique_type=COD=5, number of acts with no_unique_type=COD=15 -> res=[5, 15]


nb_cs=4


def get_cs(cs, min_cs=1, max_cs=20):
    #check that the cs given in parameter is part of the cs_list whose boundaries are defined by min_cs and max_cs (usually between 1 and 20)
    cs_int=int(cs[:2])
    if min_cs <= cs_int <= max_cs:
        return cs[:2]
    return None


def get_act(Model, act):
    #ActIds or MinAttend
    if Model!=Act:
        act=act.act
    return act


def check_vars(act_ids, check_vars_act, check_vars_act_ids):
    for key, value in check_vars_act.iteritems():
        if getattr(act_ids.act, key)!=value:
            return False
    for key, value in check_vars_act_ids.iteritems():
        if getattr(act_ids, key)!=value:
            return False
    return True


def get_by_cs(res, count=True, Model=Act, variable=None, excluded_values=[None], filter_vars={}, check_vars_act={}, check_vars_act_ids={}):
    filter_vars=get_validated_acts(Model, filter_vars)
    for act in Model.objects.filter(**filter_vars):
        act_act=get_act(Model, act)
        value=1
        if variable is not None:
            value=getattr(act, variable)
        if value not in excluded_values:
            ok=check_vars(act, check_vars_act, check_vars_act_ids)
            for nb in range(1,nb_cs+1):
                code_sect=getattr(act_act, "code_sect_"+str(nb))
                if code_sect is not None:
                    cs=get_cs(code_sect.code_sect)
                    if count:
                        res[cs][1]+=1
                        if variable is not None or ok:
                            res[cs][0]+=value
                    else:
                        res[cs]+=value

    print "res", res
    return res


def get_by_year(res, count=True, Model=Act, variable=None, excluded_values=[None], filter_vars={}, check_vars_act={}, check_vars_act_ids={}):
    filter_vars=get_validated_acts(Model, filter_vars)
    for act in Model.objects.filter(**filter_vars):
        act_act=get_act(Model, act)
        year=str(act_act.releve_annee)
        value=1
        if variable is not None:
            value=getattr(act, variable)
        if value not in excluded_values:
            ok=check_vars(act, check_vars_act, check_vars_act_ids)
            if count:
                res[year][1]+=1
                if variable is not None or ok:
                    res[year][0]+=value
            else:
                res[year]+=value

    print "res", res
    return res


def get_by_month(res, variable, count=True, filter_variables={}):
    for act_id in ActIds.objects.filter(src="index", act__validated=2, **filter_variables):
        act=act_id.act
        value=getattr(act, variable)
        if value>0:
            month=str(act.releve_mois)
            if count:
                res[month][1]+=1
                res[month][0]+=value
            else:
                res[month]+=value

    print "res", res
    return res


def get_by_cs_year(res, count=True, Model=Act, variable=None, excluded_values=[None], total_year=False, filter_vars={}, check_vars_act={}, check_vars_act_ids={}):
    filter_vars=get_validated_acts(Model, filter_vars)
    for act in Model.objects.filter(**filter_vars):
        act_act=get_act(Model, act)
        value=1
        if variable is not None:
            value=getattr(act, variable)
        if value not in excluded_values:
            ok=check_vars(act, check_vars_act, check_vars_act_ids)
            for nb in range(1,nb_cs+1):
                code_sect=getattr(act_act, "code_sect_"+str(nb))
                if code_sect is not None:
                    cs=get_cs(code_sect.code_sect)
                    year=str(act_act.releve_annee)
                    if count:
                        res[cs][year][1]+=1
                        if variable is not None or ok:
                            res[cs][year][0]+=value
                        if total_year:
                            total_year[year]+=value
                    else:
                        res[cs][year]+=value
    print "res", res
    if total_year:
        print "total_year", total_year
        return res, total_year
    return res


def get_list_pers_cs(res, pers_type, max_nb, year_var=False, filter_variables={}):
    for act_ids in ActIds.objects.filter(act__validated=2, src="index", **filter_variables):
        act=act_ids.act
        #loop over each cs
        for nb in range(1,nb_cs+1):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect is not None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)

                #loop over each pers
                for nb in range(1, max_nb+1):
                    pers=getattr(act, pers_type+"_"+str(nb))
                    #by cs and by year
                    if year_var:
                        if pers not in [None, 0]:
                            if pers not in res[cs][year]:
                                res[cs][year][pers]=1
                            else:
                                res[cs][year][pers]+=1
                    #by cs
                    else:
                        if pers not in [None, 0]:
                            if pers not in res[cs]:
                                res[cs][pers]=1
                            else:
                                res[cs][pers]+=1
    return res


def get_list_pers_year(res, pers_type, max_nb, filter_variables={}):
    for act_ids in ActIds.objects.filter(act__validated=2, src="index", **filter_variables):
        act=act_ids.act
        year=str(act.releve_annee)
        #loop over each pers
        for nb in range(1, max_nb+1):
            pers=getattr(act, pers_type+"_"+str(nb))
            if pers not in [None, 0]:
                if pers not in res[year]:
                    res[year][pers]=1
                else:
                    res[year][pers]+=1
    return res


def get_pf(pers):
    return PartyFamily.objects.get(country=pers.country, party=pers.party).party_family.encode("utf-8")


def get_stat(var, pers):
    #statistics on party family
    if var=="pf":
        stat=get_pf(pers)
    #statistics on country
    else:
        stat=pers.country.country_code
    return stat


def get_percent_pers_cs(res, pers_type, max_nb, var="pf", year_var=False, filter_vars={}):
    #percentage of each party family or country for Rapporteurs and RespPropos
    #cs only / cs and year
    filter_vars=get_validated_acts(ActIds, filter_vars)
    for act_ids in ActIds.objects.filter(**filter_vars):
        act=act_ids.act
        #loop over each cs
        for nb in range(1,nb_cs+1):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect is not None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)

                #loop over each pers
                for nb in range(1, max_nb+1):
                    pers=getattr(act, pers_type+"_"+str(nb))
                    if pers is not None:
                        stat=get_stat(var, pers)
                        #by cs and by year
                        if year_var:
                            res[cs][year]["total"]+=1
                            if stat not in res[cs][year]:
                                res[cs][year][stat]=1
                            else:
                                res[cs][year][stat]+=1
                        #by cs
                        else:
                            res[cs]["total"]+=1
                            if stat not in res[cs]:
                                res[cs][stat]=1
                            else:
                                res[cs][stat]+=1
    print "res", res
    return res


def get_percent_pers_year(res, pers_type, max_nb, var="pf", filter_vars={}):
    #percentage of each party family or country for Rapporteurs and RespPropos
    #year only
    filter_vars=get_validated_acts(ActIds, filter_vars)
    for act_ids in ActIds.objects.filter(**filter_vars):
        act=act_ids.act
        year=str(act.releve_annee)
        #loop over each pers
        for nb in range(1, max_nb+1):
            pers=getattr(act, pers_type+"_"+str(nb))
            if pers is not None:
                stat=get_stat(var, pers)
                res[year]["total"]+=1
                if stat not in res[year]:
                    res[year][stat]=1
                else:
                    res[year][stat]+=1
    print "res", res
    return res



def get_by_period(res, Model, filter_vars, filter_total, exclude_vars={}, avg_variable=None, adopt_cs={}):
    for index in range(nb_periods):
        filter_vars_periods=get_validated_acts_periods(Model, periods[index], filter_vars)
        temp_filter=Model.objects.filter(**filter_vars_periods).exclude(**exclude_vars)

        if Model==MinAttend:
            for act in temp_filter:
                #~ print act.id
                status=Status.objects.get(verbatim=act.verbatim, country=act.country).status
                if status not in ["NA", "AB"]:
                    res[index][1]+=1
                    if status in ["CS", "CS_PR"]:
                        res[index][0]+=1
        else:
            #percentage among all the acts
            if avg_variable is None:
                if adopt_cs:
                    res[index][0]=temp_filter.annotate(nb_countries=Count("adopt_cs_contre")).filter(**adopt_cs).count()
                else:
                    res[index][0]=temp_filter.count()
                #total
                filter_total.update(get_validated_acts_periods(Model, periods[index], filter_total))
                res[index][1]=Model.objects.filter(**filter_total).count()
            #average
            else:
                for act in temp_filter:
                    res[index][0]+=getattr(act, avg_variable)
                    res[index][1]+=1
    return res


def get_list_acts_cs(cs, Model=Act):
    acts=[]
    #get validated acts only
    filter_vars=get_validated_acts(Model)

    #~ #get all the acts that match the cs in parameter (each act can be counted up to 4 times, one for each matching cs)
    for act in Model.objects.filter(**filter_vars):
        act_act=get_act(Model, act)
        #loop over each cs
        for nb in range(1,nb_cs+1):
            code_sect=getattr(act_act, "code_sect_"+str(nb))
            if code_sect is not None:
                cs_filter=get_cs(code_sect.code_sect, min_cs=cs, max_cs=cs)
                #if the cs corresponds to the cs in parameter
                if cs_filter is not None:
                    acts.append(act)
            else:
                #if one cs is null, all the following are null too
                break

    return acts


def filter_exclude_list(list_acts, filter_vars={}, exclude_vars={}):
    list_acts_new=[]
    for act in list_acts:
        ok=True
        for key, value in filter_vars.iteritems():
            #related object: "act__validated_attendance":1
            if key[:5]=="act__":
                key=key[5:]
                instance=act.act
            else:
                instance=act

            #greater than or equal: "nb_point_a__gte": 1
            if key[-5:]=="__gte":
                if getattr(instance, key[:-5])<value:
                    ok=False
                    break
            #greater than or equal: "nb_point_a__lte": 1
            elif key[-5:]=="__lte":
                if getattr(instance, key[:-5])>value:
                    ok=False
                    break

            elif key[-8:]=="__isnull":
                var=getattr(instance, key[:-8])
                #"com_amdt_tabled__isnull": False
                if not value and var is None:
                    ok=False
                    break
                #"nb_point_b__isnull": True
                elif value and var is not None:
                    ok=False
                    break
            #equal to: "nb_point_a": 1
            elif getattr(instance, key) != value:
                ok=False
                break

        if ok:
            for key, value in exclude_vars.iteritems():
                #"adopt_cs_abs": None
                if key=="adopt_cs_abs" and value is None:
                    if not getattr(instance, key).exists():
                        ok=False
                        break
                #different from: "nb_point_a": 1
                elif getattr(instance, key) == value:
                    ok=False
                    break

            if ok:
                list_acts_new.append(act)

    return list_acts_new


def get_by_period_cs(list_acts, periods, nb_periods, res, Model, filter_vars, filter_total, exclude_vars={}, avg_variable=None, adopt_cs={}):
    for index in range(nb_periods):
        filter_vars_periods=get_validated_acts_periods(Model, periods[index], filter_vars)
        #from the list of acts with a specific cs, create a new list taking into account other filters / excludes
        list_acts_new=filter_exclude_list(list_acts, filter_vars=filter_vars_periods, exclude_vars=exclude_vars)

        if Model==MinAttend:
            for act in list_acts_new:
                #~ print act.id
                status=Status.objects.get(verbatim=act.verbatim, country=act.country).status
                if status not in ["NA", "AB"]:
                    res[index][1]+=1
                    if status in ["CS", "CS_PR"]:
                        res[index][0]+=1
        else:
            #percentage among all the acts
            if avg_variable is None:
                if adopt_cs:
                    key, value = adopt_cs.items()[0]
                    for act in list_acts_new:
                        nb_countries=len(act.adopt_cs_contre.all())
                        #"nb_countries": 1 or "nb_countries__gte": 2
                        if (key=="nb_countries" and nb_countries==value) or (key=="nb_countries__gte" and nb_countries>=value):
                            res[index][0]+=1
                else:
                    res[index][0]=len(list_acts_new)
                #total
                filter_total.update(get_validated_acts_periods(Model, periods[index], filter_total))
                res[index][1]=len(filter_exclude_list(list_acts, filter_vars=filter_total))
            #average
            else:
                for act in list_acts_new:
                    res[index][0]+=getattr(act, avg_variable)
                    res[index][1]+=1
    return res
