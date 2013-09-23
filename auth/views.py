#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
#use json for the ajax request
from django.utils import simplejson
from django.http import HttpResponse


def login_view(request):
	"""
	VIEW
	displays the login page / checks the ids of the user
	template called: auth/index.html
	"""
	logout(request)
	response_dic={}

	if request.POST:
		#page posted with ajax
		msg = ''
		msg_class="error_msg"

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				msg = "You're successfully logged in!"
				msg_class= "success_msg"
				#for ajax function
				response_dic["username"]=username
			else:
				msg = "Your account is not active, please contact the site admin."
		else:
			msg = "Your username and/or password were incorrect."

		response_dic["msg"]=msg
		response_dic["msg_class"]=msg_class

		#transform the data to json so it can be used in jquery
		if request.is_ajax():
			return HttpResponse(simplejson.dumps(response_dic), mimetype='application/json')

	#displays the page (GET) or POST if javascript disabled
	return render_to_response('auth/index.html', response_dic, context_instance=RequestContext(request))
