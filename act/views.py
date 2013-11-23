#-*- coding: utf-8 -*-
from act_ids.forms import ActIdsForm
from act.forms import ActForm, Add, Modif
from act.models import Act, DG, Person, NP, PartyFamily, Country, CodeSect
from import_app.models import ImportNP
from common.db import get_act_ids
#get the add_modif fct
from act_ids.views import add_modif_fct
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.models import model_to_dict
#variables name
import act_ids.var_name_ids as var_name_ids
import act.var_name_data as var_name_data
#retrieve url contents
from import_app.get_ids_eurlex import get_url_eurlex, get_url_content_eurlex
from import_app.get_ids_oeil import get_url_oeil, get_url_content_oeil
from import_app.get_ids_prelex import get_url_prelex, get_url_content_prelex
#retrieve data
from get_data_eurlex import get_data_eurlex
from get_data_oeil import get_data_oeil
from get_data_prelex import get_data_prelex
#redirect to login page if not logged
from django.contrib.auth.decorators import login_required
#use json for the ajax request
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import simplejson


def get_urls(act_ids, url_prelex, dos_id):
	"""
	FUNCTION
	get the eurlex, oeil and prelex urls
	PARAMETERS
	act_ids: ids of the act [ActIds model instance]
	url_prelex: url of prelex [string]
	dos_id: validated dos_id of the act or None if does not exist
	RETURN
	urls: urls of eurlex, oeil and prelex [dictionary of strings]
	"""
	urls={}
	urls["url_eurlex"]=get_url_eurlex(act_ids.no_celex)
	urls["url_oeil"]=get_url_oeil(str(act_ids.no_unique_type), str(act_ids.no_unique_annee), str(act_ids.no_unique_chrono))
	#for ids retrieval, if split proposition (ProposChrono has a dash)-> oeil ids to construct url
	#for data retrieval, if split proposition (ProposChrono has a dash)-> dos_id to construct url
	if "-" in act_ids.propos_chrono and dos_id!=None:
		urls["url_prelex"]=get_url_prelex(dos_id)
	else:
		#url saved in the database using the oeil ids in case of a split proposition
		urls["url_prelex"]=url_prelex

	return urls


def link_get_act_opal(act, act_ids):
	"""
	FUNCTION
	fill the table which links an act to its opal variables
	PARAMETERS
	act: instance of the act [Act model instance]
	act_ids: instance of the ids of the act [ActIds model instance]
	RETURN
	opal_dic: opal variables [dictionary]
	"""
	opal_dic={}

	#Are there matches in the ImportOpal table?
	opals=ImportNP.objects.defer("no_celex").filter(no_celex=act_ids.no_celex)

	for opal in opals:
		#store data
		country=opal.np
		#initialization
		if country not in opal_dic:
			opal_dic[country]={"act_type": "", "act_date": "", "case_nb": ""}
		opal_dic[country]["act_type"]+=opal.act_type+"; "
		opal_dic[country]["act_date"]+=str(opal.act_date)+"; "
		opal_dic[country]["case_nb"]+=str(opal.case_nb)+"; "

		try:
			#save opal instances
			fields={"case_nb": opal.case_nb, "np": Country.objects.get(pk=opal.np), "act_type": opal.act_type, "act_date": opal.act_date , "act": act}
			NP.objects.create(**fields)
		except Exception, e:
			print "opal varibles already saved!", e

	#remove last "; "
	for country in opal_dic:
		for field in opal_dic[country]:
			opal_dic[country][field]=opal_dic[country][field][:-2]

	return opal_dic


def get_party_family(resps):
	"""
	FUNCTION
	get the party family variable for each resp
	PARAMETERS
	resps: dictionary of responsibles [dictionary of Person model instances]
	RETURN
	party_family: dictionary of party_family variables for each responsible [dictionary of strings]
	"""
	for index in resps:
		if resps[index]!=None:
			#if id and not instance, get the instance instead
			if type(resps[index]) is long:
				resps[index]=Person.objects.get(pk=resps[index])
			resps[index]=PartyFamily.objects.get(party=resps[index].party, country=resps[index].country).party_family
		else:
			resps[index]=None
	return resps


