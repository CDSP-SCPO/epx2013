# -*- coding: utf-8 -*-
"""
get the data from Prelex (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
#dg codes
from act.models import DGSigle, DG, Person
import dateFunctions as dateFct
from datetime import datetime


def get_adopt_com_table(soup):
	"""
	FUNCTION
	get the html content of the table tag "Adoption by Commission" from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	html content of the table "Adoption by Commission"
	"""
	try:
		return soup.find("b", text=re.compile("Adoption by Commission")).findParent('table')
	except:
		print "no table called 'Adoption by Commission' (prelex)"
		return None


def get_adopt_propos_origineine(soup, propos_origine):
	"""
	FUNCTION
	get the adopt_propos_origine variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	adopt_propos_origine
	"""
	try:
		adopt_propos_origine=None
		if propos_origine=="COM":
			adopt_propos_origine=soup.find("a", text=re.compile("Adoption by Commission")).findNext('br').next.strip()
		if propos_origine=="JAI":
			adopt_propos_origine=get_transm_council(soup, propos_origine)
		if propos_origine=="CONS":
			print "TODO: extraction pdf almost done (see tests)"

		#transform dates to the iso format (YYYY-MM-DD)
		if adopt_propos_origine!=None:
			year, month, day=dateFct.splitFrenchFormatDate(adopt_propos_origine)
			adopt_propos_origine=dateFct.dateToIso(year, month, day)

		return adopt_propos_origine
	except:
		print "no adopt_propos_origine!"
		return None

#~ Date in front of "Adoption by Commission"
#~ not NULL
#~ AAAA-MM-JJ format
#~ ProposOrigine=COM -> date adoption de la proposition par la Commission
#~ ProposOrigine=JAI -> TransmissionConseil date
#~ EM -> not processed because appears only when no_unique_type=CS which concerns non definitive acts (not processed)
#~ ProposOrigine=CONS -> date in pdf document (council path link)
#~ TODO: case where propos_origine=CONS


def get_com_proc(soup, propos_origine):
	"""
	FUNCTION
	get the com_proc variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	com_proc
	"""
	try:
		if propos_origine=="COM":
			return soup.find("td", text="Decision mode:").findNext('td').get_text().strip()
	except:
		print "no com_proc!"
	return None

#~ in front of "Decision mode"
#~ Possible values:
#~ "Oral Procedure", "Written Procedure", "Empowerment procedure"
#~ Null if ProposOrigine !=COM


def saveRespProposAndGetresp_(person):
	"""
	FUNCTION
	save person if doesn't exist in the db yet and get personId
	PARAMETERS
	person: full name of person
	RETURN
	personId: id of person
	"""
	try:
		#check if person already exists in the db
		return Person.objects.get(person=person).id
	except:
		#person doesn't exist in the db yet -> we add it in the table
		personDB=Person(person=person)
		personDB.save()
		print "personDB.id", personDB.id
		#we get person
		return personDB.id

	return None


def get_jointly_resps(soup):
	"""
	FUNCTION
	get the jointly responsible persons (dg_2 and resp_2 (+id) or RespPropos3 (+id)) from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	list of jointly responsible persons (dg_2 and resp_2 or resp_3)
	"""
	dg_2=resp_2=resp_2=None
	try:
		#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=191926
		jointly_resps=soup.findAll("td", text="Jointly responsible")
		#dg_2
		dg_2=specialDgSearch(jointly_resps[0].findNext('td').get_text().strip())
		#resp_2 or 3
		resp_2=jointly_resps[1].findNext('td').get_text().strip()
		#get the id from Person
		resp_2=saveRespProposAndGetresp_(resp_2)

	except:
		print "no dg_2, resp_2, resp_2"

	return dg_2, resp_2, resp_2

#in front of "Jointly responsible"
#can be Null


#NOT USED ANYMORE
#REPLACED BY DATABASE TABLES
#~ def specialDgSearch(dg):
	#~ """
	#~ FUNCTION
	#~ gives the "official" name of special values of primarily responsible
	#~ PARAMETERS
	#~ dg: primarily responsible
	#~ RETURN
	#~ new official name or None if dg is a "normal" name
	#~ """
	#list of short names: http://publications.europa.eu/code/en/en-390600.htm
	#example: http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=187691
	#~ if dg==u"Secretariat-General":
		#~ return "SG"
	#~ if dg=="Legal Service":
		#~ return "SJ"
	#~ if dg=="DG Communication":
		#~ return "COMM"
	#~ if dg=="Bureau of European Policy Advisers":
		#~ return "BEPA"
	#~ if dg==u"DG Economic and Financial Affairs":
		#~ return "ECFIN"
	#~ if dg=="DG Enterprises" or dg=="DG Enterprise and Industry" or dg=="DG 23":
		#~ return "ENTR"
	#~ if dg=="DG Competition":
		#~ return "COMP"
	#~ if dg=="DG Employment, Social Affairs" or dg==u"DG Employment, Social Affairs and Inclusion" or dg=="DG05":
		#~ return "EMPL"
	#~ if dg=="DG Agriculture" or dg==u"DG Agriculture and Rural Development" or dg=="DG06":
		#~ return "AGRI"
	#~ if dg=="DG Energy" or dg=="DG Energy and Transport":
		#~ return "ENER"
	#~ if dg=="DG Mobility and Transports":
		#~ return "MOVE"
	#~ if dg=="DG Climate Action":
		#~ return "CLIMA"
	#~ if dg=="DG Environment":
		#~ return "ENV"
	#~ if dg=="DG Research and Innovation":
		#~ return "RTD"
	#~ if dg=="Joint Research Centre":
		#~ return "JRC"
	#~ if dg=="DG Communications Networks, Content and Technology" or dg=="Communications Networks, Content and Technology DG" or dg=="INFSO" or dg==u"DG Information Society" or dg==u"Information Society and Media DG" or dg=="DG Information Society and Media" or dg=="Directorate-General for the Information Society and Media" or dg=="Directorate-General for Communications Networks, Content and Technology":
		#~ return "CNECT"
	#~ if dg==u"DG Fisheries" or dg==u"DG Maritime Affairs and Fisheries":
		#~ return "MARE"
	#~ if dg==u"DG Internal Market" or dg==u"DG Internal Market and Services" or dg=="DG15":
		#~ return "MARKT"
	#~ if dg==u"Regional Policy DG" or dg=="DG Regional and Urban Policy" or dg=="Regional and Urban Policy DG":
		#~ return "REGIO"
	#~ if dg==u"DG Taxation and Customs Union":
		#~ return "TAXUD"
	#~ if dg=="DG Education et culture":
		#~ return "EAC"
	#~ if dg==u"DG Health and Consumers" or dg=="DG24":
		#~ return "SANCO"
	#~ if dg=="DG Home Affairs":
		#~ return "HOME"
	#~ if dg==u"DG Justice":
		#~ return "JUST"
	#~ if dg=="Service for Foreign Policy Instruments" or dg=="Foreign Policy Instruments Service" or dg=="FPIS":
		#~ return "FPI"
	#~ if dg=="DG Trade":
		#~ return "TRADE"
	#~ if dg=="DG Enlargement":
		#~ return "ELARG"
	#~ if dg==u"DG Development and Cooperation — EuropeAid" or dg=="EuropeAid Development and Cooperation DG" or dg=="EuropeAid Development and Cooperation Directorate-General" or dg=="Directorate-General for Development and Cooperation — EuropeAid" or dg=="Development and Cooperation DG — EuropeAid":
		#~ return "DEVCO"
	#~ if dg=="DG Humanitarian Aid and Civil Protection (ECHO)":
		#~ return "ECHO"
	#~ if dg=="Eurostat" or dg=="Office statistique":
		#~ return "ESTAT"
	#~ if dg=="DG Human Resources and Security":
		#~ return "HR"
	#~ if dg=="DG Informatics":
		#~ return "DIGIT"
	#~ if dg=="DG Budget":
		#~ return "BUDG"
	#~ if dg=="Internal Audit Service":
		#~ return "IAS"
	#~ if dg=="European Anti-Fraud Office":
		#~ return "OLAF"
	#~ if dg=="DG Interpretation":
		#~ return "SCIC"
	#~ if dg=="DG Translation":
		#~ return "DGT"
	#~ if dg=="Publications Office":
		#~ return "OP"
	#~ if dg=="Office for Infrastructure and Logistics in Brussels":
		#~ return "OIB"
	#~ if dg=="Office for the Administration and Payment of Individual Entitlements":
		#~ return "PMO"
	#~ if dg=="Office for Infrastructure and Logistics in Luxembourg":
		#~ return "OIL"
	#~ if dg=="European Personnel Selection Office":
		#~ return "EPSO"
	#~ if dg=="Executive Agency for Competitiveness and Innovation":
		#~ return "EACI"
	#~ if dg=="Education, Audiovisual and Culture Executive Agency":
		#~ return "EACEA"
	#~ if dg=="Executive Agency for Health and Consumers":
		#~ return "EAHC"
	#~ if dg=="Trans-European Transport Network Executive Agency":
		#~ return "TENEA"
	#~ if dg=="European Research Council Executive Agency":
		#~ return "ERCEA"
	#~ if dg=="Research Executive Agency":
		#~ return "REA"
	#~ if dg==u"DG Relations extérieures":
		#~ return "RELEX"
	#~ return None


