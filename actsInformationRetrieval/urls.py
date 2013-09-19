from django.conf.urls import patterns, url

urlpatterns = patterns('actsInformationRetrieval.views',
	url(r'^/?$', 'act_info', name='act_info'),
	url(r'^form.html$', 'act_info', name='act_info'),
	url(r'^reset_form.html$', 'reset_form', name='reset_info_form'),
	url(r'^respPropos.html$', 'update_respPropos', name='update_respPropos'),
)
