from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns=patterns('',
	#load the homepage template (no view)
	url(r'^/?$', direct_to_template, {'template': 'index.html'}, name="homepage"),
	#tests page
	#~ url(r'^tests/$', 'tests.views.testView'),
	#login page
	url(r'^login/$', 'login.views.login_view', name='login'),
	#acts ids validation page
	url(r'^act_ids/', include('act_ids.urls')),
	#acts data retrieval page
	url(r'^act/', include('act.urls')),
	#import page
	url(r'^import/', include('import_app.urls')),
	#export page
	url(r'^export/', include('export.urls')),
	#export library
	#url(r'^exports/', include('data_exports.urls', namespace='data_exports')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)

if settings.DEBUG:
	urlpatterns +=patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': settings.STATIC_ROOT, 'show_indexes': True})
)