def specialDgSearch(dg):
	"""
	FUNCTION
	gives the standard short name of special values for the primarily responsible
	PARAMETERS
	dg: primarily responsible
	RETURN
	short name or dg itself if it is not associated to a dg_sigle in the db
	"""
	dg_sigle=dg
	try:
		#if there is a match in the db -> return dg_sigle
		dg_sigle=DG.objects.get(dg=dg).dg_sigle_id
		dg_sigle=DGSigle.objects.get(id=dg_sigle).dg_sigle
	except:
		print "Full name not stored in db"

	print "dg_sigle", dg_sigle
	return dg_sigle


def get_dg_1(soup):
	"""
	FUNCTION
	get the dg_1 variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	dg_1
	"""
	try:
		#dg
		dg=soup.find("td", text="Primarily responsible").findNext('td').get_text().strip()
		specialDg=specialDgSearch(dg)
		#the variable corresponds to a real personon
		if specialDg==None:
			return dg
		#it can be associated to a dg_sigle
		#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=111863
		return specialDg

	except:
		return None

#~ in front of "Primarily responsible"
#can be Null


def get_resps(soup):
	"""
	FUNCTION
	get the responsible(s) from the prelex url (resp_1, resp_2, resp_3)
	PARAMETERS
	soup: prelex url content
	RETURN
	persons: list of responsible(s) with ids and full names
	"""
	persons=[]
	for index in range(0, 3):
		persons.append((None, None))

	try:
		resp=soup.find("td", text="Responsible").findNext('td').get_text().strip()
		temp=resp.split(";")
		print "temp responsible", temp
		#only one responsible
		persons[0][0]=saveRespProposAndGetresp_(temp[0].strip())
		persons[0][1]=temp[0].strip()
		print "temp responsible 2", temp
		#two responsibles
		#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=191554
		persons[1][0]=saveRespProposAndGetresp_(temp[1].strip())
		persons[1][1]=temp[1].strip()
		print "temp responsible 3", temp
		#three responsibles
		persons[2][0]=saveRespProposAndGetresp_(temp[2].strip())
		persons[2][1]=temp[2].strip()
		print "persons", persons
	except:
		print "no Responsible"

	return persons

