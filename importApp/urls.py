from django.conf.urls import patterns, url

urlpatterns = patterns('importApp.views',
	url(r'^/?$', 'importView', name='import'),
	url(r'^/?help_text.html$', 'help_text', name='help_text'),
)
