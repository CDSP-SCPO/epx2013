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
	if country=="Belgique":
		return 'BE'
	if country=="Bulgarie":
		return 'BG'
	if country=="République Tchèque":
		return 'CZ'
	if country=="Danemark":
		return 'DK'
	if country=="Allemagne":
		return 'DE'
	if country=="Estonie":
		return 'EE'
	if country=="Irlande":
		return 'IE'
	if country=="Grèce":
		return 'EL'
	if country=="Espagne":
		return 'ES'
	if country=="France":
		return 'FR'
	if country=="Italie":
		return 'IT'
	if country=="Chypre":
		return 'CY'
	if country=="Lituanie":
		return 'LT'
	if country=="Lettonie":
		return 'LV'
	if country=="Luxembourg":
		return 'LU'
	if country=="Hongrie":
		return 'HU'
	if country=="Malte":
		return 'MT'
	if country=="Pays-bas":
		return 'NL'
	if country=="Autriche":
		return 'AT'
	if country=="Pologne":
		return 'PL'
	if country=="Portugal":
		return 'PT'
	if country=="Roumanie":
		return 'RO'
	if country=="Slovénie":
		return 'SI'
	if country=="Finlande":
		return 'FI'
	if country=="Suède":
		return 'SE'
	if country=="Royaume-Uni":
		return 'UK'
	if country=="Slovaquie":
		return 'SK'
	if country=="Croatie":
		return 'HR'
	if country=="Islande":
		return 'IS'
	if country=="Monténégro":
		return 'ME'
	if country=="Serbie":
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


def getOeilNombreLecturesFromOeil(soup):
	"""
	FUNCTION
	get the oeilNombreLectures variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilNombreLectures
	"""
	return None




def getOeilInformation(soup):
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
	dataDic['oeilNombreLectures']=getOeilNombreLecturesFromOeil(soup)
	print "oeilNombreLectures:", dataDic['oeilNombreLectures']

	return dataDic