#~ in front of "Responsible"
#can be Null


def get_transm_council(soup, propos_origine):
	"""
	FUNCTION
	get the transm_council variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	transm_council
	"""
	transm_council=None
	try:
		if propos_origine=="CONS":
			transm_council=get_adopt_propos_origineine(soup, propos_origine)
		else:
			transm_council=soup.find("a", text=re.compile("Transmission to Council")).findNext('br').next.strip()
	except:
		print "pb transm_council"

	#transform dates to the iso format (YYYY-MM-DD)
	if transm_council!=None:
		year, month, day=dateFct.splitFrenchFormatDate(transm_council)
		transm_council=dateFct.dateToIso(year, month, day)
	return transm_council

#date in front of "Transmission to Council"
#not Null (except blank page -> error on page)
#AAAA-MM-JJ format
#ProposOrigine=CONS -> AdoptionProposOrigine


def get_nb_point_b(soup, propos_origine):
	"""
	FUNCTION
	get the nb_point_b variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	nb_point_b
	"""
	try:
		if propos_origine=="CONS" or propos_origine=="BCE":
			return None
		return len(soup.findAll(text=re.compile('ITEM "B"')))
	except:
		print "no nb_point_b!"
		return None

#~ in front of "COUNCIL AGENDA": counts the number of 'ITEM "B"' on the page
#~ not NULL
#~ De 0 a 20
#~ if propos_origine=="CONS" or "BCE", filled manually


