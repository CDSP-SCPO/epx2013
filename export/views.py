# Create your views here.
#-*- coding: utf-8 -*-
import csv
from django.db.models.loading import get_model
from django.conf import settings
from django.shortcuts import render, render_to_response
from django.template import RequestContext
#display drop down lists
from export.forms import ActsExportForm
#data to export coming from the two main models ActsIdsModel and ActsInformationModel
from actsIdsValidation.models import ActsIdsModel
from actsInformationRetrieval.models import ActsInformationModel
#for the export
import os, tempfile, zipfile
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
import mimetypes
#change variable names (first row of the csv file)
import actsIdsValidation.variablesNameForIds as vnIds
import actsInformationRetrieval.variablesNameForInformation as vnInfo

#redirect to login page if not logged
from django.contrib.auth.decorators import login_required

#use json for the ajax request
from django.utils import simplejson
from django.http import HttpResponse


def getHeaders(act_ids_exclude_list, act_info_exclude_list):
	"""
	FUNCTION
	returns the headers for the fields too export acts of the model
	PARAMETERS
	act_ids_exclude_list: list of fields not to be exported (ActsIdsModel)
	act_info_exclude_list:  list of fields not to be exported (ActsInformationModel)
	RETURNS
	list of headers
	"""
	headers_list=[]
	#ActsIdsModel
	for field in ActsIdsModel()._meta.fields:
		if field.name not in act_ids_exclude_list:
			headers_list.append(vnIds.variablesNameDic[field.name])

	#ActsInformationModel
	for field in ActsInformationModel()._meta.fields:
		if field.name not in act_info_exclude_list:
			headers_list.append(vnInfo.variablesNameDic[field.name])

	#NPModel (gvtCompo)
	headers_list.append(vnInfo.variablesNameDic["prelexNationGvtPoliticalComposition"])

	#RespProposModel and related
	for index in xrange(1, 4):
		index=str(index)
		headers_list.append(vnInfo.variablesNameDic["prelexRespProposId"+index])
		headers_list.append(vnInfo.variablesNameDic["prelexNationResp"+index])
		headers_list.append(vnInfo.variablesNameDic["prelexNationalPartyResp"+index])
		headers_list.append(vnInfo.variablesNameDic["prelexEUGroupResp"+index])

	return headers_list



def fetchValidatedActs(act_ids_exclude_list, act_info_exclude_list):
	"""
	FUNCTION
	returns all the validated acts of the model
	PARAMETERS
	act_ids_exclude_list: list of fields not to be exported (ActsIdsModel)
	act_info_exclude_list:  list of fields not to be exported (ActsInformationModel)
	RETURNS
	list of lists of acts
	"""
	db_queryset=ActsInformationModel.objects.filter(validated = 1).prefetch_related('prelexNationGvtPoliticalComposition')
	#list of lists of acts
	acts_list=[]

	for act in db_queryset.iterator():
		#list of values for one act
		act_list=[]
		#ActsIdsModel
		for field in act.actId.__class__._meta.fields:
			if field.name not in act_ids_exclude_list:
				act_list.append(getattr(act.actId, field.name))

		#ActsInformationModel
		for field in ActsInformationModel()._meta.fields:
			if field.name not in act_info_exclude_list:
				act_list.append(getattr(act, field.name))

		#NPModel (gvtCompo)
		gvt_compo=""
		for gvtCompo in act.prelexNationGvtPoliticalComposition.all():
			gvt_compo+=gvtCompo.nationGvtPoliticalComposition+"; "
		#delete last "; "
		act_list.append(gvt_compo[:-2])

		#RespProposModel (3 respPropos)
		for index in xrange(1,4):
			index=str(index)
			try:
				act_list.append(getattr(act, "prelexRespProposId"+index).respPropos)
				act_list.append(getattr(act, "prelexRespProposId"+index).nationResp.nationResp)
				act_list.append(getattr(act, "prelexRespProposId"+index).euGroupResp.euGroupResp)
			except Exception, e:
				print "exception", e

		acts_list.append(act_list)

	return acts_list


