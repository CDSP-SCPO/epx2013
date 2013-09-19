#-*- coding: utf-8 -*-
from actsIdsValidation.models import ActsIdsModel
from actsIdsValidation.forms import ActsIdsForm
from actsInformationRetrieval.forms import ActsInformationForm, ActsAddForm, ActsModifForm
from actsInformationRetrieval.models import ActsInformationModel, RespProposModel
#get the addModif fct from the actsIdsValidation.views view
from actsIdsValidation.views import addOrModifFct
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.models import model_to_dict

#variables name
import actsIdsValidation.variablesNameForIds as vnIds
import variablesNameForInformation as vnInfo

#retrieve url contents
from importApp.getEurlexIdsFunctions import getEurlexUrl, getEurlexUrlContent
from importApp.getOeilIdsFunctions import getOeilUrl, getOeilUrlContent
from importApp.getPrelexIdsFunctions import getPrelexUrl, getPrelexUrlContent

#retrieve information
from getEurlexInformationFunctions import getEurlexInformation
from getOeilInformationFunctions import getOeilInformation
from getPrelexInformationFunctions import getPrelexInformation
from getOpalInfo import getOpalInfo
from getGvtCompoInfo import getGvtCompoInfo, getAssocVariables
from getRespProposInfo import getRespProposInfo

#redirect to login page if not logged
from django.contrib.auth.decorators import login_required

#use json for the ajax request
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import simplejson


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
	extraFieldsDic=model_to_dict(actId, fields=["releveAnnee", "releveMois", "noOrdre", "prelexProposOrigine", "prelexNoUniqueType", "proposSplittee", "suite2eLecturePE", "adoptCSRegleVote", "adoptCSAbs", "adoptCSContre"])
	extraFieldsDic["signPECS"]=act.oeilSignPECS
	extraFieldsDic["fullCodeSectRep01"]=act.eurlexFullCodeSectRep01
	return getInformation("prelex", actId, act, prelexUrl, extraFieldsDic)


def getInformationFromOpal(noCelex):
	"""
	FUNCTION
	get all the information of a given act from opal
	PARAMETERS
	noCelex: no celex of the act
	act: information of the act
	RETURN
	act object which contains retrieved information
	"""
	opal=getOpalInfo(noCelex)
	return opal


