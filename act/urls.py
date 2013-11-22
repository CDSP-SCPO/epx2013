from django.conf.urls import patterns, url

urlpatterns=patterns('act.views',
	url(r'^/?$', 'act', name='act'),
	url(r'^form.html$', 'act', name='act'),
	url(r'^reset_form.html$', 'reset_form', name='reset_form'),
	url(r'^code_sect.html$', 'update_code_sect', name='update_code_sect'),
	url(r'^person.html$', 'update_person', name='update_person'),
	url(r'^dg.html$', 'update_dg', name='update_dg'),
)
