# -*- coding: utf-8 -*-
"""
get the information from Eurlex (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag


def getEurlexTitreEn(soup):
	"""
	FUNCTION
	get the eurlexTitreEn variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	eurlexTitreEn
	"""
	return soup.find("h2", text="Title and reference").findNext("p").get_text()

#right under "Title and reference"
#not NULL



def getEurlexDirectoryCode(soup):
	"""
	FUNCTION
	get the html code of the directory code part from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	directory code part
	"""
	try:
		return soup.find("strong", text="Directory code:").findParent()
	except:
		print "no directory code section (eurlex)!"
		return None


def getEurlexCodeSectRep(soup):
	"""
	FUNCTION
	get the codeSectRep01-04 variables from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	eurlexCodeSectRep01, eurlexCodeSectRep02, eurlexCodeSectRep03, eurlexCodeSectRep04
	"""
	codeSectRepVars=[]
	codeSectRepVars.append(None)
	codeSectRepVars.append(None)
	codeSectRepVars.append(None)
	codeSectRepVars.append(None)
	try:
		codeSectRep=soup.findAll('em')
		for i in range(4):
			codeSectRepVars.append(None)

		for i in range(len(codeSectRep)):
			codeSectRepVars[i]=codeSectRep[i].get_text().strip()
	except:
		print "no eurlexCodeSectRep!"

	return codeSectRepVars[0], codeSectRepVars[1], codeSectRepVars[2], codeSectRepVars[3]

#first, second, third and fourth code under "Directory code:"
#8 chiffres sous cette forme : 12.34.56.78
#first not NULL
#second, third and fourth: can be null


def getEurlexRepEn(soup):
	"""
	FUNCTION
	get the eurlexRepEn1, eurlexRepEn2, eurlexRepEn3 and eurlexRepEn4 variables from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	eurlexRepEn1, eurlexRepEn2, eurlexRepEn3 and eurlexRepEn4
	"""
	repEn1=repEn2=repEn3=repEn4=""
	try:
		linksList=soup.findAll('a')
		delimitorsList=[]
		#find where 2 variables get separated
		for link in linksList:
			if link.nextSibling.strip()!="/":
				delimitorsList.append(linksList.index(link)+1)

		#repEn1
		for i in range(delimitorsList[0]):
			repEn1+=linksList[i].get_text()+"; "

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

#texts in front of the eurlexCodeSectRep01, eurlexCodeSectRep02, eurlexCodeSectRep03 and eurlexCodeSectRep04 variables (under "Directory code:")
#eurlexRepEn1 not NULL
#eurlexRepEn2, eurlexRepEn3, eurlexRepEn4 can be Null


def getEurlexTypeActe(soup):
	"""
	FUNCTION
	get the eurlexTypeActe variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	eurlexTypeActe
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
		if "addressee" in form:
			if "without" in form:
				return authorAcronym+"DEC W/O ADD"
			return authorAcronym+"DEC W/ ADD"
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


def getEurlexBaseJuridique(soup):
	"""
	FUNCTION
	get the eurlexBaseJuridique variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	eurlexBaseJuridique
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

	#eurlexTitreEn
	dataDic['eurlexTitreEn']=getEurlexTitreEn(soup)
	print "eurlexTitreEn:", dataDic['eurlexTitreEn']

	directoryCodeSoup=getEurlexDirectoryCode(soup)

	#eurlexCodeSectRep01, eurlexCodeSectRep02, eurlexCodeSectRep03, eurlexCodeSectRep04
	dataDic['eurlexCodeSectRep01'], dataDic['eurlexCodeSectRep02'], dataDic['eurlexCodeSectRep03'], dataDic['eurlexCodeSectRep04']=getEurlexCodeSectRep(directoryCodeSoup)
	print "eurlexCodeSectRep01:", dataDic['eurlexCodeSectRep01']
	print "eurlexCodeSectRep02:", dataDic['eurlexCodeSectRep02']
	print "eurlexCodeSectRep03:", dataDic['eurlexCodeSectRep03']
	print "eurlexCodeSectRep04:", dataDic['eurlexCodeSectRep04']

	#eurlexRepEn1, eurlexRepEn2, eurlexRepEn3, eurlexRepEn4
	dataDic['eurlexRepEn1'], dataDic['eurlexRepEn2'], dataDic['eurlexRepEn3'], dataDic['eurlexRepEn4']=getEurlexRepEn(directoryCodeSoup)
	print "eurlexRepEn1:", dataDic['eurlexRepEn1']
	print "eurlexRepEn2:", dataDic['eurlexRepEn2']
	print "eurlexRepEn3:", dataDic['eurlexRepEn3']
	print "eurlexRepEn4:", dataDic['eurlexRepEn4']

	#eurlexTypeActe
	dataDic['eurlexTypeActe']=getEurlexTypeActe(soup)
	print "eurlexTypeActe:", dataDic['eurlexTypeActe']

	#eurlexBaseJuridique
	dataDic['eurlexBaseJuridique']=getEurlexBaseJuridique(soup)
	print "eurlexBaseJuridique:", dataDic['eurlexBaseJuridique']

	return dataDic
