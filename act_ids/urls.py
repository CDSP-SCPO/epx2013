from django.conf.urls import patterns, url

urlpatterns=patterns('act_ids.views',
	url(r'^/?$', 'act_ids', name='act_ids'),
	url(r'^form.html$', 'act_ids', name='act_ids'),
	url(r'^reset_ids_form.html$', 'reset_ids_form', name='reset_ids_form'),
)
