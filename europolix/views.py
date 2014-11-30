#-*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import simplejson
from django.conf import settings


def reload_menu(request):
    """
    VIEW
    reload the left menu
    TEMPLATES
    menu.html
    """
    response={}
    response["user"]={}
    response["user"]["username"]=request.POST["username"]

    return HttpResponse(render_to_string('menu.html', response, RequestContext(request)))
