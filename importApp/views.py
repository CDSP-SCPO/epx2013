#-*- coding: utf-8 -*-
import csv
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from forms import CSVUploadForm
from models import CSVUploadModel, DosIdModel
from actsIdsValidation.models import ActsIdsModel
from actsInformationRetrieval.models import ConfigConsModel, CodeSectRepModel, CodeAgendaModel, AdoptPCModel, GvtCompoModel,RespProposModel, NationRespModel, NationalPartyRespModel, EUGroupRespModel, NPModel
#call function to save date in the iso format (YYYY-MM-DD)
import datetime
import os
#cross validation functions and get information from eurlex, oeil, prelex
import getIdsFunctions as info
#redirect to login page if not logged
from django.contrib.auth.decorators import login_required
#variables name
import actsIdsValidation.variablesNameForIds as vnIds
import actsInformationRetrieval.variablesNameForInformation as vnInfo
#model as parameter
from django.db.models.loading import get_model


def detectDelimiter(csvFile):
	"""
	FUNCTION
	detect the delimiter of a csv file and returns it
	PARAMETERS
	csvFile: csv file to check
	RETURN
	delimiter character
	"""
	with open(csvFile, 'r') as myCsvfile:
		header=myCsvfile.readline()
		if header.find(";")!=-1:
			#~ print "delimiter=';'"
			return ";"
		if header.find(",")!=-1:
			#~ print "delimiter=','"
			return ","
	#default delimiter (MS Office export)
	return ";"


def emptyOrVar(var, varType):
	"""
	FUNCTION
	returns the variable of None if it contains no value
	PARAMETERS
	var: variable to test
	varType: type of the variable (string, int)
	RETURN
	variable or None
	"""
	returnValue=None
	if varType=="str":
		if var.strip()!="NULL" and var.strip()!="":
			#~ print "not null str"
			returnValue=var
	elif varType=="int":
		try:
			int(var)
			#~ print "not null int"
			returnValue=var
		except:
			#~ print "not int"
			pass

	return returnValue


def import2Tables(csvFile, table1, table2):
	"""
	FUNCTION
	open a csv file and save its variables variables in the database (in 2 different tables ->  used for configCons, codeAgenda and respPropos*)
	PARAMETERS
	csvFile: file to handle
	table1: list of model name, field name, position in the csv file for table1
	table2: list of model name, field name, position in the csv file for table2 [USED FOR THE JOIN]
	RETURN
	list of rows saved / not saved
	"""
	errorList=[]
	attr1List=[]
	with open(csvFile, 'r') as myCsvfile:
		reader=csv.reader(myCsvfile,delimiter=detectDelimiter(csvFile))
		header=reader.next()
		for row in reader:
			model1 = get_model('actsInformationRetrieval', table1[0])
			model2 = get_model('actsInformationRetrieval', table2[0])
			attrName1=table1[1]
			attrName2=table2[1]
			attrIdName1=attrName1+"_id"
			attr1=row[table1[2]].strip()
			attr2=row[table2[2]].strip()
			#if respPropos -> change name format of respPropos: "LASTNAME, Firstname" -> "LASTNAME Firstname"
			if attrName2=="respPropos":
				attr2=attr2.replace(",","")
			attr1Exist=False
			attr2Exist=False
			error=False
			msg="The row "+attrName2+"="+attr2+", "+attrName1+"="+attr1
			errorMsg=msg+" couldn't be saved!"
			noErrorMsg=msg+" has been saved!"


			#does attrName1 already exist in the db?
			try:
				attr1Instance=model1.objects.get(**{attrName1: attr1})
				attr1Exist=True
			except Exception, e:
				print "exception", e

			try:
				#does attrName2 already exist in the db?
				attr2Instance=model2.objects.get(**{attrName2: attr2})
				#the attrName1 foreign key is not filled
				if getattr(attr2Instance, attrIdName1)==None:
					attr2Exist="attr2"
				else:
					#the attrName1 foreign key is filled -> nothing to do for this raw!
					attr2Exist="attr2+foreignKey"
					error=True
					errorList.append(errorMsg)
			except Exception, e:
				print "exception", e

			#save attrName1
			if not attr1Exist:
				try:
					model1(**{attrName1: attr1}).save()
				except:
					print "ERROR, "+attrName1+" could not be saved"
					if not error:
						error=True
						errorList.append(errorMsg)

			#check attrName1 exists
			if not attr1Exist or not error:
				#retrieve attrName1
				attr1Instance=model1.objects.get(**{attrName1: attr1}).id

				if not attr2Exist:
					#save attr2
					attr2Instance=model2(**{attrName2: attr2, attrIdName1: attr1Instance})

				#update attr2 with attrName1
				elif attr2Exist=="attr2":
					attr2Instance=model2.objects.get(**{attrName2: attr2})
					setattr(attr2Instance, attrIdName1, attr1Instance)

				#save attr2
				try:
					attr2Instance.save()
					attr1List.append(noErrorMsg)
				except IntegrityError, e:
					print "exception", e
					if not error:
						errorList.append(errorMsg)

	return attr1List, errorList


