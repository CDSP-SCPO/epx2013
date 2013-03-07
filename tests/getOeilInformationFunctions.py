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

#on vote page:
#First table "Final vote [Date]": For (column)


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

#on vote page:
#First table "Final vote [Date]": Against (column)


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

#on vote page:
#First table "Final vote [Date]": Abstentions (column)


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

#on vote page:
#Second table "Final vote Part two": For (column)


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

#on vote page:
#Second table "Final vote Part two": Against (column)


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

#on vote page:
#Second table "Final vote Part two": Abstentions (column)


def getOeilRapporteursSection(soup):
	"""
	FUNCTION
	get the html content about rapporteurs from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	html content about rapporteurs
	"""
	#~ return soup.find("span", {"class": "tiptip"}).findParent("td", {"class": "players_rapporter_com"})
	return soup.find(text="Committee responsible").findParent("table")


def getAllOeilGroupePolitiqueRapporteur(soup):
	"""
	FUNCTION
	get all the oeilGroupePolitiqueRapporteur variables from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilGroupePolitiqueRapporteur1-5
	"""
	try:
		return soup.findAll("span", {"class": "tiptip"})
	except:
		#~ print "no groupePolitiqueRapporteur! (oeil)"
		return None

#below "Rapporteur", before the name of the Rapporteur
#can be NULL


def getAllOeilRapporteurPE(soup):
	"""
	FUNCTION
	get all the oeilRapporteurPE variables from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilRapporteurPE1-5
	"""
	try:
		return soup.findAll("span", {"class": "players_rapporter_text"})
	except:
		#~ print "no rapporteurPE! (oeil)"
		return None

#below "Rapporteur", name of the Rapporteur
#can be NULL


def getAllOeilEtatMbRapport(soup):
	"""
	FUNCTION
	get all the oeilEtatMbRapport variables from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilEtatMbRapport1-5
	"""
	try:
		links=soup.findAll("span", {"class": "players_rapporter_text"})
		oeilEtatMbRapportList=[]
		for link in links:
			deputyLink=link.find("a")['href']
			deputyLinkSoup=BeautifulSoup(urllib.urlopen(deputyLink))
			#return acronym of the country
			oeilEtatMbRapportList.append(getCountryAcronym(deputyLinkSoup.find("span", {"class": "ep_country"}).get_text()))
		return oeilEtatMbRapportList
	except:
		#~ print "no etatMbRapport! (oeil)"
		return None


def getOeilGroupePolitiqueRapporteur1(allPoliticalGroups):
	"""
	FUNCTION
	get the oeilGroupePolitiqueRapporteur1 variable from the oeil url
	PARAMETERS
	allPoliticalGroups: allPoliticalGroups variable
	RETURN
	oeilGroupePolitiqueRapporteur1
	"""
	try:
		return allPoliticalGroups[0].get_text()
	except:
		#~ print "no groupePolitiqueRapporteur1! (oeil)"
		return None

#below "Rapporteur", before the name of the Rapporteur
#can be NULL


def getOeilRapporteurPE1(allRapporteursNames):
	"""
	FUNCTION
	get the oeilRapporteurPE1 variable from the oeil url
	PARAMETERS
	allRapporteursNames: allRapporteursNames variable
	RETURN
	oeilRapporteurPE1
	"""
	try:
		return allRapporteursNames[0].get_text()
	except:
		#~ print "no rapporteurPE1! (oeil)"
		return None

#below "Rapporteur", name of the Rapporteur
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


def getOeilEtatMbRapport1(oeilEtatMbRapportList):
	"""
	FUNCTION
	get the oeilEtatMbRapport1 variable from the oeil url
	PARAMETERS
	oeilEtatMbRapportList: oeilEtatMbRapportList variable
	RETURN
	oeilEtatMbRapport1
	"""
	try:
		return oeilEtatMbRapportList[0]
	except:
		#~ print "no etatMbRapport1! (oeil)"
		return None

