from django.conf.urls import patterns, url

urlpatterns = patterns('actsInformationRetrieval.views',
	url(r'^/?$', 'actsView', name='informationRetrieval'),
	url(r'^index.html$', 'actsView', name='informationRetrieval'),
)
