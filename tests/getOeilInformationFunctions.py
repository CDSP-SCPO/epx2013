# -*- coding: utf-8 -*-
"""
get the information from Oeil (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
import urllib


def getCommissionPEFromOeil(soup):
	"""
	FUNCTION
	get the commissionPE variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	commissionPE
	"""
	try:
		return soup.find(text="Committee responsible").findNext("acronym").get_text()
	except:
		#~ print "no commissionPE! (oeil)"
		return None

#can be NULL


def getVotesPageFromOeil(soup):
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


def getEPComAndtTabledFromOeil(soup):
	"""
	FUNCTION
	get the epComAndtTabled variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	epComAndtTabled
	"""
	return soup.find(text="EP Committee").findNext('td').get_text()
	
	
def getEPComAndtAdoptFromOeil(soup):
	"""
	FUNCTION
	get the epComAndtAdopt variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	epComAndtAdopt
	"""
	return soup.find(text="EP Committee").findNext('td').findNext('td').get_text()


def getEPVotesFor1FromOeil(soup):
	"""
	FUNCTION
	get the variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	epVotesFor1
	"""
	try:
		return soup.find("p", text="For").findNext("p").get_text()
	except:
		#~ print "no epVotesFor1! (oeil)"
		return None


def getEPVotesAgst1FromOeil(soup):
	"""
	FUNCTION
	get the epVotesAgst1 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	epVotesAgst1
	"""
	try:
		return soup.find("p", text="Against").findNext("p").get_text()
	except:
		#~ print "no epVotesAgst1! (oeil)"
		return None


def getEPVotesAbs1FromOeil(soup):
	"""
	FUNCTION
	get the epVotesAbs1 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	epVotesAbs1
	"""
	try:
		return soup.find("p", text="Abstentions").findNext("p").get_text()
	except:
		#~ print "no epVotesAbs1! (oeil)"
		return None


def getEPVotesFor2FromOeil(soup):
	"""
	FUNCTION
	get the epVotesFor2 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	epVotesFor2
	"""
	try:
		return soup.find(text="Final vote Part two").findNext("p", text="For").findNext("p").get_text()
	except:
		#~ print "no epVotesFor2! (oeil)"
		return None


def getEPVotesAgst2FromOeil(soup):
	"""
	FUNCTION
	get the epVotesAgst2 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	epVotesAgst2
	"""
	try:
		return soup.find(text="Final vote Part two").findNext("p", text="Against").findNext("p").get_text()
	except:
		#~ print "no epVotesAgst2! (oeil)"
		return None


def getEPVotesAbs2FromOeil(soup):
	"""
	FUNCTION
	get the epVotesAbs2 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	epVotesAbs2
	"""
	try:
		return soup.find(text="Final vote Part two").findNext("p", text="Abstentions").findNext("p").get_text()
	except:
		#~ print "no epVotesAbs2! (oeil)"
		return None


def getRapporteursSectionFromOeil(soup):
	"""
	FUNCTION
	get the html content about rapporteurs from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	html content about rapporteurs
	"""
	return soup.find("span", {"class": "tiptip"}).findParent("td", {"class": "players_rapporter_com"})


def getGroupePolitiqueRapporteur1FromOeil(soup):
	"""
	FUNCTION
	get the groupePolitiqueRapporteur1 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	groupePolitiqueRapporteur1
	"""
	try:
		return soup.findAll("span", {"class": "tiptip"})[0].get_text()
	except:
		#~ print "no groupePolitiqueRapporteur1! (oeil)"
		return None

#can be NULL


def getRapporteurPE1FromOeil(soup):
	"""
	FUNCTION
	get the rapporteurPE1 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	rapporteurPE1
	"""
	try:
		return soup.findAll("span", {"class": "players_rapporter_text"})[0].get_text()
	except:
		#~ print "no rapporteurPE1! (oeil)"
		return None

#can be NULL


def getEtatMbRapport1FromOeil(soup):
	"""
	FUNCTION
	get the etatMbRapport1 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	etatMbRapport1
	"""
	try:
		deputyLink=soup.find("span", {"class": "players_rapporter_text"}).find("a")['href']
		deputyLinkSoup = BeautifulSoup(urllib.urlopen(deputyLink))
		return deputyLinkSoup.find("span", {"class": "ep_country"}).get_text()
	except:
		#~ print "no etatMbRapport1! (oeil)"
		return None

#can be NULL
#27 possible values (EU countries)


def getGroupePolitiqueRapporteur2FromOeil(soup):
	"""
	FUNCTION
	get the groupePolitiqueRapporteur2 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	groupePolitiqueRapporteur2
	"""
	try:
		return soup.findAll("span", {"class": "tiptip"})[1].get_text()
	except:
		#~ print "no groupePolitiqueRapporteur2! (oeil)"
		return None

#can be NULL


def getRapporteurPE2FromOeil(soup):
	"""
	FUNCTION
	get the rapporteurPE2 variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	rapporteurPE2
	"""
	try:
		return soup.findAll("span", {"class": "players_rapporter_text"})[1].get_text()
	except:
		#~ print "no rapporteurPE2! (oeil)"
		return None

#can be NULL


def getModifProposFromOeil(soup):
	"""
	FUNCTION
	get the modifPropos variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	modifPropos
	"""
	return None


def getNombreLecturesFromOeil(soup):
	"""
	FUNCTION
	get the nombreLectures variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	nombreLectures
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
	
	#commissionPE
	dataDic['commissionPE']=getCommissionPEFromOeil(soup)
	print "commissionPE (oeil):", dataDic['commissionPE']
	
	#html content of the votes page
	votesPageSoup=getVotesPageFromOeil(soup)
	#~ print votesSectionSoup
	
	#epComAndtTabled
	dataDic['epComAndtTabled']=getEPComAndtTabledFromOeil(votesPageSoup)
	print "epComAndtTabled (oeil):", dataDic['epComAndtTabled']
	
	#epComAndtAdopt
	dataDic['epComAndtAdopt']=getEPComAndtAdoptFromOeil(votesPageSoup)
	print "epComAndtAdopt (oeil):", dataDic['epComAndtAdopt']
	
	#epVotesFor1
	dataDic['epVotesFor1']=getEPVotesFor1FromOeil(votesPageSoup)
	print "epVotesFor1 (oeil):", dataDic['epVotesFor1']
	
	#epVotesAgst1
	dataDic['epVotesAgst1']=getEPVotesAgst1FromOeil(votesPageSoup)
	print "epVotesAgst1 (oeil):", dataDic['epVotesAgst1']
	
	#epVotesAbs1
	dataDic['epVotesAbs1']=getEPVotesAbs1FromOeil(votesPageSoup)
	print "epVotesAbs1 (oeil):", dataDic['epVotesAbs1']
	
	#epVotesFor2
	dataDic['epVotesFor2']=getEPVotesFor2FromOeil(votesPageSoup)
	print "epVotesFor2 (oeil):", dataDic['epVotesFor2']
	
	#epVotesAgst2
	dataDic['epVotesAgst2']=getEPVotesAgst2FromOeil(votesPageSoup)
	print "epVotesAgst2 (oeil):", dataDic['epVotesAgst2']
	
	#epVotesAbs2
	dataDic['epVotesAbs2']=getEPVotesAbs2FromOeil(votesPageSoup)
	print "epVotesAbs2 (oeil):", dataDic['epVotesAbs2']
	
	#rapporteurs section
	rapporteursSectionSoup=getRapporteursSectionFromOeil(soup)
	#~ print rapporteurSectionSoup
	
	#groupePolitiqueRapporteur1
	dataDic['groupePolitiqueRapporteur1']=getGroupePolitiqueRapporteur1FromOeil(rapporteursSectionSoup)
	print "groupePolitiqueRapporteur1 (oeil):", dataDic['groupePolitiqueRapporteur1']
	
	#rapporteurPE1
	dataDic['rapporteurPE1']=getRapporteurPE1FromOeil(rapporteursSectionSoup)
	print "rapporteurPE1 (oeil):", dataDic['rapporteurPE1']
	
	#etatMbRapport1
	dataDic['etatMbRapport1']=getEtatMbRapport1FromOeil(rapporteursSectionSoup)
	print "etatMbRapport1 (oeil):", dataDic['etatMbRapport1']
	
	#groupePolitiqueRapporteur2
	dataDic['groupePolitiqueRapporteur2']=getGroupePolitiqueRapporteur2FromOeil(rapporteursSectionSoup)
	print "groupePolitiqueRapporteur2 (oeil):", dataDic['groupePolitiqueRapporteur2']
	
	#rapporteurPE2
	dataDic['rapporteurPE2']=getRapporteurPE2FromOeil(rapporteursSectionSoup)
	print "rapporteurPE2 (oeil):", dataDic['rapporteurPE2']
	
	#modifPropos
	dataDic['modifPropos']=getModifProposFromOeil(soup)
	print "modifPropos (oeil):", dataDic['modifPropos']
	
	#nombreLectures
	dataDic['nombreLectures']=getNombreLecturesFromOeil(soup)
	print "nombreLectures (oeil):", dataDic['nombreLectures']

	return dataDic
