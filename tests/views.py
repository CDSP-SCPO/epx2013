#-*- coding: utf-8 -*-
from django.shortcuts import render

def testView(request):
	"""
	VIEW
	displays the homepage
	template used: tests/index.html
	"""
	return render(request, 'tests/index.html') 
