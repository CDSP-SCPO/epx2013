# -*- coding: utf-8 -*-
"""
get the information from Prelex (fields for the statistical analysis)
"""
import re
from bs4 import BeautifulSoup
#dg codes
from actsInformationRetrieval.models import DGCodeModel, DGFullNameModel, RespProposModel, CodeSectRepModel, ConfigConsModel, RespProposModel, NationRespModel, NationalPartyRespModel, EUGroupRespModel, AdoptPCModel
from common.commonFunctions import stringToIsoDate, listReverseEnum
from datetime import datetime
#model as parameter
from django.db.models.loading import get_model
#remove accents
from common.commonFunctions import remove_nonspacing_marks


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
	try:
		adoptionProposOrigine=None
		if proposOrigine=="COM":
			adoptionProposOrigine=soup.find("a", text=re.compile("Adoption by Commission")).findNext('br').next.strip()
		if proposOrigine=="JAI":
			adoptionProposOrigine=getPrelexTransmissionCouncil(soup, proposOrigine)
		if proposOrigine=="CONS":
			print "TODO: extraction pdf almost done (see tests)"

		#transform dates to the iso format (YYYY-MM-DD)
		if adoptionProposOrigine!=None:
			adoptionProposOrigine=stringToIsoDate(adoptionProposOrigine)

		return adoptionProposOrigine
	except:
		print "no prelexAdoptionProposOrigine!"
		return None

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


def saveRespProposAndGetRespProposObject(respPropos):
	"""
	FUNCTION
	save respPropos if doesn't exist in the db yet and get respProposId (needed for the foreign key)
	PARAMETERS
	respPropos: full name of respPropos
	RETURN
	respProposObject: instance of respProposModel
	"""
	#remove trailing "'"
	if respPropos[-1]=="'":
		respPropos=respPropos[:-1]
	#remove accents
	respPropos=remove_nonspacing_marks(respPropos)
	#change name format: "Firstname LASTNAME" -> "LASTNAME Firstname"
	respPropos=respPropos.split()
	first_name=last_name=""
	#get first names
	for name in respPropos:
		#get last names
		if name.isupper():
			last_name+=name+" "
		#get first names
		else:
			first_name+=name+" "

	respPropos=last_name[:-1]+" "+first_name[:-1]
	print "respPropos", respPropos

	try:
		#checks if respPropos already exists in the db
		respProposObject=RespProposModel.objects.get(respPropos=respPropos)
		print "respProposObject1", respProposObject
		return respProposObject
	except:
		#respPropos doesn't exist in the db yet -> we add it in the table
		respProposObject=RespProposModel(respPropos=respPropos).save()
		print "respProposObject2", respProposObject
		#get respPropos
		return respProposObject

	return None


def getPrelexJointlyResponsibles(soup):
	"""
	FUNCTION
	gets the jointly responsible persons (prelexDGProposition2 and prelexRespProposId2 (object) or prelexRespProposId3 (object) from the prelex url
	PARAMETERS
	soup: prelex url content
	RETURN
	list of jointly responsible persons (prelexDGProposition2 and prelexRespProposId2 (object) or prelexRespProposId3 (object))
	"""
	prelexDGProposition2=prelexRespProposObject2=None
	try:
		#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=191926
		jointlyResponsibles=soup.findAll("td", text="Jointly responsible")
		#prelexDGProposition2
		prelexDGProposition2=jointlyResponsibles[0].findNext('td').get_text().strip()
		#prelexRespPropos2 or 3
		prelexRespPropos2=jointlyResponsibles[1].findNext('td').get_text().strip()
		#get the id from RespProposModel
		prelexRespProposObject2=saveRespProposAndGetRespProposObject(prelexRespPropos2)

	except:
		print "no prelexDGProposition2, or prelexRespProposId2"

	return prelexDGProposition2, prelexRespProposObject2

#in front of "Jointly responsible"
#can be Null


def getPrelexSiglesDG(dg):
	"""
	FUNCTION
	gives the standard short name of the primarily responsible (if exists)
	PARAMETERS
	dg: primarily responsible
	RETURN
	short name of prelexDGProposition1-2
	"""
	dgCode=None
	try:
		#if there is a match in the db -> return dgCode
		dgCode_id=DGFullNameModel.objects.get(dgFullName=dg).dgCode_id
		dgCode=DGCodeModel.objects.get(id=dgCode_id).dgCode
		#it can be associated to a dgCode
		#~ http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=111863
	except:
		print "no short name for dg"

	return dgCode


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
		return soup.find("td", text="Primarily responsible").findNext('td').get_text().strip()
	except:
		return None