#on the deputy's personal page: country (next to the flag, next to the picture)
#can be NULL
#27 possible values (EU countries)


def getOeilGroupePolitiqueRapporteur2(allPoliticalGroups):
	"""
	FUNCTION
	get the oeilGroupePolitiqueRapporteur2 variable from the oeil url
	PARAMETERS
	allPoliticalGroups: allPoliticalGroups variable
	RETURN
	oeilGroupePolitiqueRapporteur2
	"""
	try:
		return allPoliticalGroups[1].get_text()
	except:
		#~ print "no groupePolitiqueRapporteur2! (oeil)"
		return None

#below "Rapporteur", before the name of the second Rapporteur
#can be NULL


def getOeilRapporteurPE2(allRapporteursNames):
	"""
	FUNCTION
	get the oeilRapporteurPE2 variable from the oeil url
	PARAMETERS
	allRapporteursNames: allRapporteursNames variable
	RETURN
	oeilRapporteurPE2
	"""
	try:
		return allRapporteursNames[1].get_text()
	except:
		#~ print "no rapporteurPE2! (oeil)"
		return None

#below "Rapporteur", name of the second Rapporteur
#can be NULL


def getOeilEtatMbRapport2(oeilEtatMbRapportList):
	"""
	FUNCTION
	get the oeilEtatMbRapport2 variable from the oeil url
	PARAMETERS
	allEtatMbRapport: allEtatMbRapport variable
	RETURN
	oeilEtatMbRapport2
	"""
	try:
		return oeilEtatMbRapportList[1]
	except:
		#~ print "no etatMbRapport2! (oeil)"
		return None

#on the deputy's personal page: country (next to the flag, next to the picture)
#can be NULL
#27 possible values (EU countries)


def getOeilGroupePolitiqueRapporteur3(allPoliticalGroups):
	"""
	FUNCTION
	get the oeilGroupePolitiqueRapporteur3 variable from the oeil url
	PARAMETERS
	allPoliticalGroups: allPoliticalGroups variable
	RETURN
	oeilGroupePolitiqueRapporteur3
	"""
	try:
		return allPoliticalGroups[2].get_text()
	except:
		#~ print "no groupePolitiqueRapporteur3! (oeil)"
		return None

#below "Rapporteur", before the name of the third Rapporteur
#can be NULL


def getOeilRapporteurPE3(allRapporteursNames):
	"""
	FUNCTION
	get the oeilRapporteurPE3 variable from the oeil url
	PARAMETERS
	allRapporteursNames: allRapporteursNames variable
	RETURN
	oeilRapporteurPE3
	"""
	try:
		return allRapporteursNames[2].get_text()
	except:
		#~ print "no rapporteurPE3! (oeil)"
		return None

#below "Rapporteur", name of the third Rapporteur
#can be NULL


def getOeilEtatMbRapport3(oeilEtatMbRapportList):
	"""
	FUNCTION
	get the oeilEtatMbRapport3 variable from the oeil url
	PARAMETERS
	allEtatMbRapport: allEtatMbRapport variable
	RETURN
	oeilEtatMbRapport3
	"""
	try:
		return oeilEtatMbRapportList[2]
	except:
		#~ print "no oeilEtatMbRapport3!"
		return None

#on the deputy's personal page: country (next to the flag, next to the picture)
#can be NULL
#27 possible values (EU countries)


def getOeilGroupePolitiqueRapporteur4(allPoliticalGroups):
	"""
	FUNCTION
	get the oeilGroupePolitiqueRapporteur4 variable from the oeil url
	PARAMETERS
	allPoliticalGroups: allPoliticalGroups variable
	RETURN
	oeilGroupePolitiqueRapporteur4
	"""
	try:
		return allPoliticalGroups[3].get_text()
	except:
		#~ print "no groupePolitiqueRapporteur4! (oeil)"
		return None

#below "Rapporteur", before the name of the fourth Rapporteur
#can be NULL


