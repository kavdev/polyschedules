"""
.. module:: poly_schedules.preferences.models
   :synopsis: Poly Schedules Preference Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.db.models import Model, ForeignKey, IntegerField

from schedules.models import Course


class CoursePreference(Model):
    course = ForeignKey(Course)
    preference = IntegerField()
