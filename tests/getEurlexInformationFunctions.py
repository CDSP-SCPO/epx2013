# -*- coding: utf-8 -*-
"""
get the data from Eurlex (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag


def get_titre_en(soup):
	"""
	FUNCTION
	get the titre_en variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	titre_en
	"""
	return soup.find("h2", text="Title and reference").findNext("p").get_text()

#right under "Title and reference"
#not NULL



def get_directory_code(soup):
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


def getEurlexCodeSect(soup):
	"""
	FUNCTION
	get the code_sect01-04 variables from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	code_sect*01, code_sect*02, code_sect*03, code_sect*04
	"""
	code_sectVars=[]
	code_sectVars.append(None)
	code_sectVars.append(None)
	code_sectVars.append(None)
	code_sectVars.append(None)
	try:
		code_sect=soup.findAll('em')
		for i in range(4):
			code_sectVars.append(None)

		for i in range(len(code_sect)):
			code_sectVars[i]=code_sect[i].get_text().strip()
	except:
		print "no code_sect*!"
	
	return code_sectVars[0], code_sectVars[1], code_sectVars[2], code_sectVars[3]

#first, second, third and fourth code under "Directory code:"
#8 chiffres sous cette forme : 12.34.56.78
#first not NULL
#second, third and fourth: can be null


def get_rep_en(soup):
	"""
	FUNCTION
	get the rep_en_1, rep_en_2, rep_en_3 and rep_en_4 variables from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	rep_en_1, rep_en_2, rep_en_3 and rep_en_4
	"""
	rep_en1=rep_en2=rep_en3=rep_en4=""
	try:
		links=soup.findAll('a')
		delimitors=[]
		#find where 2 variables get separated
		for link in links:
			if link.nextSibling.strip()!="/":
				delimitors.append(links.index(link)+1)

		#rep_en1 
		for i in range(delimitors[0]):
			rep_en1+=links[i].get_text()+"; "
		
		#rep_en2
		for i in range(delimitors[0], delimitors[1]):
			rep_en2+=links[i].get_text()+"; "
			
		#rep_en3
		for i in range(delimitors[1], delimitors[2]):
			rep_en3+=links[i].get_text()+"; "
		
		#rep_en4
		for i in range(delimitors[2], len(links)):
			rep_en4+=links[i].get_text()+"; "
	except:
		print "less than four rep_en"

	return rep_en1[:-2], rep_en2[:-2], rep_en3[:-2], rep_en4[:-2]

#texts in front of the code_sect*01, code_sect*02, code_sect*03 and code_sect*04 variables (under "Directory code:")
#rep_en_1 not NULL
#rep_en_2, rep_en_3, rep_en_4 can be Null


def get_type_acte(soup):
	"""
	FUNCTION
	get the type_acte variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	type_acte
	"""
	#author part
	author=soup.find("h2", text="Miscellaneous data").findNext("strong", text="Author:").findNext('br').next.strip().lower()
	#form part
	form=soup.find("h2", text="Miscellaneous data").findNext("strong", text="Form:").findNext('br').next.strip().lower()
	
	#return acronyms
	author_code=""
	if "european parliament" not in author:
		author_code="CS "
	#decision
	if "decision" in form:
		#framework decision
		if "framework" in form:
			return author_code+"DEC CAD"
		if "addressee" in form:
			if "without" in form:
				return author_code+"DEC W/O ADD"
			return author_code+"DEC W/ ADD"
		return author_code+"DEC"
	#directive
	if form=="directive":
		return author_code+"DVE"
	#regulation
	if form=="regulation":
		return author_code+"REG"

	return author+" "+form

#act type under Miscellaneous data->Author and Miscellaneous data->Form
#not NULL
#List of possible values (acronyms of real values): CS DEC, CS DEC CAD, CS DVE, CS REG, DEC, DVE, REG, CS DEC SUI, DEC SUI.


def get_base_j(soup):
	"""
	FUNCTION
	get the base_j variable from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	base_j
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



def get_data_eurlex(soup):
	"""
	FUNCTION
	get all the data from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	dictionary of retrieved data from eurlex
	"""
	fields={}
	
	#titre_en
	fields['titre_en']=get_titre_en(soup)
	print "titre_en:", fields['titre_en']
	
	directoryCodeSoup=get_directory_code(soup)
	
	#code_sect*01, code_sect*02, code_sect*03, code_sect*04
	fields['code_sect*01'], fields['code_sect*02'], fields['code_sect*03'], fields['code_sect*04']=getEurlexCodeSect(directoryCodeSoup)
	print "code_sect*01:", fields['code_sect*01']
	print "code_sect*02:", fields['code_sect*02']
	print "code_sect*03:", fields['code_sect*03']
	print "code_sect*04:", fields['code_sect*04']

	#rep_en_1, rep_en_2, rep_en_3, rep_en_4
	fields['rep_en_1'], fields['rep_en_2'], fields['rep_en_3'], fields['rep_en_4']=get_rep_en(directoryCodeSoup)
	print "rep_en_1:", fields['rep_en_1']
	print "rep_en_2:", fields['rep_en_2']
	print "rep_en_3:", fields['rep_en_3']
	print "rep_en_4:", fields['rep_en_4']

	#type_acte
	fields['type_acte']=get_type_acte(soup)
	print "type_acte:", fields['type_acte']
	
	#base_j
	fields['base_j']=get_base_j(soup)
	print "base_j:", fields['base_j']

	return fields