def getOeilRapporteurPE4(allRapporteursNames):
	"""
	FUNCTION
	get the oeilRapporteurPE4 variable from the oeil url
	PARAMETERS
	allRapporteursNames: allRapporteursNames variable
	RETURN
	oeilRapporteurPE4
	"""
	try:
		return allRapporteursNames[3].get_text()
	except:
		#~ print "no rapporteurPE4! (oeil)"
		return None

#below "Rapporteur", name of the fourth Rapporteur
#can be NULL


def getOeilEtatMbRapport4(oeilEtatMbRapportList):
	"""
	FUNCTION
	get the oeilEtatMbRapport4 variable from the oeil url
	PARAMETERS
	allEtatMbRapport: allEtatMbRapport variable
	RETURN
	oeilEtatMbRapport4
	"""
	try:
		return oeilEtatMbRapportList[3]
	except:
		#~ print "no oeilEtatMbRapport4!"
		return None

#on the deputy's personal page: country (next to the flag, next to the picture)
#can be NULL
#27 possible values (EU countries)


def getOeilGroupePolitiqueRapporteur5(allPoliticalGroups):
	"""
	FUNCTION
	get the oeilGroupePolitiqueRapporteur5 variable from the oeil url
	PARAMETERS
	allPoliticalGroups: allPoliticalGroups variable
	RETURN
	oeilGroupePolitiqueRapporteur5
	"""
	try:
		return allPoliticalGroups[4].get_text()
	except:
		#~ print "no groupePolitiqueRapporteur5! (oeil)"
		return None

#below "Rapporteur", before the name of the fifth Rapporteur
#can be NULL


def getOeilRapporteurPE5(allRapporteursNames):
	"""
	FUNCTION
	get the oeilRapporteurPE5 variable from the oeil url
	PARAMETERS
	allRapporteursNames: allRapporteursNames variable
	RETURN
	oeilRapporteurPE5
	"""
	try:
		return allRapporteursNames[4].get_text()
	except:
		#~ print "no rapporteurPE5! (oeil)"
		return None

#below "Rapporteur", name of the fifth Rapporteur
#can be NULL


def getOeilEtatMbRapport5(oeilEtatMbRapportList):
	"""
	FUNCTION
	get the oeilEtatMbRapport5 variable from the oeil url
	PARAMETERS
	allEtatMbRapport: allEtatMbRapport variable
	RETURN
	oeilEtatMbRapport5
	"""
	try:
		return oeilEtatMbRapportList[4]
	except:
		#~ print "no oeilEtatMbRapport5!"
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
	modifProposList=["Modified legislative proposal published", "Amended legislative proposal for reconsultation published", "Legislative proposal published"]
	for modifPropos in modifProposList:
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


