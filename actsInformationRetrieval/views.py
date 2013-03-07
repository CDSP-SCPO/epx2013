#-*- coding: utf-8 -*-
from actsIdsValidation.models import ActsIdsModel
from actsIdsValidation.forms import ActsIdsForm
from actsInformationRetrieval.forms import ActsInformationForm
from actsInformationRetrieval.models import ActsInformationModel
from datetime import date
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.forms.models import model_to_dict

#variables name
import actsIdsValidation.variablesNameForIds as vnIds
import variablesNameForInformation as vnInfo
#retrieve url contents
import sys
sys.path.append('import')
import getEurlexIdsFunctions as eurlexIds
import getOeilIdsFunctions as oeilIds
import getPrelexIdsFunctions as prelexIds
#retrieve information
import getEurlexInformationFunctions as eurlex
import getOeilInformationFunctions as oeil
import getPrelexInformationFunctions as prelex


def splitFrenchFormatDate(dateString):
	"""
	FUNCTION
	split a date ('DD-MM-YYYY') into year, month and day
	PARAMETERS
	dateString: date to split
	RETURN
	year, month and day of the date
	"""
	day=dateString[:2]
	month=dateString[3:5]
	year=dateString[6:]

	return year, month, day


def dateToIso(year, month, day):
	"""
	FUNCTION
	transform a date to the iso format ('YYYY-MM-DD')
	PARAMETERS
	year, month, day: year, month and day of the date to transform
	RETURN
	date in the iso format
	"""
	return date(int(year), int(month), int(day)).isoformat()


def getInformationFromEurlex(actId, act, eurlexUrl):
	"""
	FUNCTION
	get all the information of a given act from eurlex
	PARAMETERS
	actId: ids of the act
	act: information of the act
	eurlexUrl: link to the eurlex page
	RETURN
	act object which contains retrieved information
	"""
	dataDic={}
	#check if eurlex url exists

	if actId.fileEurlexUrlExists==True:
		#if yes, retrieve the information and pass it to an object

		html=eurlexIds.getEurlexUrlContent(eurlexUrl)
		dataDic=eurlex.getEurlexInformation(html)

		#store dictionary information variables into the model object
		act.__dict__.update(dataDic)
	else:
		print "No eurlex url"

	return act


def getInformationFromOeil(actId, act, oeilUrl):
	"""
	FUNCTION
	get all the information of a given act from oeil
	PARAMETERS
	actId: ids of the act
	act: information of the act
	eurlexUrl: link to the oeil page
	RETURN
	act object which contains retrieved information
	"""
	dataDic={}
	#check if oeil url exists

	if actId.fileOeilUrlExists==True:
		#if yes, retrieve the information and pass it to an object

		html=oeilIds.getOeilUrlContent(oeilUrl)
		#store all the fields useful for the act information retrieval in a dictionary
		tempDic=model_to_dict(actId, fields=["oeilNoUniqueType", "suite2eLecturePE"])
		dataDic=oeil.getOeilInformation(html, tempDic)

		if dataDic['oeilSignPECS']!=None:
			year, month, day=splitFrenchFormatDate(dataDic['oeilSignPECS'])
			dataDic['oeilSignPECS']=dateToIso(year, month, day)

		#store dictionary information variables into the model object
		act.__dict__.update(dataDic)
	else:
		print "No oeil url"

	return act


def getInformationFromPrelex(actId, act, prelexUrl):
	"""
	FUNCTION
	get all the information of a given act from prelex
	PARAMETERS
	actId: ids of the act
	act: information of the act
	prelexUrl: link to the prelex page
	RETURN
	act object which contains retrieved information
	"""
	dataDic={}
	#check if prelex url exists
	if actId.filePrelexUrlExists==True:
		#if yes, retrieve the information and pass it to an object
		html=prelexIds.getPrelexUrlContent(prelexUrl)
		#store all the fields useful for the act information retrieval in a dictionary
		tempDic=model_to_dict(actId, fields=["prelexProposOrigine", "prelexNoUniqueType", "proposSplittee", "suite2eLecturePE"])
		dataDic=prelex.getPrelexInformation(html, tempDic)

		if dataDic['prelexAdoptionProposOrigine']!=None:
			year, month, day=splitFrenchFormatDate(dataDic['prelexAdoptionProposOrigine'])
			dataDic['prelexAdoptionProposOrigine']=dateToIso(year, month, day)
		if dataDic['prelexTransmissionCouncil']!=None:
			year, month, day=splitFrenchFormatDate(dataDic['prelexTransmissionCouncil'])
			dataDic['prelexTransmissionCouncil']=dateToIso(year, month, day)
		if dataDic['prelexAdoptionConseil']!=None:
			year, month, day=splitFrenchFormatDate(dataDic['prelexAdoptionConseil'])
			dataDic['prelexAdoptionConseil']=dateToIso(year, month, day)

		#store dictionary information variables into the model object
		act.__dict__.update(dataDic)
	else:
		print "No prelex url"

	return act


