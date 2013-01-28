from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from europolix.views import homepageView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	#homepage
	url(r'^/?$', homepageView),
	url(r'^index.html$', homepageView),
	#tests page
	url(r'^tests/$', 'tests.views.testView'),
	#login page
	url(r'^login/$', 'auth.views.loginView'),
	#acts ids validation page
	url(r'^actsIdsValidation/', include('actsIdsValidation.urls')),
	#acts information retrieval page
	url(r'^actsInformationRetrieval/', include('actsInformationRetrieval.urls')),
	#import page
	url(r'^import/', include('import.urls')),
	#export page
	url(r'^export/', include('export.urls')),
	#export library
	#url(r'^exports/', include('data_exports.urls', namespace='data_exports')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
