#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
#use json for the ajax request
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import simplejson
#models
from act.models import PartyFamily
from act.get_data_prelex import format_resp_name
#forms
from forms import AddDG, AddResp
#variables names
import act.var_name_data as var_name_data


def init_response(field):
	"""
	FUNCTION
	initialize the response dictionary passed to the template
	PARAMETERS
	field: "dg" or "resp" [string]
	RETURN
	response: first variables of the dictionary containing all the variables to be displayed in th html form [dictionary]
	"""
	response={}
	response['display_name']=var_name_data.var_name
	#html page of the form
	response['form_template']='db_mgmt/form_add.html'
	response["var"]=field
	if field=="dg":
		response["model"]=AddDG
	elif field=="resp":
		response["model"]=AddResp

	return response


def add(request, field):
	"""
	VIEW
	processes the add of a DG or responsible
	PARAMETERS
	request: request Object [object]
	field: main field to add "dg" or "resp" [string]
	form: "AddDG" or "AddResp" [string]
	TEMPLATES:
	db_mgmt/add.html: display a form to add a dg or a responsible and theirs related fields
	"""
	response=init_response(field)

	if request.method=='POST':
		form=response["model"](request.POST)
		response["msg_class"]="error_msg"

		if form.is_valid():
			instance = form.save(commit=False)
			try:
				if response["var"]=="resp":
					instance.name=format_resp_name(instance.name)
					instance.src="resp"
					#save party family
					try:
						PartyFamily.objects.create(party=instance.party, country=instance.country, party_family=form.cleaned_data["party_family"])
					except Exception, e:
						print "party_family already exists", e

				instance.save(force_insert=True)
				response["msg_class"]="success_msg"
				msg="The "+var_name_data.var_name[response["var"]]+" has been saved. "
				if request.is_ajax():
					response["msg"]= msg+"You can now close the window and resume the validation of the act."
					#used to add the record in the drop down list
					if response["var"]=="resp":
						response["new_value"]=instance.name
					elif  response["var"]=="dg":
						response["new_value"]=instance.dg
					response["new_id"]=instance.pk

				else:
					response["msg"]=msg+"You can now close the tab, click on the update button next to the drop down list and select the value you just added."
			except Exception, e:
				print "exception", e
				response["msg"]="The "+var_name_data.var_name[response["var"]]+" already exists!"
		else:
			#display form errors
			if request.is_ajax():
				response["form_errors"]=dict([(k, form.error_class.as_text(v)) for k, v in form.errors.items()])
				response["msg"]=""
			else:
				response['form']=form

		if request.is_ajax():
			response.pop("model", None)
			return HttpResponse(simplejson.dumps(response), mimetype="application/json")

	#unbound forms
	if "form" not in response:
		response["form"]=response["model"]()

	#displays the page (GET) or POST if javascript disabled
	return render_to_response('db_mgmt/add.html', response, context_instance=RequestContext(request))


def form_add(request, field):
	"""
	VIEW
	display the form to add a dg / resp
	TEMPLATES
	'db_mgmt/form_add'
	"""
	response=init_response(field)
	response["form"]=response["model"]()
	return render_to_response(response['form_template'], response, context_instance=RequestContext(request))
