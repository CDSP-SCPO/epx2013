from django.conf.urls import patterns, url

urlpatterns=patterns('export.views',
	url(r'^/?$', 'export', name='export'),
)

