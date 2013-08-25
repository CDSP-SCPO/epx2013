#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext


def loginView(request):
	"""
	VIEW
	displays the login page / checks the ids of the user
	template called: auth/index.html
	"""
	logout(request)
	state = "Please log in below..."
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "You're successfully logged in!"
			else:
				state = "Your account is not active, please contact the site admin."
		else:
			state = "Your username and/or password were incorrect."

	return render_to_response('auth/index.html', {'state':state, 'username': username}, context_instance=RequestContext(request))
