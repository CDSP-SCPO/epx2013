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
    # reload the left menu
    url(r'^menu.html$', 'europolix.views.reload_menu', name='reload_menu'),
    #login page
    url(r'^login/$', 'login.views.login_view', name='login'),
    #import page
    url(r'^import/', include('import_app.urls')),
    #acts ids validation page
    url(r'^act_ids/', include('act_ids.urls')),
    #acts data validation page
    url(r'^act/', include('act.urls')),
    #attendance validation page
    url(r'^attendance/', include('attendance.urls')),
    #db management page
    url(r'^db_mgmt/', include('db_mgmt.urls')),
    #export page
    url(r'^export/', include('export.urls')),
    #history page
    url(r'^history/', include('history.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

     #tests page
    #~ url(r'^tests/$', 'tests.views.testView'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)

if settings.DEBUG:
    #display static files on the web (images)
    urlpatterns +=patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True})
    )
    #display media files on the web (latest database export)
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ) + urlpatterns

