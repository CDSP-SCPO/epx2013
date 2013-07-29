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
from importApp.getEurlexIdsFunctions import getEurlexUrl, getEurlexUrlContent
from importApp.getOeilIdsFunctions import getOeilUrl, getOeilUrlContent
from importApp.getPrelexIdsFunctions import getPrelexUrl, getPrelexUrlContent
#retrieve information
from getEurlexInformationFunctions import getEurlexInformation
from getOeilInformationFunctions import getOeilInformation
from getPrelexInformationFunctions import getPrelexInformation
from getOpalInfo import getOpalInfo
from getGvtCompoInfo import getGvtCompoInfo
from getRespProposInfo import getRespProposInfo

#get the addModif fct from the actsIdsValidation.views view
from actsIdsValidation.views import addOrModifFct

#redirect to login page if not logged
from django.contrib.auth.decorators import login_required

#check var is class
import inspect


def getInformation(src, actId, act, url, extraFieldsDic=None):
	"""
	FUNCTION
	get all the information of an act from a source in parameter
	PARAMETERS
	src: source (eurlex, oeil or prelex)
	actId: ids of the act
	act: information of the act
	url: link to the act page
	extraFieldsDic: dictionary of variables needed for the retrieving of data
	RETURN
	act object which contains retrieved information
	"""
	dataDic={}
	srcCap=src[0].upper()+src[1:]
	urlContent=eval("get"+srcCap+"UrlContent")(url)
	#act doesn't exist, problem on page or problem with the Internet connection
	if urlContent!=False:
		setattr(actId, "file"+srcCap+"UrlExists", True)
		#if yes, retrieve the information and pass it to an object
		dataDic=eval("get"+srcCap+"Information")(urlContent, extraFieldsDic)
		#store dictionary information variables into the model object
		act.__dict__.update(dataDic)
	else:
		setattr(actId, "file"+srcCap+"UrlExists", False)
		print "error while retrieving "+src+" url"

	#actualization url existence
	actId.save()

	return act


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
	return getInformation("eurlex", actId, act, eurlexUrl)


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
	extraFieldsDic=model_to_dict(actId, fields=["oeilNoUniqueType", "suite2eLecturePE"])
	return getInformation("oeil", actId, act, oeilUrl, extraFieldsDic)


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
	extraFieldsDic=model_to_dict(actId, fields=["releveAnnee", "releveMois", "noOrdre", "prelexProposOrigine", "prelexNoUniqueType", "proposSplittee", "suite2eLecturePE"])
	extraFieldsDic["signPECS"]=act.oeilSignPECS
	extraFieldsDic["fullCodeSectRep01"]=act.eurlexFullCodeSectRep01
	return getInformation("prelex", actId, act, prelexUrl, extraFieldsDic)


def getInformationFromOpal(actId, act):
	"""
	FUNCTION
	get all the information of a given act from opal
	PARAMETERS
	actId: ids of the act
	act: information of the act
	RETURN
	act object which contains retrieved information
	"""
	dataDic={}
	dataDic=getOpalInfo(actId.fileNoCelex)
	act.__dict__.update(dataDic)
	return act


def getGvtCompo(act):
	"""
	FUNCTION
	get all the information of a given act from GvtCompoModel
	PARAMETERS
	act: information of the act
	RETURN
	act object which contains retrieved information
	"""
	dataDic={}
	dataDic=getGvtCompoInfo(act)
	act.__dict__.update(dataDic)
	return act


