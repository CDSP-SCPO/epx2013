"""
get the ids from Oeil
"""

import urllib
import re
from bs4 import BeautifulSoup
import configurationFile as conf


def getOeilUrl(noUniqueType, noUniqueAnnee, noUniqueChrono):
	"""
	FUNCTION
	returns the oeil url
	PARAMETERS
	noUniqueAnnee: noUniqueAnnee variable
	noUniqueChrono: noUniqueChrono variable
	noUniqueType: noUniqueType variable
	RETURN
	url of the oeil page
	"""
	#noUniqueChrono coded on 4 digits if numbers only and 5 if final character is a letter
	#if only digits
	if noUniqueChrono[-1].isdigit():
		noUniqueChronoLen=4
	else:
		noUniqueChronoLen=5

	while len(noUniqueChrono)!=noUniqueChronoLen:
		noUniqueChrono="0"+str(noUniqueChrono)

	#http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2005/0223(COD)
	#~ dummyUrl="http://www.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=NOUNIQUEANNEE/NOUNIQUECHRONO(NOUNIQUETYPE)"
	dummyUrl=conf.oeilUrl
	dummyUrl=dummyUrl.replace("NOUNIQUEANNEE", noUniqueAnnee, 1)
	dummyUrl=dummyUrl.replace("NOUNIQUECHRONO", noUniqueChrono, 1)
	dummyUrl=dummyUrl.replace("NOUNIQUETYPE", noUniqueType, 1)
	return dummyUrl


def getOeilUrlContent(url):
	"""
	FUNCTION
	checks if the oeil url exists and return its content
	PARAMETERS
	url: oeil url
	RETURN
	content of the page if the url exists and false otherwise
	"""
	try:
		soup = BeautifulSoup(urllib.urlopen(url))
		if (soup.title.string=="Procedure File: ERROR"):
			return False
		else:
			return soup
	except:
		return False


def getEurlexIdFromOeil(soup):
	"""
	FUNCTION
	gets noCelex from oeil
	PARAMETERS
	soup: oeil url content
	RETURN
	noCelex
	"""
	try:
		noCelex=soup.find("div", {"id": "final_act"}).find("a", {"class": "sumbutton"})["title"]
		return noCelex.split(" ")[-1]

	except:
		#~ print "numero celex PAS ok (oeil):"
		return None


def getOeilIdsFromOeil(soup):
	"""
	FUNCTION
	gets oeil ids from oeil
	PARAMETERS
	soup: oeil url content
	RETURN
	oeil ids (noUniqueType, noUniqueAnnee, noUniqueChrono)
	"""
	try:
		title=soup.title.string
		#~ print "title (oeil):", title
		#Procedure File: 2005/0223(COD)
		title = title.replace('Procedure File: ','').split("/")
		print "new title (oeil):", title
		noUniqueAnnee=title[0]
		title=title[1].split("(")
		tempNoUniqueChrono=title[0]
		#we remove the 0s at the beginning
		beginIndex=0
		for character in tempNoUniqueChrono:
			if character=="0":
				beginIndex+=1
			else:
				break
		noUniqueChrono=tempNoUniqueChrono[beginIndex:]
		noUniqueType=title[1][:-1].upper()

		return noUniqueType, noUniqueAnnee, noUniqueChrono
	except:
		return None, None, None


def getPrelexIdsFromOeil(soup):
	"""
	FUNCTION
	gets prelex ids from oeil
	PARAMETERS
	soup: oeil url content
	RETURN
	prelex ids (proposOrigine, proposAnnee, proposChrono)
	"""
	#3 different kinds of acts -> 3 possibilities to retrieve prelex ids
	kindOfAct=["Legislative proposal published", "Non-legislative basic document", "Supplementary legislative basic document", "Initial legislative proposal published"]
	for act in kindOfAct:
		try:
			prelex=soup.find(text=act).findParent().findParent().find("td", {"class": "event_column_document"}).find('a')
			#~ print "prelex (oeil):", prelex
			prelexIds=prelex.get_text().strip()
			#~ print "prelexIds (oeil):", prelexIds

			if prelexIds=="":
				prelexIds=prelex.previousSibling.strip()

			#~ print "prelexId (oeil):", prelexIds
			prelexIds=prelexIds.split('(')
			proposOrigine=prelexIds[0].upper()
			prelexIds=prelexIds[1].split(')')
			proposAnnee=prelexIds[0]
			tempProposChrono=prelexIds[1]
			#~ print "tempProposChrono (oeil):", tempProposChrono

			#remove trailing zeros
			beginIndex=0
			for character in tempProposChrono:
				if character=="0":
					beginIndex+=1
				else:
					break

			#if regex catches text after oeil ids, we delete it -> starts with '\r' or `'n'
			spaces=tempProposChrono.find('\r')
			endIndex=spaces

			spaces=tempProposChrono.find('\n')
			if spaces!=-1 and (spaces<endIndex or endIndex==-1):
				endIndex=spaces

			if endIndex==-1:
				proposChrono=tempProposChrono[beginIndex:]
			else:
				proposChrono=tempProposChrono[beginIndex:endIndex]
			break

		except:
			proposOrigine=None
			proposAnnee=None
			proposChrono=None
			print "no prelex page (oeil)"

	return proposOrigine, proposAnnee, proposChrono


def getAllOeilIds(soup):
	"""
	FUNCTION
	gets all the ids from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	dictionary of retrieved data from oeil
	"""
	dataDic={}

	#eurlex id
	dataDic['oeilNoCelex']=getEurlexIdFromOeil(soup)
	print "oeilNoCelex:", dataDic['oeilNoCelex']

	#oeil ids
	dataDic['oeilNoUniqueType'], dataDic['oeilNoUniqueAnnee'], dataDic['oeilNoUniqueChrono']=getOeilIdsFromOeil(soup)
	print "oeilNoUniqueType:", dataDic['oeilNoUniqueType']
	print "oeilNoUniqueAnnee:", dataDic['oeilNoUniqueAnnee']
	print "oeilNoUniqueChrono:", dataDic['oeilNoUniqueChrono']

	#prelex ids
	dataDic['oeilProposOrigine'], dataDic['oeilProposAnnee'], dataDic['oeilProposChrono']= getPrelexIdsFromOeil(soup)
	print "oeilProposOrigine:", dataDic['oeilProposOrigine']
	print "oeilProposAnnee:", dataDic['oeilProposAnnee']
	print "oeilProposChrono:", dataDic['oeilProposChrono']

	return dataDic