#~ in front of "Primarily responsible"
#can be Null


def getPrelexRespProposList(soup):
	"""
	FUNCTION
	gets the responsible(s) from the prelex url (prelexRespProposId1, prelexRespProposId2, prelexRespProposId3)
	PARAMETERS
	soup: prelex url content
	RETURN
	respProposList: list of responsibles(RespProposModel object)
	"""
	respProposList=[None for i in range(3)]

	try:
		resp=soup.find("td", text="Responsible").findNext('td').get_text().strip()
		temp=resp.split(";")
		#only one responsible
		for index in xrange(len(respProposList)):
			respProposList[index]=saveRespProposAndGetRespProposObject(temp[index].strip())
			#two responsibles
			#http://ec.europa.eu/prelex/detail_dossier_real.cfm?CL=en&DosId=191554
	except Exception, e:
		print "exception", e

	#~ print "respProposList", respProposList
	return respProposList

#~ in front of "Responsible"
#can be Null


def getConfigConsOrCodeAgenda(table1, table2):
	"""
	FUNCTION
	gets the prelex configCons or eurlex codeAgenda variables
	PARAMETERS
	table1: list of model name, field name in the csv file for table1
	table2: list of model name, field name and value in the csv file for table2 [USED FOR THE JOIN]
	RETURN
	configCons or codeAgenda
	"""
	if table2[2]!=None:
		model1 = get_model('actsInformationRetrieval', table1[0])
		model2 = get_model('actsInformationRetrieval', table2[0])
		attrName1=table1[1]
		attrName2=table2[1]
		attrIdName1=attrName1+"_id"
		attr2=table2[2].strip()
		for index, item in listReverseEnum(attr2):
			if item==".":
				newAttr2=attr2[:index]
				try:
					#does this newAttr2 exist in model2?
					instance2=model2.objects.get(**{attrName2: newAttr2})
					attrId1=getattr(instance2, attrIdName1)
					#if it exist, we get attr1 from model1
					instance1=model1.objects.get(id=attrId1)
					return getattr(instance1, attrName1)
				except Exception, e:
					print "exception", e

	return None


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
		transmissionCouncil=stringToIsoDate(transmissionCouncil)
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
	try:
		if proposOrigine=="CONS" or proposOrigine=="BCE":
			return None
		return len(soup.findAll(text=re.compile('ITEM "B"')))
	except:
		print "no prelexNbPointB!"
		return None

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
	try:
		if proposOrigine!="CONS":
			consB=""
			for tables in soup.findAll(text=re.compile('ITEM "B" ON COUNCIL AGENDA')):
				consB+=tables.findParent('table').find(text=re.compile("SUBJECT")).findNext("font", {"size":-2}).get_text().strip()+'; '
			if consB=="":
				return None
			return consB[:-2]
		return None
	except:
		print "no prelexNbPointB!"
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
		adoptionCouncil=stringToIsoDate(adoptionCouncil)
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
	try:
		if proposOrigine=="CONS" or proposOrigine=="BCE":
			return None
		return len(soup.findAll(text=re.compile('ITEM "A"')))
	except:
		print "no prelexNbPointA!"
		return None

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
	try:
		councilA=""
		for tables in soup.findAll(text=re.compile('ITEM "A" ON COUNCIL AGENDA')):
			councilA+=tables.findParent('table').find(text=re.compile("SUBJECT")).findNext("font", {"size":-2}).get_text().strip()+'; '
		return councilA[:-2]
	except:
		print "no prelexCouncilA!"
		return None

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


def getPrelexConfigCons(fullCodeSectRep01):
	"""
	FUNCTION
	gets the prelexConfigCons variable from fullCodeSectRep01, CodeSectRepModel and ConfigConsModel
	PARAMETERS
	fullCodeSectRep01: fullCodeSectRep01 variable
	RETURN
	prelexConfigCons variable associated to fullCodeSectRep01
	"""
	table1=["ConfigConsModel", "configCons"]
	table2=["CodeSectRepModel", "codeSectRep", fullCodeSectRep01]
	#get prelexConfigCons
	return getConfigConsOrCodeAgenda(table1, table2)



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
	if date1!=None and date1!="None" and date2!=None:
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


