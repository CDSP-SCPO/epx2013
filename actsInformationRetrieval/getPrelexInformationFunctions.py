# -*- coding: utf-8 -*-
"""
get the information from Prelex (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
#dg codes
from actsInformationRetrieval.models import DgCodeModel, DgFullNameModel


def getAdoptionByCommissionTableFromPrelex(soup):
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
		return None


def getAdoptionProposOrigineFromPrelex(soup, proposOrigine):
	"""
	FUNCTION
	gets the date of adoption by commission from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	adoption by commission date
	"""
	if proposOrigine=="COM":
		return soup.find("a", text=re.compile("Adoption by Commission")).findNext('br').next.strip()
	if proposOrigine=="JAI":
		return getTransmissionCouncilFromPrelex(soup, proposOrigine)
	if proposOrigine=="CONS":
		print "TODO: extraction pdf almost done (see tests)"
		return "00-00-0000"

#~ Date in front of "Adoption by Commission"
#~ not NULL
#~ AAAA-MM-JJ format
#~ ProposOrigine = COM -> date adoption de la proposition par la Commission
#~ ProposOrigine = JAI -> TransmissionConseil date
#~ EM -> not processed because appears only when noUniqueType=CS which concerns non definitive acts (not processed)
#~ ProposOrigine = CONS -> date in pdf document (council path link)
#~ TODO: case where proposOrigine=CONS


def getComProcFromPrelex(soup, proposOrigine):
	"""
	FUNCTION
	gets the mode of decision from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	decision mode
	"""
	if proposOrigine== "COM":
		return soup.find("td", text="Decision mode:").findNext('td').get_text().strip()
	return None

#~ in front of "Decision mode"
#~ Possible values:
#~ "Oral Procedure", "Written Procedure", "Empowerment procedure"
#~ Null if ProposOrigine != COM


def getJointlyResponsiblesFromPrelex(soup):
	"""
	FUNCTION
	gets the jointly responsible persons (dgProposition2 and respPropos2) from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	list of jointly responsible persons (dgProposition2 and respPropos2)
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
		dgCode=DgFullNameModel.objects.get(fullName=dg).values("dgCode_id")
		return DgCodeModel.objects.get(id=dgCode).values("acronym")
	except:
		print "Full name not stored in db"
		return dg


def getDgPropositionFromPrelex(soup):
	"""
	FUNCTION
	gets the primarily responsible from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	primarily responsible
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


def getRespProposListFromPrelex(soup):
	"""
	FUNCTION
	gets the responsible(s) from the prelex url (respPropos1, respPropos2, respPropos3)
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


def getTransmissionCouncilFromPrelex(soup, proposOrigine):
	"""
	FUNCTION
	gets the date of transmission to council from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	transmission to council date
	"""
	if proposOrigine=="CONS":
		return getAdoptionProposOrigineFromPrelex(soup, proposOrigine)
	return soup.find("a", text=re.compile("Transmission to Council")).findNext('br').next.strip()

#date in front of "Transmission to Council"
#not Null
#~ AAAA-MM-JJ format
#~ ProposOrigine = CONS -> AdoptionProposOrigine


def getNbPointBFromPrelex(soup, proposOrigine):
	"""
	FUNCTION
	gets the number of items "B" from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	number of items "B"
	"""
	if proposOrigine=="CONS" or proposOrigine=="BCE":
		return None
	return len(soup.findAll(text=re.compile('ITEM "B"')))

#~ in front of "COUNCIL AGENDA": counts the number of 'ITEM "B"' on the page
#~ not NULL
#~ De 0 a 20
#~ if proposOrigine=="CONS" or "BCE", filled manually


