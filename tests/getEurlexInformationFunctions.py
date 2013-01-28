# -*- coding: utf-8 -*-
"""
get the information from Eurlex (fields for the statistical analysis)
TEST GITHUB
"""
import re
from bs4 import BeautifulSoup


def getTitreEnFromEurlex(soup):
	"""
	FUNCTION
	get the titreEn variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	titreEn
	"""
	return soup.find("h2", text="Title and reference").findNext("p")


def getDirectoryCodeFromEurlex(soup):
	"""
	FUNCTION
	get the html code of the directory code part from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	beginning of the directory code part
	"""
	return soup.find("a", text="Directory code:")


def getCodeSectRep01FromEurlex(soup):
	"""
	FUNCTION
	get the codeSectRep01 variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	codeSectRep01
	"""
	return soup.findNext('em')


def getCodeSectRep02FromEurlex(soup):
	"""
	FUNCTION
	get the codeSectRep02 variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	codeSectRep02
	"""
	return soup.findNext('em').findNext('em')


def getRepEn1FromEurlex(soup):
	"""
	FUNCTION
	get the repEn1 variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	repEn1
	"""
	return None


def getRepEn2FromEurlex(soup):
	"""
	FUNCTION
	get the repEn2 variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	repEn2
	"""
	return None


def getTypeActeFromEurlex(soup):
	"""
	FUNCTION
	get the typeActe variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	typeActe
	"""
	author=soup.find("h2", text="Miscellaneous information").findNext("strong", text="Author:").findNext('br').next.strip()
	form=soup.find("h2", text="Miscellaneous information").findNext("strong", text="Form:").findNext('br').next.strip()
	return author+" "+form


def getBaseJuridiqueFromEurlex(soup):
	"""
	FUNCTION
	get the baseJuridique variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	baseJuridique
	"""
	return soup.find("h2", text="Relationship between documents").findNext("strong", text="Legal basis:").findNext('a')


def getEurlexInformation(soup):
	"""
	FUNCTION
	get all the information from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	dictionary of retrieved data from eurlex
	"""
	dataDic={}
	
	#titreEn
	dataDic['titreEn']=getTitreEnFromEurlex(soup)
	print "titreEn (eurlex):", dataDic['titreEn']
	
	directoryCodeSoup=getDirectoryCodeFromEurlex(soup)
	
	#codeSectRep01
	dataDic['codeSectRep01']=getCodeSectRep01FromEurlex(directoryCodeSoup)
	print "codeSectRep01 (eurlex):", dataDic['codeSectRep01']

	#codeSectRep02
	dataDic['codeSectRep02']=getCodeSectRep02FromEurlex(directoryCodeSoup)
	print "codeSectRep02 (eurlex):", dataDic['codeSectRep02']

	#repEn1
	dataDic['repEn1']=getRepEn1FromEurlex(directoryCodeSoup)
	print "repEn1 (eurlex):", dataDic['repEn1']

	#repEn2
	dataDic['repEn2']=getRepEn2FromEurlex(directoryCodeSoup)
	print "repEn2 (eurlex):", dataDic['repEn2']

	#typeActe
	dataDic['typeActe']=getTypeActeFromEurlex(soup)
	print "typeActe (eurlex):", dataDic['typeActe']
	
	#baseJuridique
	dataDic['baseJuridique']=getBaseJuridiqueFromEurlex(soup)
	print "baseJuridique (eurlex):", dataDic['baseJuridique']

	return dataDic
