#-*- coding: utf-8 -*-

#get the corresponding data for each variable and put them in a dictionary
from django.db import models
from act.models import Act, MinAttend, Status, NP, PartyFamily
from act_ids.models import ActIds
from django.db.models import Count
from  common import *
import copy



#count=False and variable=True: count the sum of all the values taken by a variable
    #e.g.: sum of all the values taken by duree_variable=1000 -> res=1000
#count=False and variable=False: count the number of occurences of items matching a set of criteria defined by filter_vars
    #e.g.: number of acts with a duree_variable greater than 0=5 -> res=5

#count=True and variable=True -> average computation: count the sum of all the values taken by a variable AND its number of occurences
    #e.g.: sum of all the values taken by duree_variable=1000, number of occurences of duree_variable=5 -> res=[1000, 5]
#count=True and variable=False -> percentage computation: count the number of occurences of items matching a set of criteria (defined by check_vars_act and check_vars_act_ids) AMONG the number of occurences of items matching the set of criteria (defined by filter_vars)
    #e.g.: number of occurences of duree_variable among the acts with no_unique_type=COD=5, number of acts with no_unique_type=COD=15 -> res=[5, 15]


#TODO
#~ filter_vars
#~ check_vars_act
#~ check_vars_act_ids



def get_cs(cs, nb_figures_cs):
    return cs[:nb_figures_cs]


def get_all_cs(act, nb_figures_cs=2):
    css=[]
    for nb in range(1,nb_cs+1):
        code_sect=getattr(act, "code_sect_"+str(nb))
        if code_sect is not None:
            cs=get_cs(code_sect.code_sect, nb_figures_cs)
            #nb_cs !=2 -> search for specific cs (e.g.: 19.10)
            if nb_figures_cs==2 or (nb_figures_cs !=2 and cs in cs_list):
                css.append(cs)
        else:
            #if one cs is null, all the following are null too
            break
    return css


def get_act(Model, act):
    #ActIds or MinAttend
    if Model!=Act:
        act=act.act
    return act


def check_vars(act, act_act, check_vars_act, check_vars_act_ids, adopt_var=None):
    for key, value in check_vars_act.iteritems():
            #greater than: "nb_lectures__gt": 1
            if key[-4:]=="__gt":
                if getattr(act_act, key[:-4])<=value:
                    return False
            #greater than or equal: "nb_lectures__gte": 1
            elif key[-5:]=="__gte":
                if getattr(act_act, key[:-5])<value:
                    return False
            elif getattr(act_act, key)!=value:
                return False
                
    for key, value in check_vars_act_ids.iteritems():
        if getattr(act, key)!=value:
            return False

    if adopt_var is not None:
        if not getattr(act, adopt_var).exists():
            return False
    
    return True


def get_division_res(act, num_vars, denom_vars, operation):
    res=0
    num=0
    denom=1

    #get the values of each variable for the act in parameter, for both the numerator and denominator
    values=[]
    values.append(getattr(act, num_vars[0]))
    values.append(getattr(act, denom_vars[0]))
    #2 variables in the numerator and 2 in the denominator
    if len(num_vars)==2:
        values.append(getattr(act, num_vars[1]))
        values.append(getattr(act, denom_vars[1]))
        
    #only one variable in the numerator and one in the denominator
    if len(num_vars)==1:
        #q111: Nombre moyen de EPComAmdtAdopt / EPComAmdtTabled
        num=values[0]
        denom=values[1]
    #2 variables in the numerator and 2 in the denominator
    else:
        #q106: Nombre moyen [(EPComAmdtAdopt+EPAmdtAdopt) / (EPComAmdtTabled+EPAmdtTabled)] 
        if operation=="+":
            num=values[0]+values[2]
            denom=values[1]+values[3]
        #q113: Nombre moyen de (amdt_adopt - com_amdt_adopt) / (amdt_tabled - com_amdt_tabled)
        else:
            num=values[0]-values[2]
            denom=values[1]-values[3]
        #~ #TEST
        #~ if num<0 or denom<0:
            #~ print "negative num or denom", act
        #if amdt=com_amdt (numerator or denominator = 0), 
        if denom==0 or num==0:
            #~ print "null num or denom", act
            num=values[0]
            denom=values[1]

    #if denom=0 -> 0    
    if denom!=0:
        res=float(num)/denom
    
    return res


def get_1_plus_2_res(vals):
    #~ print vals
    num=0
    denom=0

    for val in vals:
        if val>0:
            num+=val
            denom+=1

    value=float(num)/denom

    #~ print value
    
    return value
    

def get_all_pfs(act, pers_type, nb_pers):
    pfs=set()
    #get all rapps or resps
    for i in range(1, nb_pers+1):
        pers=getattr(act, pers_type+"_"+str(i))
        #no more rapp or resp
        if pers is None:
            break
        else:
            pf=PartyFamily.objects.get(country=pers.country, party=pers.party).party_family.strip().encode("utf-8")
            pfs.add(pf)
    return pfs