def getConsBFromPrelex(soup, proposOrigine):
	"""
	FUNCTION
	gets all the subjects of items "B" from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	list of subjects of items "B"
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


def getAdoptionConseilFromPrelex(soup, suite2LecturePE, proposSplittee, nbLectures):
	"""
	FUNCTION
	gets the date of adoption by council from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	adoption date
	"""
	# if there is no  2d Lecture at PE
	if suite2LecturePE==0:
		actsList=["Formal adoption by Council", "Adoption common position", "Council approval 1st rdg"]
		for act in actsList:
			try:
				return soup.find("a", text=re.compile(act)).findNext('br').next.strip()
			except:
				print "pb", act
	# if Suite2LecturePE=Y and proposSplittee=N
	date="00-00-0000"
	if proposSplittee==0:
		if nbLectures==2:
			try:
				#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=156619
				dateTableSoup=soup.find("b", text="EP opinion 2nd rdg").findParent("table")
				#check table contains "Approval without amendment"
				approval=dateTableSoup.find(text="Approval without amendment")
				#check next table title is "Signature by EP and Council"
				nextTableTitle=dateTableSoup.findNext("table").find(text="Signature by EP and Council")
				#if conditions are met, then get the date
				date=dateTableSoup.find("b").get_text()
			except:
				print "pb AdoptionConseil (case proposSplittee==0)"
				return date
		elif nbLectures==3:
			#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=137644
			dateTableSoup=soup.find("b", text="Council decision at 3rd rdg").findParent("table")
			#check next table title is "Signature by EP and Council"
			nextTableTitle=dateTableSoup.findNext("table").find(text="Signature by EP and Council")
			#if conditions are met, then get the date
			date=dateTableSoup.find("b").get_text()
			#~ return soup.find("a", text=re.compile("Council decision at 3rd rdg")).findNext('br').next.strip()
		
	return date

#~ date in front of "Formal adoption by Council" or "Adoption common position" or "Council approval 1st rdg"
#not Null
#~ AAAA-MM-JJ format

#~ quand Suite2LecturePE= Y ET quand ProposSplittee= N and nbLectures=2. Dans ce cas, la date AdoptionConseil= la date qui se trouve en face de la ligne « EP Opinion 2nd rdg » (vérifier qu’à la ligne qui suit dans le même carré, on trouve « Approval without amendment » et que le titre du carré qui suit est bien « Signature by EP and Council »
#~ Exemple : http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=156619

#~ quand Suite2LecturePE= Y ET quand ProposSplittee= N and nbLectures=3 -> date in front of Council decision at 3rd rdg (vérifier que le titre du carré qui suit est bien « Signature by EP and Council »)
#~ Example: http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=137644

# if Suite2LecturePE=Y and proposSplittee=Y -> to fill manually


def getNbPointAFromPrelex(soup, proposOrigine):
	"""
	FUNCTION
	gets the number of items "A" from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	number of items "A"
	"""
	if proposOrigine=="CONS" or proposOrigine=="BCE":
		return None
	return len(soup.findAll(text=re.compile('ITEM "A"')))

#~ in front of "COUNCIL AGENDA": counts the number of 'ITEM "A"' on the page
#~ not NULL
#~ De 0 a 20
#~ if proposOrigine=="CONS" or "BCE", filled manually


def getCouncilAFromPrelex(soup):
	"""
	FUNCTION
	gets all the subjects of items "A" from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	list of subjects of items "A"
	"""
	councilA=""
	for tables in soup.findAll(text=re.compile('ITEM "A" ON COUNCIL AGENDA')):
		councilA+=tables.findParent('table').find(text=re.compile("SUBJECT")).findNext("font", {"size":-2}).get_text().strip()+'; '
	return councilA[:-2]

#not Null
#in front of SUBJECT, only if the act is processed at A point (preceded by 'ITEM "A" ON COUNCIL AGENDA')
#concatenate all the values, even if redundancy


def getNbLecturesFromPrelex(soup, noUniqueType, proposSplittee):
	"""
	FUNCTION
	gets the number of lectures from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	number of lectures
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
	#~ if page contains "EP opinion 3rd rdg" or "EP decision 3rd rdg" -> NbLectures=3
	#~ if page contains "EP opinion 2nd rdg" -> NbLectures=2
	#~ if page contains "EP opinion 1st rdg" -> NbLectures=1
	#~ otherwise error
