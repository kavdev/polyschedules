"""
.. module:: poly_schedules.core.admin
   :synopsis: Poly Schedules Core Admin.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib import admin

from .models import Course, Location, Section, Week, Term

admin.site.register(Course)
admin.site.register(Location)
admin.site.register(Section)
admin.site.register(Week)
admin.site.register(Term)
