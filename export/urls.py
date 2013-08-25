from django.conf.urls import patterns, url

urlpatterns = patterns('export.views',
	url(r'^/?$', 'exportView', name='export'),
	url(r'^index.html$', 'exportView', name='export'),
)