def get_data(src, act_ids, url, act=None):
	"""
	FUNCTION
	get data of an act from a source in parameter
	PARAMETERS
	src: source (eurlex, oeil or prelex) [string]
	act_ids: ids of the act for a given source source [ActIds model instance]
	url: link to the act page [BeautifulSoup object]
	act: data of the act for prelex only [Act model instance]
	RETURN
	fields:  dictionary which contains retrieved data for a given source [dictionary]
	"""
	fields={}
	url_content=eval("get_url_content_"+src)(url)
	#act doesn't exist, problem on page or problem with the Internet connection
	if url_content!=False:
		#set the url_exists attribute of the given source to True
		print
		setattr(act_ids, "url_exists", True)
		#call the corresponding function to retrieve the data and pass it to an object
		fields=eval("get_data_"+src)(url_content, act_ids, act)
		#store dictionary data variables into the model object
		#~ for (key, value) in fields.items():
			#~ setattr(act_ids.act, key, value)
	else:
		setattr(act_ids, "url_exists", False)
		print "error while retrieving "+src+" url"

	#actualization url exist attribute
	act_ids.save()

	return fields


def check_multiple_dgs(act):
	"""
	FUNCTION
	check if act.dg_1 or act.dg_2 contains one or more dgs (if it's a DG with a number, there can be 2 or 3 possible DGs)
	assignate the first one to the corresponding act field and store all the possibilities in a dictionary (to be displayed in the template)
	PARAMETERS
	act: instance of the data of the act [Act model instance]
	RETURN
	dgs:  dictionary that contains all the possible dgs for each dg [dictionary of (lists of) DG model instances]
	act: updated instance of the data of the act [Act model instance]
	"""
	dgs={}
	for index in range(1,3):
		num=str(index)
		name="dg_"+num+"_id"
		instances=getattr(act, name)
		try:
			nb=instances.count()
			if nb>1:
				#store all the possible values to be displayed in the template
				dgs_temp=[dg.dg for dg in instances]
				dgs[num]=", ".join(dgs_temp)+"."
				#if many possible dgs, keep the first one only (to be displayed in the drop down list)
				setattr(act, name, instances[0])
		except Exception, e:
			print "dg is None", e
	print "dgs", dgs
	return dgs, act


def get_data_all(state, add_modif, act, POST, response):
	"""
	FUNCTION
	get all data of an act (from eurlex, oeil and prelex)
	PARAMETERS
	state: display (display the data of an act), saved (the act is being saved) or ongoing (validation errors while saving) [string]
	add_modif: "add" if the form is in add mode, "modif" otherwise [string]
	act: instance of the data of the act [Act model instance]
	POST: request.POST object [dictionary]
	response: variables to be displayed in the html form [dictionary]
	RETURN
	response: update of the variables to be displayed in the html form [dictionary]
	"""
	#retrieve the act ids for each source
	act_ids=get_act_ids(act)

	#"compute" the url of the eurlex, oeil and prelex page
	urls=get_urls(act_ids["index"], act.url_prelex, act_ids["index"].dos_id)

	#an act has been selected in the drop down list -> the related data is displayed
	#if state different of modif, save and ongoing and if the act is not being modified
	if state=="display" and add_modif=="add":
		print "data retrieval"
		#retrieve all the data from all the sources
		act.__dict__.update(get_data("eurlex", act_ids["eurlex"], urls["url_eurlex"], act))
		act.__dict__.update(get_data("oeil", act_ids["oeil"], urls["url_oeil"], act))
		#prelex config_cons needs eurlex, gvt_compo needs oeil
		act.__dict__.update(get_data("prelex", act_ids["prelex"], urls["url_prelex"], act))
		#check multiple values for dgs with numbers
		response["dg"], act=check_multiple_dgs(act)

	if "add_act" in POST or "modif_act" in POST:
		#~ act=get_foreign_key_fields(act)
		form_data=ActForm(instance=act)
	else:
		print "post", POST
		form_data=ActForm(POST, instance=act)

	print "typeof act.code_agenda_"
	response["urls"]=urls
	response['act']=act
	response['opals']=link_get_act_opal(act, act_ids["index"])
	response["party_family"]=get_party_family({"1": act.resp_1_id, "2": act.resp_2_id, "3": act.resp_3_id})
	response['act_ids']=act_ids
	response['form_data']=form_data

	return response


