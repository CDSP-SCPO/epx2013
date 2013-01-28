from django.conf.urls import patterns, url

urlpatterns = patterns('import.views',
	url(r'^/?$', 'importView'),
	url(r'^index.html$', 'importView'),
)
