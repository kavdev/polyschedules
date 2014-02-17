"""
.. module:: poly_schedules.preferences.models
   :synopsis: Poly Schedules Preference Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.db.models import Model
from django.db.models.fields import PositiveSmallIntegerField
from django.db.models.fields.related import ForeignKey

from schedules.models import Course


class CoursePreference(Model):
    """An instructor's course preference."""

    course = ForeignKey(Course)
    preference = PositiveSmallIntegerField()
