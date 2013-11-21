from django.conf.urls import patterns, url

urlpatterns=patterns('import_app.views',
	url(r'^/?$', 'import_view', name='import'),
	url(r'^/?help_text.html$', 'help_text', name='help_text'),
)
