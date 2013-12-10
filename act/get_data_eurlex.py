#-*- coding: utf-8 -*-
#for accents between comments inside this file
"""
get data from Eurlex (data for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
from act.models import CodeSect
from common.functions import list_reverse_enum, date_string_to_iso
from common.db import save_fk_code_sect, save_get_object


def get_titre_en(soup):
	"""
	FUNCTION
	get the titre_en variable from the eurlex url
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	RETURN
	titre_en [string]
	"""
	try:
		return soup.find("h2", text="Title and reference").find_next("p").get_text()
	except:
		print "no titre_en!"
		return None

#right under "Title and reference"
#not NULL


def get_directory_code(soup):
	"""
	FUNCTION
	get the html code of the directory code part from the eurlex url
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	RETURN
	directory code part  [BeautifulSoup object]
	"""
	try:
		return soup.find("strong", text="Directory code:").find_parent()
	except:
		print "no directory code section!"
		return None


def get_code_sect(soup):
	"""
	FUNCTION
	get the CodeSect1-4 variables from the eurlex url
	PARAMETERS
	soup: eurlex url content  [BeautifulSoup object]
	RETURN
	code_sects: code_sect_* variables [list of CodeSect model instances]
	"""
	code_sects=[None for i in range(4)]

	try:
		code_sects_temp=soup.find_all('em')

		for i in range(len(code_sects_temp)):
			code_sects[i]=save_get_object(CodeSect,  {"code_sect": code_sects_temp[i].get_text().strip()})
	except Exception, e:
		print "no code_sect_*!", e

	return code_sects

#first, second, third and fourth code under "Directory code:"
#8 chiffres sous cette forme : 12.34.56.78
#first not NULL
#second, third and fourth: can be null


def save_code_agenda(code_sects):
	"""
	FUNCTION
	save the code_agenda_* fk variables into the CodeSect model
	PARAMETERS
	code_sects: code_sect_* instances [list of CodeSect model instances]
	RETURN
	None
	"""
	#for each code_sect
	for i in range(len(code_sects)):
		instance=code_sects[i]
		save_fk_code_sect(instance, "code_agenda")


def get_rep_en(soup):
	"""
	FUNCTION
	get the rep_en_1, rep_en_2, rep_en_3 and rep_en_4 variables from the eurlex url
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	RETURN
	rep_ens: rep_en_* variab1es [list of strings]
	"""
	rep_ens=["" for i in range(4)]
	try:
		links=soup.find_all('a')
		delimitors=[]
		#find where 2 variables get separated
		for link in links:
			if link.next_sibling.strip()!="/":
				delimitors.append(links.index(link)+1)

		#repEn1
		for i in range(delimitors[0]):
			rep_ens[0]+=links[i].get_text()+"; "

		#repEn2
		for i in range(delimitors[0], delimitors[1]):
			rep_ens[1]+=links[i].get_text()+"; "

		#repEn3
		for i in range(delimitors[1], delimitors[2]):
			rep_ens[2]+=links[i].get_text()+"; "

		#repEn4
		for i in range(delimitors[2], len(links)):
			rep_ens[3]+=links[i].get_text()+"; "
	except:
		print "less than four rep_en_*"

	#remove trailing "; "
	for i in range(len(rep_ens)):
		rep_ens[i]=rep_ens[i][:-2]

	return rep_ens

#texts in front of the code_sect_1, code_sect_2, code_sect_3 and code_sect_4 variables (under "Directory code:")
#rep_en_1 not NULL
#rep_en_2, rep_en_3, rep_en_4 can be Null


def get_type_acte(soup):
	"""
	FUNCTION
	get the type_acte variable from the eurlex url
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	RETURN
	type_acte [string]
	"""
	try:
		#author part
		author=soup.find("h2", text="Miscellaneous data").find_next("strong", text="Author:").find_next('br').next.strip().lower()
		#form part
		form=soup.find("h2", text="Miscellaneous data").find_next("strong", text="Form:").find_next('br').next.strip().lower()

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
	except:
		print "no type_acte!"
		return None

#act type under Miscellaneous data->Author and Miscellaneous data->Form
#not NULL
#List of possible values (acronyms of real values): CS DEC, CS DEC CAD, CS DVE, CS REG, DEC, DVE, REG, CS DEC SUI, DEC SUI.


def get_base_j(soup):
	"""
	FUNCTION
	get the base_j variable from the eurlex url
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	RETURN
	base_j [string]
	"""
	try:
		#http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32002L0090:EN:NOT
		li=soup.find("h2", text="Relationship between documents").find_next("strong", text="Legal basis:").find_parent('li')
		legal_bases=li.find_all('a')
		var=""
		for legal_base in legal_bases:
			var+=legal_base.get_text()+legal_base.next_sibling.strip()+"; "

		return var[:-2]
	except:
		print "no base_j!"
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


def get_date_doc(soup):
	"""
	FUNCTION
	get the date of the act (used for gvt_compo when ProposOrigine="EM", "CONS", "BCE", "CJUE") from the eurlex url
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	RETURN
	titre_en [string]
	"""
	try:
		return date_string_to_iso(soup.find("h2", text="Dates").find_next("ul").find(text=re.compile("of document")).strip()[-10:])
	except Exception, e:
		print "no date gvt_compo!", e
		return None

#right under "Title and reference"
#not NULL


def get_data_eurlex(soup, act_ids=None, act=None):
	"""
	FUNCTION
	get all data from the eurlex url
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	RETURN
	data: retrieved data from eurlex [dictionary]
	"""
	data={}

	#titre_en
	data['titre_en']=get_titre_en(soup)
	print "titre_en:", data['titre_en']

	directory_code_soup=get_directory_code(soup)

	#code_sect_1, code_sect_2, code_sect_3, code_sect_4
	code_sects=get_code_sect(directory_code_soup)

	#code_agenda_1-4
	save_code_agenda(code_sects)

	#print code_sect_* and code_agenda_*
	for index in xrange(len(code_sects)):
		num=str(index+1)
		#django adds "_id" to foreign keys field names
		data['code_sect_'+num+"_id"]=code_sects[index]
		if code_sects[index]!=None:
			print 'code_sect_'+num+": ", data['code_sect_'+num+"_id"].code_sect
			print 'code_agenda_'+num+": ", data['code_sect_'+num+"_id"].code_agenda.code_agenda

	#rep_en_1, rep_en_2, rep_en_3, rep_en_4
	rep_ens=get_rep_en(directory_code_soup)
	for index in xrange(len(rep_ens)):
		num=str(index+1)
		data['rep_en_'+num]=rep_ens[index]
		print 'rep_en_'+num+": ", data['rep_en_'+num]

	#type_acte
	data['type_acte']=get_type_acte(soup)
	print "type_acte:", data['type_acte']

	#base_j
	data['base_j']=get_base_j(soup)
	print "base_j:", data['base_j']

	#date_doc
	data['date_doc']=get_date_doc(soup)
	print "date_doc:", data['date_doc']

	return data
