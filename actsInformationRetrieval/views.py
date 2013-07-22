#-*- coding: utf-8 -*-
from actsIdsValidation.models import ActsIdsModel
from actsIdsValidation.forms import ActsIdsForm
from actsInformationRetrieval.forms import ActsInformationForm, ActsAddForm, ActsModifForm
from actsInformationRetrieval.models import ActsInformationModel
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.forms.models import model_to_dict

#variables name
import actsIdsValidation.variablesNameForIds as vnIds
import variablesNameForInformation as vnInfo
#retrieve url contents
import sys
from django.conf import settings
#~ sys.path.append(settings.SITE_ROOT+'import')
import importApp.getEurlexIdsFunctions as eurlexIds
import importApp.getOeilIdsFunctions as oeilIds
import importApp.getPrelexIdsFunctions as prelexIds
#retrieve information
import getEurlexInformationFunctions as eurlex
import getOeilInformationFunctions as oeil
import getPrelexInformationFunctions as prelex

#get the addModif fct from the actsIdsValidation.views view
from actsIdsValidation.views import addOrModifFct

#redirect to login page if not logged
from django.contrib.auth.decorators import login_required


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
	eurlexUrlContent=eurlexIds.getEurlexUrlContent(eurlexUrl)
	#act doesn't exist, problem on page or problem with the Internet connection
	if eurlexUrlContent!=False:
		actId.fileEurlexUrlExists=True
		#if yes, retrieve the information and pass it to an object
		dataDic=eurlex.getEurlexInformation(eurlexUrlContent)
		#store dictionary information variables into the model object
		act.__dict__.update(dataDic)
	else:
		actId.fileEurlexUrlExists=False
		print "error while retrieving eurlex url"

	actId.save()

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
	oeilUrlContent=oeilIds.getOeilUrlContent(oeilUrl)
	#act doesn't exist, problem on page or problem with the Internet connection
	if oeilUrlContent!=False:
		actId.fileOeilUrlExists=True
		#if yes, retrieve the information and pass it to an object
		#store all the fields useful for the act information retrieval in a dictionary
		tempDic=model_to_dict(actId, fields=["oeilNoUniqueType", "suite2eLecturePE"])
		dataDic=oeil.getOeilInformation(oeilUrlContent, tempDic)
		#store dictionary information variables into the model object
		act.__dict__.update(dataDic)
	else:
		actId.fileOeilUrlExists=False
		print "error while retrieving oeil url"

	actId.save()

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
	prelexUrlContent=prelexIds.getPrelexUrlContent(prelexUrl)
	#act doesn't exist, problem on page or problem with the Internet connection
	if prelexUrlContent!=False:
		actId.filePrelexUrlExists=True
		#if yes, retrieve the information and pass it to an object
		#store all the fields useful for the act information retrieval in a dictionary
		tempDic=model_to_dict(actId, fields=["prelexProposOrigine", "prelexNoUniqueType", "proposSplittee", "suite2eLecturePE"])
		tempDic["signPECS"]=act.oeilSignPECS
		dataDic=prelex.getPrelexInformation(prelexUrlContent, tempDic)
		#store dictionary information variables into the model object
		act.__dict__.update(dataDic)
	else:
		actId.filePrelexUrlExists=False
		print "error while retrieving prelex url"

	actId.save()

	return act


@login_required
def actsView(request):
	"""
	VIEW
	displays and processes the acts information retrieval page
	template called: actsInformationRetrieval/index.html
	"""

	#SELECT * FROM europolix.actsInformationRetrieval_dgfullnamemodel fn, europolix.actsInformationRetrieval_dgcodemodel code where fn.dgCode_id=code.id;
	#update europolix.actsInformationRetrieval_actsinformationmodel set validated=0;

	responseDic={}
	#display "real" name of variables (names given by europolix team, not the names stored in db)
	responseDic['displayName']=vnIds.variablesNameDic
	responseDic['displayName'].update(vnInfo.variablesNameDic)
	state="display"

	if request.method == 'POST':

		#addOrModif=None, "add" or "modif"
		#act=act to validate / modify or None if no act is found (modifcation)
		#responseDic: add addForm or modifForm to the forms being displayed / to be displayed
		addOrModif, actId, responseDic=addOrModifFct(request.POST, responseDic, ActsAddForm, ActsModifForm)

		#if we are about to add or modif an act (the add or modif form is valid)
		if addOrModif!=None:
			print "addOrModif", addOrModif
			act=ActsInformationModel.objects.get(actId_id=actId.id)
			#saves the act
			if 'actsValidationSaveButton' in request.POST:
				print "save"
				act.validated=True
				form = ActsInformationForm(request.POST, instance=act)
				if form.is_valid():
					print "form valid"
					form.save()
					#save notes
					actId.notes=request.POST['notes']
					actId.save()
					state="saved"
					responseDic['success']="The act " + str(act.actId) + " has been validated!"
					del form
					if addOrModif=="modif":
						responseDic.pop("modifForm", None)
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
				#in ActsIdsValidation, if split proposition (ProposChrono has a dash)-> oeil ids to construct url
				#in ActsInformationRetrieval, if split proposition (ProposChrono has a dash)-> dosId to construct url
				if actId.fileDosId!=None and actId.fileProposChrono!=None and "-" in actId.fileProposChrono:
					urlDic["prelexUrl"]=prelexIds.getPrelexUrl(actId.fileDosId)
				else:
					#url saved in the database using the oeil ids in case of a split proposition
					urlDic["prelexUrl"]=actId.filePrelexUrl
				responseDic["url"]=urlDic
				#an act has been selected in the drop down list -> the related information are displayed
				if state=="display":
					if addOrModif=="add":
						act=getInformationFromEurlex(actId, act, urlDic["eurlexUrl"])
						act=getInformationFromOeil(actId, act, urlDic["oeilUrl"])
						act=getInformationFromPrelex(actId, act, urlDic["prelexUrl"])
						addForm=ActsAddForm(request.POST)
					else:
						modifForm=ActsModifForm(request.POST)
					form = ActsInformationForm(instance=act)
					idForm=ActsIdsForm(instance=actId)
				#an error occured while validating the act -> display of these errors
				elif state=="ongoing":
					print "ongoing"
					if addOrModif=="add":
						addForm=ActsAddForm(request.POST)
					else:
						modifForm=ActsModifForm(request.POST)
					form = ActsInformationForm(request.POST, instance=act)
					idForm=ActsIdsForm(request.POST, instance=actId)

				responseDic['actId']=actId
				responseDic['act']=act
				responseDic['idForm']=idForm
				responseDic['form']=form

	#~ #if form has not been created yet -> unbound form
	if 'form' not in locals():
		responseDic['idForm'] = ActsIdsForm()
		responseDic['form'] = ActsInformationForm()
	if 'addForm' not in responseDic:
		responseDic['addForm'] = ActsAddForm()
	if 'modifForm' not in responseDic:
		"modif form reinitialisation"
		responseDic['modifForm'] = ActsModifForm()

	return render_to_response('actsInformationRetrieval/index.html', responseDic, context_instance=RequestContext(request))
