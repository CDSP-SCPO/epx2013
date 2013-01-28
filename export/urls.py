from django.conf.urls import patterns, url

urlpatterns = patterns('export.views',
	url(r'^/?$', 'exportView'),
	url(r'^index.html$', 'exportView'),
)

