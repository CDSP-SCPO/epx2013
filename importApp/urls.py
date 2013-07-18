from django.conf.urls import patterns, url

urlpatterns = patterns('importApp.views',
	url(r'^/?$', 'importView', name='import'),
	url(r'^index.html$', 'importView', name='import'),
)