def save_act(act, request, response):
	"""
	FUNCTION
	get the data of an act
	PARAMETERS
	act: instance of the data of the act [model instance]
	request: request object [HttpRequest object]
	response: dictionary containing all the variables to be displayed in th html form [dictionary]
	RETURN
	response: update of the dictionary containing all the variables to be displayed in th html form [dictionary]
	state: saved or ongoing (if errors) [string]
	"""
	act.validated=2
	act.notes=request.POST['notes']
	form_data=ActForm(request.POST, instance=act)
	print "save"
	if form_data.is_valid():
		print "form_data valid"
		form_data.save()
		state="saved"
		response["msg"]="The act " + str(act) + " has been validated!"
		response["msg_class"]="success_msg"
	else:
		print "form_data not valid", form_data.errors
		if request.is_ajax():
			response['save_act_errors']= dict([(k, form_data.error_class.as_text(v)) for k, v in form_data.errors.items()])
		else:
			response['form_data']=form_data
		response["msg"]="The form contains errors! Please correct them before submitting again."
		response["msg_class"]="error_msg"
		state="ongoing"

	return response, state


def init_response():
	"""
	FUNCTION
	initialize the response dictionary passed to the template with list of variables and names to display
	PARAMETERS
	None
	RETURN
	response: first variables of the dictionary containing all the variables to be displayed in th html form [dictionary]
	"""
	response={}
	#display "real" name of variables (names given by europolix team, not the names stored in db)
	response['display_name']=var_name_ids.var_name
	response['display_name'].update(var_name_data.var_name)
	#one table (used to display one source) displays a subset of variables of the Act model only -> create list to loop over each subset
	response["vars_eurlex"]=["titre_en", "code_sect_1", "code_sect_2", "code_sect_3", "code_sect_4", "rep_en_1", "rep_en_2", "rep_en_3", "rep_en_4", "type_acte", "base_j"]
	response["vars_oeil"]=["commission", "com_amdt_tabled", "com_amdt_adopt", "amdt_tabled", "amdt_adopt", "votes_for_1", "votes_agst_1", "votes_abs_1", "votes_for_2", "votes_agst_2", "votes_abs_2", "rapp_1", "rapp_2", "rapp_3", "rapp_4", "rapp_5", "modif_propos", "nb_lectures", "sign_pecs"]
	response["vars_prelex_1"]=["adopt_propos_origine", "com_proc", "dg_1", "dg_2", "resp_1", "resp_2", "resp_3", "transm_council", "cons_b", "nb_point_b", "adopt_conseil", "nb_point_a", "council_a"]
	response["vars_prelex_2"]=["rejet_conseil", "chgt_base_j", "duree_adopt_trans", "duree_proc_depuis_prop_com", "duree_proc_depuis_trans_cons", "duree_tot_depuis_prop_com", "duree_tot_depuis_trans_cons", "vote_public", "adopt_cs_regle_vote", "adopt_cs_contre", "adopt_cs_abs", "adopt_pc_contre", "adopt_pc_abs", "adopt_ap_contre", "adopt_ap_abs", "dde_em", "split_propos", "proc_ecrite", "suite_2e_lecture_pe", "gvt_compo"]
	return response


