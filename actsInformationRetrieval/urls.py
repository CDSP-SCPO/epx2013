from django.conf.urls import patterns, url

urlpatterns = patterns('actsInformationRetrieval.views',
	url(r'^/?$', 'actsView'),
	url(r'^index.html$', 'actsView'),
)
