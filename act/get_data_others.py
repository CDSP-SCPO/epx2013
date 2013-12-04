#-*- coding: utf-8 -*-
#for accents between comments inside this file
"""
get government composition from the file Composition politique gvts nationaux 93-12.csv (NationGvtPoliticalComposition) and opal variables
"""
from act.models import GvtCompo
from import_app.models import ImportNP
from common.functions import date_string_to_iso
from bs4 import BeautifulSoup
import re


def get_date(soup):
	"""
	FUNCTION
	get the date of the act (used for gvt_compo when ProposOrigine=EM) from the eurlex url
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	RETURN
	titre_en [string]
	"""
	try:
		return date_string_to_iso(soup.find("h2", text="Dates").find_next("ul").find(text=re.compile("of document")).strip()[-10:])
	except Exception, e:
		print "no date gvt_compo!", e
		return None

#right under "Title and reference"
#not NULL


def link_act_gvt_compo(soup, act_ids, act):
	"""
	FUNCTION
	fill the assocation table which links an act to its governments composition
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	act_ids: instance of the ids of the act [ActIds model instance]
	act: instance of an act [Act model instance]
	RETURN
	None
	"""
	#retrieve all the rows from GvtCompo for which start_date<adoptionConseil<end_date
	date=None
	if act.adopt_conseil!=None:
		date=act.adopt_conseil
	elif act.sign_pecs!=None:
		#if no adopt_conseil, take sign_pecs
		date=act.sign_pecs
	elif act_ids.propos_origine in["EM", "CONS", "BCE", "CJUE"]:
		date=get_date(soup)

	if date==None:
		return None

	gvt_compos=GvtCompo.objects.filter(start_date__lte=date, end_date__gte=date)
	#fill the association
	for gvt_compo in gvt_compos:
		try:
			act.gvt_compo.add(gvt_compo)
		except Exception, e:
			print "gvt compo already exists!", e
	else:
		print "gvt compo: no matching date"


def link_get_act_opal(act_ids, act):
	"""
	FUNCTION
	fill the table which links an act to its opal variables
	PARAMETERS
	act_ids: instance of the ids of the act [ActIds model instance]
	act: instance of the act [Act model instance]
	RETURN
	opal_dic: opal variables [dictionary]
	"""
	opal_dic={}

	#Are there matches in the ImportOpal table?
	opals=ImportNP.objects.defer("no_celex").filter(no_celex=act_ids.no_celex)

	for opal in opals:
		#store data
		country=opal.np
		#initialization
		if country not in opal_dic:
			opal_dic[country]={"act_type": "", "act_date": "", "case_nb": ""}
		opal_dic[country]["act_type"]+=opal.act_type+"; "
		opal_dic[country]["act_date"]+=str(opal.act_date)+"; "
		opal_dic[country]["case_nb"]+=str(opal.case_nb)+"; "

		try:
			#save opal instances
			fields={"case_nb": opal.case_nb, "np": Country.objects.get(pk=opal.np), "act_type": opal.act_type, "act_date": opal.act_date , "act": act}
			NP.objects.create(**fields)
		except Exception, e:
			print "opal varibles already saved!", e

	#remove last "; "
	for country in opal_dic:
		for field in opal_dic[country]:
			opal_dic[country][field]=opal_dic[country][field][:-2]

	return opal_dic



def get_data_others(soup, act_ids, act):
	"""
	FUNCTION
	link the government composition of each European country at the time of the act (given in parameter) and get the opal variables
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	act_ids: instance of the ids of the act [ActIds model instance]
	act: instance of the data of the act [Act model instance]
	RETURN
	opal variables [dictionary]
	"""

	#TEST ONLY -> TO REMOVE
	#~ act.adopt_conseil="2012-02-21"
	link_act_gvt_compo(soup, act_ids, act)
	for gvt_compo in act.gvt_compo.all():
		print "gvt_compo_country:", gvt_compo.country.country_code
		partys=""
		for party in gvt_compo.party.all():
			partys+=party.party+"; "
		print "gvt_compo_partys:", partys[:-2]

	#opal
	return link_get_act_opal(act_ids, act)
