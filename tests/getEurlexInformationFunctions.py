# -*- coding: utf-8 -*-
"""
get the information from Eurlex (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag


def getTitreEnFromEurlex(soup):
	"""
	FUNCTION
	get the titreEn variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	titreEn
	"""
	return soup.find("h2", text="Title and reference").findNext("p").get_text()


def getDirectoryCodeFromEurlex(soup):
	"""
	FUNCTION
	get the html code of the directory code part from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	directory code part
	"""
	return soup.find("strong", text="Directory code:").findParent()


def getCodeSectRep01FromEurlex(soup):
	"""
	FUNCTION
	get the codeSectRep01 variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	codeSectRep01
	"""
	return soup.findNext('em').get_text().strip()


def getCodeSectRep02FromEurlex(soup):
	"""
	FUNCTION
	get the codeSectRep02 variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	codeSectRep02
	"""
	return soup.findNext('em').findNext('em').get_text().strip()


def getRepEn1FromEurlex(soup):
	"""
	FUNCTION
	get the repEn1 variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	repEn1
	"""

	i=0
	found=False
	while i<20:
		nextElement=soup.nextSibling
		print nextElement
		i+=1
		if type(nextElement) is Tag:
			print nextElement
			if nextElement.name!=u'em':
				if nextElement.name==u'a':
					print nextElement.get_text()
			else:
				found=True
	
	#~ print soup.nextSibling
	#~ repEn1=""
	#~ soup=soup.findNext('em')
	#~ print soup.contents
	#~ for item in soup.contents:
		#~ if type(item) is Tag:
			#~ if item.name!=u'em':
				#~ if item.name==u'a':
					#~ print item.get_text()
					#~ repEn1+=item.get_text()+"; "
			#~ else:
				#~ print "em found"

	#~ print "repEn1", repEn1
#~ 
	#~ for a in soup.childGenerator():
		 #~ print "type", type(a)
		 #~ print "str", str(a)

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
	return soup.find("h2", text="Relationship between documents").findNext("strong", text="Legal basis:").findNext('a').get_text()


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