def compare_all_rapp_resp(act):
    pfs_rapp=get_all_pfs(act, "rapp", nb_rapp)
    pfs_resp=get_all_pfs(act, "resp", nb_resp)
    #same=True if all the rapps and resps have the same party family, False otherwise
    same=True

    #if there is at least one rapp and one resp
    if pfs_rapp and pfs_resp:
        for pf_rapp in pfs_rapp:
            #we have found at least two different parties -> exit the function
            if not same:
                break
            for pf_resp in pfs_resp:
                #if there are at least two different party families (one from the rapps, one from the resps)
                if pf_rapp!=pf_resp:
                    same=False
                    break
    return same

    
def copy_data_for_computation(analysis, res, act_act=None):
    year=None

    #copy data for computation
    if analysis in ["all", "cs", "country"]:
        res_temp=copy.copy(res)
    elif analysis in ["year", "csyear"]:
        year=str(act_act.releve_annee)
        res_temp=copy.copy(res[year])
        
    return res_temp, year


def compute(res_temp, value, count, variable=None, ok=None, same=None, adopt_var=None, res_total=None, act_act=None):
    #computation
    if count:
        res_temp[1]+=1
        #check discordance: if there are at least two different party families (one from the rapps, one from the resps)
        if same is not None:
            if not same:
                res_temp[0]+=value
        elif variable is not None or ok:
            res_temp[0]+=value
    else:
        if res_total is not None:
            res_total+=1
            
        #country factor
        if adopt_var is not None:
            countries=getattr(act_act, adopt_var)
            #for each country
            for country in countries.all():
                res_temp[country.country_code]+=value
        else:
            res_temp+=value

    return res_temp, res_total


def copy_data_back_to_res(analysis, res_temp, res=None, cs=None, year=None):
    #copy data back to res dictionary (for final result)
    res_temp=list(res_temp)
    if analysis in ["all", "country"]:
        res=res_temp
    elif analysis=="year":
        res[year]=res_temp
    elif analysis=="cs":
        res[cs]=res_temp
    elif analysis=="csyear":
        res[cs][year]=res_temp
    return res


def get_all_year(analysis, res, act_act, value, count, variable, ok, same):
    #copy data for computation
    res_temp, year=copy_data_for_computation(analysis, res, act_act)
    #computation
    res_temp, res_total=compute(res_temp, value, count, variable, ok, same)
    #copy data back to res dictionary (for final result)
    res=copy_data_back_to_res(analysis, res_temp, res, year=year)
    return res


def get_countries(analysis, res, value, count, adopt_var, res_total, act_act):
    #copy data for computation
    res_temp, year=copy_data_for_computation(analysis, res)
    #computation
    res_temp, res_total=compute(res_temp, value, count, adopt_var=adopt_var, res_total=res_total, act_act=act_act)
    #copy data back to res dictionary (for final result)
    res=copy_data_back_to_res(analysis, res_temp)
    return res_temp, res_total


def get_cs_csyear(analysis, res, act_act, value, count, variable, ok, same, nb_figures_cs):
    #get all cs
    css=get_all_cs(act_act, nb_figures_cs=nb_figures_cs)
    
    #if there is at least one non null css
    #for each cs
    for cs in css:
        #TEST
        if act_act.releve_annee==2008 and cs=="19.20":
            print act_act, act_act.votes_agst_1, act_act.votes_agst_2
        #copy data for computation
        res_temp, year=copy_data_for_computation(analysis, res[cs], act_act)
        #computation
        res_temp, res_total=compute(res_temp, value, count, variable, ok, same)
        #copy data back to res dictionary (for final result)
        res=copy_data_back_to_res(analysis, res_temp, res, cs=cs, year=year)

    return res


def check_var1_var2(val_1, val_2):
    if val_1 in [None, 0] and val_2 in [None, 0]:
        return False
    return True
    

def get(analysis, res, num_vars=None, denom_vars=None, count=True, Model=Act, variable=None, variable_2=None, excluded_values=[None, ""], filter_vars_acts={}, exclude_vars_acts={},check_vars_acts={}, check_vars_act_ids={}, query=None, operation=None, adopt_var=None, nb_figures_cs=2, res_total=None):
    same=None
    filter_vars=get_validated_acts(Model, filter_vars_acts=filter_vars_acts)

    for act in Model.objects.filter(**filter_vars).exclude(**exclude_vars_acts):
        ok=True
        act_act=get_act(Model, act)
        value=1
        if variable is not None:
            value=getattr(act, variable)
            if variable_2 is not None:
                value_2=getattr(act, variable_2)
                ok=check_var1_var2(value, value_2)
        if value not in excluded_values and ok:
            ok=check_vars(act, act_act, check_vars_acts, check_vars_act_ids, adopt_var)
            
            #division mode, res=num/denom -> q111: #Nombre moyen de EPComAmdtAdopt / EPComAmdtTabled
            if num_vars is not None:
                value=get_division_res(act_act, num_vars, denom_vars, operation)
            #"1+2" with at least one non null value -> q100: Moyenne EPVotesFor1-2
            elif variable_2 is not None:
                value=get_1_plus_2_res([value, value_2])
            #get percentage of different political families for rapp1 and resp1
            elif query=="discordance":
                same=compare_all_rapp_resp(act_act)

            if analysis in ["all", "year"]:
                res=get_all_year(analysis, res, act_act, value, count, variable, ok, same)
            elif analysis=="country":
                res, res_total=get_countries(analysis, res, value, count, adopt_var, res_total, act_act)
            elif analysis in ["cs", "csyear"]:
                res=get_cs_csyear(analysis, res, act_act, value, count, variable, ok, same, nb_figures_cs)

    print "res", res
    if res_total is not None:
        return res, res_total
    return res

    
