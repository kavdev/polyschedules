"""
.. module:: poly_schedules.preferences.admin
   :synopsis: Poly Schedules Preferences Admin.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib import admin

from .models import CoursePreference, TimePreference

admin.site.register(CoursePreference)
admin.site.register(TimePreference)
