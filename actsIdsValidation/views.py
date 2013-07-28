#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
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


def addOrModifFct(post, responseDic, addFormName, modifFormName):
	"""
	FUNCTION
	check if the form is in any of add and modification mode
	PARAMETERS
	post: request.POST variable
	responseDic: dictionary containing all the different forms
	RETURN
	addOrModif (None if it's neither an add nor a modif form or pb on the form, "add" if the form is in adding mode and "modif" if the form is in modification mode)
	act: act to validate or modify
	responseDic: dictionary containing forms being used or to use
	"""
	addOrModif=act=None

	#adding of an act (validation of a new act)
	if post["actsToValidate"]!="" and "actsModificationFindButton" not in post:
		print "add mode"
		addForm=addFormName(post)
		responseDic['addForm']=addForm
		#if an act has been selected in the drop down list
		if addForm.is_valid():
			addOrModif="add"
			actToValidate=addForm.cleaned_data['actsToValidate']
			#acts validation
			try:
				actToValidateId=actToValidate.id
			#acts information retrieval
			except:
				actToValidateId=actToValidate.actId_id

			act=ActsIdsModel.objects.get(id=actToValidateId)
		#empty selection for the drop down list
		else:
			print "add form not valid", addForm.errors

	#modification of an act -> display
	elif "actsModificationFindButton" in post or post["releveAnneeModif"]!="":
		print "modification mode"
		modifForm = modifFormName(post)
		responseDic['modifForm']=modifForm
		if modifForm.is_valid():
			addOrModif="modif"
			print "modif form valid"
			#we display the act to modify it
			releveAnneeModif=modifForm.cleaned_data['releveAnneeModif']
			releveMoisModif=modifForm.cleaned_data['releveMoisModif']
			noOrdreModif=modifForm.cleaned_data['noOrdreModif']
			act=ActsIdsModel.objects.get(releveAnnee=releveAnneeModif, releveMois=releveMoisModif, noOrdre=noOrdreModif, validated=1)
		else:
			print "modif form not valid", modifForm.errors

	return addOrModif, act, responseDic


@login_required
def actsView(request):
	"""
	VIEW
	displays and processes the acts validation page
	template called: actsIdsValidation/index.html
	"""

	#update europolix.actsInformationRetrieval_actsinformationmodel set validated=0;
	#update europolix.actsIdsValidation_actsidsmodel set validated=0;
	#delete from europolix.actsInformationRetrieval_actsinformationmodel;
	#delete from europolix.actsIdsValidation_actsidsmodel;

	responseDic={}
	#display "real" name of variables (not the one stored in db)
	responseDic['displayName']=vn.variablesNameDic
	#state=display (display the ids of an act), saved (the act is being saved) or ongoing (validation errors while saving)
	state="display"

	if request.method == 'POST':

		#addOrModif=None, "add" or "modif"
		#act=act to validate / modify or None if no act is found (modifcation)
		#responseDic: add addForm or modifForm to the forms being displayed / to be displayed
		addOrModif, act, responseDic=addOrModifFct(request.POST, responseDic, ActsAddForm, ActsModifForm)

		#if we are about to add or modif an act (the add or modif form is valid)
		if addOrModif!=None:
			#saves the act
			if 'actsValidationSaveButton' in request.POST:
				print "save"
				act.validated=True
				form = ActsIdsForm(request.POST, instance=act)

				if form.is_valid():
					print "form valid"
					form.save()
					#save the id of the validated act in the model which retrieves information on acts
					newAct=ActsInformationModel()
					newAct.actId_id=act.id
					#~ print "actsToValidate", form.cleaned_data['actsToValidate']
					newAct.save()
					#~ print "new act", newAct.actId
					state="saved"
					#success message
					releveAnnee=vn.variablesNameDic['releveAnnee'] + "=" + str(act.releveAnnee)
					releveMois=vn.variablesNameDic['releveMois'] + "=" + str(act.releveMois)
					noOrdre=vn.variablesNameDic['noOrdre'] + "=" + str(act.noOrdre)
					responseDic['success']="The act " + releveAnnee + ", " + releveMois + ", " + noOrdre + " has been validated!"
					del form
				else:
					print "form not valid", form.errors
					state="ongoing"

			#if click on the actualisation button
			if 'actsValidationActualisationButton' in request.POST:
				print "actualisation"
				#news ids must be saved in the database
				form = ActsIdsForm(request.POST, instance=act)
				if form.is_valid():
					print "actualisation: form valid"
					form.save()
				#we retrieve and save the new ids (from the new urls)
				idsList=[]
				idsList.append((act.releveAnnee, act.releveMois, act.noOrdre))
				#actualisation button -> use acts ids retrieval from the import module
				importView.getAndSaveRetrievedIds(idsList)
				act=ActsIdsModel.objects.get(id=act.id)


			#displays the retrieved information of the act to validate (selection of a act in the drop down list)
			if state!="saved":
				print 'actsToValidate display'
				#an act has been selected in the drop down list -> the related information are displayed
				if state=="display":
					if addOrModif=="add":
						addForm=ActsAddForm(request.POST)
					else:
						modifForm=ActsModifForm(request.POST)
					form = ActsIdsForm(instance=act, initial={'releveAnnee': act.releveAnnee, 'releveMois': act.releveMois, 'noOrdre': act.noOrdre})
				#an error occured while validating the act -> display of these errors
				elif state=="ongoing":
					if addOrModif=="add":
						addForm=ActsAddForm(request.POST)
					else:
						modifForm=ActsModifForm(request.POST)
					form = ActsIdsForm(request.POST, instance=act, initial={'releveAnnee': act.releveAnnee, 'releveMois': act.releveMois, 'noOrdre': act.noOrdre})

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

				responseDic['form']=form
				responseDic['act']=act
				responseDic['info']=infoDic
				responseDic['addOrModif']=addOrModif


	#~ #if form has not been created yet -> unbound form
	if 'form' not in locals():
		responseDic['form'] = ActsIdsForm()
	if 'addForm' not in responseDic:
		responseDic['addForm'] = ActsAddForm()
	if 'modifForm' not in responseDic:
		responseDic['modifForm'] = ActsModifForm()


	return render_to_response('actsIdsValidation/index.html', responseDic, context_instance=RequestContext(request))
