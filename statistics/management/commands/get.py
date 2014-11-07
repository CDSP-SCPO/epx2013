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



def get_cs(cs):
    if cs[:2] in get_cs_list():
        cs=cs[:2]
    else:
        cs=None
    return cs

		

def get_act(Model, act):
    if Model==ActIds:
        act_act=act.act
    else:
        act_act=act
    return act_act



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
		if variable!=None:
			value=getattr(act, variable)
		if value not in excluded_values:
			ok=check_vars(act, check_vars_act, check_vars_act_ids)
			for nb in range(1,5):
				code_sect=getattr(act_act, "code_sect_"+str(nb))
				if code_sect!=None:
					cs=get_cs(code_sect.code_sect)
					if count:
						res[cs][1]+=1
						if variable!=None or ok:
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
		if variable!=None:
			value=getattr(act, variable)
		if value not in excluded_values:
			ok=check_vars(act, check_vars_act, check_vars_act_ids)
			if count:
				res[year][1]+=1
				if variable!=None or ok:
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
		if variable!=None:
			value=getattr(act, variable)
		if value not in excluded_values:
			ok=check_vars(act, check_vars_act, check_vars_act_ids)
			for nb in range(1,5):
				code_sect=getattr(act_act, "code_sect_"+str(nb))
				if code_sect!=None:
					cs=get_cs(code_sect.code_sect)
					year=str(act_act.releve_annee)
					if count:
						res[cs][year][1]+=1
						if variable!=None or ok:
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
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
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
        for nb in range(1,5):
            code_sect=getattr(act, "code_sect_"+str(nb))
            if code_sect!=None:
                cs=get_cs(code_sect.code_sect)
                year=str(act.releve_annee)

                #loop over each pers
                for nb in range(1, max_nb+1):
                    pers=getattr(act, pers_type+"_"+str(nb))
                    if pers!=None:
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
			if pers!=None:
				stat=get_stat(var, pers)
				res[year]["total"]+=1
				if stat not in res[year]:
					res[year][stat]=1
				else:
					res[year][stat]+=1
	print "res", res
    return res



def get_by_period(periods, nb_periods, res, Model, filter_vars, filter_total, exclude_vars={}, avg_variable=None, adopt_cs={}):
			
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