def sort_acts(list_of_lists, sort_field_index, sort_direction):
	"""
	FUNCTION
	sorts a query set according to a sorting field and sort direction
	PARAMETERS
	list_of_lists: list of lists of acts to sort
	sort_field_index: index of the field to use for the sort
	sort_direction: direction of the sort (ascending or descending)
	RETURNS
	sorted query set
	"""
	if sort_direction=="ascending":
		list_of_lists.sort(key = lambda row: row[sort_field_index])
	else:
		list_of_lists.sort(key = lambda row: row[sort_field_index], reverse=True)
	return list_of_lists


def querySetToCsvFile(headers_list, acts_list, outfile_path):
	"""
	FUNCTION
	saves a query set in a csv file on the server
	PARAMETERS
	headers_list: list of headers
	acts_list: list of acts
	outfile_path: path of the file to save
	RETURNS
	none
	"""
	writer = csv.writer(open(outfile_path, 'w'))

	#write headers
	writer.writerow(headers_list)

	#write every acts in the db
	for act in acts_list:
		writer.writerow(act)


def send_file(request, serverFileName, clientFileName):
	"""
	FUNCTION
	downloads a file from the server
	PARAMETERS
	request: html request
	RETURNS
	response: html response
	SRC
	http://stackoverflow.com/questions/1930983/django-download-csv-file-using-a-link
	"""
	wrapper      = FileWrapper(open(serverFileName))
	content_type = mimetypes.guess_type(serverFileName)[0]
	response     = HttpResponse(wrapper,content_type=content_type)
	response['Content-Length']      = os.path.getsize(serverFileName)
	response['Content-Disposition'] = "attachment; filename=%s"%clientFileName
	return response


@login_required
def exportView(request):
	"""
	VIEW
	displays the export page -> export all the acts in the db regarding the sorting variable
	template called: export/index.html
	"""
	response_dic={}
	if request.method == 'POST':
		form = ActsExportForm(request.POST)
		if form.is_valid():
			#for key, value in request.POST.iteritems():
			sort_field = request.POST['sortFields']
			sort_direction = request.POST['sortDirection']
			serverDirectory = settings.MEDIA_ROOT+"/export/"
			fileName="europeanActs.csv"
			#if a file with the same name already exists, we delete it
			if os.path.exists(serverDirectory+fileName):
				os.remove(serverDirectory+fileName)
			#get the headers
			act_ids_exclude_list=["id", "filePrelexUrl", "validated"]
			act_info_exclude_list=["id", "actId", "prelexRespProposId1", "prelexRespProposId2", "prelexRespProposId3", "validated"]
			headers_list=getHeaders(act_ids_exclude_list, act_info_exclude_list)
			#fetch every acts in the db
			acts_list=fetchValidatedActs(act_ids_exclude_list, act_info_exclude_list)
			sort_field_index=headers_list.index(vnInfo.variablesNameDic[sort_field])
			#sort the acts
			acts_list=sort_acts(acts_list, sort_field_index, sort_direction)
			#save into csv file
			querySetToCsvFile(headers_list, acts_list, serverDirectory+fileName)
			print "csv export"
			return send_file(request, serverDirectory+fileName, fileName)
		else:
			if 'iframe' in request.POST:
				response_dic['form_errors']=  dict([(k, form.error_class.as_text(v)) for k, v in form.errors.items()])
				return HttpResponse(simplejson.dumps(response_dic), mimetype="application/json")
			else:
				response_dic['form']=form
	#GET
	else:
		#fill the hidden input field with the number of acts to export
		response_dic["acts_nb"]=ActsInformationModel.objects.filter(validated = 1).count()

	#unbound forms
	if "form" not in response_dic:
		response_dic['form']= ActsExportForm()

	#displays the page (GET) or POST if javascript disabled
	return render_to_response('export/index.html', response_dic, context_instance=RequestContext(request))
