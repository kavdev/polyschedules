"""
.. module:: poly_schedules.core.admin
   :synopsis: Poly Schedules Core Admin.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PolySchedulesUser

admin.site.register(PolySchedulesUser, UserAdmin)
