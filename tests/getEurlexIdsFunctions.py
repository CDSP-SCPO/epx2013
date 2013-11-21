"""
get the ids from Eurlex
"""

import urllib
import re
from bs4 import BeautifulSoup
import config_file as conf


def get_url_eurlex(act):
	"""
	FUNCTION
	return the eurlex url
	PARAMETERS
	act: act variable
	RETURN
	url of the eurlex page
	"""
	#http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32006R1921:EN:NOT
	#~ url="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:NOCELEX:EN:NOT"
	url=conf.url_eurlex
	url=url.replace("NOCELEX", act, 1)
	return url


def get_url_content_eurlex(url):
	"""
	FUNCTION
	check if the eurlex url exists and return its content
	PARAMETERS
	url: eurlex url
	RETURN
	content of the page if the url exists and false otherwise
	"""
	try:
		soup=BeautifulSoup(urllib.urlopen(url))
		if(soup.title.string=='EUR-Lex - Simple search'):
			return False
		else:
			return soup
	except:
		return False


def get_no_celex(soup):
	"""
	FUNCTION
	get act from eurlex
	PARAMETERS
	soup: eurlex url content
	RETURN
	act
	"""
	return soup.title.string.split("-")[2].strip()


def get_nos_unique(soup):
	"""
	FUNCTION
	get oeil ids from eurlex
	PARAMETERS
	soup: eurlex url content
	RETURN
	oeil ids (no_unique_type, no_unique_annee, no_unique_chrono)
	"""
	try:
		oldOeilUrl=soup.find(text="European Parliament - Legislative observatory").findParent().findParent()['href']
		#~ print "old oeil url (eurlex):", oldOeilUrl
		#http://www.europarl.europa.eu/oeil/FindByProcnum.do?lang=2&procnum=COD/2005/0223
		
		oldOeilUrl=oldOeilUrl[oldOeilUrl.rfind('='):][1:].split("/")
		no_unique_type=oldOeilUrl[0].upper()
		#~ print 'no_unique_type (eurlex):', no_unique_type
		no_unique_annee=oldOeilUrl[1]
		#~ print 'no_unique_annee (eurlex):', no_unique_annee
		no_unique_chrono_temp=oldOeilUrl[2]
		#~ print "no_unique_chrono_temp (eurlex):", no_unique_chrono_temp
		index_start=0
		#we remove the 0s at the beginning
		for character in no_unique_chrono_temp:
			if character=="0":
				index_start+=1
			else:
				break
		no_unique_chrono=no_unique_chrono_temp[index_start:]
		#~ print 'no_unique_chrono (eurlex):', no_unique_chrono
	except:
		try:
			ids_oeil=soup.find(text="Procedure number:").findNext('br').next.strip()
			#~ print "ids_oeil (eurlex):", ids_oeil
			ids_oeil=ids_oeil.split("(")
			no_unique_type=ids_oeil[0].strip().upper()
			#~ print 'no_unique_type (eurlex):', no_unique_type
			ids_oeil=ids_oeil[1].split(")")
			no_unique_annee=ids_oeil[0]
			#~ print 'no_unique_annee (eurlex):', no_unique_annee
			no_unique_chrono_temp=ids_oeil[1].strip()
			#~ print "no_unique_chrono_temp (eurlex):", no_unique_chrono_temp
			#we remove the 0s at the beginning
			index_start=0
			for character in no_unique_chrono_temp:
				if character=="0":
					index_start+=1
				else:
					break
			no_unique_chrono=no_unique_chrono_temp[index_start:]
			#~ print 'no_unique_chrono (eurlex):', no_unique_chrono
		except:
			no_unique_type=None
			no_unique_annee=None
			no_unique_chrono=None
			print "no oeil page (eurlex)"
	
	return no_unique_type, no_unique_annee, no_unique_chrono


def get_proposs(soup):
	"""
	FUNCTION
	get prelex ids from eurlex
	PARAMETERS
	soup: eurlex url content
	RETURN
	prelex ids (propos_origine, propos_annee, propos_chrono)
	"""
	try:
		ids_prelex=soup.find(text=re.compile("Proposal Commission")).split(";")[1].strip()
		#~ print "ids_prelex (eurlex):", ids_prelex
		ids_prelex=ids_prelex.split(" ")
		propos_origine=ids_prelex[0].upper()
		if propos_origine=="COMMITTEE":
			propos_origine="COM"
		ids_prelex=ids_prelex[1].split("/")
		propos_annee=ids_prelex[0]
		propos_chrono_temp=ids_prelex[1]
		#we remove the 0s at the beginning
		index_start=0
		for character in propos_chrono_temp:
			if character=="0":
				index_start+=1
			else:
				break
		propos_chrono=propos_chrono_temp[index_start:]
	except:
		propos_origine=None
		propos_annee=None
		propos_chrono=None
		print "no prelex page (eurlex)"
		
	return propos_origine, propos_annee, propos_chrono


def get_ids_eurlex(soup):
	"""
	FUNCTION
	get all the ids from the eurlex url
	PARAMETERS
	soup: eurlex url content
	RETURN
	dictionary of retrieved data from eurlex
	"""
	fields={}
	
	#act
	fields['no_celex']=get_no_celex(soup)
	print "no_celex:", fields['no_celex']
	
	#oeil ids
	fields['no_unique_type'], fields['no_unique_annee'], fields['no_unique_chrono']=get_nos_unique(soup)
	print 'no_unique_type:', fields['no_unique_type']
	print 'no_unique_annee:', fields['no_unique_annee']
	print 'no_unique_chrono:', fields['no_unique_chrono']
		
	#prelex ids
	fields['propos_origine'], fields['propos_annee'], fields['propos_chrono']=get_proposs(soup)
	print 'propos_origine:', fields['propos_origine']
	print 'propos_annee:', fields['propos_annee']
	print 'propos_chrono:', fields['propos_chrono']
		
	return fields
