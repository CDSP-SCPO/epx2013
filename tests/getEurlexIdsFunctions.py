"""
get the ids from Eurlex
"""

import urllib
import re
from bs4 import BeautifulSoup
import configurationFile as conf


def getEurlexUrl(noCelex):
	"""
	FUNCTION
	returns the eurlex url
	PARAMETERS
	noCelex: noCelex variable
	RETURN
	url of the eurlex page
	"""
	#http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32006R1921:EN:NOT
	#~ dummyUrl="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:NOCELEX:EN:NOT"
	dummyUrl=conf.eurlexUrl
	dummyUrl=dummyUrl.replace("NOCELEX", noCelex, 1)
	return dummyUrl


def getEurlexUrlContent(url):
	"""
	FUNCTION
	checks if the eurlex url exists and return its content
	PARAMETERS
	url: eurlex url
	RETURN
	content of the page if the url exists and false otherwise
	"""
	try:
		soup = BeautifulSoup(urllib.urlopen(url))
		if(soup.title.string=='EUR-Lex - Simple search'):
			return False
		else:
			return soup
	except:
		return False


def getEurlexIdFromEurlex(soup):
	"""
	FUNCTION
	gets noCelex from eurlex
	PARAMETERS
	soup: eurlex url content
	RETURN
	noCelex
	"""
	return soup.title.string.split("-")[2].strip()


def getOeilIdsFromEurlex(soup):
	"""
	FUNCTION
	gets oeil ids from eurlex
	PARAMETERS
	soup: eurlex url content
	RETURN
	oeil ids (noUniqueType, noUniqueAnnee, noUniqueChrono)
	"""
	try:
		oldOeilUrl=soup.find(text="European Parliament - Legislative observatory").findParent().findParent()['href']
		#~ print "old oeil url (eurlex):", oldOeilUrl
		#http://www.europarl.europa.eu/oeil/FindByProcnum.do?lang=2&procnum=COD/2005/0223
		
		oldOeilUrl=oldOeilUrl[oldOeilUrl.rfind('='):][1:].split("/")
		noUniqueType=oldOeilUrl[0].upper()
		#~ print 'noUniqueType (eurlex):', noUniqueType
		noUniqueAnnee=oldOeilUrl[1]
		#~ print 'noUniqueAnnee (eurlex):', noUniqueAnnee
		tempNoUniqueChrono=oldOeilUrl[2]
		#~ print "tempNoUniqueChrono (eurlex):", tempNoUniqueChrono
		beginIndex=0
		#we remove the 0s at the beginning
		for character in tempNoUniqueChrono:
			if character=="0":
				beginIndex+=1
			else:
				break
		noUniqueChrono=tempNoUniqueChrono[beginIndex:]
		#~ print 'noUniqueChrono (eurlex):', noUniqueChrono
	except:
		try:
			oeilIds=soup.find(text="Procedure number:").findNext('br').next.strip()
			#~ print "oeilIds (eurlex):", oeilIds
			oeilIds=oeilIds.split("(")
			noUniqueType=oeilIds[0].strip().upper()
			#~ print 'noUniqueType (eurlex):', noUniqueType
			oeilIds=oeilIds[1].split(")")
			noUniqueAnnee=oeilIds[0]
			#~ print 'noUniqueAnnee (eurlex):', noUniqueAnnee
			tempNoUniqueChrono=oeilIds[1].strip()
			#~ print "tempNoUniqueChrono (eurlex):", tempNoUniqueChrono
			#we remove the 0s at the beginning
			beginIndex=0
			for character in tempNoUniqueChrono:
				if character=="0":
					beginIndex+=1
				else:
					break
			noUniqueChrono=tempNoUniqueChrono[beginIndex:]
			#~ print 'noUniqueChrono (eurlex):', noUniqueChrono
		except:
			noUniqueType=None
			noUniqueAnnee=None
			noUniqueChrono=None
			print "no oeil page (eurlex)"
	
	return noUniqueType, noUniqueAnnee, noUniqueChrono


def getPrelexIdsFromEurlex(soup):
	"""
	FUNCTION
	gets prelex ids from eurlex
	PARAMETERS
	soup: eurlex url content
	RETURN
	prelex ids (proposOrigine, proposAnnee, proposChrono)
	"""
	try:
		prelexIds=soup.find(text=re.compile("Proposal Commission")).split(";")[1].strip()
		#~ print "prelexIds (eurlex):", prelexIds
		prelexIds=prelexIds.split(" ")
		proposOrigine=prelexIds[0].upper()
		if proposOrigine=="COMMITTEE":
			proposOrigine="COM"
		prelexIds=prelexIds[1].split("/")
		proposAnnee=prelexIds[0]
		tempProposChrono=prelexIds[1]
		#we remove the 0s at the beginning
		beginIndex=0
		for character in tempProposChrono:
			if character=="0":
				beginIndex+=1
			else:
				break
		proposChrono=tempProposChrono[beginIndex:]
	except:
		proposOrigine=None
		proposAnnee=None
		proposChrono=None
		print "no prelex page (eurlex)"
		
	return proposOrigine, proposAnnee, proposChrono


def getAllEurlexIds(soup):
	"""
	FUNCTION
	gets all the ids from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	dictionary of retrieved data from eurlex
	"""
	dataDic={}
	
	#noCelex
	dataDic['eurlexNoCelex']=getEurlexIdFromEurlex(soup)
	print "eurlexNoCelex:", dataDic['eurlexNoCelex']
	
	#oeil ids
	dataDic['eurlexNoUniqueType'], dataDic['eurlexNoUniqueAnnee'], dataDic['eurlexNoUniqueChrono']=getOeilIdsFromEurlex(soup)
	print 'eurlexNoUniqueType:', dataDic['eurlexNoUniqueType']
	print 'eurlexNoUniqueAnnee:', dataDic['eurlexNoUniqueAnnee']
	print 'eurlexNoUniqueChrono:', dataDic['eurlexNoUniqueChrono']
		
	#prelex ids
	dataDic['eurlexProposOrigine'], dataDic['eurlexProposAnnee'], dataDic['eurlexProposChrono']= getPrelexIdsFromEurlex(soup)
	print 'eurlexProposOrigine:', dataDic['eurlexProposOrigine']
	print 'eurlexProposAnnee:', dataDic['eurlexProposAnnee']
	print 'eurlexProposChrono:', dataDic['eurlexProposChrono']
		
	return dataDic
