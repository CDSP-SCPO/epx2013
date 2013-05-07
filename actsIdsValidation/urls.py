from django.conf.urls import patterns, url

urlpatterns = patterns('actsIdsValidation.views',
	url(r'^/?$', 'actsView', name='ids'),
	url(r'^index.html$', 'actsView', name='ids'),
)