def get_cons_b(soup, propos_origine):
	"""
	FUNCTION
	get the cons_b variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	cons_b
	"""
	try:
		if propos_origine!="CONS":
			cons_b_temp=""
			for tables in soup.findAll(text=re.compile('ITEM "B" ON COUNCIL AGENDA')):
				cons_b_temp+=tables.findParent('table').find(text=re.compile("SUBJECT")).findNext("font", {"size":-2}).get_text().strip()+'; '
			if cons_b_temp=="":
				return None
			return cons_b_temp[:-2]
		return None
	except:
		print "no nb_point_b!"
		return None

#can be Null
#in front of SUBJECT, only if the act is processed at B point (preceded by 'ITEM "B" ON COUNCIL AGENDA')
#concatenate all the values, even if redundancy
#~ if propos_origine=="CONS", filled manually


def get_adopt_conseil(soup, suite_2e_lecture_pe, split_propos, nb_lectures):
	"""
	FUNCTION
	get the adopt_conseil variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	adopt_conseil
	"""
	adopt_conseil=None
	# if there is no  2d Lecture at PE
	if suite_2e_lecture_pe==0:
		acts=["Formal adoption by Council", "Adoption common position", "Council approval 1st rdg"]
		for act in acts:
			try:
				adopt_conseil=soup.find("a", text=re.compile(act)).findNext('br').next.strip()
				break
			except:
				print "pb", act
	# if Suite2LecturePE=Y and split_propos=N
	elif split_propos==0:
		if nb_lectures==2:
			try:
				#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=156619
				date_table_soup=soup.find("b", text="EP opinion 2nd rdg").findParent("table")
				#check table contains "Approval without amendment"
				approval=date_table_soup.find(text="Approval without amendment")
				#check next table title is "Signature by EP and Council"
				next_table_title=date_table_soup.findNext("table").find(text="Signature by EP and Council")
				#if conditions are met, then get the date
				adopt_conseil=date_table_soup.find("b").get_text()
			except:
				print "pb AdoptionConseil (case split_propos==0)"
		elif nb_lectures==3:
			#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=137644
			date_table_soup=soup.find("b", text="Council decision at 3rd rdg").findParent("table")
			#check next table title is "Signature by EP and Council"
			next_table_title=date_table_soup.findNext("table").find(text="Signature by EP and Council")
			#if conditions are met, then get the date
			adopt_conseil=date_table_soup.find("b").get_text()
			#~ return soup.find("a", text=re.compile("Council decision at 3rd rdg")).findNext('br').next.strip()

		#transform dates to the iso format (YYYY-MM-DD)
	if adopt_conseil!=None:
		year, month, day=dateFct.splitFrenchFormatDate(adopt_conseil)
		adopt_conseil=dateFct.dateToIso(year, month, day)
	return adopt_conseil

#~ date in front of "Formal adoption by Council" or "Adoption common position" or "Council approval 1st rdg"
#not Null
#~ AAAA-MM-JJ format

#~ quand Suite2LecturePE=Y ET quand ProposSplittee=N and nb_lectures=2. Dans ce cas, la date AdoptionConseil=la date qui se trouve en face de la ligne « EP Opinion 2nd rdg » (vérifier qu’à la ligne qui suit dans le même carré, on trouve « Approval without amendment » et que le titre du carré qui suit est bien « Signature by EP and Council »
#~ Exemple : http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=156619

#~ quand Suite2LecturePE=Y ET quand ProposSplittee=N and nb_lectures=3 -> date in front of Council decision at 3rd rdg (vérifier que le titre du carré qui suit est bien « Signature by EP and Council »)
#~ Example: http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=137644

# if Suite2LecturePE=Y and split_propos=Y -> to fill manually


def get_nb_point_a(soup, propos_origine):
	"""
	FUNCTION
	get the nb_point_a variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	nb_point_a
	"""
	try:
		if propos_origine=="CONS" or propos_origine=="BCE":
			return None
		return len(soup.findAll(text=re.compile('ITEM "A"')))
	except:
		print "no nb_point_a!"
		return None

