# -*- coding: utf-8 -*-
"""
get the information from Prelex (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
#dg codes
from actsInformationRetrieval.models import DGCodeModel, DGFullNameModel
import dateFunctions as dateFct
from datetime import datetime


def getPrelexAdoptionByCommissionTable(soup):
	"""
	FUNCTION
	gets the html content of the table tag "Adoption by Commission" from the prelex url
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


def getPrelexAdoptionProposOrigine(soup, proposOrigine):
	"""
	FUNCTION
	gets the prelexAdoptionProposOrigine variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	prelexAdoptionProposOrigine
	"""
	adoptionProposOrigine=None
	if proposOrigine=="COM":
		adoptionProposOrigine=soup.find("a", text=re.compile("Adoption by Commission")).findNext('br').next.strip()
	if proposOrigine=="JAI":
		adoptionProposOrigine=getPrelexTransmissionCouncil(soup, proposOrigine)
	if proposOrigine=="CONS":
		print "TODO: extraction pdf almost done (see tests)"

	#transform dates to the iso format (YYYY-MM-DD)
	if adoptionProposOrigine!=None:
		year, month, day=dateFct.splitFrenchFormatDate(adoptionProposOrigine)
		adoptionProposOrigine=dateFct.dateToIso(year, month, day)

	return adoptionProposOrigine

#~ Date in front of "Adoption by Commission"
#~ not NULL
#~ AAAA-MM-JJ format
#~ ProposOrigine = COM -> date adoption de la proposition par la Commission
#~ ProposOrigine = JAI -> TransmissionConseil date
#~ EM -> not processed because appears only when noUniqueType=CS which concerns non definitive acts (not processed)
#~ ProposOrigine = CONS -> date in pdf document (council path link)
#~ TODO: case where proposOrigine=CONS


def getPrelexComProc(soup, proposOrigine):
	"""
	FUNCTION
	gets the prelexComProc variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	prelexComProc
	"""
	try:
		if proposOrigine== "COM":
			return soup.find("td", text="Decision mode:").findNext('td').get_text().strip()
	except:
		print "no prelexComProc!"
	return None

#~ in front of "Decision mode"
#~ Possible values:
#~ "Oral Procedure", "Written Procedure", "Empowerment procedure"
#~ Null if ProposOrigine != COM


