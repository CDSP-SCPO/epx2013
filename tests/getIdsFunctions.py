"""
1/ids and errors retrieval
2/get the urls of European institutions from the ids
3/cross validation between the websites
"""

import get_ids_eurlex as eurlex
import get_ids_oeil as oeil
import get_ids_prelex as prelex


def check_get_ids_eurlex(act):
	"""
	FUNCTION
	check and get all the ids from the eurlex id
	PARAMETERS
	act: act id (Eurlex)
	RETURN
	dictionary of retrieved data from eurlex
	"""
	fields={}
	url_eurlex=eurlex.get_url_eurlex(act)
	print "eurlex url", url_eurlex
	url_eurlex_content=eurlex.get_url_content_eurlex(url_eurlex)
	if url_eurlex_content!=False:
		#~ #get data from eurlex
		fields['url_exists']=True
		fields.update(eurlex.get_ids_eurlex(url_eurlex_content))
	else:
		fields['url_exists']=False
		print "eurlex url does not exist!!"

	return fields


def check_get_ids_oeil(no_unique_type, no_unique_annee, no_unique_chrono):
	"""
	FUNCTION
	check and get all the ids from the oeil ids
	PARAMETERS
	no_unique_annee: no_unique_annee id
	no_unique_chrono: no_unique_chrono id
	no_unique_type: no_unique_type id
	RETURN
	dictionary of retrieved data from oeil
	"""
	fields={}
	url_oeil=oeil.get_url_oeil(no_unique_type, no_unique_annee, no_unique_chrono)
	print "oeil url", url_oeil
	url_oeil_content=oeil.get_url_content_oeil(url_oeil)
	if url_oeil_content!=False:
		#~ #get data from oeil
		fields['url_exists']=True
		fields.update(oeil.get_ids_oeil(url_oeil_content))
	else:
		print "oeil url does not exist!!"
		fields['url_exists']=False
		fields['no_celex']=None
		fields['no_unique_annee']=None
		fields['no_unique_type']=None
		fields['no_unique_chrono']=None
		fields['propos_origine']=None
		fields['propos_annee']=None
		fields['propos_chrono']=None

	return fields

def check_get_ids_prelex(ids):
	"""
	FUNCTION
	check and get all the ids from the prelex ids
	PARAMETERS
	ids: dos_id or propos_origine propos_annee propos_chrono
	RETURN
	dictionary of retrieved data from prelex
	"""
	fields={}
	if "propos_origine" in ids:
		url_prelex=prelex.get_url_prelex_propos(ids['propos_origine'], ids['propos_annee'], ids['propos_chrono'])
	elif "no_unique_type" in ids:
		url_prelex=prelex.get_url_prelex_no_unique(ids['no_unique_type'], ids['no_unique_annee'], ids['no_unique_chrono'])
	elif "dos_id" in ids:
		url_prelex=prelex.get_url_prelex(ids['dos_id'])

	url_prelex_content=prelex.get_url_content_prelex(url_prelex)
	if url_prelex_content!=False:
		#~ #get data from prelex
		fields['url_exists']=True
		fields.update(prelex.get_ids_prelex(url_prelex_content))
	else:
		print "prelex url does not exist!!"
		fields['url_exists']=False
		fields['no_celex']=None
		fields['dos_id']=None
		fields['no_unique_annee']=None
		fields['no_unique_type']=None
		fields['no_unique_chrono']=None
		fields['propos_origine']=None
		fields['propos_annee']=None
		fields['propos_chrono']=None

	fields['url_prelex']=url_prelex

	return fields
