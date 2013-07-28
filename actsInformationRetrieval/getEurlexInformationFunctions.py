# -*- coding: utf-8 -*-
"""
get the information from Eurlex (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag
from actsInformationRetrieval.models import CodeSectRepModel, CodeAgendaModel
from actsInformationRetrieval.getPrelexInformationFunctions import getConfigConsOrCodeAgenda
from common.commonFunctions import listReverseEnum, show


def getEurlexTitreEn(soup):
	"""
	FUNCTION
	get the eurlexTitreEn variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	eurlexTitreEn
	"""
	try:
		return soup.find("h2", text="Title and reference").findNext("p").get_text()
	except:
		print "no title (eurlex)!"
		return None

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


def getEurlexFullCodeSectRep(soup):
	"""
	FUNCTION
	get the fullCodeSectRep01-04 variables from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	fullCodeSectRepList: list of eurlexFullCodeSectRep variables
	"""
	fullCodeSectRepList=[None for i in range(4)]

	try:
		fullCodeSectReps=soup.findAll('em')

		for i in range(len(fullCodeSectReps)):
			fullCodeSectRepList[i]=fullCodeSectReps[i].get_text().strip()
	except:
		print "no eurlexFullCodeSectRep!"

	return fullCodeSectRepList

#first, second, third and fourth code under "Directory code:"
#8 chiffres sous cette forme : 12.34.56.78
#first not NULL
#second, third and fourth: can be null


def getEurlexCodeAgendas(eurlexCodeSectRepList):
	"""
	FUNCTION
	gets the eurlexCodeAgenda variable from eurlexCodeSectRepList, CodeSectRepModel and CodeAgendaModel
	PARAMETERS
	eurlexCodeSectRepList: list of eurlexCodeAgenda variables
	RETURN
	codeAgendaList: list of eurlexCodeAgenda variables associated to each eurlexCodeSectRep of eurlexCodeSectRepList
	"""
	codeAgendaList=[None for i in range(4)]
	table1=["CodeAgendaModel", "codeAgenda"]
	table2=["CodeSectRepModel", "codeSectRep", ""]
	#for each eurlexCodeSectRep
	for codeSectRepNum in range(len(eurlexCodeSectRepList)):
		table2[2]=eurlexCodeSectRepList[codeSectRepNum]
		codeAgendaList[codeSectRepNum]=getConfigConsOrCodeAgenda(table1, table2)
	return codeAgendaList


def getEurlexRepEn(soup):
	"""
	FUNCTION
	get the eurlexRepEn1, eurlexRepEn2, eurlexRepEn3 and eurlexRepEn4 variables from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	repEnList: list of eurlexRepEn variab1es
	"""
	repEnList=["" for i in range(4)]
	try:
		linksList=soup.findAll('a')
		delimitorsList=[]
		#find where 2 variables get separated
		for link in linksList:
			if link.nextSibling.strip()!="/":
				delimitorsList.append(linksList.index(link)+1)

		#repEn1
		for i in range(delimitorsList[0]):
			repEnList[0]+=linksList[i].get_text()+"; "

		#repEn2
		for i in range(delimitorsList[0], delimitorsList[1]):
			repEnList[1]+=linksList[i].get_text()+"; "

		#repEn3
		for i in range(delimitorsList[1], delimitorsList[2]):
			repEnList[2]+=linksList[i].get_text()+"; "

		#repEn4
		for i in range(delimitorsList[2], len(linksList)):
			repEnList[3]+=linksList[i].get_text()+"; "
	except:
		print "less than four repEn"

	return repEnList

#texts in front of the eurlexFullCodeSectRep01, eurlexFullCodeSectRep02, eurlexFullCodeSectRep03 and eurlexFullCodeSectRep04 variables (under "Directory code:")
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
	try:
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
	except:
		print "no act type (eurlex)!"
		return None

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
	try:
		#http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32002L0090:EN:NOT
		li=soup.find("h2", text="Relationship between documents").findNext("strong", text="Legal basis:").findParent('li')
		legalBases=li.findAll('a')
		var=""
		for legalBasis in legalBases:
			var+=legalBasis.get_text()+legalBasis.nextSibling.strip()+"; "

		return var[:-2]
	except:
		print "no base juridique (eurlex)!"
		return None

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



def getEurlexInformation(soup, extraFieldsDic={}):
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

	#eurlexFullCodeSectRep01, eurlexFullCodeSectRep02, eurlexFullCodeSectRep03, eurlexFullCodeSectRep04
	eurlexFullCodeSectRepList=getEurlexFullCodeSectRep(directoryCodeSoup)
	for index in xrange(len(eurlexFullCodeSectRepList)):
		num=str(index+1)
		dataDic['eurlexFullCodeSectRep0'+num]=eurlexFullCodeSectRepList[index]
		print 'eurlexFullCodeSectRep0'+num+": ", dataDic['eurlexFullCodeSectRep0'+num]

	#eurlexCodeAgenda01-4
	eurlexCodeAgendaList=getEurlexCodeAgendas(eurlexFullCodeSectRepList)
	for index in xrange(len(eurlexCodeAgendaList)):
		num=str(index+1)
		dataDic['eurlexCodeAgenda0'+num]=eurlexCodeAgendaList[index]
		print 'eurlexCodeAgenda0'+num+": ", dataDic['eurlexCodeAgenda0'+num]


	#eurlexRepEn1, eurlexRepEn2, eurlexRepEn3, eurlexRepEn4
	eurlexRepEnList=getEurlexRepEn(directoryCodeSoup)
	for index in xrange(len(eurlexRepEnList)):
		num=str(index+1)
		dataDic['eurlexRepEn'+num]=eurlexRepEnList[index]
		print 'eurlexRepEn'+num+": ", dataDic['eurlexRepEn'+num]

	#eurlexTypeActe
	dataDic['eurlexTypeActe']=getEurlexTypeActe(soup)
	print "eurlexTypeActe:", dataDic['eurlexTypeActe']

	#eurlexBaseJuridique
	dataDic['eurlexBaseJuridique']=getEurlexBaseJuridique(soup)
	print "eurlexBaseJuridique:", dataDic['eurlexBaseJuridique']

	return dataDic