def getRespProposRelatedData(resProposId):
	"""
	FUNCTION
	get the related data of RespPropos (from NationRespModel, NationalPartyRespModel, EUGroupRespModel)
	PARAMETERS
	resProposId: id of respPropos
	RETURN
	nationResp, nationalPartyResp and euGroupResp objects whith retrieved information
	"""
	nationResp, nationalPartyResp, euGroupResp=getRespProposInfo(resProposId)
	return nationResp, nationalPartyResp, euGroupResp


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
			act=ActsInformationModel.objects.get(actId_id=actId.id)
			#saves the act
			if 'actsValidationSaveButton' in request.POST:
				print "save"
				act.validated=True
				#~ act.prelexNationGvtPoliticalComposition=request.POST["prelexNationGvtPoliticalComposition"]
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
				urlDic["eurlexUrl"]=getEurlexUrl(actId.fileNoCelex)
				urlDic["oeilUrl"]=getOeilUrl(str(actId.fileNoUniqueType), str(actId.fileNoUniqueAnnee), str(actId.fileNoUniqueChrono))
				#in ActsIdsValidation, if split proposition (ProposChrono has a dash)-> oeil ids to construct url
				#in ActsInformationRetrieval, if split proposition (ProposChrono has a dash)-> dosId to construct url
				if actId.fileDosId!=None and actId.fileProposChrono!=None and "-" in actId.fileProposChrono:
					urlDic["prelexUrl"]=getPrelexUrl(actId.fileDosId)
				else:
					#url saved in the database using the oeil ids in case of a split proposition
					urlDic["prelexUrl"]=actId.filePrelexUrl
				responseDic["url"]=urlDic
				#an act has been selected in the drop down list -> the related information are displayed
				if state=="display":
					if addOrModif=="add":
						#retrieve all the information from all the sources
						act=getInformationFromEurlex(actId, act, urlDic["eurlexUrl"])
						act=getInformationFromOeil(actId, act, urlDic["oeilUrl"])
						act=getInformationFromPrelex(actId, act, urlDic["prelexUrl"])
						act=getInformationFromOpal(actId, act)
						addForm=ActsAddForm(request.POST)
					else:
						modifForm=ActsModifForm(request.POST)
					act=getGvtCompo(act)
					form = ActsInformationForm(instance=act)
					idForm=ActsIdsForm(instance=actId)
				#an error occured while validating the act -> display of these errors
				elif state=="ongoing":
					print "ongoing"
					if addOrModif=="add":
						addForm=ActsAddForm(request.POST)
					else:
						modifForm=ActsModifForm(request.POST)
					act=getGvtCompo(act)
					form = ActsInformationForm(request.POST, instance=act)
					idForm=ActsIdsForm(request.POST, instance=actId)

				#TEST ONLY -> to remove
				#~ from actsInformationRetrieval.models import RespProposModel
				#~ respPropos=RespProposModel.objects.get(id=2)
				#~ act.prelexRespProposId1_id=respPropos

				respProposId1=respProposId2=respProposId3=None
				respProposDic={}
				for index in xrange(1,4):
					index=str(index)
					respPropos=getattr(act, "prelexRespProposId"+index+"_id")
					respProposId=eval("respProposId"+index)
					#long
					if type(respPropos) is long:
						respProposId=respPropos
					#object
					elif respPropos!=None:
						respProposId=respPropos.id
					respProposDic["prelexNationResp"+index], respProposDic["prelexNationalPartyResp"+index], respProposDic["prelexEUGroupResp"+index]=getRespProposRelatedData(respProposId)


				responseDic['actId']=actId
				responseDic['act']=act
				responseDic['respPropos']=respProposDic
				responseDic['idForm']=idForm
				responseDic['form']=form
				#~ for gvtCompo in responseDic['act'].prelexNationGvtPoliticalComposition.all():
					#~ print "prelexNationGvtPoliticalComposition:", gvtCompo.id

	#~ #if form has not been created yet -> unbound form
	if 'form' not in locals():
		responseDic['idForm'] = ActsIdsForm()
		responseDic['form'] = ActsInformationForm()
		responseDic['respPropos']={}
	if 'addForm' not in responseDic:
		responseDic['addForm'] = ActsAddForm()
	if 'modifForm' not in responseDic:
		responseDic['modifForm'] = ActsModifForm()


	return render_to_response('actsInformationRetrieval/index.html', responseDic, context_instance=RequestContext(request))
