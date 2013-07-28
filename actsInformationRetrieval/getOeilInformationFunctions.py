# -*- coding: utf-8 -*-
"""
get the information from Oeil (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
import urllib
from common.commonFunctions import stringToIsoDate


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
		oeilCommissionPE=soup.find(text="Committee responsible").findNext("acronym")
		if oeilCommissionPE.get_text()=="DELE":
			return oeilCommissionPE.findNext("acronym").get_text()
		else:
			return oeilCommissionPE.get_text()
	except:
		#~ print "no commissionPE! (oeil)"
		return None

#Acronym under "Committee responsible"
#can be NULL


#~ http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2005/0017(COD)
def getOeilVotesPage(soup):
	"""
	FUNCTION
	get the html page about votes from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	html page about votes
	"""
	try:
		votesLink=soup.find(text="Results of vote in Parliament").findNext("td").find("a")["href"]
		return BeautifulSoup(urllib.urlopen("http://www.europarl.europa.eu/"+votesLink))
	except:
		print "no vote page (oeil)"
		return None


def getOeilEPComAndtTabled(soup):
	"""
	FUNCTION
	get the oeilEPComAndtTabled variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilEPComAndtTabled
	"""
	try:
		return soup.find(text="EP Committee").findNext('td').get_text()
	except:
		print "no oeilEPComAndtTabled!"
		return None

#on vote page:
#Last table "Amendments adopted in plenary": EP Committee (row) and Tabled by (column)


def getOeilEPComAndtAdopt(soup):
	"""
	FUNCTION
	get the oeilEPComAndtAdopt variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilEPComAndtAdopt
	"""
	try:
		return soup.find(text="EP Committee").findNext('td').findNext('td').get_text()
	except:
		print "no oeilEPComAndtAdopt"
		return None

#on vote page:
#Last table "Amendments adopted in plenary": EP Committee (row) and Adopted (column)


def getOeilEPAmdtTabled(soup):
	"""
	FUNCTION
	get the oeilEPAmdtTabled variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilEPAmdtTabled
	"""
	try:
		return soup.find(text="Total").findNext('th').get_text()
	except:
		print "no oeilEPAmdtTabled"
		return None


def getOeilEPAmdtAdopt(soup):
	"""
	FUNCTION
	get the oeilEPAmdtAdopt variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilEPAmdtAdopt
	"""
	try:
		return soup.find(text="Total").findNext('th').findNext('th').get_text()
	except:
		print "no oeilEPAmdtAdopt"
		return None


def getOeilEPVoteTables(soup):
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
	tableVotesList=[None]*2
	try:
		tableVotesTemp=soup.findAll("td", {"class": "rowtitle"})
		tableVotesList[0]=tableVotesTemp[0].findNext("table").find("table")
		tableVotesList[1]=tableVotesTemp[1].findNext("table").find("table")
		#~ print "tableVotesList[0]", tableVotesList[0]
		#~ print "tableVotesList[1]", tableVotesList[1]
		return tableVotesList
	except:
		#~ print "no table of vote! (oeil)"
		return tableVotesList


def getOeilEPVote(tableVote, vote):
	"""
	FUNCTION
	get the vote variable For, Against or Abstentions from one of the two vote tables
	PARAMETERS
	tableVote: html content of the first or second vote table
	vote="For", "Against" or "Abstentions"
	RETURN
	one of the following vote variables: getOeilEPVotesFor1, oeilEPVotesAgst1, oeilEPVotesAbs1, getOeilEPVotesFor2, oeilEPVotesAgst2, oeilEPVotesAbs2
	"""
	if tableVote!=None:
		return tableVote.find("p", text=vote).findNext("p").get_text()
	else:
		#~ print "no vote variable! (oeil)"
		return None


def getOeilRapporteursList(soup):
	"""
	FUNCTION
	get the html content about rapporteurs from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	list of rapporteurs infos
	"""
	rapporteursList=[None]*5
	try:
		#exclude shadow rapporteurs (parent: <div class="result_moreinfo shadow">)
		rapporteursListTemp=[rapporteur for rapporteur in soup.find(text="Committee responsible").findNext("td", {"class": "players_rapporter_com "}).findAll("p", {"class": "players_content"}) if rapporteur.parent.name!="div"]
		for index in range(len(rapporteursListTemp)):
			rapporteursList[index]=rapporteursListTemp[index]
	except:
		return rapporteursList
	return rapporteursList


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


def getOeilGroupePolitiqueRapporteur(rapporteurInfos):
	"""
	FUNCTION
	get the oeilGroupePolitiqueRapporteur1-5 variable from infos of the rapporteur
	PARAMETERS
	rapporteurInfos: rapporteur information
	RETURN
	oeilGroupePolitiqueRapporteur1-5
	"""
	try:
		return rapporteurInfos.find("span", {"class": "tiptip"})["title"]
	except:
		#~ print "no groupePolitiqueRapporteur! (oeil)"
		return None

#below "Rapporteur", before the name of the Rapporteur
#can be NULL


def getOeilRapporteurPE(rapporteurInfos):
	"""
	FUNCTION
	get the oeilRapporteurPE1-5 variable from the infos of the rapporteur
	PARAMETERS
	rapporteurInfos: rapporteur information
	RETURN
	oeilRapporteurPE1-5
	"""
	try:
		return rapporteurInfos.find("span", {"class": "players_rapporter_text"}).get_text()
	except:
		#~ print "no rapporteurPE! (oeil)"
		return None

#below "Rapporteur", name of the Rapporteur
#can be NULL


def getOeilEtatMbRapport(rapporteurInfos):
	"""
	FUNCTION
	get the oeilEtatMbRapport1-5 variable from the infos of the rapporteur
	PARAMETERS
	rapporteurInfos: rapporteur information
	RETURN
	oeilEtatMbRapport1-5
	"""
	try:
		link=rapporteurInfos.find("span", {"class": "players_rapporter_text"}).find("a")['href']
		deputyLinkSoup=BeautifulSoup(urllib.urlopen(link))
		#return acronym of the country
		return(getCountryAcronym(deputyLinkSoup.find("li", {"class": "nationality"}).contents[0].strip()))
	except:
		#~ print "no etatMbRapport! (oeil)"
		return None

#on the deputy's personal page: country (next to the flag, next to the picture)
#can be NULL
#27 possible values (EU countries)


def getOeilModifPropos(soup):
	"""
	FUNCTION
	get the oeilModifPropos variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilModifPropos
	"""
	try:
		modifProposList=["Modified legislative proposal published", "Amended legislative proposal for reconsultation published", "Legislative proposal published"]
		for modifPropos in modifProposList:
			if soup.find(text=re.compile(modifPropos))!=None:
				if modifPropos=="Legislative proposal published":
					if soup.find(text=re.compile("Initial legislative proposal published"))==None:
						return None
				return True
		return False
	except:
		print "no oeilModifPropos! (oeil)"
		return None

#In key events:
	#- if "Modified legislative proposal published" or "Amended legislative proposal for reconsultation published" -> Modif Propos=Y.
	#http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2002/0203%28CNS%29&l=en
	#http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2000/0062B%28CNS%29&l=en
	#- if "Legislative proposal published"
			#- if "Initial legislative proposal published" -> Modif Propos=Y.
			#http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2003/0059%28COD%29&l=en
			#- otherwise -> Modif Propos=NULL.
	#- otherwise -> Modif Propos=N (http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2005/0223(COD))


def getOeilNombreLectures(soup, suite2eLecturePE):
	"""
	FUNCTION
	get the oeilNombreLectures variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilNombreLectures
	"""
	try:
		#search in the key event table only
		keyEventsSoup=soup.find("a", {"class": "expand_button"}, text="Key events").findNext("table")

		#3d lecture
		if keyEventsSoup.find(text=re.compile('Decision by Council, 3rd rdg'))>0 or keyEventsSoup.find(text=re.compile('Decision by Council, 3rd reading'))>0:
			return 3

		#2d lecture
		#if suite2eLecturePE=Yes
		if suite2eLecturePE==1:
			pattern="Decision by Parliament, 2nd reading"
		#if suite2eLecturePE=No
		else:
			pattern="Act approved by Council, 2nd reading"
		if keyEventsSoup.find(text=re.compile(pattern))>0:
			return 2

		#1st lecture
		if keyEventsSoup.find(text=re.compile("Act adopted by Council after Parliament's 1st reading"))>0:
			return 1

		return None
	except:
		print  "no oeilNombreLectures! (oeil)"
		return None

#possible values: 1, 2, 3 or NULL
#3: "Decision by Council, 3rd rdg ou reading"
#2:	- Suite2LecturePE= Y, "Decision by Parliament 2nd reading".
#	- Suite2LecturePE=N, "Act approved by Council, 2nd reading"
#1: "Act adopted by Council after Parliament's 1st reading"


def getOeilSignPECS(soup, noUniqueType):
	"""
	FUNCTION
	get the oeilSignPECS variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilSignPECS
	"""
	signPECS=None
	if noUniqueType=="COD" or noUniqueType=="ACI":
		signPECS=soup.find("td", text="Final act signed").findPrevious("td").get_text()
		if signPECS!=None:
			signPECS=stringToIsoDate(signPECS)

	return signPECS

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

	#oeilEPAmdtTabled
	dataDic['oeilEPAmdtTabled']=getOeilEPAmdtTabled(votesPageSoup)
	print "oeilEPAmdtTabled:", dataDic['oeilEPAmdtTabled']

	#oeilEPAmdtAdopt
	dataDic['oeilEPAmdtAdopt']=getOeilEPAmdtAdopt(votesPageSoup)
	print "oeilEPAmdtAdopt:", dataDic['oeilEPAmdtAdopt']

	#html content of the 2 tables of vote (Final vote and Final vote part two):
	voteTables=getOeilEPVoteTables(votesPageSoup)
	voteTable1=voteTables[0]
	voteTable2=voteTables[1]

	#oeilEPVotesFor1
	dataDic['oeilEPVotesFor1']=getOeilEPVote(voteTable1, "For")
	print "oeilEPVotesFor1:", dataDic['oeilEPVotesFor1']

	#oeilEPVotesAgst1
	dataDic['oeilEPVotesAgst1']=getOeilEPVote(voteTable1, "Against")
	print "oeilEPVotesAgst1:", dataDic['oeilEPVotesAgst1']

	#oeilEPVotesAbs1
	dataDic['oeilEPVotesAbs1']=getOeilEPVote(voteTable1, "Abstentions")
	print "oeilEPVotesAbs1:", dataDic['oeilEPVotesAbs1']

	#oeilEPVotesFor2
	dataDic['oeilEPVotesFor2']=getOeilEPVote(voteTable2, "For")
	print "oeilEPVotesFor2:", dataDic['oeilEPVotesFor2']

	#oeilEPVotesAgst2
	dataDic['oeilEPVotesAgst2']=getOeilEPVote(voteTable2, "Against")
	print "oeilEPVotesAgst2:", dataDic['oeilEPVotesAgst2']

	#oeilEPVotesAbs2
	dataDic['oeilEPVotesAbs2']=getOeilEPVote(voteTable2, "Abstentions")
	print "oeilEPVotesAbs2:", dataDic['oeilEPVotesAbs2']

	#rapporteurs list
	rapporteursList=getOeilRapporteursList(soup)

	#oeilGroupePolitiqueRapporteur, oeilRapporteurPE, oeilEtatMbRapport variables
	for index in xrange(len(rapporteursList)):
		num=str(index+1)
		dataDic['oeilGroupePolitiqueRapporteur'+num]=getOeilGroupePolitiqueRapporteur(rapporteursList[index])
		print 'oeilGroupePolitiqueRapporteur'+num+": ", dataDic['oeilGroupePolitiqueRapporteur'+num]
		dataDic['oeilRapporteurPE'+num]=getOeilRapporteurPE(rapporteursList[index])
		print 'oeilRapporteurPE'+num+": ", dataDic['oeilRapporteurPE'+num]
		dataDic['oeilEtatMbRapport'+num]=getOeilEtatMbRapport(rapporteursList[index])
		print 'oeilEtatMbRapport'+num+": ", dataDic['oeilEtatMbRapport'+num]

	#oeilModifPropos
	dataDic['oeilModifPropos']=getOeilModifPropos(soup)
	print "oeilModifPropos:", dataDic['oeilModifPropos']

	#oeilNombreLectures
	dataDic['oeilNombreLectures']=getOeilNombreLectures(soup, idsDic["suite2eLecturePE"])
	print "oeilNombreLectures:", dataDic['oeilNombreLectures']

	#oeilSignPECS
	dataDic['oeilSignPECS']=getOeilSignPECS(soup, idsDic["oeilNoUniqueType"])
	print "oeilSignPECS:", dataDic['oeilSignPECS']

	return dataDic
