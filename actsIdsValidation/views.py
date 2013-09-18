#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from actsIdsValidation.forms import ActsIdsForm, ActsAddForm, ActsModifForm
from actsIdsValidation.models import ActsIdsModel
from actsInformationRetrieval.models import ActsInformationModel

#variables name
import variablesNameForIds as vn
#used to recreate and display the urls
import sys
from django.conf import settings
#~ sys.path.append(settings.SITE_ROOT+'import')
import importApp.getEurlexIdsFunctions as eurlex
import importApp.getOeilIdsFunctions as oeil
import importApp.getPrelexIdsFunctions as prelex
import importApp.views as importView

#redirect to login page if not logged
from django.contrib.auth.decorators import login_required

#ajax
#use json for the ajax request
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import simplejson


def checkEqualityFields(fieldsList):
	"""
	FUNCTION
	check if fields of a list are all equal
	PARAMETERS
	fieldsList: list of the fields to check
	RETURN
	true if all the fields are equal, false otherwise
	"""
	for item in fieldsList:
		if fieldsList[0]!=item:
			return False
	return True


def addOrModifFct(post, response_dic, add_form_name, modif_form_name):
	"""
	FUNCTION
	check if the form is in any of add and modification mode
	PARAMETERS
	post: request.POST variable
	response_dic: dictionary containing all the different forms
	RETURN
	mode: "add" if selection of an act to add from the drop down list, "modif" if click on the modif_act button and None otherwise
	addOrModif: same than mode but returns None if the add or modif form is not valid
	act: act to validate or modify
	response_dic: dictionary containing forms being used or to use
	"""
	addOrModif=mode=act=None

	#adding of an act (validation of a new act)
	if post["actsToValidate"]!="" and "modif_act" not in post:
		print "add mode"
		mode="add"
		add_form=add_form_name(post)
		#if an act has been selected in the drop down list
		if add_form.is_valid():
			addOrModif="add"
			actToValidate=add_form.cleaned_data['actsToValidate']
			#get the primary key
			actToValidateId=actToValidate.pk
			act=ActsIdsModel.objects.get(id=actToValidateId)
		#empty selection for the drop down list
		else:
			response_dic['add_act_errors']=dict([(k, add_form.error_class.as_text(v)) for k, v in add_form.errors.items()])
			print "add form not valid", add_form.errors

	#modification of an act -> display
	elif "modif_act" in post or post["modif_button_clicked"]=="yes":
		print "modification mode"
		mode="modif"
		modif_form = modif_form_name(post)
		if modif_form.is_valid():
			addOrModif="modif"
			print "modif form valid"
			#we display the act to modify it
			releveAnneeModif=modif_form.cleaned_data['releveAnneeModif']
			releveMoisModif=modif_form.cleaned_data['releveMoisModif']
			noOrdreModif=modif_form.cleaned_data['noOrdreModif']
			act=ActsIdsModel.objects.get(releveAnnee=releveAnneeModif, releveMois=releveMoisModif, noOrdre=noOrdreModif, validated=1)
		else:
			response_dic['modif_act_errors']=dict([(k, modif_form.error_class.as_text(v)) for k, v in modif_form.errors.items()])
			print "modif form not valid", modif_form.errors

	return mode, addOrModif, act, response_dic


