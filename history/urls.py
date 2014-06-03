from django.conf.urls import patterns, url
from views import HistoryListView
#redirect to login page if not logged
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(HistoryListView.as_view()), name='history'),
)
