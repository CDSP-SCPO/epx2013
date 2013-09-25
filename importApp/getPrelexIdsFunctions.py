"""
get the ids from Prelex
"""

import urllib
import re
from bs4 import BeautifulSoup
import configurationFile as conf


def getOldPrelexUrl(proposOrigine, proposAnnee, proposChrono):
	"""
	FUNCTION
	returns the old prelex url
	PARAMETERS
	proposOrigine: proposOrigine variable
	proposAnnee: proposAnnee variable
	proposChrono: proposChrono variable
	RETURN
	url of the old prelex page
	"""
	#http://prelex.europa.eu/liste_resultats.cfm?ReqId=0&CL=en&DocType=COM&DocYear=2005&DocNum=566
	#~ dummyUrl="http://prelex.europa.eu/liste_resultats.cfm?ReqId=0&CL=en&DocType=PROPOSORIGINE&DocYear=PROPOSANNEE&DocNum=PROPOSCHRONO"
	dummyUrl=conf.oldPrelexUrl
	dummyUrl=dummyUrl.replace("PROPOSORIGINE", proposOrigine, 1)
	dummyUrl=dummyUrl.replace("PROPOSANNEE", proposAnnee, 1)
	dummyUrl=dummyUrl.replace("PROPOSCHRONO", proposChrono, 1)
	return dummyUrl

def getOldPrelexUrlWithOeilIds(noUniqueType, noUniqueAnnee, noUniqueChrono):
	"""
	FUNCTION
	returns the old prelex url with the oeils ids (USEFUL if proposChrono contains a dash)
	PARAMETERS
	proposOrigine: proposOrigine variable
	proposAnnee: proposAnnee variable
	proposChrono: proposChrono variable
	RETURN
	url of the old prelex page
	"""
	#noUniqueChrono coded on 4 digits if numbers only and 5 if final character is a letter
	#proposChrono coded on 4 digits
	if noUniqueChrono[-1].isdigit():
		noUniqueChronoLen=4
	else:
		noUniqueChronoLen=5

	while len(noUniqueChrono)!=noUniqueChronoLen:
		noUniqueChrono="0"+str(noUniqueChrono)

	#http://ec.europa.eu/prelex/liste_resultats.cfm?CL=en&ReqId=0&DocType=COD&DocYear=2005&DocNum=0223
	#~ dummyUrl="http://ec.europa.eu/prelex/liste_resultats.cfm?CL=en&ReqId=0&DocType=NOUNIQUETYPE&DocYear=NOUNIQUEANNEE&DocNum=0NOUNIQUECHRONO"
	dummyUrl=conf.oldPrelexUrlWithOeilIds
	dummyUrl=dummyUrl.replace("NOUNIQUETYPE", noUniqueType, 1)
	dummyUrl=dummyUrl.replace("NOUNIQUEANNEE", noUniqueAnnee, 1)
	dummyUrl=dummyUrl.replace("NOUNIQUECHRONO", noUniqueChrono, 1)
	return dummyUrl

def getPrelexUrl(dossierId):
	"""
	FUNCTION
	returns the prelex url (USEFUL if proposChrono contains a dash and there is no noUnique)
	PARAMETERS
	dossierId: dossierId variable
	RETURN
	url of the prelex page
	"""
	#http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=193517
	#~ dummyUrl="http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=DOSSIERID"
	dummyUrl=conf.newPrelexUrl
	dummyUrl=dummyUrl.replace("DOSSIERID", str(dossierId), 1)
	return dummyUrl


def getPrelexUrlContent(url):
	"""
	FUNCTION
	checks if the prelex url exists and return its content
	PARAMETERS
	url: prelex url
	RETURN
	content of the page if the url exists and false otherwise
	"""
	try:
		soup = BeautifulSoup(urllib.urlopen(url))
		if soup.find(text='This page does not exists') or soup.find(text=re.compile('The document is not available in PreLex')):
			return False
		else:
			return soup
	except:
		return False


def getEurlexIdFromPrelex(soup):
	"""
	FUNCTION
	gets nosCelex from prelex
	PARAMETERS
	soup: prelex url content
	RETURN
	nosCelex
	"""
	try:
		eurlexUrls=[text.get('href') for text in soup.findAll('a', {"href": re.compile("^(.)*uri=CELEX:[0-9](195[789]|19[6-9][0-9]|20[0-1][0-9])[dflrDFLR][0-9]{4}(\(01\)|R\(01\))?")})]
		nosCelex=set()
		for eurlexUrl in eurlexUrls:
			nosCelex.add(eurlexUrl.split(":")[2])
		return nosCelex
	except:
		print "no eurlex page (prelex)"
		return None