@login_required
def act(request):
	"""
	VIEW
	displays and processes the acts data retrieval page
	TEMPLATES:
	act/index.html: display the act data page which itself calls the template of the act form
	act/form.html: display the act form
	"""
	#fill the dictionary sent to the template with the list of variables along with the names to display
	response=init_response()
	#state=display (display the data of an act), saved (the act is being saved) or ongoing (validation errors while saving)
	state="display"
	#html page of the form
	form_template='act/form.html'

	if request.method=='POST':
		#add_modif=None, "add" or "modif"
		#act=act to validate / modify or None if no act is found (modifcation)
		#response: add add or modif to the forms being displayed / to be displayed
		mode, add_modif, act, response=add_modif_fct(request, response, Add, Modif)

		#if any of this key is present in the response dictionary -> no act display and return the errors with a json object
		#otherwise display act and return the html form of the act to validate or modif in a string format
		keys=["msg", "add_act_errors", "modif_act_errors"]

		#if selection of an act in the drop down list or click on the modif_act button
		if mode!=None:
			#if we are about to add or modif an act (the add or modif form is valid)
			if add_modif!=None:
				#saves the act
				if 'save_act' in request.POST:
					response, state=save_act(act, request, response)

				#update person variables if the form is not saved
				if state!="saved":
					print "update"
					#~ state="update"

				#displays the retrieved data of the act to validate / modify
				#(selection of an act in the add / modif form  with no form error)
				#or errors when saving the form if ajax deactivated
				if not any(key in response for key in keys) or not request.is_ajax() and state!="saved":
					print 'act_to_validate display'
					#get the data of the act
					response=get_data_all(state, add_modif, act, request.POST, response)

				response['mode']=mode

			if request.is_ajax():
				#save act (with or without errors) or act display and modif (with errors)
				if any(key in response for key in keys):
					return HttpResponse(simplejson.dumps(response), mimetype="application/json")
				else:
					#act display or modif (without errors)
					return HttpResponse(render_to_string(form_template, response, RequestContext(request)))

		if request.is_ajax():
			#no act has been selected-> do nothing
			return HttpResponse(simplejson.dumps(""), mimetype="application/json")

	#unbound forms
	forms=[("form_data", ActForm()), ("add", Add()), ("modif", Modif())]
	for form in forms:
		if form[0] not in response or state=="saved":
			response[form[0]]=form[1]

	response['form_template']=form_template

	#displays the page (GET) or POST if javascript disabled
	return render_to_response('act/index.html', response, context_instance=RequestContext(request))


def reset_form(request):
	"""
	VIEW
	reset the act form (except add and modif)
	TEMPLATES
	act/form.html
	"""
	response=init_response()
	response['form_data']=ActForm()
	return render_to_response('act/form.html', response, context_instance=RequestContext(request))


def update_code_sect(request):
	"""
	VIEW
	update the code_agenda when a different code_sect is selected from the drop down list
	TEMPLATES
	None (Ajax only)
	"""
	response={}
	if request.POST["code_sect_id"]!="":
		instance=CodeSect.objects.get(pk=request.POST["code_sect_id"])
		response["code_agenda"]=instance.code_agenda.code_agenda
	else:
		response["code_agenda"]=None
	return HttpResponse(simplejson.dumps(response), mimetype="application/json")


def update_person(request):
	"""
	VIEW
	update the rapp (oeil) or resp (prelex) variables when a different person is selected from the drop down list
	TEMPLATES
	None (Ajax only)
	"""
	response={}
	if request.POST["person_id"]!="":
		instance=Person.objects.get(pk=request.POST["person_id"])
		response["country"]=instance.country.pk
		party=instance.party
		response["party"]=party.party
		if request.POST["src"]=="resp":
			response["party_family"]=PartyFamily.objects.only("party_family").get(party=party, country=response["country"]).party_family
	else:
		response["country"]=None
		response["party"]=None
		response["party_family"]=None

	return HttpResponse(simplejson.dumps(response), mimetype="application/json")


def update_dg(request):
	"""
	VIEW
	update the dg_sigle when a different dg is selected from the drop down list
	TEMPLATES
	None (Ajax only)
	"""
	response={}
	if request.POST["dg_id"]!="":
		instance=DG.objects.get(pk=request.POST["dg_id"])
		response["dg_sigle"]=instance.dg_sigle.dg_sigle
	else:
		response["dg_sigle"]=None
	return HttpResponse(simplejson.dumps(response), mimetype="application/json")
