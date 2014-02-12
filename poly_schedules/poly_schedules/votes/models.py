"""
.. module:: poly_schedules.votes.models
   :synopsis: Poly Schedules Vote Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.conf import settings
from django.db.models import Model, ForeignKey

from schedules.models import Course, Term


class Vote(Model):
    student = ForeignKey(settings.AUTH_USER_MODEL)
    course = ForeignKey(Course)
    term = ForeignKey(Term)
