#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from actsIdsValidation.forms import ActsIdsForm
from actsIdsValidation.models import ActsIdsModel
from actsInformationRetrieval.models import ActsInformationModel

#variables name
import variablesNameForIds as vn
#used to recreate and display the urls
import sys
from django.conf import settings
sys.path.append(settings.SITE_ROOT+'import')
import getEurlexIdsFunctions as eurlex
import getOeilIdsFunctions as oeil
import getPrelexIdsFunctions as prelex

#redirect to login page if not logged
from django.contrib.auth.decorators import login_required

def checkFieldError(form, field):
	"""
	FUNCTION
	check if a form field contains an error
	PARAMETERS
	form: form to ckeck
	field: name of the field to check
	RETURN
	true if no error false otherwise
	"""
	if field in form.errors:
		return False
	else:
		return True

@login_required
def actsView(request):
	"""
	VIEW
	displays and processes the acts validation page
	template called: actsIdsValidation/index.html
	"""
	import os
	test=os.path.join(os.path.dirname(os.getcwd()), "import/")
	print test
	responseDic={}
	#display "real" name of variables (not the one stored in db)
	responseDic['displayName']=vn.variablesNameDic
	state="display"

	if request.method == 'POST':
		actToValidate=request.POST.getlist('actsToValidate')[0]

		#if an act is selected
		if actToValidate!="":
			act=ActsIdsModel.objects.get(id=actToValidate)

			#saves the act
			if 'actsValidationSaveButton' in request.POST:
				print "save"
				#update europolix.actsIdsValidation_actsidsmodel set validated=0;
				#delete from europolix.actsIdsValidation_actsidsmodel;
				act.validated=True
				form = ActsIdsForm(request.POST, instance=act)

				if form.is_valid():
					print "form valid"
					form.save()
					#save the id of the validated act in the model which retrieves information on acts
					newAct=ActsInformationModel()
					newAct.actId=form.cleaned_data['actsToValidate']
					#~ print "actsToValidate", form.cleaned_data['actsToValidate']
					newAct.save()
					#~ print "new act", newAct.actId
					del form
					state="saved"
					responseDic['success']="The act releveAnnee=" + str(act.releveAnnee) + ", releveMois=" + str(act.releveMois) + ", noOrdre=" + str(act.noOrdre) + " has been validated!"
				else:
					print "form not valid", form.errors
					state="ongoing"

			#displays the retrieved information of the act to validate (selection of a act in the drop down list)
			if state!="saved":
				print 'actsToValidate display'
				#a act has been selected in the drop down list -> the related information are displayed
				if state=="display":
					form = ActsIdsForm(instance=act, initial={'actsToValidate': actToValidate, 'releveAnnee': act.releveAnnee, 'releveMois': act.releveMois, 'noOrdre': act.noOrdre})
				#an error occured while validating the act -> display of these errors
				elif state=="ongoing":
					print "ok"
					form = ActsIdsForm(request.POST, instance=act, initial={'actsToValidate': actToValidate, 'releveAnnee': act.releveAnnee, 'releveMois': act.releveMois, 'noOrdre': act.noOrdre})

				infoDic={}

				#check if the noCelex of the file exists in the list of nosCelex of prelex
				if act.prelexNosCelex!=None and act.fileNoCelex in act.prelexNosCelex:
					infoDic["nosCelex"]=True
				else:
					infoDic["nosCelex"]=False

				#checks if the corresponding data are equal
				if act.fileNoCelex==act.eurlexNoCelex and act.fileNoCelex==act.oeilNoCelex:
					infoDic["noCelex"]=True
				else:
					infoDic["noCelex"]=False

				if act.fileProposAnnee==act.eurlexProposAnnee and act.fileProposAnnee==act.oeilProposAnnee and act.fileProposAnnee==act.prelexProposAnnee:
					infoDic["proposAnnee"]=True
				else:
					infoDic["proposAnnee"]=False

				if act.fileProposChrono==act.eurlexProposChrono and act.fileProposChrono==act.oeilProposChrono and act.fileProposChrono==act.prelexProposChrono:
					infoDic["proposChrono"]=True
				else:
					infoDic["proposChrono"]=False

				if act.fileProposOrigine==act.eurlexProposOrigine and act.fileProposOrigine==act.oeilProposOrigine and act.fileProposOrigine==act.prelexProposOrigine:
					infoDic["proposOrigine"]=True
				else:
					infoDic["proposOrigine"]=False

				if act.fileNoUniqueAnnee==act.eurlexNoUniqueAnnee and act.fileNoUniqueAnnee==act.oeilNoUniqueAnnee and act.fileNoUniqueAnnee==act.prelexNoUniqueAnnee:
					infoDic["noUniqueAnnee"]=True
				else:
					infoDic["noUniqueAnnee"]=False

				if act.fileNoUniqueType==act.eurlexNoUniqueType and act.fileNoUniqueType==act.oeilNoUniqueType and act.fileNoUniqueType==act.prelexNoUniqueType:
					infoDic["noUniqueType"]=True
				else:
					infoDic["noUniqueType"]=False

				if act.fileNoUniqueChrono==act.eurlexNoUniqueChrono and act.fileNoUniqueChrono==act.oeilNoUniqueChrono and act.fileNoUniqueChrono==act.prelexNoUniqueChrono:
					infoDic["noUniqueChrono"]=True
				else:
					infoDic["noUniqueChrono"]=False

				if act.prelexDosId==act.fileDosId:
					infoDic["dosId"]=True
				else:
					infoDic["dosId"]=False

				#gets urls
				infoDic["eurlexUrl"]=eurlex.getEurlexUrl(act.fileNoCelex)
				infoDic["oeilUrl"]=oeil.getOeilUrl(str(act.fileNoUniqueType), str(act.fileNoUniqueAnnee), str(act.fileNoUniqueChrono))
				infoDic["prelexUrl"]=act.filePrelexUrl

				responseDic['form']=form
				responseDic['act']=act
				responseDic['info']=infoDic

	#~ #if form has not been created yet -> unbound form
	if 'form' not in locals():
		responseDic['form'] = ActsIdsForm()

	return render_to_response('actsIdsValidation/index.html', responseDic, context_instance=RequestContext(request))