def get_month(res, variable, count=True, filter_variables={}):
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



def get_list_acts_cs(cs, Model=Act):
    acts=[]
    #get validated acts only
    filter_vars=get_validated_acts(Model)

    #~ #get all the acts that match the cs in parameter (each act can be counted up to 4 times, one for each matching cs)
    for act in Model.objects.filter(**filter_vars):
        act_act=get_act(Model, act)
        #get all cs
        css=get_all_cs(act_act)
        #for each cs (if there is at least one non null css)
        for cs in css:
            acts.append(act)

    print "get_list_acts_cs", acts

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
            #greater than: "nb_point_a__gt": 0
            elif key[-4:]=="__gt":
                if getattr(instance, key[:-4])<=value:
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


def init_by_period(Model, periods, filter_vars, list_acts, exclude_vars):
    filter_vars_periods=get_validated_acts_periods(Model, periods, filter_vars)
    if list_acts is None:
        temp_filter=Model.objects.filter(**filter_vars_periods).exclude(**exclude_vars)
    #for a specific cs
    else:
        #from the list of acts with a specific cs, create a new list taking into account other filters / excludes
        temp_filter=filter_exclude_list(list_acts, filter_vars=filter_vars_periods, exclude_vars=exclude_vars)
    return temp_filter

    
def compute_min_attend(res, index, temp_filter):
    for act in temp_filter:
        #~ print act.id
        status=Status.objects.get(verbatim=act.verbatim, country=act.country).status
        if status not in ["NA", "AB"]:
            res[index][1]+=1
            if status in ["CS", "CS_PR"]:
                res[index][0]+=1
    return res


def compute_country(res, index, temp_filter, total, adopt_cs):
    for act in temp_filter:
        total[index]+=1
        countries=getattr(act, adopt_cs)
        #for each country
        for country in countries.all():
            res[index][country.country_code]+=1
    return res


def compute_adopt_cs(res, index, temp_filter, adopt_cs):
    res[index][0]=temp_filter.annotate(nb_countries=Count("adopt_cs_contre")).filter(**adopt_cs).count()
    #OR specific cs
    #~ key, value = adopt_cs.items()[0]
    #~ for act in temp_filter:
        #~ nb_countries=len(act.adopt_cs_contre.all())
        #~ #"nb_countries": 1 or "nb_countries__gte": 2
        #~ if (key=="nb_countries" and nb_countries==value) or (key=="nb_countries__gte" and nb_countries>=value):
            #~ res[index][0]+=1
    return res


def compute_total(res, index, filter_total, Model, periods, list_acts):
    #total
    filter_total.update(get_validated_acts_periods(Model, periods[index], filter_total))
    if list_acts is None:
        res[index][1]=Model.objects.filter(**filter_total).count()
    else:
        res[index][1]=len(filter_exclude_list(list_acts, filter_vars=filter_total))
    return res


def compute_avg(res, index, temp_filter, avg_variable):
    for act in temp_filter:
        res[index][0]+=getattr(act, avg_variable)
        res[index][1]+=1
    return res
    

def get_by_period(res, filter_vars, filter_total, list_acts=None, res_total=None, Model=Act, exclude_vars_acts={}, avg_variable=None, adopt_cs={}, query=None):
    #list_acts used when query for specific cs
    for index in range(nb_periods):
        temp_filter=init_by_period(Model, periods[index], filter_vars, list_acts, exclude_vars_acts)

        if Model==MinAttend:
           res=compute_min_attend(res, index, temp_filter)
                        
        #q114: 1/pourcentage de AdoptCSContre et 2/pourcentage de AdoptCSAbs pour chaque Etat membre, par périodes
        elif query=="country":
          res=compute_country(res, index, temp_filter, res_total, adopt_cs)
          
        else:
            #percentage among all the acts
            if avg_variable is None:
                if adopt_cs:
                   res=compute_adopt_cs(res, index, temp_filter, adopt_cs)
                else:
                    if list_acts is None:
                        res[index][0]=temp_filter.count()
                    else:
                        res[index][0]=len(temp_filter)
                #total
                res=compute_total(res, index, filter_total, Model, periods, list_acts)
            #average
            else:
                res=compute_avg(res, index, temp_filter, avg_variable)
                    
    print "res", res
    if query=="country":
        return res, res_total
    return res
