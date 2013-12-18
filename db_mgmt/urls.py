from django.conf.urls import patterns, url

urlpatterns=patterns('db_mgmt.views',
	url(r'^add/(?P<field>\w+)/$', 'add', name='add'),
	url(r'^form_add.html/(?P<field>\w+)/$', 'form_add', name='form_add'),
)
