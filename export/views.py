# Create your views here.
#-*- coding: utf-8 -*-
import csv 
from django.db.models.loading import get_model
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from export.forms import ActsExportForm
from export.models import ActsExportDb
import os


def fetchDataInTableFunction(modelName):
	"""
	FUNCTION
	returns all the records of a model
	PARAMETERS
	modelName: name of the model
	RETURNS
	query set
	"""
	return modelName.objects.all()


def sortingQuerySetFunction(querySet, sortingField, sortingDirection):
	"""
	FUNCTION
	sorts a query set according to a sorting field and sorting direction
	PARAMETERS
	querySet: query set for the sorting
	sortingField: fields for the sorting
	sortingDirection: direction of the sorting (ascending or descending)
	RETURNS
	sorted query set
	"""
	direction=""
	if sortingDirection=="descending":
		direction="-"
	
	return querySet.order_by(direction + sortingField)


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
	for field in model._meta.fields:
		headers.append(field.name)
	writer.writerow(headers)
	
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
	import os, tempfile, zipfile
	from django.core.servers.basehttp import FileWrapper
	from django.conf import settings
	import mimetypes

	wrapper      = FileWrapper(open(serverFileName))
	content_type = mimetypes.guess_type(serverFileName)[0]
	response     = HttpResponse(wrapper,content_type=content_type)
	response['Content-Length']      = os.path.getsize(serverFileName)    
	response['Content-Disposition'] = "attachment; filename=%s"%clientFileName
	return response


def exportView(request):
	"""
	VIEW
	displays the export page -> export all the acts in the db regarding the sorting variable
	template called: export/index.html
	"""
	if request.method == 'POST': #S'il s'agit d'une requête POST
		form = ActsExportForm(request.POST) #On reprend les données
		if form.is_valid(): 
			#for key, value in request.POST.iteritems():
			sortingFields = request.POST['sortFields']
			sortingDirection = request.POST['sortDirection']
			querySet=fetchDataInTableFunction(ActsExportDb)
			querySet=sortingQuerySetFunction(querySet, sortingFields, sortingDirection)
			serverDirectory = settings.MEDIA_ROOT+"export/"
			fileName="europeanActs.csv"
			#if a file with the same name already exists, we delete it
			if os.path.exists(serverDirectory+fileName):
				os.remove(serverDirectory+fileName)
			querySetToCsvFile(querySet, serverDirectory+fileName)
			return send_file(request, serverDirectory+fileName, fileName)
		else:
			return render_to_response('export/index.html', {'form': form}, context_instance=RequestContext(request))
	else: #Si c'est pas du POST, c'est probablement une requête GET
		form = ActsExportForm() # On crée un formulaire vide
		
	return render_to_response('export/index.html', {'form': form}, context_instance=RequestContext(request))
