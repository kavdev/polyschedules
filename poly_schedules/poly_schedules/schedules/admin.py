"""
.. module:: poly_schedules.core.admin
   :synopsis: Poly Schedules Core Admin.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib import admin

from .models import Course, Location, Section, SectionTime, Week, Schedule, Term

admin.site.register(Course)
admin.site.register(Location)
admin.site.register(Section)
admin.site.register(SectionTime)
admin.site.register(Week)
admin.site.register(Schedule)
admin.site.register(Term)
