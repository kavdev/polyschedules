"""
.. module:: poly_schedules.votes.admin
   :synopsis: Poly Schedules Votes Admin.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib import admin

from .models import Vote

admin.site.register(Vote)