def getGvtCompo(act):
	"""
	FUNCTION
	get all the information of a given act from GvtCompoModel
	PARAMETERS
	act: information of the act
	RETURN
	string which contains retrieved information
	"""
	gvt_compo=getGvtCompoInfo(act)
	return gvt_compo


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
def act_info(request):
	"""
	VIEW
	displays and processes the acts information retrieval page
	template called: actsInformationRetrieval/index.html
	"""
	#SELECT * FROM europolix.actsInformationRetrieval_dgfullnamemodel fn, europolix.actsInformationRetrieval_dgcodemodel code where fn.dgCode_id=code.id;
	#update europolix.actsInformationRetrieval_actsinformationmodel set validated=0;

	response_dic={}
	gvt_compo=opal=""
	#display "real" name of variables (names given by europolix team, not the names stored in db)
	response_dic['displayName']=vnIds.variablesNameDic
	response_dic['displayName'].update(vnInfo.variablesNameDic)
	#state=display (display the info of an act), saved (the act is being saved) or ongoing (validation errors while saving)
	state="display"
	#html page of the form
	form_template='actsInformationRetrieval/form.html'

	if request.method == 'POST':
		#addOrModif=None, "add" or "modif"
		#act=act to validate / modify or None if no act is found (modifcation)
		#response_dic: add add_form or modif_form to the forms being displayed / to be displayed
		mode, addOrModif, actId, response_dic=addOrModifFct(request.POST, response_dic, ActsAddForm, ActsModifForm)

		#if any of this key is present in the response dictionary -> no act display and return the errors with a json object
		#otherwise display act and return the html form of the act to validate or modif in a string format
		keys=["msg", "add_act_errors", "modif_act_errors"]

		#if selection of an act in the drop down list or click on the modif_act button
		if mode!=None:
			#if we are about to add or modif an act (the add or modif form is valid)
			if addOrModif!=None:
				act=ActsInformationModel.objects.get(actId_id=actId.id)
				info_form = ActsInformationForm(request.POST, instance=act)
				#saves the act
				if 'save_act' in request.POST:
					print "save"
					act.validated=True
					if info_form.is_valid():
						print "info_form valid"
						info_form.save()
						#save notes
						actId.notes=request.POST['notes']
						actId.save()
						state="saved"
						response_dic["msg"]="The act " + str(act.actId) + " has been validated!"
						response_dic["msg_class"]="success_msg"
					else:
						print "info_form not valid", info_form.errors
						response_dic['save_act_errors']=  dict([(k, info_form.error_class.as_text(v)) for k, v in info_form.errors.items()])
						response_dic["msg"]="The form contains errors! Please correct them before submitting the data."
						response_dic["msg_class"]="error_msg"
						state="ongoing"

				#displays the retrieved information of the act to validate (selection of an act in the drop down list or click modif button)
				#(selection of an act in the add / modif form  with no form error)
				if not any(key in response_dic for key in keys):
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
					response_dic["url"]=urlDic
					#an act has been selected in the drop down list (or modification of an act) -> the related information is displayed
					if state=="display":
						if addOrModif=="add":
							print "info retrieval"
							#retrieve all the information from all the sources
							#~ act=getInformationFromEurlex(actId, act, urlDic["eurlexUrl"])
							#~ act=getInformationFromOeil(actId, act, urlDic["oeilUrl"])
							#prelex configCons needs eurlex
							act=getInformationFromPrelex(actId, act, urlDic["prelexUrl"])
						info_form = ActsInformationForm(instance=act)
						ids_form=ActsIdsForm(instance=actId)

					#~ opal=getInformationFromOpal(actId.fileNoCelex)
					#need oeil and prelex
					#~ gvt_compo=getGvtCompo(act)
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

					response_dic['actId']=actId
					response_dic['act']=act
					response_dic['respPropos']=respProposDic
					response_dic['gvt_compo']=gvt_compo
					response_dic['opal']=opal
					response_dic['ids_form']=ids_form
					response_dic['info_form']=info_form

				response_dic['mode']=mode

			#save act (with or without errors) or act display and modif (with errors)
			if any(key in response_dic for key in keys):
				return HttpResponse(simplejson.dumps(response_dic), mimetype="application/json")
			else:
				#act display or modif (without errors)
				return HttpResponse(render_to_string(form_template, response_dic, RequestContext(request)))

		#no act has been selected-> do nothing
		return HttpResponse(simplejson.dumps(""), mimetype="application/json")

	#GET
	#unbound forms
	response_dic['ids_form'] = ActsIdsForm()
	response_dic['info_form'] = ActsInformationForm()
	response_dic['respPropos']={}
	response_dic['add_form'] = ActsAddForm()
	response_dic['modif_form'] = ActsModifForm()
	response_dic['form_template'] = form_template


	return render_to_response('actsInformationRetrieval/index.html', response_dic, context_instance=RequestContext(request))


def reset_form(request):
	"""
	VIEW
	reset the act_info form (except add and modif_form)
	template called: 'actsInformationRetrieval/form.html'
	"""
	response_dic={}
	#display "real" name of variables (not the one stored in db)
	response_dic['displayName']=vnIds.variablesNameDic
	response_dic['displayName'].update(vnInfo.variablesNameDic)
	response_dic['ids_form'] = ActsIdsForm()
	response_dic['info_form'] = ActsInformationForm()
	return render_to_response('actsInformationRetrieval/form.html', response_dic, context_instance=RequestContext(request))


def update_respPropos(request):
	"""
	VIEW
	update the respPropos variables when a different respPropos is selected from the drop down list
	"""
	response_dic={}
	respPropos_id=request.POST["respPropos_id"]
	response_dic["nationResp"], response_dic["nationalPartyResp"], response_dic["euGroupResp"]=getRespProposInfo(respPropos_id)

	return HttpResponse(simplejson.dumps(response_dic), mimetype="application/json")
