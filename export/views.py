# Create your views here.
#-*- coding: utf-8 -*-
import csv
from django.db.models.loading import get_model
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
#display drop down lists
from export.forms import ActsExportForm
#data to export coming from the two main models ActsIdsModel and ActsInformationModel
#~ from actsIdsValidation.models import ActsIdsModel
from actsInformationRetrieval.models import ActsInformationModel
#for the export
import os, tempfile, zipfile
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
import mimetypes
#change variable names (first row of the csv file)
import actsInformationRetrieval.variablesNameForInformation as vn

#redirect to login page if not logged
from django.contrib.auth.decorators import login_required


def fetchValidatedActsFunction(modelName):
	"""
	FUNCTION
	returns all the validated acts of the model
	PARAMETERS
	modelName: name of the model
	RETURNS
	query set
	"""
	return modelName.objects.filter(validated=1)


def sortQuerySetFunction(querySet, sortField, sortDirection):
	"""
	FUNCTION
	sorts a query set according to a sorting field and sort direction
	PARAMETERS
	querySet: query set for the sort
	sortingField: fields for the sort
	sortingDirection: direction of the sort (ascending or descending)
	RETURNS
	sorted query set
	"""
	direction=""
	if sortDirection=="descending":
		direction="-"

	return querySet.order_by(direction + sortField)


def querySetToCsvFile(qs, outfile_path):
	"""
	FUNCTION
	saves a query set in a csv file on the server
	PARAMETERS
	qs: query set
	outfile_path: path of the file to save
	RETURNS
	none
	SRC
	http://palewi.re/posts/2009/03/03/django-recipe-dump-your-queryset-out-as-a-csv-file/
	"""
	model = qs.model
	writer = csv.writer(open(outfile_path, 'w'))

	headers = []
	realHeaders=[]
	for field in model._meta.fields:
		if field.name!="actId" and field.name!="validated":
			headers.append(field.name)
			#display "real" variable names (first row)
			realHeaders.append(vn.variablesNameDic[field.name])
	writer.writerow(realHeaders)

	for obj in qs:
		row = []
		for field in headers:
			val = getattr(obj, field)
			if callable(val):
				val = val()
			if type(val) == unicode:
				val = val.encode("utf-8")
			row.append(val)
		writer.writerow(row)


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
	if request.method == 'POST':
		form = ActsExportForm(request.POST)
		if form.is_valid():
			#for key, value in request.POST.iteritems():
			sortingFields = request.POST['sortFields']
			sortingDirection = request.POST['sortDirection']
			#select all the validated acts from ActsInformationModel
			querySet=fetchValidatedActsFunction(ActsInformationModel)
			#~ .objects.select_related()
			querySet=sortQuerySetFunction(querySet, sortingFields, sortingDirection)
			serverDirectory = settings.MEDIA_ROOT+"export/"
			fileName="europeanActs.csv"
			#if a file with the same name already exists, we delete it
			if os.path.exists(serverDirectory+fileName):
				os.remove(serverDirectory+fileName)
			querySetToCsvFile(querySet, serverDirectory+fileName)
			return send_file(request, serverDirectory+fileName, fileName)
		else:
			return render_to_response('export/index.html', {'form': form}, context_instance=RequestContext(request))
	else:
		form = ActsExportForm()

	return render_to_response('export/index.html', {'form': form}, context_instance=RequestContext(request))
