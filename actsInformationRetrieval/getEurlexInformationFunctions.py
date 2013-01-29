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

#right under "Title and reference"
#not NULL



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

#first code under "Directory code:"
#8 chiffres sous cette forme : 12.34.56.78
#not NULL
#TODO:
#~ Lorsqu’exceptionnellement, on ne trouve pas de code répertoire sur la fiche Celex de l’acte :
#~ - on le cherche l’acte en question dans la liste des actes par secteur sur le site du répertoire http://eur-
#~ lex.europa.eu/fr/repert/index.htm
#~ - si c’est infructueux, on prend le(s) code(s) répertoire(s) de l’acte qu’il modifie.


def getCodeSectRep02FromEurlex(soup):
	"""
	FUNCTION
	get the codeSectRep02 variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	codeSectRep02
	"""
	try:
		return soup.findNext('em').findNext('em').get_text().strip()
	except:
		return None

#second code under "Directory code:"
#8 chiffres sous cette forme : 12.34.56.78
#not NULL?


def getRepEnFromEurlex(soup):
	"""
	FUNCTION
	get the repEn1 and repEn2 variables from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	repEn1 and repEn2
	"""
	linksList=soup.findAll('a')
	#find where the 2 variables get separated
	for link in linksList:
		if link.nextSibling.strip()!="/":
			index=linksList.index(link)+1
			break

	#repEn1
	repEn1=""
	for i in range(index):
		repEn1+=linksList[i].get_text()+"; "
	
	#repEn2
	repEn2=""
	for i in range(index, len(linksList)):
		repEn2+=linksList[i].get_text()+"; "

	return repEn1[:-2], repEn2[:-2]

#texts in front of the codeSectRep01 and codeSectRep02 variables (under "Directory code:")
#not NULL


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

#act type under Miscellaneous information->Author and Miscellaneous information->Form
#not NULL
#List of possible values (acronyms of real values): CS DEC, CS DEC CAD, CS DVE, CS REG, DEC, DVE, REG, CS DEC SUI, DEC SUI.


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

#under "Legal basis:"
#not null
#decomposition of the variable:
#~ 1/ 1, 2, 3 ou 4
#~ 2/ 4 chiffres suivants : année de l'acte constituant la base juridique
#~ 3/ "E", "M", "R", "L" ou "D" 
#~ 4/ 3 or 4 figures
#~ 5/éventuellement tiret puis au choix:
#~ (
	#~ - "A": followed by figures
	#~ - "P": followed by figures
	#~ - "FR": followed by figures
	#~ - "L": followed by figures
	#~ - "PT": followed by (one figure or one caps letter or one roman figure) and one parenthesis and/or one caps letter and one parenthesis and/or figures and sometimes one parenthesis
#~ ) -> can be repeated


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

	repEn=getRepEnFromEurlex(directoryCodeSoup)
	
	#repEn1
	dataDic['repEn1']=repEn[0]
	print "repEn1 (eurlex):", dataDic['repEn1']

	#repEn2
	dataDic['repEn2']=repEn[1]
	print "repEn2 (eurlex):", dataDic['repEn2']

	#typeActe
	dataDic['typeActe']=getTypeActeFromEurlex(soup)
	print "typeActe (eurlex):", dataDic['typeActe']
	
	#baseJuridique
	dataDic['baseJuridique']=getBaseJuridiqueFromEurlex(soup)
	print "baseJuridique (eurlex):", dataDic['baseJuridique']

	return dataDic
