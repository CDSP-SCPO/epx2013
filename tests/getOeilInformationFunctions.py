# -*- coding: utf-8 -*-
"""
get the information from Oeil (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup


def getFromOeil(soup):
	"""
	FUNCTION
	get the variable from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	titreEn
	"""
	return None



def getOeilInformation(soup):
	"""
	FUNCTION
	get all the information from the oeil url
	PARAMETERS
	soup: oeil url content
	RETURN
	dictionary of retrieved data from oeil
	"""
	dataDic={}
	
	#var
	dataDic['var']=getFromOeil(soup)
	print "var (oeil):", dataDic['var']
	

	return dataDic
