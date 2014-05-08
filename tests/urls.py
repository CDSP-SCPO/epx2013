from django.conf.urls import patterns, url

urlpatterns=patterns('tests.views',
	url(r'^/?$', 'testView'),
	url(r'^index.html$', 'testView'),
)