def getOeilNombreLectures(soup, suite2eLecturePE):
	"""
	FUNCTION
	get the oeilNombreLectures variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	oeilNombreLectures
	"""
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
	if noUniqueType=="COD" or noUniqueType=="ACI":
		return soup.find("td", text="Final act signed").findPrevious("td").get_text()
	#null value
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

	#oeilEPAmdtTabled
	dataDic['oeilEPAmdtTabled']=getOeilEPAmdtTabled(votesPageSoup)
	print "oeilEPAmdtTabled:", dataDic['oeilEPAmdtTabled']

	#oeilEPAmdtAdopt
	dataDic['oeilEPAmdtAdopt']=getOeilEPAmdtAdopt(votesPageSoup)
	print "oeilEPAmdtAdopt:", dataDic['oeilEPAmdtAdopt']

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

	#all rapporteurs's political groups
	allPoliticalGroups=getAllOeilGroupePolitiqueRapporteur(rapporteursSectionSoup)

	#all rapporteurs's names
	allRapporteursNames=getAllOeilRapporteurPE(rapporteursSectionSoup)

	#all rapporteurs's personal pages
	allOeilEtatMbRapports=getAllOeilEtatMbRapport(rapporteursSectionSoup)

	#oeilGroupePolitiqueRapporteur1
	dataDic['oeilGroupePolitiqueRapporteur1']=getOeilGroupePolitiqueRapporteur1(allPoliticalGroups)
	print "oeilGroupePolitiqueRapporteur1:", dataDic['oeilGroupePolitiqueRapporteur1']

	#oeilRapporteurPE1
	dataDic['oeilRapporteurPE1']=getOeilRapporteurPE1(allRapporteursNames)
	print "oeilRapporteurPE1:", dataDic['oeilRapporteurPE1']

	#oeilEtatMbRapport1
	dataDic['oeilEtatMbRapport1']=getOeilEtatMbRapport1(allOeilEtatMbRapports)
	print "oeilEtatMbRapport1:", dataDic['oeilEtatMbRapport1']

	#oeilGroupePolitiqueRapporteur2
	dataDic['oeilGroupePolitiqueRapporteur2']=getOeilGroupePolitiqueRapporteur2(allPoliticalGroups)
	print "oeilGroupePolitiqueRapporteur2:", dataDic['oeilGroupePolitiqueRapporteur2']

	#oeilRapporteurPE2
	dataDic['oeilRapporteurPE2']=getOeilRapporteurPE2(allRapporteursNames)
	print "oeilRapporteurPE2:", dataDic['oeilRapporteurPE2']

	#oeilEtatMbRapport2
	dataDic['oeilEtatMbRapport2']=getOeilEtatMbRapport2(allOeilEtatMbRapports)
	print "oeilEtatMbRapport2:", dataDic['oeilEtatMbRapport2']

	#oeilGroupePolitiqueRapporteur3
	dataDic['oeilGroupePolitiqueRapporteur3']=getOeilGroupePolitiqueRapporteur3(allPoliticalGroups)
	print "oeilGroupePolitiqueRapporteur3:", dataDic['oeilGroupePolitiqueRapporteur3']

	#oeilRapporteurPE3
	dataDic['oeilRapporteurPE3']=getOeilRapporteurPE3(allRapporteursNames)
	print "oeilRapporteurPE3:", dataDic['oeilRapporteurPE3']

	#oeilEtatMbRapport3
	dataDic['oeilEtatMbRapport3']=getOeilEtatMbRapport3(allOeilEtatMbRapports)
	print "oeilEtatMbRapport3:", dataDic['oeilEtatMbRapport3']

	#oeilGroupePolitiqueRapporteur4
	dataDic['oeilGroupePolitiqueRapporteur4']=getOeilGroupePolitiqueRapporteur4(allPoliticalGroups)
	print "oeilGroupePolitiqueRapporteur4:", dataDic['oeilGroupePolitiqueRapporteur4']

	#oeilRapporteurPE4
	dataDic['oeilRapporteurPE4']=getOeilRapporteurPE4(allRapporteursNames)
	print "oeilRapporteurPE4:", dataDic['oeilRapporteurPE4']

	#oeilEtatMbRapport4
	dataDic['oeilEtatMbRapport4']=getOeilEtatMbRapport4(allOeilEtatMbRapports)
	print "oeilEtatMbRapport4:", dataDic['oeilEtatMbRapport4']

	#oeilGroupePolitiqueRapporteur5
	dataDic['oeilGroupePolitiqueRapporteur5']=getOeilGroupePolitiqueRapporteur5(allPoliticalGroups)
	print "oeilGroupePolitiqueRapporteur5:", dataDic['oeilGroupePolitiqueRapporteur5']

	#oeilRapporteurPE5
	dataDic['oeilRapporteurPE5']=getOeilRapporteurPE5(allRapporteursNames)
	print "oeilRapporteurPE5:", dataDic['oeilRapporteurPE5']

	#oeilEtatMbRapport5
	dataDic['oeilEtatMbRapport5']=getOeilEtatMbRapport5(allOeilEtatMbRapports)
	print "oeilEtatMbRapport5:", dataDic['oeilEtatMbRapport5']

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