def getDosIdData(row):
	"""
	FUNCTION
	get a string (row from csv file) and put its content into an instance of DosIdModel
	PARAMETERS
	row: row from the csv file
	RETURN
	instance: instance of the model with the extracted data
	msg: id of the row (instance), used to display an error message
	"""
	instance = DosIdModel()
	if row[0].strip() !="":
		instance.dosId=int(row[0])
		instance.proposOrigine=row[1].strip()
		instance.proposAnnee=int(row[2])
		instance.proposChrono=row[3].strip()
		instance.splitNumber=emptyOrVar(row[4], "int")

	msg=(instance.dosId)
	return instance, msg


def getActData(row):
	"""
	FUNCTION
	get a string (row from csv file) and put its content into an instance of ActsIdsModel
	PARAMETERS
	row: row from the csv file
	RETURN
	instance: instance of the model with the extracted data
	msg: id of the row (instance), used to display an error message
	"""
	instance = ActsIdsModel()
	if row[7].strip()!="":
		instance.releveAnnee=int(row[0])
		instance.releveMois=int(row[1])
		instance.noOrdre=int(row[2])
		instance.titreRMC=row[3].strip()
		instance.adopCSRegleVote=row[4].strip()
		adopCSAbs=''.join(row[5].split())
		instance.adopCSAbs=adopCSAbs
		instance.adoptCSContre=row[6].strip()
		instance.fileNoCelex=row[7].strip()
		instance.fileProposAnnee=emptyOrVar(row[8], "int")
		instance.fileProposChrono=emptyOrVar(row[9].replace(" ", ""), "str")
		instance.fileProposOrigine=emptyOrVar(row[10], "str")
		instance.fileNoUniqueAnnee=emptyOrVar(row[11], "int")
		instance.fileNoUniqueType=emptyOrVar(row[12], "str")
		instance.fileNoUniqueChrono=emptyOrVar(row[13], "str")
		if row[14].strip()=="Y":
			instance.proposSplittee=True
		if row[15].strip()=="Y":
			instance.suite2eLecturePE=True
		instance.councilPath=row[16].strip()
		if instance.councilPath!="" and instance.councilPath[-1]==".":
			instance.councilPath=instance.councilPath[:-1]
		#we don't take the council path column
		instance.notes=row[17].strip()

		#we save fileDosId from the dosIdModel model
		try:
			#if split proposition
			if len(instance.fileProposChrono)>2 and instance.fileProposChrono[-2]=="-":
				newFileProposChrono=instance.fileProposChrono[:-2]
				newSplitNumber=instance.fileProposChrono[-1]
				fileDosId=DosIdModel.objects.get(proposOrigine=instance.fileProposOrigine, proposAnnee=instance.fileProposAnnee, proposChrono=newFileProposChrono, splitNumber=newSplitNumber)
				instance.fileDosId=fileDosId.dosId
			else:
				fileDosId=DosIdModel.objects.get(proposOrigine=instance.fileProposOrigine, proposAnnee=instance.fileProposAnnee, proposChrono=instance.fileProposChrono)
				instance.fileDosId=fileDosId.dosId
		except Exception, e:
			instance.fileDosId=None
			print e

	msg=(instance.releveAnnee, instance.releveMois, instance.noOrdre)
	return instance, msg


