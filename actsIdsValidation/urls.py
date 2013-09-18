from django.conf.urls import patterns, url

urlpatterns = patterns('actsIdsValidation.views',
	url(r'^/?$', 'act_ids', name='act_ids'),
	url(r'^form.html$', 'act_ids', name='act_ids'),
	url(r'^reset_form.html$', 'reset_form', name='reset_ids_form'),
)