def getPrelexAdoptPCVariables(releveIds, columnName):
	"""
	FUNCTION
	get adoptPCAbs or adoptPCContre
	PARAMETERS
	releveIds: list of ids of the model
	columnName: name of the variable ot retrieve
	RETURN
	value of the variable
	"""
	try:
		#get attrId1 from model2
		instance=AdoptPCModel.objects.get(releveAnnee=releveIds[0], releveMois=releveIds[1], noOrdre=releveIds[2])
		return getattr(instance, columnName)
	except Exception, e:
		print "exception", e

	return None


def getPrelexAdoptPCAbs(releveIds):
	"""
	FUNCTION
	get adoptPCAbs
	PARAMETERS
	releveIds: list of ids of the model
	RETURN
	value of the variable
	"""
	return getPrelexAdoptPCVariables(releveIds, "adoptPCAbs")


def getPrelexAdoptPCContre(releveIds):
	"""
	FUNCTION
	get adoptPCContre
	PARAMETERS
	releveIds: list of ids of the model
	RETURN
	value of the variable
	"""
	return getPrelexAdoptPCVariables(releveIds, "adoptPCContre")



def getPrelexInformation(soup, otherVariablesDic):
	"""
	FUNCTION
	gets all the information from the prelex url
	PARAMETERS
	soup: prelex url content
	otherVariablesDic: dictionary of variables needed to get some prelex variables
	RETURN
	dictionary of retrieved data from prelex
	"""
	dataDic={}

	#prelexAdoptionProposOrigine
	dataDic['prelexAdoptionProposOrigine']=getPrelexAdoptionProposOrigine(soup, otherVariablesDic['prelexProposOrigine'])
	print "prelexAdoptionProposOrigine:", dataDic['prelexAdoptionProposOrigine']

	#extract Adoption by Commission table (html content)
	adoptionByCommissionTableSoup=getPrelexAdoptionByCommissionTable(soup)
	#~ print "adoptionByCommissionTableSoup", adoptionByCommissionTableSoup

	#prelexComProc
	dataDic['prelexComProc']=getPrelexComProc(adoptionByCommissionTableSoup, otherVariablesDic['prelexProposOrigine'])
	print "prelexComProc:", dataDic['prelexComProc']

	#jointly responsible persons (prelexDGProposition2 and prelexRespProposObject2 or prelexRespProposObject3)
	prelexDGProposition2, prelexRespProposObject2=getPrelexJointlyResponsibles(adoptionByCommissionTableSoup)

	#prelexDGProposition1 and prelexSiglesDG1
	dataDic['prelexDGProposition1']=getPrelexDGProposition1(adoptionByCommissionTableSoup)
	dataDic['prelexSiglesDG1']=getPrelexSiglesDG(dataDic['prelexDGProposition1'])
	print "prelexDGProposition1:", dataDic['prelexDGProposition1']
	print "prelexSiglesDG1:", dataDic['prelexSiglesDG1']

	#prelexDGProposition2 and prelexSiglesDG2
	dataDic['prelexDGProposition2']=prelexDGProposition2
	dataDic['prelexSiglesDG2']=getPrelexSiglesDG(dataDic['prelexDGProposition2'])
	print "prelexDGProposition2:", dataDic['prelexDGProposition2']
	print "prelexSiglesDG2:", dataDic['prelexSiglesDG2']

	#prelexRespProposObject1, prelexRespProposObject2, prelexRespProposObject3
	respProposList=getPrelexRespProposList(adoptionByCommissionTableSoup)
	for index in xrange(len(respProposList)):
		dataDic['prelexRespProposId'+str(index+1)+'_id']=respProposList[index]

	#jointly responsible (prelexRespProposObject2 or prelexRespProposObject3)
	if prelexRespProposObject2!=None:
		if dataDic['prelexRespProposId2_id']==None:
			dataDic['prelexRespProposId2_id']=prelexRespProposObject2
		elif dataDic['prelexRespProposId3_id']==None:
			dataDic['prelexRespProposId3_id']=prelexRespProposObject2

	for index in xrange(len(respProposList)):
		name="prelexRespProposId"+str(index+1)+"_id"
		if dataDic[name]!=None:
			print name+":", dataDic[name].id
		else:
			print name+":", None

	#prelexTransmissionCouncil
	dataDic['prelexTransmissionCouncil']=getPrelexTransmissionCouncil(soup, otherVariablesDic['prelexProposOrigine'])
	print "prelexTransmissionCouncil:", dataDic['prelexTransmissionCouncil']

	#prelexNbPointB
	dataDic['prelexNbPointB']=getPrelexNbPointB(soup, otherVariablesDic['prelexProposOrigine'])
	print "prelexNbPointB:", dataDic['prelexNbPointB']

	#prelexConsB
	dataDic['prelexConsB']=getPrelexConsB(soup, otherVariablesDic['prelexProposOrigine'])
	print "prelexConsB:", dataDic['prelexConsB']

	#prelexNombreLectures -> ALREADY IN OEIL -> used only for prelexAdoptionConseil!
	dataDic['prelexNombreLectures']=getPrelexNombreLectures(soup, otherVariablesDic['prelexNoUniqueType'], otherVariablesDic['proposSplittee'])
	#~ print "prelexNombreLectures:", dataDic['prelexNombreLectures']

	#prelexAdoptionConseil
	dataDic['prelexAdoptionConseil']=getPrelexAdoptionConseil(soup, otherVariablesDic['suite2eLecturePE'], otherVariablesDic['proposSplittee'], dataDic['prelexNombreLectures'])
	print "prelexAdoptionConseil:", dataDic['prelexAdoptionConseil']

	#prelexNbPointA
	dataDic['prelexNbPointA']=getPrelexNbPointA(soup, otherVariablesDic['prelexProposOrigine'])
	print "prelexNbPointA:", dataDic['prelexNbPointA']

	#prelexCouncilA
	dataDic['prelexCouncilA']=getPrelexCouncilA(soup)
	print "prelexCouncilA:", dataDic['prelexCouncilA']

	#prelexConfigCons
	dataDic['prelexConfigCons']=getPrelexConfigCons(otherVariablesDic['fullCodeSectRep01'])
	print "prelexConfigCons:", dataDic['prelexConfigCons']

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
	dataDic['prelexDureeTotaleDepuisPropCom']=getPrelexDateDiff(str(otherVariablesDic["signPECS"]), dataDic['prelexAdoptionProposOrigine'])
	if dataDic['prelexDureeTotaleDepuisPropCom']==None:
		dataDic['prelexDureeTotaleDepuisPropCom']=dataDic['prelexDureeProcedureDepuisPropCom']
	print "prelexDureeTotaleDepuisPropCom:", dataDic['prelexDureeTotaleDepuisPropCom']

	#prelexDureeTotaleDepuisTransCons
	dataDic['prelexDureeTotaleDepuisTransCons']=getPrelexDateDiff(str(otherVariablesDic["signPECS"]), dataDic['prelexTransmissionCouncil'])
	if dataDic['prelexDureeTotaleDepuisTransCons']==None:
		dataDic['prelexDureeTotaleDepuisTransCons']=dataDic['prelexDureeProcedureDepuisTransCons']
	print "prelexDureeTotaleDepuisTransCons:", dataDic['prelexDureeTotaleDepuisTransCons']

	#prelexAdoptCSRegleVote
	dataDic['prelexAdoptCSRegleVote']=otherVariablesDic["adopCSRegleVote"]
	print "prelexAdoptCSRegleVote:", dataDic['prelexAdoptCSRegleVote']

	#prelexAdoptCSContre
	dataDic['prelexAdoptCSContre']=otherVariablesDic["adoptCSContre"]
	print "prelexAdoptCSContre:", dataDic['prelexAdoptCSContre']

	#prelexAdoptCSAbs
	dataDic['prelexAdoptCSAbs']=otherVariablesDic["adopCSAbs"]
	print "prelexAdoptCSAbs:", dataDic['prelexAdoptCSAbs']

	#prelexAdoptPCAbs
	dataDic['prelexAdoptPCAbs']=getPrelexAdoptPCAbs([otherVariablesDic["releveAnnee"], otherVariablesDic["releveMois"], otherVariablesDic["noOrdre"]])
	print "prelexAdoptPCAbs:", dataDic['prelexAdoptPCAbs']

	#prelexAdoptPCContre
	dataDic['prelexAdoptPCContre']=getPrelexAdoptPCContre([otherVariablesDic["releveAnnee"], otherVariablesDic["releveMois"], otherVariablesDic["noOrdre"]])
	print "prelexAdoptPCContre:", dataDic['prelexAdoptPCContre']

	return dataDic
