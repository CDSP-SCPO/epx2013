from django.conf.urls import patterns, url
from views import MinAttendUpdate
#redirect to login page if not logged
from django.contrib.auth.decorators import login_required


urlpatterns=patterns('attendance.views',
    url(r'^$', login_required(MinAttendUpdate.as_view()), name='attendance'),
    url(r'^attendance.html$', login_required(MinAttendUpdate.as_view()), name='attendance'),
    url(r'^reset_form_attendance.html$', 'reset_form_attendance', name='reset_form_attendance'),
)