def getAndSaveRetrievedIds(idsList):
	"""
	FUNCTION
	get and save retrieved ids from eurlex, oeil and prelex in the the database
	PARAMETERS
	idsList: list of act ids to save (monthly summary ids)
	RETURN
	no
	"""
	dataDic={}
	for ids in idsList:
		releveAnneeVar=ids[0]
		releveMoisVar=ids[1]
		noOrdreVar=ids[2]
		#~ print "releveAnneeVar", releveAnneeVar
		#~ print "releveMoisVar", releveMoisVar
		#~ print "noOrdreVar", noOrdreVar
		act=ActsIdsModel.objects.get(releveAnnee=releveAnneeVar,releveMois=releveMoisVar,noOrdre=noOrdreVar)

		#get ids
		#eurlex
		dataDic=info.checkAndGetEurlexIds(str(act.fileNoCelex))
		#oeil
		dataDic.update(info.checkAndGetOeilIds(str(act.fileNoUniqueType), str(act.fileNoUniqueAnnee), str(act.fileNoUniqueChrono)))
		#prelex
		idsDic={}
		#try with dosId
		if act.fileDosId!=None:
			idsDic['dosId']=str(act.fileDosId)
		#no fileProposChrono? is it a split proposition?
		elif act.fileProposChrono==None or "-" in act.fileProposChrono:
			#try with the oeil ids
			idsDic['noUniqueType']=str(act.fileNoUniqueType)
			idsDic['noUniqueAnnee']=str(act.fileNoUniqueAnnee)
			idsDic['noUniqueChrono']=str(act.fileNoUniqueChrono)
		else:
			#prelex ids
			idsDic['proposOrigine']=str(act.fileProposOrigine)
			idsDic['proposAnnee']=str(act.fileProposAnnee)
			idsDic['proposChrono']=str(act.fileProposChrono)

		dataDic.update(info.checkAndGetPrelexIds(idsDic))

		#store dictionary ids into the model object
		act.__dict__.update(dataDic)

		try:
			#save the object
			act.save()
			print "act", releveAnneeVar, releveMoisVar, noOrdreVar,"saved"
		except IntegrityError, e:
			print e


def getAdoptPCData(row):
	"""
	FUNCTION
	get a string (row from csv file) and put its content into an instance of AdoptPCModel
	PARAMETERS
	row: row from the csv file
	RETURN
	instance: instance of the model with the extracted data
	msg: id of the row (instance), used to display an error message
	"""
	instance = AdoptPCModel()
	instance.releveAnnee=int(row[0])
	instance.releveMois=int(row[1])
	instance.noOrdre=int(row[2])
	instance.adoptPCAbs=row[3].strip()
	instance.adoptPCContre=row[4].strip()
	msg=(instance.releveAnnee, instance.releveMois, instance.noOrdre)
	return instance, msg


def getGvtCompoData(row):
	"""
	FUNCTION
	get a string (row from csv file) and put its content into an instance of GvtCompoModel
	PARAMETERS
	row: row from the csv file
	RETURN
	instance: instance of the model with the extracted data
	msg: id of the row (instance), used to display an error message
	"""
	instance = GvtCompoModel()
	instance.startDate=row[0].strip().replace("/", "-")
	instance.endDate=row[1].strip().replace("/", "-")
	instance.nationGvtPoliticalComposition=row[2].strip()
	msg=(instance.startDate, instance.endDate, instance.nationGvtPoliticalComposition)
	return instance, msg


def getNpData(row):
	"""
	FUNCTION
	get a string (row from csv file) and put its content into an instance of NPModel
	PARAMETERS
	row: row from the csv file
	RETURN
	instance: instance of the model with the extracted data
	msg: id of the row (instance), used to display an error message
	"""
	instance = NPModel()
	instance.npCaseNumber=int(row[0])
	instance.noCelex=row[1].strip()
	instance.np=row[2].strip()
	instance.npActivityType=row[3].strip()
	dateNP=row[4].strip().replace("/", "-")
	if dateNP=="NULL":
		dateNP=None
	instance.npActivityDate=dateNP
	msg=(instance.npCaseNumber)
	return instance, msg


