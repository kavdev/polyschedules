"""
.. module:: poly_schedules.core.admin
   :synopsis: Poly Schedules Core Admin.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib import admin

from .models import Course, Location, Section, Schedule, Day, Term

admin.site.register(Course)
admin.site.register(Location)
admin.site.register(Section)
admin.site.register(Schedule)
admin.site.register(Day)
admin.site.register(Term)