#~ if NoUniqueType=COD and if the proposition is splitted:
	#~ if page contains "EP: position, 3rd reading" or "EP: decision, 3rd reading" or "EP: legislative resolution, 3rd reading" -> NbLectures=3
	#~ if page contains "EP: position, 2nd reading" -> NbLectures=2
	#~ if page contains "EP: position, 1st reading" -> NbLectures=1
	#~ otherwise error


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
	
	#adoptionProposOrigine
	dataDic['adoptionProposOrigine']=getAdoptionProposOrigineFromPrelex(soup, idsDataDic['prelexProposOrigine'])
	print "adoptionProposOrigine (prelex):", dataDic['adoptionProposOrigine']
	
	#extract Adoption by Commission table (html content)
	adoptionByCommissionTableSoup=getAdoptionByCommissionTableFromPrelex(soup)
	#~ print "adoptionByCommissionTableSoup", adoptionByCommissionTableSoup
	
	#if there is a table called "Adoption by Commission"
	if adoptionByCommissionTableSoup!=None:
		#comProc
		dataDic['comProc']=getComProcFromPrelex(adoptionByCommissionTableSoup, idsDataDic['prelexProposOrigine'])
		print "comProc (prelex):", dataDic['comProc']
		
		#jointly responsible persons (dgProposition2 and respPropos2 or respPropos3)
		jointlyResponsibleList=getJointlyResponsiblesFromPrelex(adoptionByCommissionTableSoup)
		
		#dgProposition
		dataDic['dgProposition']=getDgPropositionFromPrelex(adoptionByCommissionTableSoup)
		dataDic['dgProposition2']=jointlyResponsibleList[0]
		print "dgProposition (prelex):", dataDic['dgProposition']
		print "dgProposition2 (prelex):", dataDic['dgProposition2']
		
		#respPropos1, respPropos2, respPropos3
		respProposList=getRespProposListFromPrelex(adoptionByCommissionTableSoup)
		dataDic['respPropos1']=respProposList[0]
		dataDic['respPropos2']=respProposList[1]
		dataDic['respPropos3']=respProposList[2]
		
		#jointly responsible (respPropos2 or respPropos3)
		if dataDic['respPropos2']==None:
			dataDic['respPropos2']=jointlyResponsibleList[1]
		elif dataDic['respPropos3']==None:
			dataDic['respPropos3']=jointlyResponsibleList[1]
		
		print "respPropos1 (prelex):", dataDic['respPropos1']
		print "respPropos2 (prelex):", dataDic['respPropos2']
		print "respPropos3 (prelex):", dataDic['respPropos3']
		
	else:
		#if there is a table called "Adoption by Commission"
		dataDic['comProc']=None
		dataDic['dgProposition']=None
		dataDic['dgProposition2']=None
		dataDic['respPropos1']=None
		dataDic['respPropos2']=None
		dataDic['respPropos3']=None
		
	
	#transmissionCouncil
	dataDic['transmissionCouncil']=getTransmissionCouncilFromPrelex(soup, idsDataDic['prelexProposOrigine'])
	print "transmissionCouncil (prelex):", dataDic['transmissionCouncil']
	
	#nbPointB
	dataDic['nbPointB']=getNbPointBFromPrelex(soup, idsDataDic['prelexProposOrigine'])
	print "nbPointB (prelex):", dataDic['nbPointB']
	
	#consB
	dataDic['consB']=getConsBFromPrelex(soup, idsDataDic['prelexProposOrigine'])
	print "consB (prelex):", dataDic['consB']
	
	#nbLectures
	dataDic['nbLectures']=getNbLecturesFromPrelex(soup, idsDataDic['prelexNoUniqueType'], idsDataDic['proposSplittee'])
	print "nbLectures (prelex):", dataDic['nbLectures']
	
	#adoptionConseil
	dataDic['adoptionConseil']=getAdoptionConseilFromPrelex(soup, idsDataDic['suite2eLecturePE'], idsDataDic['proposSplittee'], dataDic['nbLectures'])
	print "adoptionConseil (prelex):", dataDic['adoptionConseil']
	
	#nbPointA
	dataDic['nbPointA']=getNbPointAFromPrelex(soup, idsDataDic['prelexProposOrigine'])
	print "nbPointA (prelex):", dataDic['nbPointA']
	
	#councilA
	dataDic['councilA']=getCouncilAFromPrelex(soup)
	print "councilA (prelex):", dataDic['councilA']	

	return dataDic
