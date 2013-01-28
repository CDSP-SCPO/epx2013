#-*- coding: utf-8 -*-
from actsIdsValidation.models import ActsIdsModel
from actsIdsValidation.forms import ActsIdsForm
from actsInformationRetrieval.forms import ActsInformationForm
from actsInformationRetrieval.models import ActsInformationModel
from datetime import date
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
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


def splitPrelexDate(dateString):
	"""
	FUNCTION
	split a prelex date ('DD-MM-YYYY') into year, month and day
	PARAMETERS
	dateString: prelex date to split
	RETURN
	year, month and day of the prelex date
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


def getInformationFromPrelex(actIdVar):
	"""
	FUNCTION
	get information of a given act from prelex
	PARAMETERS
	actIdVar: id of the act
	RETURN
	actId object which contains prelex ids and act object which contains retrieved information
	"""
	dataDic={}
	#check if prelex url exists
	actId=ActsIdsModel.objects.get(id=actIdVar)
	
	if actId.filePrelexUrlExists==True:
		#if yes, retrieve the information and pass it to an object
		act=ActsInformationModel.objects.get(actId=actIdVar)
		url=actId.prelexUrl
		html=prelexIds.getPrelexUrlContent(url)
		#store all the fields useful for the act information retrieval in a dictionary
		from django.forms.models import model_to_dict
		tempDic=model_to_dict(actId, fields=["prelexProposOrigine", "prelexNoUniqueType", "proposSplittee", "suite2eLecturePE"])
		dataDic=prelex.getPrelexInformation(html, tempDic)
		
		year, month, day=splitPrelexDate(dataDic['adoptionProposOrigine'])
		act.adoptionProposOrigine=dateToIso(year, month, day)
		act.comProc=dataDic['comProc']
		act.dgProposition=dataDic['dgProposition']
		act.respPropos1=dataDic['respPropos1']
		year, month, day=splitPrelexDate(dataDic['transmissionCouncil'])
		act.nbPointB=dataDic['nbPointB']
		act.consB=dataDic['consB']
		act.transmissionCouncil=dateToIso(year, month, day)
		year, month, day=splitPrelexDate(dataDic['adoptionConseil'])
		act.adoptionConseil=dateToIso(year, month, day)
		act.nbPointA=dataDic['nbPointA']
		act.councilA=dataDic['councilA']
		act.nbLectures=dataDic['nbLectures']
	else:
		print "No prelex url"
		act=None
	
	return actId, act


def actsView(request):
	"""
	VIEW
	displays and processes the acts information retrieval page
	template called: actsInformationRetrieval/index.html
	"""
	responseDic={}
	state="display"
	if request.method == 'POST':
		print "post"
		actToValidate=request.POST.getlist('actsToValidate')[0]
		
		#if an act is selected
		if actToValidate!="":
			#saves the act
			if 'actsValidationSaveButton' in request.POST:
				print "save"
				#update europolix.actsInformationRetrieval_actsinformationmodel set validated=0;
				#delete from europolix.actsInformationRetrieval_actsinformationmodel;
				#delete from europolix.actsIdsValidation_actsidsmodel;
				#~ INSERT INTO europolix.actsInformationRetrieval_actsinformationmodel (actId_id) SELECT id FROM europolix.actsIdsValidation_actsidsmodel
				act=ActsInformationModel.objects.get(actId=actToValidate)
				act.validated=True
				form = ActsInformationForm(request.POST, instance=act)

				if form.is_valid():
					print "form valid"
					form.save()
					del form
					#save notes
					actId=ActsIdsModel.objects.get(id=actToValidate)
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
				#a act has been selected in the drop down list -> the related information are displayed
				if state=="display":
					actId, act=getInformationFromPrelex(actToValidate)
					print "act", act
					urlDic={}
					urlDic["eurlexUrl"]=eurlexIds.getEurlexUrl(actId.fileNoCelex)
					urlDic["oeilUrl"]=oeilIds.getOeilUrl(str(actId.fileNoUniqueType), str(actId.fileNoUniqueAnnee), str(actId.fileNoUniqueChrono))
					urlDic["prelexUrl"]=actId.prelexUrl
					form = ActsInformationForm(instance=act, initial={'actsToValidate': actToValidate})
					idForm=ActsIdsForm(instance=actId)
				#an error occured while validating the act -> display of these errors
				elif state=="ongoing":
					print "ongoing"
					form = ActsInformationForm(request.POST, instance=act, initial={'actsToValidate': actToValidate})
					idForm=ActsIdsForm(request.POST, instance=actId)
				
				responseDic['actId']=actId
				responseDic['act']=act
				responseDic["url"]=urlDic
				responseDic['form']=form
				responseDic['idForm']=idForm
		
	#~ #if form has not been created yet -> unbound form
	if 'form' not in locals():
		print "ok"
		responseDic['idForm'] = ActsIdsForm()
		responseDic['form'] = ActsInformationForm()
		#~ print "responseDic['form']", responseDic['form']
	
	return render_to_response('actsInformationRetrieval/index.html', responseDic, context_instance=RequestContext(request))
