from django.conf.urls import patterns, url

urlpatterns = patterns('actsIdsValidation.views',
	url(r'^/?$', 'actsView'),
	url(r'^index.html$', 'actsView'),
)