def import1Table(csvFile, importType):
	"""
	FUNCTION
	open a csv file and save its AdoptPC variables in the database (in one table -> used for dosId, act, adoptPC, gvtCompo and np)
	PARAMETERS
	csvFile: file to handle
	importSrc: type of the file to import
	RETURN
	list of variables saved / not saved
	"""
	savedList=[]
	errorList=[]
	with open(csvFile, 'r') as myCsvfile:
		reader=csv.reader(myCsvfile,delimiter=detectDelimiter(csvFile))
		header=reader.next()
		for row in reader:
			#according to the type of import, extract the content of the row and put it in an instance model
			instance, msg=eval("get"+importType[0].upper()+importType[1:]+"Data")(row)
			try:
				instance.save()
				savedList.append(msg)
			except IntegrityError, e:
				error= "The row " + str(msg) + " ALREADY EXISTS!!"
				errorList.append(error)
				print "error", e

	return savedList, errorList


#~ @login_required(login_url=settings.projectRoot+'/login/')
@login_required
def importView(request):
	"""
	VIEW
	displays and processes the import page
	template called: import/index.html
	"""
	responseDic={}
	responseDic['displayName']=vnIds.variablesNameDic
	responseDic['displayName'].update(vnInfo.variablesNameDic)
	#~ print "vnIds", vnIds.variablesNameDic

	if request.method == 'POST':
		if "csvFile" in request.POST and request.POST["csvFile"]!="" or "csvFile" in request.FILES and request.FILES["csvFile"]!="":
			form = CSVUploadForm(request.POST, request.FILES)
			responseDic['form']=form
			#the form is valid and the import can be processed
			if form.is_valid():
				print "csv import"
				fileToImport=form.cleaned_data['fileToImport']
				newFilename=" ".join(request.FILES['csvFile'].name.split())
				path = settings.MEDIA_ROOT+"import/"+newFilename
				#if a file with the same name already exists, we delete it
				if os.path.exists(path):
					os.remove(path)
				newCsvFile = CSVUploadModel(csvFile = request.FILES['csvFile'])
				newCsvFile.save()
				savedList=[]
				errorList=[]

				#importation of dosId, act, adoptPC, gvtCompo or np file
				if fileToImport in ["dosId","act","adoptPC","gvtCompo", "np"]:
					savedList, errorList= import1Table(path, fileToImport)
					if fileToImport=="act":
						#save retrieved ids
						getAndSaveRetrievedIds(savedList)
				#importation of configCons or codeAgenda
				elif fileToImport in["configCons", "codeAgenda"]:
					#model name, field name, position in the csv file
					table1=[fileToImport[0].upper()+fileToImport[1:]+"Model", fileToImport, 1]
					table2=["CodeSectRepModel", "codeSectRep", 0]
					savedList, errorList= import2Tables(path, table1, table2)
				#importation of respPropos
				elif fileToImport=="respPropos":
					#respPropos
					table2=["RespProposModel", "respPropos", 0]
					#nationResp
					table1=["NationRespModel", "nationResp", 3]
					savedList, errorList= import2Tables(path, table1, table2)
					#nationalPartyResp
					table1=["NationalPartyRespModel", "nationalPartyResp", 1]
					savedList, errorList= import2Tables(path, table1, table2)
					#euGroupResp
					table1=["EUGroupRespModel", "euGroupResp", 2]
					savedList, errorList= import2Tables(path, table1, table2)

				responseDic['errorList']=errorList
				responseDic['success']=str(len(savedList)) + " raw(s) imported, "+ str(len(errorList)) +" error(s)!"

		#a selection has been made in the drop down list
		else:
			responseDic['form'] = CSVUploadForm(initial={'fileToImport': request.POST["fileToImport"]})

	else:
		responseDic['form']=CSVUploadForm()

	return render_to_response('import/index.html', responseDic, context_instance=RequestContext(request))