def getOeilIdsFromPrelex(soup):
	"""
	FUNCTION
	gets oeil ids from prelex
	PARAMETERS
	soup: prelex url content
	RETURN
	oeil ids (noUniqueType, noUniqueAnnee, noUniqueChrono)
	"""
	try:
		oeilIds=soup.get_text()
		#~ print "oeil ids (prelex):", oldOeilUrl
		oeilIds=oeilIds.split("/")
		noUniqueType=oeilIds[2].upper()
		noUniqueAnnee=oeilIds[0]
		tempNoUniqueChrono=oeilIds[1]
		#we remove the 0s at the beginning
		beginIndex=0
		for character in tempNoUniqueChrono:
			if character=="0":
				beginIndex+=1
			else:
				break
		noUniqueChrono=tempNoUniqueChrono[beginIndex:]

	except:
		noUniqueType=None
		noUniqueAnnee=None
		noUniqueChrono=None
		print "no oeil page (prelex)"

	return noUniqueType, noUniqueAnnee, noUniqueChrono


def getPrelexDosIdFromPrelex(soup):
	"""
	FUNCTION
	gets prelex dosId from prelex
	PARAMETERS
	soup: prelex url content
	RETURN
	dosId
	"""
	try:
		dosId=soup.find('a', {"href": re.compile("DosId=")})['href']
		return dosId[(str(dosId).rfind('=')+1):]
	except:
		print "problem on page (prelex)"
		return None


def getPrelexIdsFromPrelex(soup):
	"""
	FUNCTION
	gets prelex ids from prelex
	PARAMETERS
	soup: prelex url content
	RETURN
	prelex ids (proposOrigine, proposAnnee, proposChrono)
	"""
	try:
		prelexIds=soup.get_text()
		#~ print "prelex ids (prelex):", prelexId
		prelexIds="".join(prelexIds.split())
		prelexIds=prelexIds.split("(")
		proposOrigine=prelexIds[0]
		prelexIds=prelexIds[1].split(")")
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
		return proposOrigine, proposAnnee, proposChrono

	except:
		return None, None, None


def getAllPrelexIds(soup):
	"""
	FUNCTION
	gets all the ids from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	dictionary of retrieved data from prelex
	"""
	dataDic={}

	#eurlex id
	dataDic['prelexNosCelex']=getEurlexIdFromPrelex(soup)
	print "dataDic['prelexNosCelex']:", dataDic['prelexNosCelex']

	prelexAndOeilIds=soup.findAll('font', {'size': "-1"})

	#if there is no error on the page
	if prelexAndOeilIds!=[]:
		#oeil ids
		dataDic['prelexNoUniqueType'], dataDic['prelexNoUniqueAnnee'], dataDic['prelexNoUniqueChrono']=getOeilIdsFromPrelex(prelexAndOeilIds[1])
		print "prelexNoUniqueType:", dataDic['prelexNoUniqueType']
		print "prelexNoUniqueAnnee:", dataDic['prelexNoUniqueAnnee']
		print "prelexNoUniqueChrono:", dataDic['prelexNoUniqueChrono']

		#prelex dosId
		dataDic['prelexDosId']=getPrelexDosIdFromPrelex(soup)
		print "prelexDosId:", dataDic['prelexDosId']

		#prelex ids
		dataDic['prelexProposOrigine'], dataDic['prelexProposAnnee'], dataDic['prelexProposChrono']= getPrelexIdsFromPrelex(prelexAndOeilIds[0])
		print "prelexProposOrigine:", dataDic['prelexProposOrigine']
		print "prelexProposAnnee:", dataDic['prelexProposAnnee']
		print "prelexProposChrono:", dataDic['prelexProposChrono']
	else:
		#if problems on page (just beginning with titles but nothing about the act)
		print "problem on page (prelex)"
		dataDic['prelexNoUniqueType']=None
		dataDic['prelexNoUniqueAnnee']=None
		dataDic['prelexNoUniqueChrono']=None
		dataDic['prelexDosId']=None
		dataDic['prelexProposOrigine']=None
		dataDic['prelexProposAnnee']=None
		dataDic['prelexProposChrono']=None
		dataDic['prelexPrelexUrlExists']=False

	return dataDic