def getPrelexJointlyResponsibles(soup):
	"""
	FUNCTION
	gets the jointly responsible persons (prelexDGProposition2 and prelexRespPropos2) from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	list of jointly responsible persons (prelexDGProposition2 and prelexRespPropos2)
	"""
	jointlyResponsibleList=[]
	jointlyResponsibleList.append(None)
	jointlyResponsibleList.append(None)
	try:
		#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=191926
		jointlyResponsibles=soup.findAll("td", text="Jointly responsible")
		jointlyResponsibleList[0]=specialDgSearch(jointlyResponsibles[0].findNext('td').get_text().strip())
		jointlyResponsibleList[1]=jointlyResponsibles[1].findNext('td').get_text().strip()
		return jointlyResponsibleList
	except:
		return jointlyResponsibleList

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
	short name or dg itself if it is not associated to an acronym in the db
	"""
	try:
		#if there is a match in the db -> return short name (acronym)
		print "dg", dg
		print "dgCode", DGFullNameModel.objects.get(fullName=dg).dgCode_id
		dgCode=DGFullNameModel.objects.get(fullName=dg).dgCode_id
		return DGCodeModel.objects.get(id=dgCode).acronym
	except:
		print "Full name not stored in db"
		return dg


def getPrelexDGProposition1(soup):
	"""
	FUNCTION
	gets the prelexDGProposition1 variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	prelexDGProposition1
	"""
	try:
		#dgProposition
		dg=soup.find("td", text="Primarily responsible").findNext('td').get_text().strip()
		specialDg=specialDgSearch(dg)
		#the variable corresponds to a real person
		if specialDg==None:
			return dg
		#it can be associated to an acronym or short name
		#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=111863
		return specialDg

	except:
		return None

#~ in front of "Primarily responsible"
#can be Null


def getPrelexRespProposList(soup):
	"""
	FUNCTION
	gets the responsible(s) from the prelex url (prelexRespPropos1, prelexRespPropos2, prelexRespPropos3)
	PARAMETERS
	soup: prelex url content
	RETURN
	list of responsible(s)
	"""
	respProposList=[]
	respProposList.append(None)
	respProposList.append(None)
	respProposList.append(None)
	try:
		resp=soup.find("td", text="Responsible").findNext('td').get_text().strip()
		temp=resp.split(";")
		#only one responsible
		respProposList[0]=temp[0].strip()
		#two responsibles
		#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=191554
		respProposList[1]=temp[1].strip()
		#three responsibles
		respProposList[2]=temp[2].strip()
	except:
		return respProposList

#~ in front of "Responsible"
#can be Null


def getPrelexTransmissionCouncil(soup, proposOrigine):
	"""
	FUNCTION
	gets the prelexTransmissionCouncil variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	prelexTransmissionCouncil
	"""
	transmissionCouncil=None
	try:
		if proposOrigine=="CONS":
			transmissionCouncil=getPrelexAdoptionProposOrigine(soup, proposOrigine)
		else:
			transmissionCouncil=soup.find("a", text=re.compile("Transmission to Council")).findNext('br').next.strip()
	except:
		print "pb transmissionCouncil"

	#transform dates to the iso format (YYYY-MM-DD)
	if transmissionCouncil!=None:
		year, month, day=dateFct.splitFrenchFormatDate(transmissionCouncil)
		transmissionCouncil=dateFct.dateToIso(year, month, day)
	return transmissionCouncil

#date in front of "Transmission to Council"
#not Null (except blank page -> error on page)
#AAAA-MM-JJ format
#ProposOrigine = CONS -> AdoptionProposOrigine


def getPrelexNbPointB(soup, proposOrigine):
	"""
	FUNCTION
	gets the prelexNbPointB variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	prelexNbPointB
	"""
	if proposOrigine=="CONS" or proposOrigine=="BCE":
		return None
	return len(soup.findAll(text=re.compile('ITEM "B"')))

#~ in front of "COUNCIL AGENDA": counts the number of 'ITEM "B"' on the page
#~ not NULL
#~ De 0 a 20
#~ if proposOrigine=="CONS" or "BCE", filled manually


def getPrelexConsB(soup, proposOrigine):
	"""
	FUNCTION
	gets the prelexConsB variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	prelexConsB
	"""
	if proposOrigine!="CONS":
		consB=""
		for tables in soup.findAll(text=re.compile('ITEM "B" ON COUNCIL AGENDA')):
			consB+=tables.findParent('table').find(text=re.compile("SUBJECT")).findNext("font", {"size":-2}).get_text().strip()+'; '
		if consB=="":
			return None
		return consB[:-2]
	return None

#can be Null
#in front of SUBJECT, only if the act is processed at B point (preceded by 'ITEM "B" ON COUNCIL AGENDA')
#concatenate all the values, even if redundancy
#~ if proposOrigine=="CONS", filled manually


def getPrelexAdoptionConseil(soup, suite2LecturePE, proposSplittee, nbLectures):
	"""
	FUNCTION
	gets the prelexAdoptionConseil variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	prelexAdoptionConseil
	"""
	adoptionCouncil=None
	# if there is no  2d Lecture at PE
	if suite2LecturePE==0:
		actsList=["Formal adoption by Council", "Adoption common position", "Council approval 1st rdg"]
		for act in actsList:
			try:
				adoptionCouncil=soup.find("a", text=re.compile(act)).findNext('br').next.strip()
				break
			except:
				print "pb", act
	# if Suite2LecturePE=Y and proposSplittee=N
	elif proposSplittee==0:
		if nbLectures==2:
			try:
				#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=156619
				dateTableSoup=soup.find("b", text="EP opinion 2nd rdg").findParent("table")
				#check table contains "Approval without amendment"
				approval=dateTableSoup.find(text="Approval without amendment")
				#check next table title is "Signature by EP and Council"
				nextTableTitle=dateTableSoup.findNext("table").find(text="Signature by EP and Council")
				#if conditions are met, then get the date
				adoptionCouncil=dateTableSoup.find("b").get_text()
			except:
				print "pb AdoptionConseil (case proposSplittee==0)"
		elif nbLectures==3:
			#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=137644
			dateTableSoup=soup.find("b", text="Council decision at 3rd rdg").findParent("table")
			#check next table title is "Signature by EP and Council"
			nextTableTitle=dateTableSoup.findNext("table").find(text="Signature by EP and Council")
			#if conditions are met, then get the date
			adoptionCouncil=dateTableSoup.find("b").get_text()
			#~ return soup.find("a", text=re.compile("Council decision at 3rd rdg")).findNext('br').next.strip()

		#transform dates to the iso format (YYYY-MM-DD)
	if adoptionCouncil!=None:
		year, month, day=dateFct.splitFrenchFormatDate(adoptionCouncil)
		adoptionCouncil=dateFct.dateToIso(year, month, day)
	return adoptionCouncil

#~ date in front of "Formal adoption by Council" or "Adoption common position" or "Council approval 1st rdg"
#not Null
#~ AAAA-MM-JJ format

#~ quand Suite2LecturePE= Y ET quand ProposSplittee= N and nbLectures=2. Dans ce cas, la date AdoptionConseil= la date qui se trouve en face de la ligne « EP Opinion 2nd rdg » (vérifier qu’à la ligne qui suit dans le même carré, on trouve « Approval without amendment » et que le titre du carré qui suit est bien « Signature by EP and Council »
#~ Exemple : http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=156619

#~ quand Suite2LecturePE= Y ET quand ProposSplittee= N and nbLectures=3 -> date in front of Council decision at 3rd rdg (vérifier que le titre du carré qui suit est bien « Signature by EP and Council »)
#~ Example: http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=137644

# if Suite2LecturePE=Y and proposSplittee=Y -> to fill manually


def getPrelexNbPointA(soup, proposOrigine):
	"""
	FUNCTION
	gets the prelexNbPointA variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	prelexNbPointA
	"""
	if proposOrigine=="CONS" or proposOrigine=="BCE":
		return None
	return len(soup.findAll(text=re.compile('ITEM "A"')))

#~ in front of "COUNCIL AGENDA": counts the number of 'ITEM "A"' on the page
#~ not NULL
#~ De 0 a 20
#~ if proposOrigine=="CONS" or "BCE", filled manually


def getPrelexCouncilA(soup):
	"""
	FUNCTION
	gets the prelexCouncilA variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	prelexCouncilA
	"""
	councilA=""
	for tables in soup.findAll(text=re.compile('ITEM "A" ON COUNCIL AGENDA')):
		councilA+=tables.findParent('table').find(text=re.compile("SUBJECT")).findNext("font", {"size":-2}).get_text().strip()+'; '
	return councilA[:-2]

#not Null
#in front of SUBJECT, only if the act is processed at A point (preceded by 'ITEM "A" ON COUNCIL AGENDA')
#concatenate all the values, even if redundancy


def getPrelexNombreLectures(soup, noUniqueType, proposSplittee):
	"""
	FUNCTION
	gets the prelexNombreLectures variable from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	prelexNombreLectures
	"""
	if noUniqueType!="COD":
		return None

	#proposition not splited
	if proposSplittee==0:
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
#~ NULL if NoUniqueType != COD
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


def getPrelexDateDiff(date1, date2):
	"""
	FUNCTION
	compute the difference between two dates
	PARAMETERS
	date1: first date
	date2: second date
	RETURN
	difference between the two dates in parameters
	"""
	if date1!=None and date2!=None:
		#transform dates to the iso format (YYYY-MM-DD)
		date1 = datetime.strptime(date1, "%Y-%m-%d")
		date2 = datetime.strptime(date2, "%Y-%m-%d")
		return (date1 - date2).days
	return None

#DureeAdoptionTrans (TransmissionConseil - AdoptionProposOrigine)
#DureeProcedureDepuisPropCom (AdoptionConseil – AdoptionProposOrigine)
#DureeProcedureDepuisTransCons (AdoptionConseil – TransmissionConseil)
#DureeTotaleDepuisPropCom (SignPECS – AdoptionProposOrigine)
#DureeTotaleDepuisTransCons (SignPECS – TransmissionConseil) 



def getPrelexInformation(soup, idsDataDic):
	"""
	FUNCTION
	gets all the information from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	dictionary of retrieved data from prelex
	"""
	dataDic={}

	#prelexAdoptionProposOrigine
	dataDic['prelexAdoptionProposOrigine']=getPrelexAdoptionProposOrigine(soup, idsDataDic['prelexProposOrigine'])
	print "prelexAdoptionProposOrigine:", dataDic['prelexAdoptionProposOrigine']

	#extract Adoption by Commission table (html content)
	adoptionByCommissionTableSoup=getPrelexAdoptionByCommissionTable(soup)
	#~ print "adoptionByCommissionTableSoup", adoptionByCommissionTableSoup

	#prelexComProc
	dataDic['prelexComProc']=getPrelexComProc(adoptionByCommissionTableSoup, idsDataDic['prelexProposOrigine'])
	print "prelexComProc:", dataDic['prelexComProc']

	#jointly responsible persons (prelexDGProposition2 and prelexRespPropos2 or prelexRespPropos3)
	jointlyResponsibleList=getPrelexJointlyResponsibles(adoptionByCommissionTableSoup)

	#prelexDGProposition1 and prelexDGProposition2
	dataDic['prelexDGProposition1']=getPrelexDGProposition1(adoptionByCommissionTableSoup)
	dataDic['prelexDGProposition2']=jointlyResponsibleList[0]
	print "prelexDGProposition1:", dataDic['prelexDGProposition1']
	print "prelexDGProposition2:", dataDic['prelexDGProposition2']

	#prelexRespPropos1, prelexRespPropos2, prelexRespPropos3
	respProposList=getPrelexRespProposList(adoptionByCommissionTableSoup)
	dataDic['prelexRespPropos1']=respProposList[0]
	dataDic['prelexRespPropos2']=respProposList[1]
	dataDic['prelexRespPropos3']=respProposList[2]

	#jointly responsible (prelexRespPropos2 or prelexRespPropos3)
	if dataDic['prelexRespPropos2']==None:
		dataDic['prelexRespPropos2']=jointlyResponsibleList[1]
	elif dataDic['prelexRespPropos3']==None:
		dataDic['prelexRespPropos3']=jointlyResponsibleList[1]

	print "prelexRespPropos1:", dataDic['prelexRespPropos1']
	print "prelexRespPropos2:", dataDic['prelexRespPropos2']
	print "prelexRespPropos3:", dataDic['prelexRespPropos3']

	#prelexTransmissionCouncil
	dataDic['prelexTransmissionCouncil']=getPrelexTransmissionCouncil(soup, idsDataDic['prelexProposOrigine'])
	print "prelexTransmissionCouncil:", dataDic['prelexTransmissionCouncil']

	#prelexNbPointB
	dataDic['prelexNbPointB']=getPrelexNbPointB(soup, idsDataDic['prelexProposOrigine'])
	print "prelexNbPointB:", dataDic['prelexNbPointB']

	#prelexConsB
	dataDic['prelexConsB']=getPrelexConsB(soup, idsDataDic['prelexProposOrigine'])
	print "prelexConsB:", dataDic['prelexConsB']

	#prelexNombreLectures -> ALREADY IN OEIL -> used only for prelexAdoptionConseil!
	dataDic['prelexNombreLectures']=getPrelexNombreLectures(soup, idsDataDic['prelexNoUniqueType'], idsDataDic['proposSplittee'])
	#~ print "prelexNombreLectures:", dataDic['prelexNombreLectures']

	#prelexAdoptionConseil
	dataDic['prelexAdoptionConseil']=getPrelexAdoptionConseil(soup, idsDataDic['suite2eLecturePE'], idsDataDic['proposSplittee'], dataDic['prelexNombreLectures'])
	print "prelexAdoptionConseil:", dataDic['prelexAdoptionConseil']

	#prelexNbPointA
	dataDic['prelexNbPointA']=getPrelexNbPointA(soup, idsDataDic['prelexProposOrigine'])
	print "prelexNbPointA:", dataDic['prelexNbPointA']

	#prelexCouncilA
	dataDic['prelexCouncilA']=getPrelexCouncilA(soup)
	print "prelexCouncilA:", dataDic['prelexCouncilA']

	#prelexDureeAdoptionTrans
	dataDic['prelexDureeAdoptionTrans']=getPrelexDateDiff(dataDic['prelexTransmissionCouncil'], dataDic['prelexAdoptionProposOrigine'])
	print "prelexDureeAdoptionTrans:", dataDic['prelexDureeAdoptionTrans']

	#prelexDureeProcedureDepuisPropCom
	dataDic['prelexDureeProcedureDepuisPropCom']=getPrelexDateDiff(dataDic['prelexAdoptionConseil'], dataDic['prelexAdoptionProposOrigine'])
	print "prelexDureeProcedureDepuisPropCom:", dataDic['prelexDureeProcedureDepuisPropCom']

	#prelexDureeProcedureDepuisTransCons
	dataDic['prelexDureeProcedureDepuisTransCons']=getPrelexDateDiff(dataDic['prelexAdoptionConseil'], dataDic['prelexTransmissionCouncil'])
	print "prelexDureeProcedureDepuisTransCons:", dataDic['prelexDureeProcedureDepuisTransCons']

	#prelexDureeTotaleDepuisPropCom
	dataDic['prelexDureeTotaleDepuisPropCom']=getPrelexDateDiff(idsDataDic["signPECS"], dataDic['prelexAdoptionProposOrigine'])
	print "prelexDureeTotaleDepuisPropCom:", dataDic['prelexDureeTotaleDepuisPropCom']

	#prelexDureeTotaleDepuisTransCons
	dataDic['prelexDureeTotaleDepuisTransCons']=getPrelexDateDiff(idsDataDic["signPECS"], dataDic['prelexTransmissionCouncil'])
	print "prelexDureeTotaleDepuisTransCons:", dataDic['prelexDureeTotaleDepuisTransCons']

	return dataDic
