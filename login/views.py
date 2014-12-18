#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
#use json for the ajax request
from django.utils import simplejson
from django.http import HttpResponse
#logging
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def login_view(request):
    """
    VIEW
    displays the login page / check the ids of the user
    TEMPLATE
    login/index.html
    """
    logger.debug('\n')
    logger.debug('login_view')
    logout(request)
    response={}

    if request.POST:
        logger.debug('login_view post')
        #page posted with ajax
        msg=''
        msg_class="error_msg"

        username=request.POST.get('username')
        password=request.POST.get('password')

        logger.debug("user: "+ username)
        logger.debug("password: "+ password)

        user=authenticate(username=username, password=password)
        if user is not None:
            logger.debug("user is not none", user.username)
            if user.is_active:
                login(request, user)
                msg="You're successfully logged in!"
                msg_class="success_msg"
                #for ajax function
                response["user"]={}
                response["user"]["username"]=user.username
            else:
                msg="Your account is not active, please contact the site admin."
                logger.debug(msg)
        else:
            msg="Your username and/or password are incorrect."
            logger.debug(msg)

        response["msg"]=msg
        response["msg_class"]=msg_class

        #transform the data to json so it can be used in jquery
        if request.is_ajax():
            logger.debug('\n')
            return HttpResponse(simplejson.dumps(response), mimetype='application/json')

    #displays the page (GET) or POST if javascript disabled
    logger.debug('\n')
    return render_to_response('login/index.html', response, context_instance=RequestContext(request))