def actsView(request):
	"""
	VIEW
	displays and processes the acts information retrieval page
	template called: actsInformationRetrieval/index.html
	"""
	responseDic={}
	#display "real" name of variables (not the one stored in db)
	responseDic['displayName']=vnIds.variablesNameDic
	responseDic['displayName'].update(vnInfo.variablesNameDic)
	state="display"

	if request.method == 'POST':
		print "post"
		actToValidate=request.POST.getlist('actsToValidate')[0]

		#if an act is selected
		if actToValidate!="":
			actId=ActsIdsModel.objects.get(id=actToValidate)
			act=ActsInformationModel.objects.get(actId_id=actToValidate)
			#saves the act
			if 'actsValidationSaveButton' in request.POST:
				print "save"
				#update europolix.actsInformationRetrieval_actsinformationmodel set validated=0;
				#delete from europolix.actsInformationRetrieval_actsinformationmodel;
				#delete from europolix.actsIdsValidation_actsidsmodel;
				#INSERT INTO europolix.actsInformationRetrieval_actsinformationmodel (actId_id) SELECT id FROM europolix.actsIdsValidation_actsidsmodel
				#SELECT * FROM europolix.actsInformationRetrieval_dgfullnamemodel fn, europolix.actsInformationRetrieval_dgcodemodel code where fn.dgCode_id=code.id;
				act.validated=True
				form = ActsInformationForm(request.POST, instance=act)
				if form.is_valid():
					print "form valid"
					form.save()
					del form
					#save notes
					actId.notes=request.POST.getlist('notes')[0]
					actId.save()
					state="saved"
					responseDic['success']="The act " + str(act.actId) + " has been validated!"
				else:
					print "form not valid", form.errors
					state="ongoing"

			#displays the retrieved information of the act to validate (selection of a act in the drop down list)
			if state!="saved":
				print 'actsToValidate display'
				#"compute" the url of the eurlex, oeil and prelex page
				urlDic={}
				urlDic["eurlexUrl"]=eurlexIds.getEurlexUrl(actId.fileNoCelex)
				urlDic["oeilUrl"]=oeilIds.getOeilUrl(str(actId.fileNoUniqueType), str(actId.fileNoUniqueAnnee), str(actId.fileNoUniqueChrono))
				urlDic["prelexUrl"]=actId.filePrelexUrl
				responseDic["url"]=urlDic
				#an act has been selected in the drop down list -> the related information are displayed
				if state=="display":
					act=getInformationFromEurlex(actId, act, urlDic["eurlexUrl"])
					act=getInformationFromOeil(actId, act, urlDic["oeilUrl"])
					act=getInformationFromPrelex(actId, act, urlDic["prelexUrl"])
					print "act", act
					form = ActsInformationForm(instance=act, initial={'actsToValidate': actToValidate})
					idForm=ActsIdsForm(instance=actId)
				#an error occured while validating the act -> display of these errors
				elif state=="ongoing":
					print "ongoing"
					form = ActsInformationForm(request.POST, instance=act, initial={'actsToValidate': actToValidate})
					idForm=ActsIdsForm(request.POST, instance=actId)

				responseDic['actId']=actId
				responseDic['act']=act
				responseDic['idForm']=idForm
				responseDic['form']=form

	#~ #if form has not been created yet -> unbound form
	if 'form' not in locals():
		print "ok"
		responseDic['idForm'] = ActsIdsForm()
		responseDic['form'] = ActsInformationForm()
		#~ print "responseDic['form']", responseDic['form']

	return render_to_response('actsInformationRetrieval/index.html', responseDic, context_instance=RequestContext(request))