#~ in front of "COUNCIL AGENDA": counts the number of 'ITEM "A"' on the page
#~ not NULL
#~ De 0 a 20
#~ if propos_origine=="CONS" or "BCE", filled manually


def get_council_a(soup):
	"""
	FUNCTION
	get the council_a variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	council_a
	"""
	try:
		council_a_temp=""
		for tables in soup.findAll(text=re.compile('ITEM "A" ON COUNCIL AGENDA')):
			council_a_temp+=tables.findParent('table').find(text=re.compile("SUBJECT")).findNext("font", {"size":-2}).get_text().strip()+'; '
		return council_a_temp[:-2]
	except:
		print "no council_a!"
		return None

#not Null
#in front of SUBJECT, only if the act is processed at A point (preceded by 'ITEM "A" ON COUNCIL AGENDA')
#concatenate all the values, even if redundancy


def get_nb_lectures(soup, no_unique_type, split_propos):
	"""
	FUNCTION
	get the nb_lectures variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	nb_lectures
	"""
	if no_unique_type!="COD":
		return None

	#proposition not splited
	if split_propos==0:
		if soup.find(text=re.compile('EP opinion 3rd rdg'))>0 or soup.find(text=re.compile('EP decision 3rd rdg'))>0 or soup.find(text=re.compile('EP decision on 3rd rdg'))>0:
			return 3
		if soup.find(text=re.compile('EP opinion 2nd rdg'))>0:
			return 2
		if soup.find(text=re.compile('EP opinion 1st rdg'))>0:
			return 1
		return 0

	#proposition is splited
	if soup.find(text=re.compile('EP: position, 3rd reading'))>0 or soup.find(text=re.compile('EP: decision, 3rd reading'))>0 or soup.find(text=re.compile('EP: legislative resolution, 3rd reading'))>0:
		return 3
	if soup.find(text=re.compile('EP: position, 2nd reading'))>0:
		return 2
	if soup.find(text=re.compile('EP: position, 1st reading'))>0:
		return 1
	return 0

#Possible values
#1, 2, 3 ou NULL
#~ NULL if NoUniqueType !=COD
#~ if NoUniqueType=COD and if the proposition is not splitted:
	#~ if page contains "EP opinion 3rd rdg" or "EP decision 3rd rdg" -> nombreLectures=3
	#~ if page contains "EP opinion 2nd rdg" -> nombreLectures=2
	#~ if page contains "EP opinion 1st rdg" -> nombreLectures=1
	#~ otherwise error
#~ if NoUniqueType=COD and if the proposition is splitted:
	#~ if page contains "EP: position, 3rd reading" or "EP: decision, 3rd reading" or "EP: legislative resolution, 3rd reading" -> nombreLectures=3
	#~ if page contains "EP: position, 2nd reading" -> nombreLectures=2
	#~ if page contains "EP: position, 1st reading" -> nombreLectures=1
	#~ otherwise error


def get_date_diff(date_1, date_2):
	"""
	FUNCTION
	compute the difference between two dates
	PARAMETERS
	date_1: first date
	date_2: second date
	RETURN
	difference between the two dates in parameters
	"""
	if date_1!=None and date_2!=None:
		#transform dates to the iso format (YYYY-MM-DD)
		date_1=datetime.strptime(date_1, "%Y-%m-%d")
		date_2=datetime.strptime(date_2, "%Y-%m-%d")
		return (date_1 - date_2).days
	return None

#DureeAdoptionTrans (TransmissionConseil - AdoptionProposOrigine)
#DureeProcedureDepuisPropCom (AdoptionConseil – AdoptionProposOrigine)
#DureeProcedureDepuisTransCons (AdoptionConseil – TransmissionConseil)
#DureeTotaleDepuisPropCom (SignPECS – AdoptionProposOrigine)
#DureeTotaleDepuisTransCons (SignPECS – TransmissionConseil) 