def act_ids(request):
	"""
	VIEW
	displays and processes the acts validation page
	template called: actsIdsValidation/index.html
	"""
	#update europolix.actsInformationRetrieval_actsinformationmodel set validated=0;
	#update europolix.actsIdsValidation_actsidsmodel set validated=0;
	#delete from europolix.actsInformationRetrieval_actsinformationmodel;
	#delete from europolix.actsIdsValidation_actsidsmodel;

	response_dic={}
	#display "real" name of variables (not the one stored in db)
	response_dic['displayName']=vn.variablesNameDic
	#state=display (display the ids of an act), saved (the act is being saved) or ongoing (validation errors while saving)
	state="display"
	#html page of the form
	form_template='actsIdsValidation/form.html'

	if request.method == 'POST':
		#mode: "add" if selection of an act to add from the drop down list, "modif" if click on the modif_act button and None otherwise
		#addOrModif: same than mode but returns None if the add or modif form is not valid
		#act=act to validate / modify or None if no act is found (modifcation)
		#response_dic: add add_form or modif_form to the forms being displayed / to be displayed
		mode, addOrModif, act, response_dic=addOrModifFct(request.POST, response_dic, ActsAddForm, ActsModifForm)
		ids_form = ActsIdsForm(request.POST, instance=act)

		#if any of this key is present in the response dictionary -> no "act validation display and return json object
		#otherwise display act and return the html form of the act to validate or update in a string format
		keys=["msg", "add_act_errors", "modif_act_errors", "update_act_errors"]

		#if selection of an act in the drop down list or click on the modif_act button
		if mode!=None:
			#~ #if we are about to add or modif an act (the add or modif form is valid)
			if addOrModif!=None:
				#saves the act
				if 'save_act' in request.POST:
					print "save"
					act.validated=True
					if ids_form.is_valid():
						print "ids_form valid"
						ids_form.save()
						#save the id of the validated act in the model which retrieves information on acts
						newAct=ActsInformationModel()
						newAct.actId_id=act.id
						newAct.save()
						state="saved"
						#success message
						releveAnnee=vn.variablesNameDic['releveAnnee'] + "=" + str(act.releveAnnee)
						releveMois=vn.variablesNameDic['releveMois'] + "=" + str(act.releveMois)
						noOrdre=vn.variablesNameDic['noOrdre'] + "=" + str(act.noOrdre)
						response_dic["msg"]="The act " + releveAnnee + ", " + releveMois + ", " + noOrdre + " has been validated!"
						response_dic["msg_class"]="success_msg"
					else:
						print "ids_form not valid", ids_form.errors
						response_dic['save_act_errors']=  dict([(k, ids_form.error_class.as_text(v)) for k, v in ids_form.errors.items()])
						response_dic["msg"]="The form contains errors! Please correct them before submitting the data."
						response_dic["msg_class"]="error_msg"
						state="ongoing"

				#if click on the actualisation button
				elif 'update_act' in request.POST:
					print "actualisation"
					#news ids must be saved in the database
					if ids_form.is_valid():
						print "actualisation: ids_form valid"
						ids_form.save()
						#we retrieve and save the new ids (from the new urls)
						idsList=[]
						idsList.append((act.releveAnnee, act.releveMois, act.noOrdre))
						#actualisation button -> use acts ids retrieval from the import module
						importView.getAndSaveRetrievedIds(idsList)
						act=ActsIdsModel.objects.get(id=act.id)
					else:
						print "ids_form not valid", ids_form.errors
						response_dic['update_act_errors']=  dict([(k, ids_form.error_class.as_text(v)) for k, v in ids_form.errors.items()])

				#displays the retrieved information of the act to validate
				#(selection of an act in the add / modif form or update of an act with no form error)
				if not any(key in response_dic for key in keys):
					print 'actsToValidate display'
					#an act has been selected in the drop down list -> the related information are displayed
					if state=="display":
						ids_form = ActsIdsForm(instance=act)

					infoDic={}

					#check if the noCelex of the file exists in the list of nosCelex of prelex
					if act.prelexNosCelex!=None and act.fileNoCelex in act.prelexNosCelex:
						infoDic["nosCelex"]=True
					else:
						infoDic["nosCelex"]=False

					#checks if the corresponding data are equal
					infoDic["noCelex"]=checkEqualityFields([act.fileNoCelex, act.eurlexNoCelex, act.oeilNoCelex])
					infoDic["proposAnnee"]=checkEqualityFields([act.fileProposAnnee, act.eurlexProposAnnee, act.oeilProposAnnee, act.prelexProposAnnee])
					infoDic["proposChrono"]=checkEqualityFields([act.fileProposChrono, act.eurlexProposChrono, act.oeilProposChrono, act.prelexProposChrono])
					infoDic["proposOrigine"]=checkEqualityFields([act.fileProposOrigine, act.eurlexProposOrigine, act.oeilProposOrigine, act.prelexProposOrigine])
					infoDic["noUniqueAnnee"]=checkEqualityFields([act.fileNoUniqueAnnee, act.eurlexNoUniqueAnnee, act.oeilNoUniqueAnnee, act.prelexNoUniqueAnnee])
					infoDic["noUniqueType"]=checkEqualityFields([act.fileNoUniqueType, act.eurlexNoUniqueType, act.oeilNoUniqueType, act.prelexNoUniqueType])
					infoDic["noUniqueChrono"]=checkEqualityFields([act.fileNoUniqueChrono, act.eurlexNoUniqueChrono, act.oeilNoUniqueChrono, act.prelexNoUniqueChrono])
					infoDic["dosId"]=checkEqualityFields([act.prelexDosId, act.fileDosId])

					#gets urls
					infoDic["eurlexUrl"]=eurlex.getEurlexUrl(act.fileNoCelex)
					infoDic["oeilUrl"]=oeil.getOeilUrl(str(act.fileNoUniqueType), str(act.fileNoUniqueAnnee), str(act.fileNoUniqueChrono))
					infoDic["prelexUrl"]=act.filePrelexUrl

					response_dic['ids_form']=ids_form
					response_dic['act']=act
					response_dic['info']=infoDic
					response_dic['addOrModif']=addOrModif

				response_dic['mode']=mode

			#save act (with or without errors) or act display, modif and update (with errors)
			if any(key in response_dic for key in keys):
				print "1"
				return HttpResponse(simplejson.dumps(response_dic), mimetype="application/json")
			else:
				#act display, modif and update (without errors)
				print "2"
				return HttpResponse(render_to_string(form_template, response_dic, RequestContext(request)))

		#no act has been selected-> do nothing
		return HttpResponse(simplejson.dumps(""), mimetype="application/json")


	#GET
	#unbound ids_form
	response_dic['ids_form'] = ActsIdsForm()
	response_dic['add_form'] = ActsAddForm()
	response_dic['modif_form'] = ActsModifForm()
	response_dic['form_template'] = form_template
	return render_to_response('actsIdsValidation/index.html', response_dic, context_instance=RequestContext(request))


def reset_form(request):
	"""
	VIEW
	reset the act_ids form (except add and modif_form)
	template called: 'actsIdsValidation/form.html'
	"""
	response_dic={}
	#display "real" name of variables (not the one stored in db)
	response_dic['displayName']=vn.variablesNameDic
	response_dic['ids_form'] = ActsIdsForm()
	return render_to_response('actsIdsValidation/form.html', response_dic, context_instance=RequestContext(request))
