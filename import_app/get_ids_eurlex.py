"""
get the ids from eurlex
"""
import urllib
import re
from bs4 import BeautifulSoup
import config_file as conf


def get_url_eurlex(no_celex):
	"""
	FUNCTION
	return the eurlex url
	PARAMETERS
	no_celex: no_celex variable [string]
	RETURN
	url: url of the eurlex page [string]
	"""
	#http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:32006R1921:EN:NOT
	#~ url="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:NOCELEX:EN:NOT"
	url=conf.url_eurlex
	url=url.replace("NOCELEX", no_celex, 1)
	return url


def get_url_content_eurlex(url):
	"""
	FUNCTION
	check if the eurlex url exists and return its content
	PARAMETERS
	url: eurlex url [string]
	RETURN
	url_content: content of the page if the url exists and false otherwise [BeautifulSoup object]
	"""
	url_content=False
	try:
		soup=BeautifulSoup(urllib.urlopen(url))
		if not(soup.title.string=='EUR-Lex - Simple search'):
			url_content=soup
	except:
		print "no content for eurlex url"

	return url_content


def get_no_celex(soup):
	"""
	FUNCTION
	get no_celex from eurlex
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	RETURN
	no_celex variable [string]
	"""
	return soup.title.string.split("-")[2].strip()


def get_chrono(chrono):
	"""
	FUNCTION
	remove the 0 at the beginning of the chrono field (no_chrono for oeil or propos_chrono for prelex)
	PARAMETERS
	chrono: no_chrono or propos_chrono [string]
	RETURN
	updated no_chrono or propos_chrono [string]
	"""
	index_start=0
	#we remove the 0s at the beginning
	for character in chrono:
		if character=="0":
			index_start+=1
		else:
			break
	return chrono[index_start:]


def get_nos_unique(soup):
	"""
	FUNCTION
	get oeil ids from eurlex
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	RETURN
	no_unique_type, no_unique_annee and no_unique_chrono variables [string, int, string]
	"""
	exist=True
	try:
		url=soup.find(text="European Parliament - Legislative observatory").find_parent().find_parent()['href']
		#~ print "old oeil url (eurlex):", url
		#http://www.europarl.europa.eu/oeil/FindByProcnum.do?lang=2&procnum=COD/2005/0223
		url=url[url.rfind('='):][1:].split("/")
		no_unique_type=url[0].upper()
		#~ print 'no_unique_type (eurlex):', no_unique_type
		no_unique_annee=url[1]
		#~ print 'no_unique_annee (eurlex):', no_unique_annee
		no_unique_chrono=url[2]
	except:
		try:
			ids_oeil=soup.find(text="Procedure number:").find_next('br').next.strip()
			#~ print "ids_oeil (eurlex):", ids_oeil
			ids_oeil=ids_oeil.split("(")
			no_unique_type=ids_oeil[0].strip().upper()
			#~ print 'no_unique_type (eurlex):', no_unique_type
			ids_oeil=ids_oeil[1].split(")")
			no_unique_annee=ids_oeil[0]
			#~ print 'no_unique_annee (eurlex):', no_unique_annee
			no_unique_chrono=ids_oeil[1].strip()
		except:
			print "no oeil page (eurlex)"
			no_unique_type, no_unique_annee, no_unique_chrono=None, None, None
			exist=False

	if exist:
		no_unique_chrono=get_chrono(no_unique_chrono)

	return no_unique_type, no_unique_annee, no_unique_chrono


def get_proposs(soup):
	"""
	FUNCTION
	get prelex ids from eurlex
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	RETURN
	propos_origine, propos_annee and propos_chrono variables [string, int, string]
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
		propos_chrono=get_chrono(ids_prelex[1])
	except Exception, e:
		print "no Proposal Commission", e
		try:
			#http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:31997D0091:EN:NOT
			#<strong>Internal reference:</strong><br/>COM/96/0299
			ids_prelex=soup.find(text="Internal reference:").find_next('br').next.strip().split("/")
			propos_origine=ids_prelex[0].upper()
			propos_annee=ids_prelex[1]
			propos_chrono=get_chrono(ids_prelex[2])
		except Exception, e:
			print "no Internal reference", e
			propos_origine, propos_annee, propos_chrono=None, None, None

	return propos_origine, propos_annee, propos_chrono


def get_ids_eurlex(soup):
	"""
	FUNCTION
	get all the ids from the eurlex url
	PARAMETERS
	soup: eurlex url content [BeautifulSoup object]
	RETURN
	fields: retrieved data from eurlex [ditionary]
	"""
	fields={}

	#act
	fields['no_celex']=get_no_celex(soup)
	print "no_celex:", fields['no_celex']

	#<div class="listNotice">
	soup=soup.find("div", {"class": "listNotice"})

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
