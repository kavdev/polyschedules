"""
.. module:: poly_schedules.urls
   :synopsis: Poly Schedules URLs.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging


from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import RedirectView, TemplateView

from dajaxice.core import dajaxice_autodiscover, dajaxice_config

admin.autodiscover()
dajaxice_autodiscover()

from core.views import LoginView, handler500

logger = logging.getLogger(__name__)
instructor_required = user_passes_test(lambda user: user.is_superuser or user.is_instructor)

handler500 = handler500

# Core
urlpatterns = patterns('core.views',
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^flugzeug/', include(admin.site.urls)),  # admin site urls, masked
    url(r'^favicon\.ico$', RedirectView.as_view(url='https://webresource.its.calpoly.edu/cpwebtemplate/5.0.1/common/images_html/favicon.ico'), name='favicon'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'logout', name='logout'),
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
