#-*- coding: utf-8 -*-

#generic view
from django.views.generic.list import ListView
#models
from django.db.models import Count
from history.models import History
from act.models import Act



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
        context['nb_acts'] = Act.objects.filter(validated=2).count
        return context
