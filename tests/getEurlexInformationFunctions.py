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


def getCodeSectRepFromEurlex(soup):
	"""
	FUNCTION
	get the codeSectRep01-04 variables from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	codeSectRep01, codeSectRep02, codeSectRep03, codeSectRep04
	"""
	codeSectRep=soup.findAll('em')
	codeSectRepVars=[]
	for i in range(4):
		codeSectRepVars.append(None)

	for i in range(len(codeSectRep)):
		codeSectRepVars[i]=codeSectRep[i].get_text().strip()
	
	return codeSectRepVars[0], codeSectRepVars[1], codeSectRepVars[2], codeSectRepVars[3]

#first, second, third and fourth code under "Directory code:"
#8 chiffres sous cette forme : 12.34.56.78
#first not NULL
#second, third and fourth: can be null


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
	delimitorsList=[]
	repEn1=repEn2=repEn3=repEn4=""
	#find where 2 variables get separated
	for link in linksList:
		if link.nextSibling.strip()!="/":
			delimitorsList.append(linksList.index(link)+1)

	#repEn1 
	for i in range(delimitorsList[0]):
		repEn1+=linksList[i].get_text()+"; "
	
	try:
		#repEn2
		for i in range(delimitorsList[0], delimitorsList[1]):
			repEn2+=linksList[i].get_text()+"; "
			
		#repEn3
		for i in range(delimitorsList[1], delimitorsList[2]):
			repEn3+=linksList[i].get_text()+"; "
		
		#repEn4
		for i in range(delimitorsList[2], len(linksList)):
			repEn4+=linksList[i].get_text()+"; "
	except:
		print "less than four repEn"

	return repEn1[:-2], repEn2[:-2], repEn3[:-2], repEn4[:-2]

#texts in front of the codeSectRep01 and codeSectRep02 variables (under "Directory code:")
#codeSectRep01 not NULL
#codeSectRep02 can be Null


def getTypeActeFromEurlex(soup):
	"""
	FUNCTION
	get the typeActe variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	typeActe
	"""
	#author part
	author=soup.find("h2", text="Miscellaneous information").findNext("strong", text="Author:").findNext('br').next.strip().lower()
	#form part
	form=soup.find("h2", text="Miscellaneous information").findNext("strong", text="Form:").findNext('br').next.strip().lower()
	
	#return acronyms
	authorAcronym=""
	if "european parliament" not in author:
		authorAcronym="CS "
	#decision
	if "decision" in form:
		#framework decision
		if "framework" in form:
			return authorAcronym+"DEC CAD"
		if "without addressee" in form:
			return authorAcronym+"DEC W/O ADD"
		return authorAcronym+"DEC"
	#directive
	if form=="directive":
		return authorAcronym+"DVE"
	#regulation
	if form=="regulation":
		return authorAcronym+"REG"

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
	#http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32002L0090:EN:NOT
	li=soup.find("h2", text="Relationship between documents").findNext("strong", text="Legal basis:").findParent('li')
	legalBases=li.findAll('a')
	var=""
	for legalBasis in legalBases:
		var+=legalBasis.get_text()+legalBasis.nextSibling.strip()+"; "
	
	return var[:-2]

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
	
	#codeSectRep01, codeSectRep02, codeSectRep03, codeSectRep04
	dataDic['codeSectRep01'], dataDic['codeSectRep02'], dataDic['codeSectRep03'], dataDic['codeSectRep04']=getCodeSectRepFromEurlex(directoryCodeSoup)
	print "codeSectRep01 (eurlex):", dataDic['codeSectRep01']
	print "codeSectRep02 (eurlex):", dataDic['codeSectRep02']
	print "codeSectRep03 (eurlex):", dataDic['codeSectRep03']
	print "codeSectRep04 (eurlex):", dataDic['codeSectRep04']

	#repEn1, repEn2, repEn3, repEn4
	dataDic['repEn1'], dataDic['repEn2'], dataDic['repEn3'], dataDic['repEn4']=getRepEnFromEurlex(directoryCodeSoup)
	print "repEn1 (eurlex):", dataDic['repEn1']
	print "repEn2 (eurlex):", dataDic['repEn2']
	print "repEn3 (eurlex):", dataDic['repEn3']
	print "repEn4 (eurlex):", dataDic['repEn4']

	#typeActe
	dataDic['typeActe']=getTypeActeFromEurlex(soup)
	print "typeActe (eurlex):", dataDic['typeActe']
	
	#baseJuridique
	dataDic['baseJuridique']=getBaseJuridiqueFromEurlex(soup)
	print "baseJuridique (eurlex):", dataDic['baseJuridique']

	return dataDic
