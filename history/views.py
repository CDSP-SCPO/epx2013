#-*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext
#use json for the ajax request
from django.utils import simplejson
from django.http import HttpResponse
#generic view
from django.views.generic.list import ListView
#models
from history.models import History



#~ @login_required
class HistoryListView(ListView):
    """
    VIEW
    displays the history page -> show a history of the last 100 validated acts
    TEMPLATES
    history/index.html
    """
    #~ model = History
    template_name = 'history/index.html'
    #get last 100 entries
    queryset = History.objects.all().order_by('pk').reverse()[:100]

    def get_context_data(self, **kwargs):
        context = super(HistoryListView, self).get_context_data(**kwargs)
        return context
