# -*- coding: utf-8 -*-
"""
get the data from Oeil (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
import urllib


def get_commission(soup):
	"""
	FUNCTION
	get the commission variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	commission
	"""
	try:
		commission=soup.find(text="Committee responsible").findNext("acronym")
		if commission.get_text()=="DELE":
			return commission.findNext("acronym").get_text()
		else:
			return commission.get_text()
	except:
		#~ print "no commissionPE! (oeil)"
		return None

#Acronym under "Committee responsible"
#can be NULL


#~ http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2005/0017(COD)
def get_vote_page(soup):
	"""
	FUNCTION
	get the html page about votes from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	html page about votes
	"""
	try:
		link_votes=soup.find(text="Results of vote in Parliament").findNext("td").find("a")["href"]
		return BeautifulSoup(urllib.urlopen("http://www.europarl.europa.eu/"+link_votes))
	except:
		print "no vote page (oeil)"
		return None


def get_com_amdt_tabled(soup):
	"""
	FUNCTION
	get the com_amdt_tabled variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	com_amdt_tabled
	"""
	try:
		return soup.find(text="EP Committee").findNext('td').get_text()
	except:
		print "no com_amdt_tabled!"
		return None

#on vote page:
#Last table "Amendments adopted in plenary": EP Committee (row) and Tabled by (column)


def get_com_amdt_adopt(soup):
	"""
	FUNCTION
	get the com_amdt_adopt variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	com_amdt_adopt
	"""
	try:
		return soup.find(text="EP Committee").findNext('td').findNext('td').get_text()
	except:
		print "no com_amdt_adopt"
		return None

#on vote page:
#Last table "Amendments adopted in plenary": EP Committee (row) and Adopted (column)


def get_amdt_tabled(soup):
	"""
	FUNCTION
	get the amdt_tabled variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	amdt_tabled
	"""
	try:
		return soup.find(text="Total").findNext('th').get_text()
	except:
		print "no amdt_tabled"
		return None


def get_amdt_adopt(soup):
	"""
	FUNCTION
	get the amdt_adopt variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	amdt_adopt
	"""
	try:
		return soup.find(text="Total").findNext('th').findNext('th').get_text()
	except:
		print "no amdt_adopt"
		return None


def get_vote_tables(soup):
	"""
	FUNCTION
	get the two tables Final vote and final vote part two from the vote page
	PARAMETERS
	soup: vote page url content
	RETURN
	list with two elements: the first and second table (empty if does not exist)
	"""
	#<td class="rowtitle">Final vote&nbsp;20/10/2010</td>
	#<td class="rowtitle">Final vote Part two</td>
	vote_tables=[None]*2
	try:
		vote_tables_temp=soup.findAll("td", {"class": "rowtitle"})
		vote_tables[0]=vote_tables_temp[0].findNext("table").find("table")
		vote_tables[1]=vote_tables_temp[1].findNext("table").find("table")
		#~ print "vote_tables[0]", vote_tables[0]
		#~ print "vote_tables[1]", vote_tables[1]
		return vote_tables
	except:
		#~ print "no table of vote! (oeil)"
		return vote_tables


def get_vote(vote_table, vote):
	"""
	FUNCTION
	get the vote variable For, Against or Abstentions from one of the two vote tables
	PARAMETERS
	vote_table: html content of the first or second vote table
	vote="For", "Against" or "Abstentions"
	RETURN
	one of the following vote variables: get_votesFor1, votes_agst_1, votes_abs_1, get_votesFor2, votes_agst_2, votes_abs_2
	"""
	if vote_table!=None:
		return vote_table.find("p", text=vote).findNext("p").get_text()
	else:
		#~ print "no vote variable! (oeil)"
		return None


def get_rapps(soup):
	"""
	FUNCTION
	get the html content about rapporteurs from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	list of rapporteurs datas
	"""
	rapps=[None]*5
	try:
		#exclude shadow rapporteurs (parent: <div class="result_moredata shadow">)
		rapps_temp=[rapporteur for rapporteur in soup.find(text="Committee responsible").findNext("td", {"class": "players_rapporter_com "}).findAll("p", {"class": "players_content"}) if rapporteur.parent.name!="div"]
		for index in range(len(rapps_temp)):
			rapps[index]=rapps_temp[index]
	except:
		return rapps
	return rapps


def get_country_code(country):
	"""
	FUNCTION
	get the acronym of the country passed in parameter
	PARAMETERS
	country: full name of the country
	RETURN
	acronym of the country
	"""
	if country=="Belgium":
		return 'BE'
	if country=="Bulgaria":
		return 'BG'
	if country=="Czech Republic":
		return 'CZ'
	if country=="Denmark":
		return 'DK'
	if country=="Germany":
		return 'DE'
	if country=="Estonia":
		return 'EE'
	if country=="Ireland":
		return 'IE'
	if country=="Greece":
		return 'EL'
	if country=="Spain":
		return 'ES'
	if country=="France":
		return 'FR'
	if country=="Italy":
		return 'IT'
	if country=="Cyprus":
		return 'CY'
	if country=="Lithuania":
		return 'LT'
	if country=="Latvia":
		return 'LV'
	if country=="Luxembourg":
		return 'LU'
	if country=="Hungary":
		return 'HU'
	if country=="Malta":
		return 'MT'
	if country=="Netherlands":
		return 'NL'
	if country=="Austria":
		return 'AT'
	if country=="Poland":
		return 'PL'
	if country=="Portugal":
		return 'PT'
	if country=="Romania":
		return 'RO'
	if country=="Slovenia":
		return 'SI'
	if country=="Finland":
		return 'FI'
	if country=="Sweden":
		return 'SE'
	if country=="United Kingdom":
		return 'UK'
	if country=="Slovakia":
		return 'SK'
	if country=="Croatia":
		return 'HR'
	if country=="Iceland":
		return 'IS'
	if country=="Montenegro":
		return 'ME'
	if country=="Serbia":
		return 'RS'

	return country


def get_party(rapps_data):
	"""
	FUNCTION
	get the rapp_party_1-5 variable from datas of the rapporteur
	PARAMETERS
	rapps_data: rapporteur data
	RETURN
	rapp_party_1-5
	"""
	try:
		return rapps_data.find("span", {"class": "tiptip"})["title"]
	except:
		#~ print "no groupePolitiqueRapporteur! (oeil)"
		return None

#below "Rapporteur", before the name of the Rapporteur
#can be NULL


def get_rapp(rapps_data):
	"""
	FUNCTION
	get the rapp_1-5 variable from the datas of the rapporteur
	PARAMETERS
	rapps_data: rapporteur data
	RETURN
	rapp_1-5
	"""
	try:
		return rapps_data.find("span", {"class": "players_rapporter_text"}).get_text()
	except:
		#~ print "no rapporteurPE! (oeil)"
		return None

#below "Rapporteur", name of the Rapporteur
#can be NULL


def get_country(rapps_data):
	"""
	FUNCTION
	get the rapp_country_1-5 variable from the datas of the rapporteur
	PARAMETERS
	rapps_data: rapporteur data
	RETURN
	rapp_country_1-5
	"""
	try:
		link=rapps_data.find("span", {"class": "players_rapporter_text"}).find("a")['href']
		link_deputy_soup=BeautifulSoup(urllib.urlopen(link))
		#return acronym of the country
		return(get_country_code(link_deputy_soup.find("li", {"class": "nationality"}).contents[0].strip()))
	except:
		#~ print "no etatMbRapport! (oeil)"
		return None

#on the deputy's persononal page: country (next to the flag, next to the picture)
#can be NULL
#27 possible values (EU countries)


def get_modif_propos(soup):
	"""
	FUNCTION
	get the modif_propos variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	modif_propos
	"""
	modif_proposs=["Modified legislative proposal published", "Amended legislative proposal for reconsultation published", "Legislative proposal published"]
	for modifPropos in modif_proposs:
		if soup.find(text=re.compile(modifPropos))!=None:
			if modifPropos=="Legislative proposal published":
				if soup.find(text=re.compile("Initial legislative proposal published"))==None:
					return None
			return True
	return False

#In key events:
	#- if "Modified legislative proposal published" or "Amended legislative proposal for reconsultation published" -> Modif Propos=Y.
	#http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2002/0203%28CNS%29&l=en
	#http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2000/0062B%28CNS%29&l=en
	#- if "Legislative proposal published"
			#- if "Initial legislative proposal published" -> Modif Propos=Y.
			#http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2003/0059%28COD%29&l=en
			#- otherwise -> Modif Propos=NULL.
	#- otherwise -> Modif Propos=N (http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2005/0223(COD))


def get_nb_lectures(soup, suite_2e_lecture_pe):
	"""
	FUNCTION
	get the nb_lectures variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	nb_lectures
	"""
	#search in the key event table only
	key_events_soup=soup.find("a", {"class": "expand_button"}, text="Key events").findNext("table")

	#3d lecture
	if key_events_soup.find(text=re.compile('Decision by Council, 3rd rdg'))>0 or key_events_soup.find(text=re.compile('Decision by Council, 3rd reading'))>0:
		return 3

	#2d lecture
	#if suite_2e_lecture_pe=Yes
	if suite_2e_lecture_pe==1:
		pattern="Decision by Parliament, 2nd reading"
	#if suite_2e_lecture_pe=No
	else:
		pattern="Act approved by Council, 2nd reading"
	if key_events_soup.find(text=re.compile(pattern))>0:
		return 2

	#1st lecture
	if key_events_soup.find(text=re.compile("Act adopted by Council after Parliament's 1st reading"))>0:
		return 1

	return None

#possible values: 1, 2, 3 or NULL
#3: "Decision by Council, 3rd rdg ou reading"
#2:	- Suite2LecturePE=Y, "Decision by Parliament 2nd reading".
#	- Suite2LecturePE=N, "Act approved by Council, 2nd reading"
#1: "Act adopted by Council after Parliament's 1st reading"


def get_sign_pecs(soup, no_unique_type):
	"""
	FUNCTION
	get the sign_pecs variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	sign_pecs
	"""
	if no_unique_type=="COD" or no_unique_type=="ACI":
		return soup.find("td", text="Final act signed").findPrevious("td").get_text()
	#null value
	return None

#date in front of "Final act signed"
#can be NULL
#only if NoUniqueType=COD or ACI



def get_data_oeil(soup, ids):
	"""
	FUNCTION
	get all the data from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	dictionary of retrieved data from oeil
	"""
	fields={}

	#commission
	fields['commission']=get_commission(soup)
	print "commission:", fields['commission']

	#html content of the votes page
	vote_page_soup=get_vote_page(soup)
	#~ print votesSectionSoup

	#com_amdt_tabled
	fields['com_amdt_tabled']=get_com_amdt_tabled(vote_page_soup)
	print "com_amdt_tabled:", fields['com_amdt_tabled']

	#com_amdt_adopt
	fields['com_amdt_adopt']=get_com_amdt_adopt(vote_page_soup)
	print "com_amdt_adopt:", fields['com_amdt_adopt']

	#amdt_tabled
	fields['amdt_tabled']=get_amdt_tabled(vote_page_soup)
	print "amdt_tabled:", fields['amdt_tabled']

	#amdt_adopt
	fields['amdt_adopt']=get_amdt_adopt(vote_page_soup)
	print "amdt_adopt:", fields['amdt_adopt']

	#html content of the 2 tables of vote (Final vote and Final vote part two):
	vote_tables=get_vote_tables(vote_page_soup)
	vote_table_1=vote_tables[0]
	vote_table_2=vote_tables[1]

	#votes_for_1
	fields['votes_for_1']=get_vote(vote_table_1, "For")
	print "votes_for_1:", fields['votes_for_1']

	#votes_agst_1
	fields['votes_agst_1']=get_vote(vote_table_1, "Against")
	print "votes_agst_1:", fields['votes_agst_1']

	#votes_abs_1
	fields['votes_abs_1']=get_vote(vote_table_1, "Abstentions")
	print "votes_abs_1:", fields['votes_abs_1']

	#votes_for_2
	fields['votes_for_2']=get_vote(vote_table_2, "For")
	print "votes_for_2:", fields['votes_for_2']

	#votes_agst_2
	fields['votes_agst_2']=get_vote(vote_table_2, "Against")
	print "votes_agst_2:", fields['votes_agst_2']

	#votes_abs_2
	fields['votes_abs_2']=get_vote(vote_table_2, "Abstentions")
	print "votes_abs_2:", fields['votes_abs_2']

	#rapporteurs list
	rapps=get_rapps(soup)

	#rapp_party_1
	fields['rapp_party_1']=get_party(rapps[0])
	print "rapp_party_1:", fields['rapp_party_1']
#~ #~
	#rapp_1
	fields['rapp_1']=get_rapp(rapps[0])
	print "rapp_1:", fields['rapp_1']
#~ #~
	#rapp_country_1
	fields['rapp_country_1']=get_country(rapps[0])
	print "rapp_country_1:", fields['rapp_country_1']
#~ #~
	#rapp_party_2
	fields['rapp_party_2']=get_party(rapps[1])
	print "rapp_party_2:", fields['rapp_party_2']
#~ #~
	#rapp_2
	fields['rapp_2']=get_rapp(rapps[1])
	print "rapp_2:", fields['rapp_2']
#~ #~
	#rapp_country_2
	fields['rapp_country_2']=get_country(rapps[1])
	print "rapp_country_2:", fields['rapp_country_2']
#~ #~
	#rapp_party_3
	fields['rapp_party_3']=get_party(rapps[2])
	print "rapp_party_3:", fields['rapp_party_3']
#~ #~
	#rapp_3
	fields['rapp_3']=get_rapp(rapps[2])
	print "rapp_3:", fields['rapp_3']
#~ #~
	#rapp_country_3
	fields['rapp_country_3']=get_country(rapps[2])
	print "rapp_country_3:", fields['rapp_country_3']
#~ #~
	#rapp_party_4
	fields['rapp_party_4']=get_party(rapps[3])
	print "rapp_party_4:", fields['rapp_party_4']
#~ #~
	#rapp_4
	fields['rapp_4']=get_rapp(rapps[3])
	print "rapp_4:", fields['rapp_4']
#~ #~
	#rapp_country_4
	fields['rapp_country_4']=get_country(rapps[3])
	print "rapp_country_4:", fields['rapp_country_4']
#~ #~
	#rapp_party_5
	fields['rapp_party_5']=get_party(rapps[4])
	print "rapp_party_5:", fields['rapp_party_5']
#~ #~
	#rapp_5
	fields['rapp_5']=get_rapp(rapps[4])
	print "rapp_5:", fields['rapp_5']
#~ #~
	#rapp_country_5
	fields['rapp_country_5']=get_country(rapps[4])
	print "rapp_country_5:", fields['rapp_country_5']

	#modif_propos
	fields['modif_propos']=get_modif_propos(soup)
	print "modif_propos:", fields['modif_propos']

	#nb_lectures
	fields['nb_lectures']=get_nb_lectures(soup, ids["suite_2e_lecture_pe"])
	print "nb_lectures:", fields['nb_lectures']

	#sign_pecs
	fields['sign_pecs']=get_sign_pecs(soup, ids["no_unique_type"])
	print "sign_pecs:", fields['sign_pecs']

	return fields
