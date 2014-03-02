"""
.. module:: poly_schedules.urls
   :synopsis: Poly Schedules URLs.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging


from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import RedirectView

from dajaxice.core import dajaxice_autodiscover, dajaxice_config

admin.autodiscover()
dajaxice_autodiscover()

from core.views import LoginView, handler500
from schedules.views import (BaseScheduleView, PopulateBaseSchedule, CourseScheduleView, PopulateCourseSchedule,
                             LocationScheduleView, PopulateLocationSchedule, InstructorScheduleView, PopulateInstructorSchedule)
from preferences.views import PreferencesView
from votes.views import VotesView

logger = logging.getLogger(__name__)
student_required = user_passes_test(lambda user: user.is_superuser or not user.is_instructor)
instructor_required = user_passes_test(lambda user: user.is_superuser or user.is_instructor)

handler500 = handler500

# Core
urlpatterns = patterns('core.views',
    url(r'^flugzeug/', include(admin.site.urls)),  # admin site urls, masked
    url(r'^favicon\.ico$', RedirectView.as_view(url='https://webresource.its.calpoly.edu/cpwebtemplate/5.0.1/common/images_html/favicon.ico'), name='favicon'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)

# Schedules
urlpatterns += patterns('',
    url(r'^$', BaseScheduleView.as_view(), name='base_schedule'),
    url(r'^populate/$', PopulateBaseSchedule.as_view(), name='populate_base_schedule'),
    url(r'^course/(?P<prefix>\w+)/(?P<course_number>\d*)/$', CourseScheduleView.as_view(), name='course_schedule'),
    url(r'^course/(?P<prefix>\w+)/(?P<course_number>\d*)/populate/$', PopulateCourseSchedule.as_view(), name='populate_course_schedule'),
    url(r'^location/(?P<building_number>\w+)/(?P<room_number>\w+)/$', LocationScheduleView.as_view(), name='location_schedule'),
    url(r'^location/(?P<building_number>\w+)/(?P<room_number>\w+)/populate/$', PopulateLocationSchedule.as_view(), name='populate_location_schedule'),
    url(r'^instructor/(?P<username>\w+)/$', InstructorScheduleView.as_view(), name='instructor_schedule'),
    url(r'^instructor/(?P<username>\w+)/populate/$', PopulateInstructorSchedule.as_view(), name='populate_instructor_schedule'),
)

# Instructor Preferences
urlpatterns += patterns('',
    url(r'^preferences/$', login_required(instructor_required(PreferencesView.as_view())), name='preferences'),
)

# Student Votes
urlpatterns += patterns('',
    url(r'^votes/$', login_required(student_required(VotesView.as_view())), name='votes'),
)

# Dajaxice
urlpatterns += patterns('',
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

#Raise errors on purpose
urlpatterns += patterns('',
    url(r'^500/$', 'ThisIsIntentionallyBroken'),
    url(r'^403/$', 'django.views.defaults.permission_denied'),
    url(r'^404/$', 'django.views.defaults.page_not_found'),
)
