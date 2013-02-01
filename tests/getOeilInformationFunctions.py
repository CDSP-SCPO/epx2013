# -*- coding: utf-8 -*-
"""
get the information from Oeil (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
import urllib


def getOeilCommissionPE(soup):
	"""
	FUNCTION
	get the oeilCommissionPE variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilCommissionPE
	"""
	try:
		return soup.find(text="Committee responsible").findNext("acronym").get_text()
	except:
		#~ print "no commissionPE! (oeil)"
		return None

#can be NULL


def getOeilVotesPage(soup):
	"""
	FUNCTION
	get the html page about votes from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	html page about votes
	"""
	votesLink=soup.find(text="Results of vote in Parliament").findNext("td").find("a")["href"]
	return BeautifulSoup(urllib.urlopen("http://www.europarl.europa.eu/"+votesLink))


def getOeilEPComAndtTabled(soup):
	"""
	FUNCTION
	get the OeilEPComAndtTabled variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	OeilEPComAndtTabled
	"""
	return soup.find(text="EP Committee").findNext('td').get_text()
	
	
def getOeilEPComAndtAdopt(soup):
	"""
	FUNCTION
	get the oeilEPComAndtAdopt variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilEPComAndtAdopt
	"""
	return soup.find(text="EP Committee").findNext('td').findNext('td').get_text()


def getOeilEPVotesFor1(soup):
	"""
	FUNCTION
	get the getOeilEPVotesFor1 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	getOeilEPVotesFor1
	"""
	try:
		return soup.find("p", text="For").findNext("p").get_text()
	except:
		#~ print "no epVotesFor1! (oeil)"
		return None


def getOeilEPVotesAgst1(soup):
	"""
	FUNCTION
	get the oeilEPVotesAgst1 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilEPVotesAgst1
	"""
	try:
		return soup.find("p", text="Against").findNext("p").get_text()
	except:
		#~ print "no epVotesAgst1! (oeil)"
		return None


def getOeilEPVotesAbs1(soup):
	"""
	FUNCTION
	get the oeilEPVotesAbs1 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilEPVotesAbs1
	"""
	try:
		return soup.find("p", text="Abstentions").findNext("p").get_text()
	except:
		#~ print "no epVotesAbs1! (oeil)"
		return None


def getOeilEPVotesFor2(soup):
	"""
	FUNCTION
	get the oeilEPVotesFor2 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilEPVotesFor2
	"""
	try:
		return soup.find(text="Final vote Part two").findNext("p", text="For").findNext("p").get_text()
	except:
		#~ print "no epVotesFor2! (oeil)"
		return None


def getOeilEPVotesAgst2(soup):
	"""
	FUNCTION
	get the oeilEPVotesAgst2 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilEPVotesAgst2
	"""
	try:
		return soup.find(text="Final vote Part two").findNext("p", text="Against").findNext("p").get_text()
	except:
		#~ print "no epVotesAgst2! (oeil)"
		return None


def getOeilEPVotesAbs2(soup):
	"""
	FUNCTION
	get the oeilEPVotesAbs2 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilEPVotesAbs2
	"""
	try:
		return soup.find(text="Final vote Part two").findNext("p", text="Abstentions").findNext("p").get_text()
	except:
		#~ print "no epVotesAbs2! (oeil)"
		return None


def getOeilRapporteursSection(soup):
	"""
	FUNCTION
	get the html content about rapporteurs from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	html content about rapporteurs
	"""
	return soup.find("span", {"class": "tiptip"}).findParent("td", {"class": "players_rapporter_com"})


def getOeilGroupePolitiqueRapporteur1(soup):
	"""
	FUNCTION
	get the oeilGroupePolitiqueRapporteur1 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilGroupePolitiqueRapporteur1
	"""
	try:
		return soup.findAll("span", {"class": "tiptip"})[0].get_text()
	except:
		#~ print "no groupePolitiqueRapporteur1! (oeil)"
		return None

#can be NULL


def getOeilRapporteurPE1(soup):
	"""
	FUNCTION
	get the oeilRapporteurPE1 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilRapporteurPE1
	"""
	try:
		return soup.findAll("span", {"class": "players_rapporter_text"})[0].get_text()
	except:
		#~ print "no rapporteurPE1! (oeil)"
		return None

#can be NULL

def getCountryAcronym(country):
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


def getOeilEtatMbRapport1(soup):
	"""
	FUNCTION
	get the oeilEtatMbRapport1 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilEtatMbRapport1
	"""
	try:
		deputyLink=soup.find("span", {"class": "players_rapporter_text"}).find("a")['href']
		deputyLinkSoup = BeautifulSoup(urllib.urlopen(deputyLink))
		#return acronym of the country
		return getCountryAcronym(deputyLinkSoup.find("span", {"class": "ep_country"}).get_text())
	except:
		#~ print "no etatMbRapport1! (oeil)"
		return None

#can be NULL
#27 possible values (EU countries)


def getOeilGroupePolitiqueRapporteur2(soup):
	"""
	FUNCTION
	get the oeilGroupePolitiqueRapporteur2 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilGroupePolitiqueRapporteur2
	"""
	try:
		return soup.findAll("span", {"class": "tiptip"})[1].get_text()
	except:
		#~ print "no groupePolitiqueRapporteur2! (oeil)"
		return None

#can be NULL


def getOeilRapporteurPE2(soup):
	"""
	FUNCTION
	get the oeilRapporteurPE2 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilRapporteurPE2
	"""
	try:
		return soup.findAll("span", {"class": "players_rapporter_text"})[1].get_text()
	except:
		#~ print "no rapporteurPE2! (oeil)"
		return None

#can be NULL


def getOeilModifPropos(soup):
	"""
	FUNCTION
	get the oeilModifPropos variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilModifPropos
	"""
	return None


def getOeilNombreLectures(soup):
	"""
	FUNCTION
	get the oeilNombreLectures variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilNombreLectures
	"""
	return None


def getOeilSignPECS(soup, noUniqueType):
	"""
	FUNCTION
	get the oeilSignPECS variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilSignPECS
	"""
	if noUniqueType=="COD" or noUniqueType=="ACI":
		return soup.find("td", text="Final act signed").findPrevious("td").get_text()
	return None

#date in front of "Final act signed"
#can be NULL
#only if NoUniqueType = COD or ACI



def getOeilInformation(soup, idsDic):
	"""
	FUNCTION
	get all the information from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	dictionary of retrieved data from oeil
	"""
	dataDic={}
	
	#oeilCommissionPE
	dataDic['oeilCommissionPE']=getOeilCommissionPE(soup)
	print "oeilCommissionPE:", dataDic['oeilCommissionPE']
	
	#html content of the votes page
	votesPageSoup=getOeilVotesPage(soup)
	#~ print votesSectionSoup
	
	#oeilEPComAndtTabled
	dataDic['oeilEPComAndtTabled']=getOeilEPComAndtTabled(votesPageSoup)
	print "oeilEPComAndtTabled:", dataDic['oeilEPComAndtTabled']
	
	#oeilEPComAndtAdopt
	dataDic['oeilEPComAndtAdopt']=getOeilEPComAndtAdopt(votesPageSoup)
	print "oeilEPComAndtAdopt:", dataDic['oeilEPComAndtAdopt']
	
	#oeilEPVotesFor1
	dataDic['oeilEPVotesFor1']=getOeilEPVotesFor1(votesPageSoup)
	print "oeilEPVotesFor1:", dataDic['oeilEPVotesFor1']
	
	#oeilEPVotesAgst1
	dataDic['oeilEPVotesAgst1']=getOeilEPVotesAgst1(votesPageSoup)
	print "oeilEPVotesAgst1:", dataDic['oeilEPVotesAgst1']
	
	#oeilEPVotesAbs1
	dataDic['oeilEPVotesAbs1']=getOeilEPVotesAbs1(votesPageSoup)
	print "oeilEPVotesAbs1:", dataDic['oeilEPVotesAbs1']
	
	#oeilEPVotesFor2
	dataDic['oeilEPVotesFor2']=getOeilEPVotesFor2(votesPageSoup)
	print "oeilEPVotesFor2:", dataDic['oeilEPVotesFor2']
	
	#oeilEPVotesAgst2
	dataDic['oeilEPVotesAgst2']=getOeilEPVotesAgst2(votesPageSoup)
	print "oeilEPVotesAgst2:", dataDic['oeilEPVotesAgst2']
	
	#oeilEPVotesAbs2
	dataDic['oeilEPVotesAbs2']=getOeilEPVotesAbs2(votesPageSoup)
	print "oeilEPVotesAbs2:", dataDic['oeilEPVotesAbs2']
	
	#rapporteurs section
	rapporteursSectionSoup=getOeilRapporteursSection(soup)
	#~ print rapporteurSectionSoup
	
	#oeilGroupePolitiqueRapporteur1
	dataDic['oeilGroupePolitiqueRapporteur1']=getOeilGroupePolitiqueRapporteur1(rapporteursSectionSoup)
	print "oeilGroupePolitiqueRapporteur1:", dataDic['oeilGroupePolitiqueRapporteur1']
	
	#oeilRapporteurPE1
	dataDic['oeilRapporteurPE1']=getOeilRapporteurPE1(rapporteursSectionSoup)
	print "oeilRapporteurPE1:", dataDic['oeilRapporteurPE1']
	
	#oeilEtatMbRapport1
	dataDic['oeilEtatMbRapport1']=getOeilEtatMbRapport1(rapporteursSectionSoup)
	print "oeilEtatMbRapport1:", dataDic['oeilEtatMbRapport1']
	
	#oeilGroupePolitiqueRapporteur2
	dataDic['oeilGroupePolitiqueRapporteur2']=getOeilGroupePolitiqueRapporteur2(rapporteursSectionSoup)
	print "oeilGroupePolitiqueRapporteur2:", dataDic['oeilGroupePolitiqueRapporteur2']
	
	#oeilRapporteurPE2
	dataDic['oeilRapporteurPE2']=getOeilRapporteurPE2(rapporteursSectionSoup)
	print "oeilRapporteurPE2:", dataDic['oeilRapporteurPE2']
	
	#oeilModifPropos
	dataDic['oeilModifPropos']=getOeilModifPropos(soup)
	print "oeilModifPropos:", dataDic['oeilModifPropos']
	
	#oeilNombreLectures
	dataDic['oeilNombreLectures']=getOeilNombreLectures(soup)
	print "oeilNombreLectures:", dataDic['oeilNombreLectures']
	
	#oeilSignPECS
	dataDic['oeilSignPECS']=getOeilSignPECS(soup, idsDic["oeilNoUniqueType"])
	print "oeilSignPECS:", dataDic['oeilSignPECS']

	return dataDic