def get_data_prelex(soup, idsDataDic):
	"""
	FUNCTION
	get all the data from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	dictionary of retrieved data from prelex
	"""
	fields={}

	#adopt_propos_origine
	fields['adopt_propos_origine']=get_adopt_propos_origineine(soup, idsDataDic['propos_origine'])
	print "adopt_propos_origine:", fields['adopt_propos_origine']

	#extract Adoption by Commission table (html content)
	adopt_com_table_oup=get_adopt_com_table(soup)
	#~ print "adopt_com_table_oup", adopt_com_table_oup

	#com_proc
	fields['com_proc']=get_com_proc(adopt_com_table_oup, idsDataDic['propos_origine'])
	print "com_proc:", fields['com_proc']

	#jointly responsible persons (dg_2 and resp_2 or resp_3)
	dg_2, resp_2, resp_2=get_jointly_resps(adopt_com_table_oup)

	#dg_1 and dg_2
	fields['dg_1']=get_dg_1(adopt_com_table_oup)
	fields['dg_2']=dg_2
	print "dg_1:", fields['dg_1']
	print "dg_2:", fields['dg_2']

	#resp_1, RespPropos1, resp_2, resp_2, resp_3, RespPropos3
	persons=get_resps(adopt_com_table_oup)
	fields['resp_1']=persons[0][0]
	fields['RespPropos1']=persons[0][1]
	fields['resp_2']=persons[1][0]
	fields['resp_2']=persons[1][1]
	fields['resp_3']=persons[2][0]
	fields['RespPropos3']=persons[2][1]

	#jointly responsible (resp_2 or resp_3)
	if fields['resp_2']==None:
		fields['resp_2']=resp_2
		fields['resp_2']=resp_2
	elif fields['resp_3']==None:
		fields['resp_3']=resp_2
		fields['RespPropos3']=resp_2

	print "resp_1:", fields['resp_1']
	print "RespPropos1:", fields['RespPropos1']
	print "resp_2:", fields['resp_2']
	print "resp_2:", fields['resp_2']
	print "resp_3:", fields['resp_3']
	print "RespPropos3:", fields['RespPropos3']

	#transm_council
	fields['transm_council']=get_transm_council(soup, idsDataDic['propos_origine'])
	print "transm_council:", fields['transm_council']

	#nb_point_b
	fields['nb_point_b']=get_nb_point_b(soup, idsDataDic['propos_origine'])
	print "nb_point_b:", fields['nb_point_b']

	#cons_b
	fields['cons_b']=get_cons_b(soup, idsDataDic['propos_origine'])
	print "cons_b:", fields['cons_b']

	#nb_lectures -> ALREADY IN OEIL -> used only for adopt_conseil!
	fields['nb_lectures']=get_nb_lectures(soup, idsDataDic['no_unique_type'], idsDataDic['split_propos'])
	#~ print "nb_lectures:", fields['nb_lectures']

	#adopt_conseil
	fields['adopt_conseil']=get_adopt_conseil(soup, idsDataDic['suite_2e_lecture_pe'], idsDataDic['split_propos'], fields['nb_lectures'])
	print "adopt_conseil:", fields['adopt_conseil']

	#nb_point_a
	fields['nb_point_a']=get_nb_point_a(soup, idsDataDic['propos_origine'])
	print "nb_point_a:", fields['nb_point_a']

	#council_a
	fields['council_a']=get_council_a(soup)
	print "council_a:", fields['council_a']

	#duree_adopt_trans
	fields['duree_adopt_trans']=get_date_diff(fields['transm_council'], fields['adopt_propos_origine'])
	print "duree_adopt_trans:", fields['duree_adopt_trans']

	#duree_proc_depuis_prop_com
	fields['duree_proc_depuis_prop_com']=get_date_diff(fields['adopt_conseil'], fields['adopt_propos_origine'])
	print "duree_proc_depuis_prop_com:", fields['duree_proc_depuis_prop_com']

	#duree_proc_depuis_trans_cons
	fields['duree_proc_depuis_trans_cons']=get_date_diff(fields['adopt_conseil'], fields['transm_council'])
	print "duree_proc_depuis_trans_cons:", fields['duree_proc_depuis_trans_cons']

	#duree_tot_depuis_prop_com
	fields['duree_tot_depuis_prop_com']=get_date_diff(idsDataDic["sign_pecs"], fields['adopt_propos_origine'])
	print "duree_tot_depuis_prop_com:", fields['duree_tot_depuis_prop_com']

	#duree_tot_depuis_trans_cons
	fields['duree_tot_depuis_trans_cons']=get_date_diff(idsDataDic["sign_pecs"], fields['transm_council'])
	print "duree_tot_depuis_trans_cons:", fields['duree_tot_depuis_trans_cons']

	return fields
