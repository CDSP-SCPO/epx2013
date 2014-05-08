from django.conf.urls import patterns, url
from views import ActUpdate
#redirect to login page if not logged
from django.contrib.auth.decorators import login_required

urlpatterns=patterns('act.views',
    url(r'^/?$', login_required(ActUpdate.as_view()), name='act'),
    url(r'^form.html$', login_required(ActUpdate.as_view()), name='act'),
    url(r'^reset_form.html$', 'reset_form', name='reset_form'),
    url(r'^code_sect.html$', 'update_code_sect', name='update_code_sect'),
    url(r'^person.html$', 'update_person', name='update_person'),
    url(r'^durations.html$', 'update_durations', name='update_durations'),
    url(r'^dg.html$', 'update_dg', name='update_dg'),
)
